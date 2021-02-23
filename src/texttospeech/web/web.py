import os
from threading import Thread
from time import sleep

from flask import Flask, jsonify, send_file

from texttospeech.util import config

app = Flask(__name__)

FILE_EXTENSION = '.ogg'
AUDIO_FOLDER = '../../' + config.AUDIOS_DIR


@app.route('/<filename>', methods=['GET'])
def audio(filename: str):
    if not filename.endswith(FILE_EXTENSION) or '/' in filename:
        return jsonify(status=403, message='Invalid file!')

    file = os.path.join(AUDIO_FOLDER, filename)

    def remove_audio():
        sleep(10)
        os.remove(config.AUDIOS_DIR + filename)

    Thread(target=remove_audio).start()
    return send_file(file, mimetype='audio/ogg')


def run():
    thread = Thread(target=lambda: app.run(host='0.0.0.0', debug=False))
    thread.start()
