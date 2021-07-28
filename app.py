from flask import Flask, render_template, request, jsonify
import ffmpeg
import yt_dlp

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get_link", methods=["POST"])
def get_link():
    data = request.get_json()
    link = data["link"]
    print(link)

    ydl_opts = ["-x", "-o temp/%(title)s.%(ext)s"]
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

    return jsonify(True)