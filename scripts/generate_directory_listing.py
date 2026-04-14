#!/usr/bin/env python3

"""
Generate directory listing HTML for repository root.

This script creates a browseable index of the repository structure
with clickable links to all configuration files and directories.

Usage:
    python3 generate_directory_listing.py [repo_root] [output_file]

Example:
    python3 generate_directory_listing.py . index.html
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import re
import html as html_module


def should_include_path(path, name):
    """Determine if path should be included in listing."""
    if name == '.opencode':
        return True
    if name == 'shared-config':
        return True
    if name == 'python':
        return True
    if name == 'distributions':
        return True
    if name in ['.git', '.github', '.gitignore', 'node_modules', '__pycache__']:
        return False
    return True


def format_size(size):
    """Format bytes to human readable."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"


def markdown_to_html(markdown_text):
    """Convert basic markdown to HTML."""
    lines = markdown_text.split('\n')
    html_lines = []
    in_code_block = False
    code_block_content = []
    
    def apply_inline_formatting(text):
        """Apply inline markdown formatting to text."""
        # Inline code
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        # Bold
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
        # Italic
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
        # Links
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        return text
    
    for line in lines:
        # Code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                html_lines.append(f'<pre><code>{"".join(code_block_content)}</code></pre>')
                code_block_content = []
                in_code_block = False
            else:
                in_code_block = True
            continue
        
        if in_code_block:
            code_block_content.append(html_module.escape(line) + '\n')
            continue
        
        # Headers
        if line.startswith('# '):
            html_lines.append(f'<h2>{html_module.escape(line[2:].strip())}</h2>')
        elif line.startswith('## '):
            html_lines.append(f'<h3>{html_module.escape(line[3:].strip())}</h3>')
        elif line.startswith('### '):
            html_lines.append(f'<h4>{html_module.escape(line[4:].strip())}</h4>')
        # List items
        elif line.strip().startswith('- '):
            list_content = html_module.escape(line[2:].strip())
            list_content = apply_inline_formatting(list_content)
            html_lines.append(f'<li>{list_content}</li>')
        # Paragraphs
        elif line.strip():
            text = html_module.escape(line.strip())
            text = apply_inline_formatting(text)
            html_lines.append(f'<p>{text}</p>')
        else:
            # Empty line
            html_lines.append('')
    
    # Wrap lists
    result = '\n'.join(html_lines)
    result = re.sub(r'(<li>.*?</li>)', lambda m: '<ul>' + m.group(1) + '</ul>' if not re.search(r'</ul>.*<li>', result) else m.group(1), result, flags=re.DOTALL)
    
    return result


def generate_file_tree(start_path, root_path, indent=0):
    """Generate HTML file tree."""
    items = []
    
    try:
        entries = sorted(os.listdir(start_path))
    except PermissionError:
        return items
    
    for entry in entries:
        full_path = os.path.join(start_path, entry)
        
        if not should_include_path(full_path, entry):
            continue
        
        if entry in ['__pycache__', 'node_modules', '.git', 'venv']:
            continue
        
        indent_str = "&nbsp;" * (indent * 2)
        is_dir = os.path.isdir(full_path)
        
        rel_path = os.path.relpath(full_path, root_path)
        url = f"./{rel_path}/"
        
        if is_dir:
            items.append(f'{indent_str}<strong>{entry}/</strong>')
            items.extend(generate_file_tree(full_path, root_path, indent + 1))
        else:
            size = os.path.getsize(full_path)
            size_str = format_size(size)
            items.append(f'{indent_str}<a href="./{rel_path}">{entry}</a> <span style="color:#999">({size_str})</span>')
    
    return items


def generate_index_html(repo_root):
    """Generate main index.html."""
    
    readme_path = os.path.join(repo_root, 'README.md')
    readme_html = ""
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as f:
            readme_markdown = f.read()
            readme_html = markdown_to_html(readme_markdown)
    
    file_tree = generate_file_tree(repo_root, repo_root)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenCode Config - File Browser</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        .container {{ max-width: 1000px; margin: 0 auto; padding: 40px 20px; }}
        header {{ background: white; padding: 30px 0; margin-bottom: 40px; border-bottom: 1px solid #eee; }}
        h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .subtitle {{ color: #666; font-size: 16px; }}
        
        .readme-section {{
            background: white;
            padding: 24px;
            border-radius: 6px;
            margin-bottom: 30px;
            border-left: 4px solid #0066cc;
        }}
        
        .file-tree-section {{
            background: white;
            padding: 24px;
            border-radius: 6px;
            margin-bottom: 30px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        .file-tree {{
            font-family: "Monaco", "Menlo", "Ubuntu Mono", monospace;
            font-size: 13px;
            line-height: 1.8;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        
        .file-tree a {{ color: #0066cc; text-decoration: none; }}
        .file-tree a:hover {{ text-decoration: underline; }}
        
         .readme-section h2 {{ font-size: 20px; margin-bottom: 15px; color: #0066cc; }}
         .readme-section h3 {{ font-size: 16px; margin-top: 20px; margin-bottom: 10px; color: #0066cc; }}
         .readme-section h4 {{ font-size: 14px; margin-top: 15px; margin-bottom: 8px; color: #555; }}
         .readme-section p {{ margin-bottom: 12px; }}
         .readme-section ul {{ margin-left: 20px; margin-bottom: 12px; }}
         .readme-section li {{ margin-bottom: 6px; }}
         .readme-section code {{ background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-family: monospace; }}
         .readme-section pre {{
             background: #f5f5f5;
             padding: 12px;
             border-radius: 3px;
             overflow-x: auto;
             margin: 10px 0;
             font-family: monospace;
             font-size: 12px;
             line-height: 1.4;
         }}
         .readme-section a {{ color: #0066cc; text-decoration: none; }}
         .readme-section a:hover {{ text-decoration: underline; }}
        
        footer {{
            text-align: center;
            padding: 20px;
            font-size: 13px;
            color: #666;
            border-top: 1px solid #eee;
            margin-top: 60px;
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>OpenCode Configuration Browser</h1>
            <p class="subtitle">Browse configurations, agents, and commands</p>
        </div>
    </header>
    
    <div class="container">
         <div class="readme-section">
             <h2>About This Repository</h2>
             <div style="line-height: 1.8;">
                 {readme_html or '<p>OpenCode configuration repository</p>'}
             </div>
         </div>
        
        <div class="file-tree-section">
            <h2>Complete File Tree</h2>
            <div class="file-tree">
{'<br>'.join(file_tree)}
            </div>
        </div>
        
        <footer>
            <p>Repository: <a href="https://github.com/fangjunzhou/opencode-config">fangjunzhou/opencode-config</a></p>
            <p><a href="./distributions/">Download Distributions</a> | <a href="./shared-config/">Shared Config</a> | <a href="./.opencode/">.opencode Directory</a></p>
            <p style="margin-top: 20px; font-size: 12px;">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
        </footer>
    </div>
</body>
</html>
"""
    
    return html


if __name__ == '__main__':
    repo_root = sys.argv[1] if len(sys.argv) > 1 else '.'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'index.html'
    
    html = generate_index_html(repo_root)
    
    output_path = os.path.join(repo_root, output_file)
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f"Generated {output_file} for {repo_root}")
