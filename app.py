# from Wav2Lip import Processor


# def main():
#     processor = Processor()
#     processor.run(r"C:\Users\HP\Desktop\pro\web\freelance\sc\Wav2lip-Fix-For-Inference\input\vi.mp4", r"C:\Users\HP\Desktop\pro\web\freelance\sc\Wav2lip-Fix-For-Inference\input\au.wav" )


# main()

from __init__ import create_app
from flask import jsonify
from flask_cors import CORS

app = create_app()

cross_origincors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
def index():
    return jsonify(message="Lipsync Backend API")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
