from flask import Flask, render_template, request, jsonify, send_file
import logging
import magic
import yt_dlp
import os
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
    file_info = BytesIO()
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            #'preferredcodec': 'mp3',
            #'preferredquality': '192',
        }],
        #'ffmpeg_location': 'ffmpeg-4.4-essentials_build/bin',
        'outtmpl': 'temp/%(title)s.%(ext)s',
        'logger': logging.getLogger(),
        #'quiet': True,
    }
    with redirect_stdout(file_info):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            filename = ydl.prepare_filename(info)
    print(filename)
    for name in os.listdir('/temp'):
        if filename in name:
            print (name)
    mime_type = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)
    print(mime_type)
    return send_file(file)
#"-o temp/%(title)s.%(ext)s"    '