from flask import Flask, request, send_file, render_template_string
import qrcode
import os

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>QR Code Generator</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(120deg, #e0eafc 0%, #cfdef3 100%);
            font-family: 'Segoe UI', Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            animation: fadeInBg 1.2s;
        }
        @keyframes fadeInBg {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        h1 {
            margin-top: 60px;
            color: #1a237e;
            letter-spacing: 2px;
            font-size: 2.7rem;
            text-shadow: 0 2px 8px #b3c6e7;
            animation: slideDown 1s;
        }
        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-40px);}
            to { opacity: 1; transform: translateY(0);}
        }
        form {
            background: #fff;
            padding: 36px 44px;
            border-radius: 18px;
            box-shadow: 0 8px 32px rgba(44, 62, 80, 0.18);
            margin-top: 36px;
            display: flex;
            gap: 18px;
            align-items: center;
            animation: fadeInForm 1.2s;
        }
        @keyframes fadeInForm {
            from { opacity: 0; transform: scale(0.95);}
            to { opacity: 1; transform: scale(1);}
        }
        input[type="text"] {
            padding: 14px 18px;
            border: 1.5px solid #b0bec5;
            border-radius: 9px;
            font-size: 1.15rem;
            width: 270px;
            transition: border 0.2s, box-shadow 0.2s;
            box-shadow: 0 1px 4px rgba(44, 62, 80, 0.05);
        }
        input[type="text"]:focus {
            border: 2px solid #1976d2;
            outline: none;
            box-shadow: 0 2px 8px #90caf9;
        }
        button {
            background: linear-gradient(90deg, #1976d2 0%, #42a5f5 100%);
            color: #fff;
            border: none;
            border-radius: 9px;
            padding: 14px 32px;
            font-size: 1.15rem;
            cursor: pointer;
            transition: background 0.2s, transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 2px 8px rgba(25, 118, 210, 0.10);
            font-weight: 500;
        }
        button:hover {
            background: linear-gradient(90deg, #1565c0 0%, #1e88e5 100%);
            transform: translateY(-2px) scale(1.05);
            box-shadow: 0 4px 16px #90caf9;
        }
        .qr-section {
            margin-top: 48px;
            text-align: center;
            animation: fadeInQR 1.2s;
        }
        @keyframes fadeInQR {
            from { opacity: 0; transform: translateY(40px);}
            to { opacity: 1; transform: translateY(0);}
        }
        .qr-section h3 {
            color: #1976d2;
            font-size: 1.3rem;
            margin-bottom: 18px;
            letter-spacing: 1px;
        }
        .qr-section img {
            margin-top: 10px;
            border-radius: 14px;
            box-shadow: 0 4px 24px rgba(44, 62, 80, 0.13);
            width: 220px;
            height: 220px;
            animation: popIn 1.2s;
        }
        @keyframes popIn {
            from { opacity: 0; transform: scale(0.8);}
            to { opacity: 1; transform: scale(1);}
        }
        .download-link {
            display: inline-block;
            margin-top: 22px;
            padding: 12px 28px;
            background: linear-gradient(90deg, #43a047 0%, #66bb6a 100%);
            color: #fff;
            border-radius: 9px;
            text-decoration: none;
            font-weight: 500;
            font-size: 1.08rem;
            transition: background 0.2s, transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 2px 8px rgba(67, 160, 71, 0.10);
        }
        .download-link:hover {
            background: linear-gradient(90deg, #388e3c 0%, #43a047 100%);
            transform: scale(1.06);
            box-shadow: 0 4px 16px #a5d6a7;
        }
        @media (max-width: 600px) {
            form { flex-direction: column; gap: 14px; padding: 24px 12px;}
            input[type="text"] { width: 100%; }
            .qr-section img { width: 160px; height: 160px; }
        }
    </style>
</head>
<body>
    <h1>QR Code Generator</h1>
    <form method="POST" autocomplete="off">
        <input type="text" name="data" placeholder="Enter data here" required>
        <button type="submit">Generate</button>
    </form>

    {% if qr_generated %}
        <div class="qr-section">
            <h3>Your QR Code:</h3>
            <img src="{{ url_for('static', filename='qr_code.png') }}" alt="QR Code">
            <br>
            <a class="download-link" href="/download">Download QR Code</a>
        </div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_generated = False
    if request.method == 'POST':
        data = request.form['data']
        img = qrcode.make(data)
        os.makedirs('static', exist_ok=True)
        img.save('static/qr_code.png')
        qr_generated = True
    return render_template_string(TEMPLATE, qr_generated=qr_generated)

@app.route('/download')
def download():
    return send_file('static/qr_code.png', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
