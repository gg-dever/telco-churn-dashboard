import json

# Read notebook
with open('telco_churn.ipynb', 'r') as f:
    nb = json.load(f)

with open('analysis_review.txt', 'w', encoding='utf-8') as out:
    out.write("=" * 80 + "\n")
    out.write("TELCO CHURN ANALYSIS - MARKDOWN & OUTPUTS ONLY\n")
    out.write("=" * 80 + "\n\n")

    for i, cell in enumerate(nb['cells'], 1):
        if cell['cell_type'] == 'markdown':
            out.write(f"[MARKDOWN CELL {i}]\n")
            out.write("-" * 80 + "\n")
            content = ''.join(cell['source'])
            out.write(content + "\n")
            out.write("-" * 80 + "\n\n")

        elif cell['cell_type'] == 'code' and cell.get('outputs'):
            out.write(f"[CODE OUTPUT {i}]\n")
            out.write("-" * 80 + "\n")
            for output in cell['outputs']:
                if output['output_type'] == 'stream':
                    out.write(''.join(output['text']) + "\n")
                elif output['output_type'] in ['execute_result', 'display_data']:
                    if 'text/plain' in output.get('data', {}):
                        out.write(''.join(output['data']['text/plain']) + "\n")
                    if 'text/html' in output.get('data', {}):
                        out.write("[HTML TABLE OUTPUT]\n")
                    if 'image/png' in output.get('data', {}):
                        out.write("[IMAGE/CHART OUTPUT]\n")
            out.write("-" * 80 + "\n\n")

    out.write("=" * 80 + "\n")
    out.write("END OF ANALYSIS\n")
    out.write("=" * 80 + "\n")

print("✓ Created: analysis_review.txt")
