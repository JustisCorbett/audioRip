from flask import Flask, render_template, request, send_file
import logging
import yt_dlp
import os

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
        'outtmpl': 'temp/%(title)s.%(ext)s',
        'logger': logging.getLogger(),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        ext = info.get("ext")
        filename = ydl.prepare_filename(info)
    title = filename.replace(("." + ext), "")
    title = title.replace(("temp/"), "")
    for name in os.listdir(temp_path):
        if title in name:
            found_file = name
    return send_file(temp_path + "/" + found_file)