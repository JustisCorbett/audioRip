from flask import Flask, render_template, request, send_from_directory, Response, jsonify
import logging
import yt_dlp
import os

app = Flask(__name__)

#temp_path = os.path

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
            #title = filename.replace(("temp/"), "")
        #else:
            title = filename.replace(ext,form)
            #title = title.replace(("temp/"), "")
        #for name in os.listdir("./temp"):
        #    if title in name:
        #       found_file = name
        #return send_from_directory(temp_path, found_file, as_attachment=True)
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