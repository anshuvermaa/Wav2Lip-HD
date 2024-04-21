import subprocess
import os

CHECKPOINT_PATH = os.path.join("checkpoints", "wav2lip_gan.pth")
SEGMENTATION_PATH = os.path.join("checkpoints", "face_segmentation.pth")
SR_PATH = os.path.join("checkpoints", "esrgan_yunying.pth")


def run_command(cmd, workdir=None):
    print('cmd is',cmd)
    result = subprocess.run(
        cmd, text=True, cwd=workdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    print('result is',result)
    if result.returncode != 0:
        error_details = f"Command '{' '.join(cmd)}' failed with return code {result.returncode}. "
        error_details += f"STDOUT: {result.stdout} "
        error_details += f"STDERR: {result.stderr}"
        print('error_details is',error_details)
        raise Exception(error_details)
    return result






def run_wav2lip_inference(face_path, audio_path, outfile_path):
    print("audio_path"+audio_path)
    print("face_path"+face_path)
    print("outfile_path"+outfile_path)

    cmd = [
        "python3",
        "inference.py",
        "--checkpoint_path",
        CHECKPOINT_PATH,
        "--segmentation_path",
        SEGMENTATION_PATH,
        "--sr_path",
        SR_PATH,
        "--face",
        face_path,
        "--audio",
        audio_path,
        "--save_frames",
        "--gt_path",
        "data/gt",
        "--pred_path",
        "data/lq",
        "--no_sr",
        "--no_segmentation",
        "--outfile",
        outfile_path,
    ]
    try:
      result = run_command(cmd)
      print("result is",result)
    except Exception as e:
        print("error is in result",e)


    # result = run_command(cmd, workdir="wav2lip-hq")

    if not os.path.exists(outfile_path):
        error_msg = result.stderr if result.stderr else result.stdout
        raise Exception(f"Error: {error_msg}")

    return outfile_path
