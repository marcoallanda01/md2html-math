import markdown
from typing import Union
import os
from pathlib import Path
import jinja2

def _get_template():
    """Get the Jinja2 template for HTML output."""
    template_dir = Path(__file__).parent / 'templates'
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(template_dir)),
        autoescape=True
    )
    return env.get_template('base.html')

def markdown_to_html(markdown_text: Union[str, None]) -> str:
    """
    Convert a markdown string to HTML.
    
    Args:
        markdown_text (Union[str, None]): The markdown text to convert. Can be None or empty string.
        
    Returns:
        str: The converted HTML string.
        
    Raises:
        ValueError: If the input is None or not a string.
    """
    if markdown_text is None:
        raise ValueError("Input cannot be None")
    
    if not isinstance(markdown_text, str):
        raise ValueError("Input must be a string")
    
    # Configure markdown extensions for better HTML output
    extensions = [
        'extra',  # Adds support for tables, fenced code blocks, etc.
        'pymdownx.superfences',  # Better fenced code block support
        'codehilite',  # Adds syntax highlighting to code blocks
        'tables',  # Better table support
        'nl2br',  # Convert newlines to <br> tags
        'sane_lists',  # Better list handling
        'footnotes',  # Footnote support
        'toc',  # Table of contents support
        'pymdownx.arithmatex',  # LaTeX math support
    ]
    
    # Configure extensions
    extension_configs = {
        'codehilite': {
            'css_class': 'hljs',
            'use_pygments': False,
            'noclasses': True,
            'guess_lang': True
        },
        'pymdownx.superfences': {
            'css_class': 'hljs',
            'preserve_tabs': True,
            'disable_indented_code_blocks': False
        },
        'pymdownx.arithmatex': {
            'generic': True,
            'preview': False
        }
    }
    
    # Convert markdown to HTML
    html = markdown.markdown(
        markdown_text,
        extensions=extensions,
        extension_configs=extension_configs,
        output_format='html5'
    )
    
    # Wrap in template
    template = _get_template()
    return template.render(
        title="Markdown Document",
        content=html
    )

def markdown_file_to_html(markdown_file: str, output_file: Union[str, None] = None) -> str:
    """
    Convert a markdown file to HTML and optionally save it to a file.
    
    Args:
        markdown_file (str): Path to the markdown file to convert.
        output_file (Union[str, None], optional): Path where to save the HTML output.
            If None, the output will be saved with the same name as input but .html extension.
            
    Returns:
        str: The converted HTML string if output_file is None, otherwise an empty string.
        
    Raises:
        FileNotFoundError: If the markdown file doesn't exist.
        ValueError: If the markdown file is not a .md file.
    """
    if not os.path.exists(markdown_file):
        raise FileNotFoundError(f"Markdown file not found: {markdown_file}")
    
    if not markdown_file.lower().endswith('.md'):
        raise ValueError("Input file must have a .md extension")
    
    # Read the markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_text = f.read()
    
    # Convert to HTML
    html = markdown_to_html(markdown_text)
    
    # If output file is not specified, use input file name with .html extension
    if output_file is None:
        output_file = os.path.splitext(markdown_file)[0] + '.html'
    elif not output_file.lower().endswith('.html'):
        output_file = f"{output_file}.html"
    
    # Save the HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return html
