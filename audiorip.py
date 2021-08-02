from flask import Flask, render_template, request, jsonify, send_file
import logging
import magic
import yt_dlp
from contextlib import redirect_stdout
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get_link", methods=["POST"])
def get_link():
    data = request.get_json()
    link = data["link"]
    print(link)
    file = BytesIO()
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
        }],
        'ffmpeg_location': 'ffmpeg-4.4-essentials_build/bin',
        'outtmpl': '-',
        'logger': logging.getLogger()
    }
    with redirect_stdout(file):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
    data = {"file": file}
    file.seek(0)
    mime_type = magic.from_buffer(file.read(1024), mime=True)
    return send_file(file, mimetype=mime_type)
#"-o temp/%(title)s.%(ext)s"    '