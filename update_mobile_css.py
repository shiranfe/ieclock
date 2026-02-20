#!/usr/bin/env python3
"""
Mobile CSS Updater for HTML files
Enhances existing media queries with comprehensive mobile-friendly CSS rules.
"""

import re
from pathlib import Path
from typing import Tuple, Optional

def extract_style_section(html_content: str) -> Tuple[Optional[str], Optional[int], Optional[int]]:
    """Extract the style section from HTML content."""
    style_start = html_content.find('<style>')
    style_end = html_content.find('</style>')
    
    if style_start == -1 or style_end == -1:
        return None, None, None
    
    style_content = html_content[style_start + 7:style_end]
    return style_content, style_start + 7, style_end

def find_media_query_bounds(style_content: str, breakpoint: str) -> Tuple[Optional[int], Optional[int]]:
    """Find the start and end positions of a media query block."""
    pattern = rf'@media\s*\(\s*max-width\s*:\s*{re.escape(breakpoint)}\s*\)\s*\{{'
    match = re.search(pattern, style_content)
    
    if not match:
        return None, None
    
    start = match.start()
    brace_count = 0
    found_opening = False
    
    # Find the matching closing brace
    for i in range(match.end() - 1, len(style_content)):
        if style_content[i] == '{':
            brace_count += 1
            found_opening = True
        elif style_content[i] == '}':
            brace_count -= 1
            if found_opening and brace_count == 0:
                return start, i + 1
    
    return None, None

def enhance_media_query(style_content: str, breakpoint: str, new_rules: str) -> str:
    """
    Enhance an existing media query by adding new CSS rules before the closing brace.
    """
    start, end = find_media_query_bounds(style_content, breakpoint)
    
    if start is None or end is None:
        return style_content
    
    # Get the current media query block
    current_block = style_content[start:end]
    
    # Insert new rules before the closing brace
    # Find the last closing brace
    insert_pos = current_block.rfind('}')
    if insert_pos != -1:
        enhanced_block = current_block[:insert_pos] + new_rules + current_block[insert_pos:]
        return style_content[:start] + enhanced_block + style_content[end:]
    
    return style_content

# CSS rules to add to each media query
MEDIA_QUERY_ENHANCEMENTS = {
    "320px": """
      
      /* Mobile optimizations for 320px - Extra small screens */
      .container {
        padding: 0 12px !important;
      }
      
      section {
        padding: 32px 0 !important;
      }
      
      .section-title {
        font-size: clamp(1.25rem, 4vw, 1.75rem) !important;
      }
      
      .section-subtitle {
        font-size: 0.9rem !important;
        margin-bottom: 1.5rem !important;
      }
      
      button, .btn, input[type="button"], input[type="submit"] {
        min-height: 44px !important;
        padding: 10px 14px !important;
        font-size: 13px !important;
      }
      
      nav {
        padding: 12px 0 !important;
      }
      
      h1 { font-size: clamp(1.35rem, 5vw, 1.75rem) !important; }
      h2 { font-size: clamp(1.15rem, 4vw, 1.5rem) !important; }
      h3 { font-size: clamp(0.95rem, 3.5vw, 1.2rem) !important; }
    """,
    
    "480px": """
      
      /* Mobile optimizations for 480px - Small phones */
      .container {
        padding: 0 16px !important;
      }
      
      section {
        padding: 40px 0 !important;
      }
      
      .section-title {
        font-size: clamp(1.5rem, 5vw, 2.25rem) !important;
        margin-bottom: 0.5em !important;
      }
      
      .section-subtitle {
        font-size: 0.95rem !important;
        margin-bottom: 2rem !important;
      }
      
      .section-header {
        margin-bottom: 2rem !important;
      }
      
      button, .btn, input[type="button"], input[type="submit"] {
        min-height: 48px !important;
        padding: 12px 18px !important;
        font-size: 15px !important;
      }
      
      nav {
        padding: 0.875rem 0 !important;
      }
      
      .nav-link, nav a {
        padding: 8px 12px !important;
      }
      
      h1 { font-size: clamp(1.5rem, 6vw, 2.25rem) !important; }
      h2 { font-size: clamp(1.25rem, 5vw, 1.75rem) !important; }
      h3 { font-size: clamp(1rem, 4vw, 1.35rem) !important; }
      
      /* Ensure grids stack on mobile */
      .grid, .grid-2, .grid-3, [class*="grid-cols"] {
        grid-template-columns: 1fr !important;
        gap: 1.5rem !important;
      }
      
      .hero-image img {
        max-height: 300px !important;
        width: 100% !important;
      }
    """,
    
    "600px": """
      
      /* Mobile optimizations for 600px - Tablets/landscape phones */
      .container {
        padding: 0 20px !important;
      }
      
      section {
        padding: 48px 0 !important;
      }
      
      .section-title {
        font-size: clamp(1.75rem, 5vw, 2.5rem) !important;
      }
      
      button, .btn, input[type="button"], input[type="submit"] {
        min-height: 48px !important;
        padding: 12px 20px !important;
      }
      
      /* Ensure grids stack */
      .grid, .grid-2, .grid-3, [class*="grid-cols"], .grid-cols-2, .grid-cols-3 {
        grid-template-columns: 1fr !important;
        gap: 1.5rem !important;
      }
      
      .footer-grid {
        grid-template-columns: 1fr !important;
      }
      
      .product-image {
        max-height: 250px !important;
      }
    """,
    
    "768px": """
      
      /* Mobile optimizations for 768px - Small tablets */
      .container {
        padding: 0 20px !important;
      }
      
      section {
        padding: 48px 0 !important;
      }
      
      .section-title {
        font-size: clamp(1.75rem, 5vw, 2.5rem) !important;
      }
      
      .section-subtitle {
        font-size: 1rem !important;
        margin-bottom: 2rem !important;
      }
      
      button, .btn, input[type="button"], input[type="submit"] {
        min-height: 48px !important;
        padding: 12px 20px !important;
        font-size: 15px !important;
      }
      
      nav {
        padding: 0.875rem 0 !important;
      }
      
      .nav-link, nav a {
        padding: 10px 14px !important;
      }
      
      /* Ensure grids stack */
      .grid, .grid-2, .grid-3, [class*="grid-cols"], .grid-cols-2, .grid-cols-3 {
        grid-template-columns: 1fr !important;
        gap: 2rem !important;
      }
      
      .footer-grid {
        grid-template-columns: 1fr !important;
      }
      
      .hero {
        flex-direction: column !important;
      }
      
      .hero-content {
        order: 2 !important;
      }
      
      .hero-image {
        order: 1 !important;
        margin-bottom: 2rem !important;
      }
    """
}

NEW_320_QUERY = """    @media (max-width: 320px) {
      /* Mobile optimizations for 320px - Extra small screens */
      .container {
        padding: 0 12px;
      }
      
      section {
        padding: 32px 0;
      }
      
      .section-title {
        font-size: clamp(1.25rem, 4vw, 1.75rem);
      }
      
      .section-subtitle {
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
      }
      
      button, .btn, input[type="button"], input[type="submit"] {
        min-height: 44px;
        padding: 10px 14px;
        font-size: 13px;
      }
      
      nav {
        padding: 12px 0;
      }
      
      h1 { font-size: clamp(1.35rem, 5vw, 1.75rem); }
      h2 { font-size: clamp(1.15rem, 4vw, 1.5rem); }
      h3 { font-size: clamp(0.95rem, 3.5vw, 1.2rem); }
    }"""

def update_html_file(file_path: str, dry_run: bool = True) -> Tuple[bool, str, Optional[str]]:
    """Update a single HTML file with improved mobile CSS."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        return False, f"Error reading {file_path}: {e}", None
    
    style_content, style_start, style_end = extract_style_section(html_content)
    if style_content is None:
        return False, f"No style section found", None
    
    new_style_content = style_content
    changes_made = []
    
    # Check if 320px media query exists
    if find_media_query_bounds(style_content, "320px")[0] is None:
        # Add 320px media query if it doesn't exist
        new_style_content += "\n\n" + NEW_320_QUERY
        changes_made.append("Added @media (max-width: 320px)")
    else:
        changes_made.append("Enhanced @media (max-width: 320px)")
    
    # Enhance other media queries
    for breakpoint in ["480px", "600px", "768px"]:
        if find_media_query_bounds(new_style_content, breakpoint)[0] is not None:
            new_style_content = enhance_media_query(new_style_content, breakpoint, MEDIA_QUERY_ENHANCEMENTS[breakpoint])
            changes_made.append(f"Enhanced @media (max-width: {breakpoint})")
    
    # Reconstruct HTML
    new_html_content = html_content[:style_start] + new_style_content + html_content[style_end:]
    
    return True, Path(file_path).name, new_html_content, changes_made

def show_diff_summary(original: str, updated: str) -> None:
    """Show a summary of changes to the CSS."""
    orig_lines = len(original.split('\n'))
    new_lines = len(updated.split('\n'))
    
    print(f"\nStyle section changes:")
    print(f"  Original: {orig_lines} lines")
    print(f"  Updated:  {new_lines} lines")
    print(f"  Added:    {new_lines - orig_lines} lines")
    
    orig_media = len(re.findall(r'@media', original))
    new_media = len(re.findall(r'@media', updated))
    print(f"\nMedia queries:")
    print(f"  Original: {orig_media} queries")
    print(f"  Updated:  {new_media} queries")
    if new_media > orig_media:
        print(f"  Added:    {new_media - orig_media} new query(ies)")

def main():
    """Main function to process all HTML files."""
    html_dir = Path("/home/user/ieclock")
    html_files = sorted(html_dir.glob("**/*.html"))
    
    print("=" * 80)
    print("MOBILE CSS UPDATER - PREVIEW")
    print("=" * 80)
    print(f"Found {len(html_files)} HTML file(s)\n")
    
    # Test on index.html first
    test_file = html_dir / "index.html"
    if not test_file.exists():
        print(f"Error: Test file not found: {test_file}")
        return
    
    print(f"Testing on: {test_file.name}")
    print("-" * 80)
    
    with open(test_file, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    success, filename, new_content, changes = update_html_file(str(test_file), dry_run=True)
    
    if success and new_content:
        orig_style, _, _ = extract_style_section(original_content)
        new_style, _, _ = extract_style_section(new_content)
        
        if orig_style and new_style:
            show_diff_summary(orig_style, new_style)
            
            print(f"\nChanges to be applied:")
            for change in changes:
                print(f"  + {change}")
            
            print("\n" + "=" * 80)
            print("MOBILE IMPROVEMENTS SUMMARY")
            print("=" * 80)
            
            print("\n320px (Extra small screens):")
            print("  - Container padding: 12px")
            print("  - Section padding: 32px")
            print("  - Touch targets: 44px minimum height")
            print("  - Font scaling with clamp()")
            
            print("\n480px (Small phones):")
            print("  - Container padding: 16px")
            print("  - Section padding: 40px")
            print("  - Touch targets: 48px minimum height")
            print("  - Grid layouts: Single column")
            print("  - Hero images: Max 300px height")
            
            print("\n600px (Tablets/landscape phones):")
            print("  - Container padding: 20px")
            print("  - Section padding: 48px")
            print("  - Grid layouts: Single column")
            print("  - Product images: Max 250px height")
            
            print("\n768px (Small tablets):")
            print("  - Container padding: 20px")
            print("  - Section padding: 48px")
            print("  - Full mobile optimizations")
            print("  - Hero sections: Column layout")
            print("  - Footer: Single column")
            
            print("\n" + "=" * 80)
            print("READY TO APPLY")
            print("=" * 80)
            print("\nTo apply these changes to ALL HTML files, run:")
            print("  python3 /home/user/ieclock/update_mobile_css.py --apply")
    else:
        print(f"Error: {filename}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--apply":
            print("=" * 80)
            print("APPLYING MOBILE CSS UPDATES TO ALL HTML FILES")
            print("=" * 80 + "\n")
            
            html_dir = Path("/home/user/ieclock")
            html_files = sorted(html_dir.glob("**/*.html"))
            
            updated_count = 0
            for html_file in html_files:
                success, filename, new_content, changes = update_html_file(str(html_file), dry_run=False)
                
                if success and new_content:
                    try:
                        with open(html_file, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"✓ {filename}")
                        for change in changes:
                            print(f"    {change}")
                        updated_count += 1
                    except Exception as e:
                        print(f"✗ {filename} - Error: {e}")
                else:
                    print(f"✗ {filename}")
            
            print("\n" + "=" * 80)
            print(f"Successfully updated {updated_count}/{len(html_files)} file(s)")
            print("=" * 80)
        
        elif sys.argv[1] == "--help":
            print("Mobile CSS Updater")
            print("\nUsage:")
            print("  python3 update_mobile_css.py          # Show preview of changes")
            print("  python3 update_mobile_css.py --apply   # Apply to all HTML files")
            print("  python3 update_mobile_css.py --help    # Show this help message")
        else:
            print("Unknown option. Use --help for available options.")
    else:
        main()
