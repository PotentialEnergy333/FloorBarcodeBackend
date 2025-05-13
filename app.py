from flask import Flask, request, render_template, send_file
from PDFGenerator import generate_pdf
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    input_text = request.form.get('barcode_input', '')
    mode = request.form.get('mode', 'standard')
    action = request.form.get('action', 'view')  # 'view' or 'download'

    barcode_list = [line.strip() for line in input_text.strip().split('\n') if line.strip()]
    pdf_stream = generate_pdf(barcode_list, mode=mode)

    return send_file(
        pdf_stream,
        mimetype='application/pdf',
        as_attachment=(action == 'download'),
        download_name='barcodes.pdf',
    )


if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)