from flask import Flask, render_template, request, jsonify, send_file
import logging
import magic
import yt_dlp
import os
from contextlib import redirect_stdout
from io import BytesIO

app = Flask(__name__)

temp_path = os.environ.get("TEMP_FOLDER_PATH")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get_link", methods=["POST"])
def get_link():
    data = request.get_json()
    link = data["link"]
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
            ext = info.get("ext")
            filename = ydl.prepare_filename(info)
    title = filename.replace(("." + ext), "")
    title = title.replace(("temp/"), "")
    for name in os.listdir(temp_path):
        if title in name:
            found_file = name
   # mime_type = magic.from_buffer(file.read(1024), mime=True)
    #file.seek(0)
    return send_file(temp_path + "/" + found_file)
#"-o temp/%(title)s.%(ext)s"    '