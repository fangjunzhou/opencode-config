#!/bin/bash

################################################################################
# build-distributions.sh - Build downloadable distribution packages for each variant
#
# Usage:
#   ./scripts/build-distributions.sh [variant] [--output /path] [--version 1.0.0]
#
# Examples:
#   ./scripts/build-distributions.sh base                    # Build base variant
#   ./scripts/build-distributions.sh python                  # Build python variant
#   ./scripts/build-distributions.sh base --output ./dist     # Custom output dir
#   ./scripts/build-distributions.sh all --version 2.0.0     # Build all with version
#
# Description:
#   Generates downloadable tar.gz distributions for each variant.
#   Includes checksums and ready-to-curl one-liners.
#
# Output Structure:
#   distributions/
#   ├── opencode-base.tar.gz
#   ├── opencode-base.tar.gz.sha256
#   ├── opencode-python.tar.gz
#   ├── opencode-python.tar.gz.sha256
#   └── SHA256SUMS (combined checksums)
#
# Exit Codes:
#   0 = Success
#   1 = Invalid arguments
#   2 = Build failed
################################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_ROOT="${PWD}"
VARIANTS=("base" "python")
OUTPUT_DIR="${REPO_ROOT}/distributions"
VERSION="1.0.0"
BUILD_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Argument parsing
while [[ $# -gt 0 ]]; do
  case $1 in
    base|python|cpp|go|rust|javascript|nodejs|java|all)
      if [[ "$1" == "all" ]]; then
        # Keep default VARIANTS array
        shift
      else
        VARIANTS=("$1")
        shift
      fi
      ;;
    --output)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    --version)
      VERSION="$2"
      shift 2
      ;;
    *)
      echo -e "${RED}Error: Unknown option '$1'${NC}"
      echo "Usage: $0 [variant|all] [--output /path] [--version 1.0.0]"
      exit 1
      ;;
  esac
done

# Logging functions
log_info() {
  echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
  echo -e "${GREEN}✓${NC} $1"
}

log_error() {
  echo -e "${RED}✗${NC} $1"
}

log_warn() {
  echo -e "${YELLOW}⚠${NC} $1"
}

# Validation
log_info "Validating build environment..."

if [[ ! -f "${REPO_ROOT}/scripts/setup-opencode.sh" ]]; then
  log_error "setup-opencode.sh not found"
  exit 2
fi

log_success "Setup script found"

# Create output directory
log_info "Creating output directory: ${OUTPUT_DIR}"
mkdir -p "${OUTPUT_DIR}"
log_success "Output directory ready"

# Build each variant
CHECKSUMS_FILE="${OUTPUT_DIR}/SHA256SUMS"
rm -f "${CHECKSUMS_FILE}"
TOTAL_BUILT=0

for variant in "${VARIANTS[@]}"; do
  log_info "Building variant: ${variant}"
  
  # Check if variant exists (except "base")
  if [[ "${variant}" != "base" && ! -d "${REPO_ROOT}/${variant}" ]]; then
    log_warn "Variant directory not found: ${variant}/, skipping"
    continue
  fi
  
  # Setup opencode for this variant
  log_info "  Setting up .opencode for ${variant}..."
  cd "${REPO_ROOT}"
  ./scripts/setup-opencode.sh "${variant}" > /dev/null 2>&1
  log_success "  .opencode configured"
  
  # Create temporary build directory
  TEMP_BUILD=$(mktemp -d)
  trap "rm -rf ${TEMP_BUILD}" EXIT
  
  BUILD_DIR="${TEMP_BUILD}/opencode"
  mkdir -p "${BUILD_DIR}"
  
  log_info "  Copying .opencode to build directory..."
  cp -r "${REPO_ROOT}/.opencode" "${BUILD_DIR}/.opencode"
  
  # Add build metadata
  cat > "${BUILD_DIR}/BUILD_INFO.txt" << EOF
OpenCode Configuration Distribution
====================================

Variant: ${variant}
Version: ${VERSION}
Built: ${BUILD_TIME}
Build System: GitHub Actions

For installation and usage, visit:
https://fangjun.github.io/opencode-config/distributions/

Quick Start:
curl -fsSL https://fangjun.github.io/opencode-config/distributions/opencode-${variant}.tar.gz | tar xz
EOF
  
  log_success "  Added build metadata"
  
  # Create tarball with deterministic settings
  TARBALL_NAME="opencode-${variant}.tar.gz"
  TARBALL_PATH="${OUTPUT_DIR}/${TARBALL_NAME}"
  
  log_info "  Creating tarball: ${TARBALL_NAME}"
  cd "${TEMP_BUILD}"
  
  # Create tarball with maximum compatibility (macOS and Linux)
  tar -czf "${TARBALL_PATH}" opencode/ || {
    log_error "  Failed to create tarball"
    exit 2
  }
  log_success "  Tarball created: ${TARBALL_NAME}"
  
  # Generate checksum for this file
  CHECKSUM_FILE="${TARBALL_PATH}.sha256"
  log_info "  Generating SHA256 checksum..."
  cd "${OUTPUT_DIR}"
  sha256sum "${TARBALL_NAME}" > "${CHECKSUM_FILE}"
  CHECKSUM=$(cat "${CHECKSUM_FILE}" | awk '{print $1}')
  log_success "  Checksum: ${CHECKSUM:0:16}..."
  
  # Add to combined checksums
  cat "${CHECKSUM_FILE}" >> "${CHECKSUMS_FILE}"
  
  # Get file size
  FILE_SIZE=$(du -h "${TARBALL_PATH}" | cut -f1)
  log_success "  Build complete: ${FILE_SIZE}"
  
  TOTAL_BUILT=$((TOTAL_BUILT + 1))
done

# Generate final summary
log_info "Generating summary..."
cd "${OUTPUT_DIR}"

SUMMARY_FILE="${OUTPUT_DIR}/SUMMARY.txt"
cat > "${SUMMARY_FILE}" << EOF
OpenCode Configuration Distributions
====================================

Version: ${VERSION}
Built: ${BUILD_TIME}

Available Distributions:
EOF

for variant in "${VARIANTS[@]}"; do
  if [[ -f "${OUTPUT_DIR}/opencode-${variant}.tar.gz" ]]; then
    FILE_SIZE=$(du -h "${OUTPUT_DIR}/opencode-${variant}.tar.gz" | cut -f1)
    CHECKSUM=$(head -1 "${OUTPUT_DIR}/opencode-${variant}.tar.gz.sha256" | awk '{print $1}')
    echo "" >> "${SUMMARY_FILE}"
    echo "Variant: ${variant}" >> "${SUMMARY_FILE}"
    echo "  File: opencode-${variant}.tar.gz (${FILE_SIZE})" >> "${SUMMARY_FILE}"
    echo "  SHA256: ${CHECKSUM}" >> "${SUMMARY_FILE}"
    echo "  Download: https://fangjun.github.io/opencode-config/distributions/opencode-${variant}.tar.gz" >> "${SUMMARY_FILE}"
    echo "  Install: curl -fsSL https://fangjun.github.io/opencode-config/distributions/opencode-${variant}.tar.gz | tar xz" >> "${SUMMARY_FILE}"
  fi
done

log_success "Summary saved"

# Final output
echo ""
log_success "Build complete!"
echo ""
echo -e "${BLUE}Output Directory:${NC} ${OUTPUT_DIR}"
echo -e "${BLUE}Variants Built:${NC} ${TOTAL_BUILT}"
echo ""
echo -e "${BLUE}Files:${NC}"
ls -lh "${OUTPUT_DIR}" | tail -n +2 | awk '{printf "  %s (%s)\n", $NF, $5}'
echo ""
echo -e "${YELLOW}Verification:${NC}"
echo "  cd ${OUTPUT_DIR}"
echo "  shasum -a 256 -c SHA256SUMS"
echo ""
echo -e "${GREEN}Ready to deploy to GitHub Pages!${NC}"

exit 0
