import json
import html

# Read the notebook
with open('telco_churn.ipynb', 'r') as f:
    notebook = json.load(f)

# Start HTML
html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Telco Churn Analysis - Review</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1000px; margin: 40px auto; padding: 0 20px; line-height: 1.6; }
        .markdown-cell { margin: 20px 0; }
        .output-cell { margin: 20px 0; padding: 15px; background: #f5f5f5; border-left: 3px solid #2196F3; }
        h1 { color: #1976D2; border-bottom: 2px solid #1976D2; padding-bottom: 10px; }
        h2 { color: #424242; margin-top: 30px; }
        h3 { color: #616161; }
        table { border-collapse: collapse; width: 100%; margin: 15px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #2196F3; color: white; }
        pre { background: #f5f5f5; padding: 10px; overflow-x: auto; }
        code { background: #f5f5f5; padding: 2px 5px; }
        img { max-width: 100%; height: auto; }
        .output-text { white-space: pre-wrap; font-family: monospace; }
    </style>
</head>
<body>
"""

# Process cells
for cell in notebook['cells']:
    if cell['cell_type'] == 'markdown':
        # Add markdown content
        content = ''.join(cell['source'])
        # Basic markdown to HTML conversion
        content = content.replace('\n\n', '</p><p>')
        content = content.replace('**', '<strong>').replace('**', '</strong>')

        # Convert headers
        for i in range(6, 0, -1):
            content = content.replace('#' * i + ' ', f'<h{i}>')
            content = content.replace('\n', f'</h{i}>\n', 1)

        html_content += f'<div class="markdown-cell">{content}</div>\n'

    elif cell['cell_type'] == 'code' and 'outputs' in cell and cell['outputs']:
        # Add outputs only
        html_content += '<div class="output-cell">\n'

        for output in cell['outputs']:
            if output['output_type'] == 'stream':
                text = ''.join(output['text'])
                html_content += f'<pre class="output-text">{html.escape(text)}</pre>\n'

            elif output['output_type'] == 'execute_result' or output['output_type'] == 'display_data':
                # Handle text/plain
                if 'text/plain' in output.get('data', {}):
                    text = ''.join(output['data']['text/plain'])
                    html_content += f'<pre class="output-text">{html.escape(text)}</pre>\n'

                # Handle HTML tables
                if 'text/html' in output.get('data', {}):
                    html_data = ''.join(output['data']['text/html'])
                    html_content += html_data + '\n'

                # Handle images
                if 'image/png' in output.get('data', {}):
                    img_data = output['data']['image/png']
                    html_content += f'<img src="data:image/png;base64,{img_data}" />\n'

        html_content += '</div>\n'

# Close HTML
html_content += """
</body>
</html>
"""

# Write output
with open('telco_churn_simplified.html', 'w') as f:
    f.write(html_content)

print("Simplified HTML created: telco_churn_simplified.html")
