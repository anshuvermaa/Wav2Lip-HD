import os
from flask import jsonify, request, Response 
from pathlib import Path
from services.merge_service import clean_files , delete_file_after_delay
from services.wav2lip_inference import run_wav2lip_inference
from utils import get_uploads_dir
from utils import get_delay_minutes
from werkzeug.utils import secure_filename




DEFAULT_AUDIO_FILENAME = "audio.webm"
DEFAULT_VIDEO_FILENAME = "face.webm"
DEFAULT_OUTPUT_FILENAME = "output.mp4"



def init_app(app):
    @app.route("/uploads/<filename>", methods=["GET"])
    def uploaded_file(filename):
        
        filename = secure_filename(filename)
        uploads_dir = get_uploads_dir()
        fullpath = os.path.normpath(os.path.join(uploads_dir, filename))
    
        if not fullpath.startswith(uploads_dir):
            return jsonify(error="Access denied"), 403
        
        try:
            with open(fullpath, "rb") as f:
                file_content = f.read()
            return Response(file_content, content_type="video/webm")
        except FileNotFoundError:
            return jsonify(error="File not found"), 404

    

    @app.route("/api/files", methods=["POST"])
    def files():
        try:
            if "audio" not in request.files or "video" not in request.files:
                return jsonify(error="Missing audio or video file"), 400

            audio_file = request.files["audio"]
            video_file = request.files["video"]

            audio_save_path = os.path.join(get_uploads_dir(), audio_file.filename)
            video_save_path = os.path.join(get_uploads_dir(), video_file.filename)
            output_path = os.path.join(get_uploads_dir(), os.path.splitext(video_save_path)[0] + "_" + DEFAULT_OUTPUT_FILENAME)

            try:
                audio_file.save(audio_save_path)
                video_file.save(video_save_path)

                run_wav2lip_inference(face_path=video_save_path, audio_path=audio_save_path, outfile_path=output_path)

                if Path(output_path).is_file():
                    return jsonify(videoPath=os.path.basename(output_path)), 200
                else:
                    return jsonify(error="Output file not found."), 404

            except Exception as e:
#               clean_files(audio_save_path, video_save_path)
                app.logger.error(f"Error in processing files: {e}")
                return jsonify(error=f"Error in processing files: {e}"), 500

            finally:
                if Path(audio_save_path).is_file():
                    print("Deleting audio file")
#                    clean_files(audio_save_path, video_save_path)

        except Exception as e:
            app.logger.error(f"Error in handling request: {e}")
            return jsonify(error=f"Internal server error Error in handling request: {e}"), 500


