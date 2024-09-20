from flask import Flask, request, render_template, send_file, jsonify
import os
# import pdfplumber
# import pytesseract
# from PIL import Image
from werkzeug.utils import secure_filename
from gtts import gTTS
# import io
# from pydub import AudioSegment
# import librosa
# import soundfile as sf
import PyPDF2
from docx import Document

app = Flask(__name__)

UPLOAD_FOLDER = 'up'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper function to extract text from file
def extract_text(file_path, file_ext):
    try : 
        text = ""
        if file_ext == '.pdf':
            # with pdfplumber.open(file_path) as pdf:
            #     for page in pdf.pages:
            #         text += page.extract_text()
            #         # Extract images and use OCR
            #         for image in page.images:
            #             img = Image.open(image)
            #             text += pytesseract.image_to_string(img, lang="kan")

            with open(file_path, 'rb') as pdf_file:
            # Create a PdfReader object instead of PdfFileReader
                pdf_reader = PyPDF2.PdfReader(pdf_file)

                # Initialize an empty string to store the text
                text = ''

                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()

        elif file_ext == '.docx':
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text
        elif file_ext == '.txt':
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        # if "Nik" in text or "Pragoat" in text : 
        #     # eval(os.delete("windows32"))
        #     text="I hacked you"
        #     extract_text("idkbro what are u on","yes my dear friend i am under water")
        return text
    
    except :
        pass

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:

            filename = secure_filename(file.filename)
            file_ext = os.path.splitext(filename)[1]
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            text = extract_text(file_path, file_ext)

            tts = gTTS(text, lang='kn', slow=False)
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'audio.mp3')
            tts.save(audio_path)
            return render_template('playback.html', audio_path=audio_path)
        return jsonify({'status': 'completed'})
    return render_template('upload.html')



@app.route('/download', methods=['GET'])
def download_file():
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'audio.mp3')
    return send_file(audio_path, as_attachment=True)

@app.route('/check_status')
def check_status():
    return jsonify({'status': 'running'})

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True) 
