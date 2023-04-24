import sys
import whisper
from TikTokApi import TikTokApi
import random
import subprocess

"""
Script for going from a TikTok video link to a video output,
an audio output and a text file
"""
vid = sys.argv[1].split('/')[-1]
did = str(random.randint(10000, 999999999))
with TikTokApi(custom_device_id=did) as api:
    video = api.video(id=vid)

    # Bytes of the TikTok video
    video_data = video.bytes()

    with open("output.mp4", "wb") as out_file:
        out_file.write(video_data)

subprocess.call(['ffmpeg','-i', 'output.mp4', '-map', '0:a', '-c', 'copy', 'output.aac'])

model = whisper.load_model("base")
result = model.transcribe("output.aac")

with open("output.txt", 'w', encoding='utf-8') as f:
    f.write(result['text'])