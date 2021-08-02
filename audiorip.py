from flask import Flask, render_template, request, jsonify
import logging
import yt_dlp
from contextlib import redirect_stdout
from io import BytesIO

#app = Flask(__name__)
# define Flask app
def create_app():
  try:

    web_app = Flask(__name__)

    logging.info('Starting up..')

    return web_app

  except Exception as e:
    logging.exception(e)


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
    return jsonify(data)
#"-o temp/%(title)s.%(ext)s"    '