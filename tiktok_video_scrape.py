from TikTokApi import TikTokApi
import random
import subprocess

did = str(random.randint(10000, 999999999))
with TikTokApi(custom_device_id=did) as api:
    video = api.video(id="7164574300257651974") #https://www.tiktok.com/@nayibbukele/video/7164574300257651974

    # Bytes of the TikTok video
    video_data = video.bytes()

    with open("out.mp4", "wb") as out_file:
        out_file.write(video_data)
