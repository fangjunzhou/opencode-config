#!/usr/bin/env python3

"""
Generate an HTML index page for the distributions directory.

This script creates a browseable index of available OpenCode distributions
with download links and verification instructions.

Usage:
    python3 generate_distribution_index.py [distributions_dir]

Example:
    python3 generate_distribution_index.py ./distributions
"""

import os
import sys
from pathlib import Path
from datetime import datetime


def generate_index(dist_dir):
    """Generate HTML index for distributions directory."""
    
    dist_path = Path(dist_dir)
    
    if not dist_path.exists():
        print(f"Error: Directory not found: {dist_dir}")
        sys.exit(1)
    
    # Find all tarballs
    tarballs = sorted([f for f in dist_path.iterdir() if f.suffix == '.gz' and f.name != '.gitkeep'])
    
    if not tarballs:
        print(f"Warning: No .tar.gz files found in {dist_dir}")
        return
    
    # Build HTML
    html_parts = []
    
    html_parts.append("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenCode Distributions - Downloads</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }
        .container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
        header { background: white; padding: 30px 0; margin-bottom: 40px; border-bottom: 1px solid #eee; }
        h1 { font-size: 28px; margin-bottom: 10px; }
        .subtitle { color: #666; font-size: 16px; }
        
        .distribution {
            background: white;
            border: 1px solid #ddd;
            border-radius: 6px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .distribution h2 {
            font-size: 20px;
            margin-bottom: 15px;
            color: #0066cc;
            text-transform: capitalize;
        }
        
        .distribution .meta {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
        }
        
        .meta-item {
            font-size: 13px;
            color: #666;
        }
        
        .meta-label {
            font-weight: 600;
            color: #333;
            display: block;
        }
        
        .download-section {
            background: #f9f9f9;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 15px;
            font-size: 13px;
            font-family: "Monaco", "Menlo", "Ubuntu Mono", monospace;
            overflow-x: auto;
        }
        
        .download-label {
            font-weight: 600;
            color: #333;
            display: block;
            margin-bottom: 8px;
            font-size: 14px;
        }
        
        .verify-section {
            background: #fffbf0;
            padding: 15px;
            border-radius: 4px;
            border-left: 3px solid #ff9800;
            margin-top: 15px;
            font-size: 13px;
        }
        
        .verify-label {
            font-weight: 600;
            color: #f57c00;
            display: block;
            margin-bottom: 8px;
        }
        
        .checksum {
            font-family: "Monaco", "Menlo", "Ubuntu Mono", monospace;
            word-break: break-all;
            background: white;
            padding: 8px 12px;
            border-radius: 3px;
            border: 1px solid #ddd;
            display: block;
            margin-top: 8px;
        }
        
        .button-group {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .button {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 4px;
            text-decoration: none;
            font-size: 13px;
            font-weight: 500;
            border: 1px solid #ddd;
            transition: all 0.2s;
        }
        
        .button-primary {
            background: #0066cc;
            color: white;
            border-color: #0066cc;
        }
        
        .button-primary:hover {
            background: #0052a3;
            border-color: #0052a3;
        }
        
        .button-secondary {
            background: white;
            color: #0066cc;
            border-color: #0066cc;
        }
        
        .button-secondary:hover {
            background: #f0f7ff;
        }
        
        footer {
            margin-top: 60px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            font-size: 13px;
            color: #666;
            text-align: center;
        }
        
        code {
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: "Monaco", "Menlo", "Ubuntu Mono", monospace;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>OpenCode Configuration Distributions</h1>
            <p class="subtitle">Download pre-configured OpenCode packages for your project variant</p>
        </div>
    </header>
    
    <div class="container">
""")
    
    # Extract variants from filenames
    variants = {}
    for tarball in tarballs:
        name = tarball.name
        if name.startswith('opencode-') and name.endswith('.tar.gz'):
            variant = name.replace('opencode-', '').replace('.tar.gz', '')
            if variant not in ['SHA256SUMS', 'SUMMARY']:
                if variant not in variants:
                    variants[variant] = {}
                variants[variant]['file'] = name
                variants[variant]['path'] = tarball
    
    # Add checksums if available
    checksums = {}
    checksums_file = dist_path / 'SHA256SUMS'
    if checksums_file.exists():
        with open(checksums_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    checksum = parts[0]
                    filename = parts[1]
                    checksums[filename] = checksum
    
    # Generate HTML for each variant
    for variant, info in sorted(variants.items()):
        if 'file' not in info:
            continue
        
        tarball_path = info['path']
        tarball_name = info['file']
        file_size = tarball_path.stat().st_size
        file_size_str = format_size(file_size)
        
        # Get checksum
        checksum = checksums.get(tarball_name, 'N/A')
        
        html_parts.append(f"""        <div class="distribution">
            <h2>{variant} Variant</h2>
            
            <div class="meta">
                <div class="meta-item">
                    <span class="meta-label">File</span>
                    {tarball_name}
                </div>
                <div class="meta-item">
                    <span class="meta-label">Size</span>
                    {file_size_str}
                </div>
                <div class="meta-item">
                    <span class="meta-label">Type</span>
                    Compressed Tarball
                </div>
            </div>
            
            <div class="download-label">📥 Installation (One-liner)</div>
            <div class="download-section">curl -fsSL https://fangjun.github.io/opencode-config/distributions/{tarball_name} | tar xz</div>
            
            <div class="button-group">
                <a href="./{tarball_name}" class="button button-primary">Direct Download</a>
                <a href="./{tarball_name}.sha256" class="button button-secondary">View Checksum</a>
            </div>
            
            <div class="verify-section">
                <span class="verify-label">🔐 Verification</span>
                <p>SHA256: <code>{checksum[:32]}...</code></p>
                <p style="margin-top: 8px;">Verify after download:</p>
                <div class="download-section" style="margin-top: 8px;">shasum -a 256 -c {tarball_name}.sha256</div>
            </div>
        </div>
""")
    
    html_parts.append("""        <footer>
            <p>🔗 Repository: <a href="https://github.com/fangjun/opencode-config">fangjun/opencode-config</a></p>
            <p>📖 Documentation: <a href="https://fangjun.github.io/opencode-config/">Browse Configs</a></p>
        </footer>
    </div>
</body>
</html>
""")
    
    # Write index.html
    index_path = dist_path / 'index.html'
    with open(index_path, 'w') as f:
        f.write('\n'.join(html_parts))
    
    print(f"✓ Generated index: {index_path}")
    print(f"✓ Variants indexed: {len(variants)}")
    for variant in sorted(variants.keys()):
        print(f"  - {variant}")


def format_size(bytes_size):
    """Format bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f} TB"


if __name__ == '__main__':
    dist_dir = sys.argv[1] if len(sys.argv) > 1 else './distributions'
    generate_index(dist_dir)
