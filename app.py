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

@app.route("/create_sn_sheet", methods=["POST"])
def create_sn_sheet():
    data = request.json  # Get data from the frontend
    postfix = data.get("postfix")
    variant = data.get("variant")

    if not postfix or not variant:
        return jsonify({"message": "Error: Please select both a postfix and a variant."})

    # Logic for creating the SN Creation Sheet
    result_message = f"SN Sheet Created with Postfix: {postfix} and Variant Path: {variant}"
    return jsonify({"message": result_message})

@app.route('/create_mapping_sheet', methods=['POST'])
def create_mapping_sheet():
    selected_variants = request.json.get('selected_variants')
    selected_ids = [variant_ids.get(variant, "Unknown") for variant in selected_variants if variant != 'more']
    return jsonify(message=f"Mapping Sheets for IDs: {', '.join(selected_ids)}")

if __name__ == '__main__':
    app.run(debug=True)
