import os
from flask import Flask, render_template, request, redirect, flash
import io, base64
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'GEHEIMESLEUTEL'
app.config['UPLOAD_FOLDER'] = 'uploads'

ALLOWED_EXTENSIONS = {'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    image_data = None
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Geen bestand gevonden.', 'warning')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Geen bestand geselecteerd.', 'warning')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            try:
                img = Image.open(file)
                img = img.resize((64, 64), Image.LANCZOS)
                img_io = io.BytesIO()
                img.save(img_io, format='PNG')
                img_io.seek(0)
                image_data = base64.b64encode(img_io.getvalue()).decode('utf-8')
                flash('Icon is succesvol geconverteerd!', 'success')
            except Exception as e:
                flash('Fout bij verwerken van het bestand.', 'danger')
                return redirect(request.url)
        else:
            flash('Alleen PNG-bestanden zijn toegestaan.', 'danger')
            return redirect(request.url)
    
    return render_template('index.html', image_data=image_data)

if __name__ == '__main__':
    app.run(debug=True, port=4003)
