from flask import Flask, render_template, request, send_from_directory, Response
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
    print(data)
    link = data["link"]
    audio_video = data["audioVideo"]
    form = data["format"]
    quality = data["quality"]
    if (audio_video == "audio" and form != "none"):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': form,
                'preferredquality': quality,
            }],
            'outtmpl': 'temp/%(title)s.%(ext)s',
            'logger': logging.getLogger(),
        }
    elif (audio_video == "video"):
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'temp/%(title)s.%(ext)s',
            'logger': logging.getLogger(),
        }
    else:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
            }],
            'outtmpl': 'temp/%(title)s.%(ext)s',
            'logger': logging.getLogger(),
        }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            ext = info.get("ext")
            filename = ydl.prepare_filename(info)
        title = filename.replace(("." + ext), "")
        title = title.replace(("temp/"), "")
        for name in os.listdir(temp_path):
            if title in name:
                found_file = name
        return send_from_directory(temp_path, found_file, as_attachment=True)
    except Exception as e:
        logging.error(e)
        return Response("{'error': e}", status=403, mimetype='application/json')