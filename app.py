from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
import os
import tempfile
from converter import convert_pdf_to_markdown

app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'}), 400

    filename = secure_filename(file.filename)
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(upload_path)

    try:
        # Generate output filename
        base_name = os.path.splitext(filename)[0]
        output_filename = f"{base_name}.md"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        # Convert PDF to Markdown
        markdown_content = convert_pdf_to_markdown(upload_path, output_path=output_path)

        # Clean up uploaded file
        os.remove(upload_path)

        return jsonify({
            'markdown': markdown_content,
            'download_url': f'/download/{output_filename}'
        })

    except Exception as e:
        # Clean up on error
        if os.path.exists(upload_path):
            os.remove(upload_path)
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    safe_filename = secure_filename(filename)
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], safe_filename)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    return send_file(file_path, as_attachment=True)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(debug=True)