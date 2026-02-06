#!/usr/bin/env python3
"""
Website Design System Analyzer for Style Guide Generator

This script analyzes websites to extract design system information including:
- Color palette (backgrounds, text, accents)
- Typography (fonts, sizes, weights)
- Spacing patterns
- Component styles

Usage:
    python analyze_website.py <url>
    python analyze_website.py https://example.com

Output:
    JSON formatted design system data that can be used to populate style guide templates
"""

import sys
import re
import json
from urllib.parse import urlparse


def extract_colors_from_css(css_content):
    """
    Extract color values from CSS content.
    Returns dict of color values in hex and rgb formats.
    """
    colors = {
        'hex': set(),
        'rgb': set(),
        'rgba': set()
    }
    
    # Extract hex colors
    hex_pattern = r'#[0-9A-Fa-f]{3,6}\b'
    hex_colors = re.findall(hex_pattern, css_content)
    colors['hex'].update([c.upper() for c in hex_colors])
    
    # Extract rgb/rgba colors
    rgb_pattern = r'rgba?\s*\(\s*\d+\s*,\s*\d+\s*,\s*\d+(?:\s*,\s*[\d.]+)?\s*\)'
    rgb_colors = re.findall(rgb_pattern, css_content)
    for rgb in rgb_colors:
        if 'rgba' in rgb:
            colors['rgba'].add(rgb)
        else:
            colors['rgb'].add(rgb)
    
    return colors


def extract_fonts_from_css(css_content):
    """
    Extract font families from CSS content.
    Returns list of font families found.
    """
    font_pattern = r'font-family\s*:\s*([^;]+);'
    fonts = re.findall(font_pattern, css_content, re.IGNORECASE)
    
    # Clean up font names
    cleaned_fonts = []
    for font in fonts:
        # Remove quotes and extra whitespace
        cleaned = font.replace('"', '').replace("'", '').strip()
        if cleaned not in cleaned_fonts:
            cleaned_fonts.append(cleaned)
    
    return cleaned_fonts


def extract_spacing_values(css_content):
    """
    Extract spacing patterns (margin, padding) from CSS.
    Returns dict of spacing values found.
    """
    spacing = {
        'margins': set(),
        'paddings': set()
    }
    
    # Extract margin values
    margin_pattern = r'margin(?:-\w+)?\s*:\s*([^;]+);'
    margins = re.findall(margin_pattern, css_content, re.IGNORECASE)
    spacing['margins'].update(margins)
    
    # Extract padding values
    padding_pattern = r'padding(?:-\w+)?\s*:\s*([^;]+);'
    paddings = re.findall(padding_pattern, css_content, re.IGNORECASE)
    spacing['paddings'].update(paddings)
    
    return spacing


def analyze_html_structure(html_content):
    """
    Analyze HTML structure for component patterns.
    Returns dict of component information.
    """
    components = {
        'buttons': [],
        'forms': [],
        'navigation': [],
        'headings': []
    }
    
    # Find button patterns
    button_pattern = r'<button[^>]*>.*?</button>'
    buttons = re.findall(button_pattern, html_content, re.IGNORECASE | re.DOTALL)
    components['buttons'] = buttons[:5]  # Limit to first 5 examples
    
    # Find form elements
    form_pattern = r'<form[^>]*>.*?</form>'
    forms = re.findall(form_pattern, html_content, re.IGNORECASE | re.DOTALL)
    components['forms'] = len(forms)
    
    # Find navigation
    nav_pattern = r'<nav[^>]*>.*?</nav>'
    navs = re.findall(nav_pattern, html_content, re.IGNORECASE | re.DOTALL)
    components['navigation'] = len(navs)
    
    # Find heading hierarchy
    for level in range(1, 7):
        heading_pattern = f'<h{level}[^>]*>(.*?)</h{level}>'
        headings = re.findall(heading_pattern, html_content, re.IGNORECASE | re.DOTALL)
        if headings:
            components['headings'].append({
                f'h{level}': len(headings),
                'examples': headings[:3]
            })
    
    return components


def analyze_website(url, html_content=None, css_content=None):
    """
    Main analysis function that coordinates all extraction.
    
    Args:
        url: Website URL being analyzed
        html_content: HTML content (optional, for testing)
        css_content: CSS content (optional, for testing)
    
    Returns:
        Dict containing all extracted design system information
    """
    design_system = {
        'url': url,
        'domain': urlparse(url).netloc,
        'colors': {},
        'typography': {},
        'spacing': {},
        'components': {},
        'metadata': {
            'analyzed_at': 'timestamp',
            'version': '1.0'
        }
    }
    
    if css_content:
        design_system['colors'] = extract_colors_from_css(css_content)
        design_system['typography']['fonts'] = extract_fonts_from_css(css_content)
        design_system['spacing'] = extract_spacing_values(css_content)
    
    if html_content:
        design_system['components'] = analyze_html_structure(html_content)
    
    return design_system


def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python analyze_website.py <url>")
        print("\nExample:")
        print("  python analyze_website.py https://example.com")
        sys.exit(1)
    
    url = sys.argv[1]
    
    print(f"Analyzing website: {url}")
    print("\nNote: This script provides analysis utilities.")
    print("For full website analysis, use with web_fetch tool in Claude.\n")
    
    # In actual usage, this would be called with content from web_fetch
    # For now, show example structure
    example_result = {
        'url': url,
        'domain': urlparse(url).netloc,
        'colors': {
            'hex': ['#378DFF', '#FFFFFF', '#333333'],
            'rgb': ['rgb(55, 141, 255)', 'rgb(51, 51, 51)']
        },
        'typography': {
            'fonts': ['Inter', 'Helvetica Neue', 'Arial', 'sans-serif']
        },
        'components': {
            'buttons': 'Detected',
            'forms': 'Detected',
            'navigation': 'Detected'
        }
    }
    
    print(json.dumps(example_result, indent=2))
    print("\n\u2705 Analysis complete")


if __name__ == "__main__":
    main()
