from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/video-info", methods=["POST"])
def video_info():

    data = request.get_json()
    url = data["url"]

    try:

        ydl_opts = {
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return jsonify({
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail")
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


@app.route("/download", methods=["POST"])
def download():

    data = request.get_json()

    url = data["url"]

    try:

        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=True)

            file_path = ydl.prepare_filename(info)

        return send_file(file_path, as_attachment=True)

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
