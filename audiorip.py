from flask import Flask, render_template, request, send_from_directory, Response, jsonify
import logging
import yt_dlp
from pathlib import Path
import time
from flask_crontab import Crontab

app = Flask(__name__)
crontab = Crontab(app)

# delete old temporary files cronjob
@crontab.job(minute="30", hour="0")
def delete_temp_files():
    temp_dir = Path("/temp")
    curr_time = time.time()
    for file in temp_dir:
        if file.stat().st_mtime - curr_time > 600:
            file.unlink()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get_link", methods=["POST"])
def get_link():
    data = request.get_json()
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
            'noplaylist': True,
            'outtmpl': 'temp/%(title)s.%(ext)s',
            'logger': logging.getLogger(),
            'restrictfilenames': True,
        }
    elif (audio_video == "video"):
        ydl_opts = {
            'format': 'best',
            'noplaylist': True,
            'outtmpl': 'temp/%(title)s.%(ext)s',
            'logger': logging.getLogger(),
            'restrictfilenames': True,
        }
    else:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
            }],
            'noplaylist': True,
            'outtmpl': 'temp/%(title)s.opus',
            'logger': logging.getLogger(),
            'restrictfilenames': True,
        }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            if (form != None):
                ext = info.get("ext")
            else:
                ext = "opus"
            filename = ydl.prepare_filename(info)
        if (audio_video != "video"):
            title = filename.replace(ext,form)
        else:
            title = filename
        return jsonify(filename=title)
    except Exception as e:
        logging.error(e)
        return Response(e, status=403, mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)