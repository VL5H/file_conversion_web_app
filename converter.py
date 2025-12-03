from markitdown import MarkItDown

def convert_pdf_to_markdown(pdf_path, output_path=None):
    md = MarkItDown()
    result = md.convert(pdf_path)
    markdown_output = result.text_content
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_output)
    return markdown_output

# Example usage:
# markdown_output = convert_pdf_to_markdown("input.pdf")
# convert_pdf_to_markdown("input.pdf", output_path="output.md")