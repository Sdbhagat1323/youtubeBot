"""
This is the main loop file for our AutoTube Bot!

Quick notes!
- Currently it's set to try and post a video then sleep for a day.
- You can change the size of the video currently it's set to post shorts.
    * Do this by adding a parameter of scale to the image_save function.
    * scale=(width,height)
"""

from datetime import date
import time
from utils.CreateMovie import CreateMovie, GetDaySuffix
from utils.RedditBot import RedditBot
from utils.upload_video import upload_video
from crop_video import CropVideo

from pytube import YouTube

import streamlit as st
import pandas as pd
import os 
import warnings
# from utils.YoutubeUtills import ytd,ytd_cutter
from utils.YoutubeUtills import YoutubeLib
warnings.filterwarnings('ignore')
import moviepy.editor as mpy
from moviepy.video.fx.all import crop

from clipsai import ClipFinder, Transcriber
from clipsai import resize,VideoFile,MediaEditor,AudioVideoFile

#Create Reddit Data Bot
# redditbot = RedditBot()

PYANNOTE_AUTH_TOKEN = "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"
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "/usr/local/Cellar/imagemagick/7.1.1-29_1/bin/magick"})

# Yt = 

youtube_video_link = "https://www.youtube.com/watch?v=t8HrZTLRCeU"

yt = YoutubeLib()
yt.create_data_folder()

yt_title = yt.ytd(youtube_video_link)

# now trim video in with start an end time

#tis part 
trim_start, trim_stop = "00:3:00", "00:3:30"
cropped_video_title = yt.ytd_cutter(yt_title, trim_start, trim_stop)
output_path = yt.convert_to_short(yt_title, cropped_video_title)

# Create the movie itself!
# CreateMovie.CreateMP4(redditbot.post_data)

# Video info for YouTube.
# This example uses the first post title.
video_data = {
        "file": output_path,
        "title": f"shorts of {yt_title}",
        "description": "this is song by of monster and mens",
        "keywords":"#shorts, #music, #songs",
        "privacyStatus":"public"
}

print(video_data["title"])

yt.ytd_upload(video_data)


# Sleep until ready to post another video!
time.sleep(60 * 60 * 24 - 1)







