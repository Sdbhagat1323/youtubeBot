
import os
import re
from pytube import YouTube
from crop_video import CropVideo
from datetime import date 
from utils.upload_video import upload_video

import moviepy.editor as mpy
from moviepy.video.fx.all import crop

from clipsai import ClipFinder, Transcriber
from clipsai import resize,VideoFile,MediaEditor,AudioVideoFile

PYANNOTE_AUTH_TOKEN = "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"
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "/usr/local/Cellar/imagemagick/7.1.1-29_1/bin/magick"})



class YoutubeLib():
    def __init__(self):
        self.media_editor = MediaEditor()
        dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        print(dir_path)
        self.data_path = os.path.join(dir_path, "data/")
        self.video_data = []
        self.already_video_data = []

        # check for video data is video_data file
        self.already_exist_video_data = os.path.join(
            self.data_path, "video_data_already.mp4")
        if os.path.isfile(self.already_exist_video_data):
            print("loading already existing video file from data folder")
            
    def create_data_folder(self):
        today = date.today()
        dt_string = today.strftime("%m%d%Y")
        data_folder_path = os.path.join(self.data_path, f"{dt_string}/")
        check_folder = os.path.isdir(data_folder_path)
        # if folder doesn't exist, then create it
        if not check_folder:
            os.makedirs(data_folder_path)
    

    # def ytd(youtube_video_link, root=os.path.dirname('/Users/admin1/Desktop/youtube_project/content_genrator/data/input/yt_video/')):
    #     # YouTube(youtube_video_link).streams.first().download()
    #     yt = YouTube(youtube_video_link)
    #     video_title = yt.title+".mp4"
    #     yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
    #     downloaded_video_path = root +"/"+ video_title
    #     return downloaded_video_path
    
    def ytd(self, url):
        dt_string = date.today().strftime("%m%d%Y")
        data_folder_path = os.path.join(self.data_path, f"{dt_string}/")
        print(data_folder_path)
        CHECK_FOLDER = os.path.isdir(data_folder_path)
        if CHECK_FOLDER:
            os.chdir(data_folder_path)
            yt = YouTube(url)
            video_title = yt.title+".mp4"
            if len(os.listdir(data_folder_path)) ==0:
                mp4_streams = yt.streams.get_highest_resolution()
                mp4_streams.download()
                # yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
                for filename in os.listdir(data_folder_path):
                    download_title = re.search(yt.title, filename, re.IGNORECASE)
                os.rename(filename, video_title) 
                return video_title
            else:
                CHECK_VIDEO = [ x for x in os.listdir(data_folder_path) if re.search(video_title, x, re.IGNORECASE)][0]
                print(f"{video_title} already in folder.")
                return CHECK_VIDEO

                

    
    def ytd_cutter(self, yt_title,start, end):
        dt_string = date.today().strftime("%m%d%Y")
        data_folder_path = os.path.join(self.data_path, f"{dt_string}/")
        CHECK_FILE = data_folder_path+yt_title
        if not CHECK_FILE:
            return CHECK_FILE
        else:
            os.chdir(data_folder_path)
            # for filename in os.listdir(data_folder_path):
            # if filename.endswith(".mp4") and not filename.startswith("shorts_"):
            cutter = CropVideo()
            input_name = data_folder_path + yt_title
            input_folder_path = data_folder_path + "input/"
            output_name = "shorts_" + yt_title
            output_path = input_folder_path
            #create input dir
            if not os.path.isdir(data_folder_path + "input/"):
                os.makedirs(data_folder_path+"input/")
                cutter(input_name, start, end, output_path+output_name)
                return output_name
            elif "shorts_"+yt_title in os.listdir(input_folder_path):
                output_name = output_name.replace(".mp4",f"({len([x for  x in os.listdir(input_folder_path)])+1})"+".mp4")
                cutter(input_name, start, end, output_path+output_name)
                return output_name
            else:
                print("------Already in folder ------------")
                return output_name
        
    
    # @staticmethod
    def convert_to_short(self, yt_title,cropped_video):
        dt_string = date.today().strftime("%m%d%Y")
        data_folder_path = os.path.join(self.data_path, f"{dt_string}/")
        input_video_path = data_folder_path+"input/"
        short_video = input_video_path + cropped_video
        # for filename in os.listdir(data_folder_path):
        # if yt_title in os.listdir(data_folder_path+"input/"):
        if cropped_video:
            # downloaded_video_path = data_folder_path
            crops = resize(
            # video_file_path=curr_path+ "/" + raw_video_filename,
            video_file_path=short_video,
            pyannote_auth_token=PYANNOTE_AUTH_TOKEN,
            aspect_ratio=(9, 16)
            )
            print("Crops: ", crops.segments)

            # use this if the file contains video stream only
            media_file = VideoFile(short_video)
            # use this if the file contains both audio and video stream
            media_file = AudioVideoFile(short_video)
            media_editor = MediaEditor()
            CHECK_FOLDER = os.path.isdir(data_folder_path+"output")
            if not CHECK_FOLDER:
                short_dir = data_folder_path+"output/"
                os.makedirs(short_dir)
                output_file_name = short_dir+cropped_video
            else:
                short_dir = data_folder_path+"output/"
                output_file_name = short_dir+cropped_video

            resized_video_file = media_editor.resize_video(
                original_video_file=media_file,
                resized_video_file_path= output_file_name,  # doesn't exist yet
                width=crops.crop_width,
                height=crops.crop_height,
                segments=crops.to_dict()["segments"],
            )
            print("video converted..")
             
        return output_file_name
    
    def ytd_upload(self, video_data):
        # dt_string = date.today().strftime("%m%d%Y")
        # data_folder_path = os.path.join(self.data_path, f"{dt_string}/")
        # short_dir = data_folder_path+"output/"
        # for filename in os.listdir(short_dir):
        #         if filename.startswith("shorts"):
        #             downloaded_video_path = data_folder_path + filename
        #             print("-UPLOADING_START-"*20)
        #             upload_video(downloaded_video_path)
        #             print("-UPLOADING_DONE-"*20)
        try:
            upload_video(video_data)
        except Exception as e:
            print(f"error in {e}")
        return None

        
