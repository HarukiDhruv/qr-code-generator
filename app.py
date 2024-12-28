from flask import Flask, render_template, request, jsonify
import qrcode
from io import BytesIO
import base64
from PIL import Image, ImageDraw

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.form.get('data')
    fg_color = request.form.get('fgColor', 'black')
    bg_color = request.form.get('bgColor', 'white')
    frame_shape = request.form.get('shape', 'square')

    if not data:
        return jsonify({"error": "Data is required!"}), 400

    # Create the QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=fg_color, back_color=bg_color)

    # Handle frame shape (circle or square)
    if frame_shape == 'circle':
        qr_img = qr_img.convert("RGBA")
        mask = Image.new("L", qr_img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + qr_img.size, fill=255)
        qr_img.putalpha(mask)

    # Convert QR code to base64
    buffered = BytesIO()
    qr_img.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return jsonify({"qr_code": qr_base64})

if __name__ == '__main__':
    app.run(debug=True)


