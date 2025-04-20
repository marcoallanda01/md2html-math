from md2html.converter import markdown_to_html

markdown = """# Math Examples

Here's Einstein's famous equation: $E = mc^2$

And here's a more complex inline formula: $\\sqrt{x^2 + y^2} = r$

Here's a block equation:

$$
\\int_{0}^{\\infty} e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}
$$"""

html = markdown_to_html(markdown)

# Save the output
with open('test_output.html', 'w') as f:
    f.write(html)

print("HTML file generated as test_output.html") 