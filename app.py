from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Variables for handling data
variant_ids = {
    'GA': 'I12345',
    'GD': 'I67890',
    'GX': 'I11223',
    'GY': 'I44556',
    'GZ': 'I77889'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_postfix', methods=['POST'])
def process_postfix():
    selected_postfix = request.json.get('postfix')
    if selected_postfix == "Other":
        return jsonify(prompt=True)
    return jsonify(prompt=False, message=f"Selected Postfix: {selected_postfix}")

@app.route('/process_variant', methods=['POST'])
def process_variant():
    variant = request.json.get('variant')
    if variant == "Other":
        return jsonify(prompt=True)
    variant_path = {'GA': 'path1', 'GD': 'path2', 'GX': 'path3'}.get(variant, 'default_path')
    return jsonify(prompt=False, message=f"Selected Variant Path: {variant_path}")

@app.route('/create_sn_sheet', methods=['POST'])
def create_sn_sheet():
    postfix = request.json.get('postfix')
    variant_path = request.json.get('variant_path')
    if not postfix or not variant_path:
        return jsonify(success=False, message="Please select a postfix and variant.")
    return jsonify(success=True, message=f"SN Sheet Created with Postfix: {postfix} and Path: {variant_path}")

@app.route('/create_mapping_sheet', methods=['POST'])
def create_mapping_sheet():
    selected_variants = request.json.get('selected_variants')
    selected_ids = [variant_ids.get(variant, "Unknown") for variant in selected_variants if variant != 'more']
    return jsonify(message=f"Mapping Sheets for IDs: {', '.join(selected_ids)}")

if __name__ == '__main__':
    app.run(debug=True)
