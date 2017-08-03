import os
import datetime
from subprocess import call, Popen, PIPE
import pprint
import shutil
from db import add_log

yesterday =  datetime.datetime.now() + datetime.timedelta(days=-1)
fol = yesterday.strftime("%Y%m%d")
folder = "/home/pi/html/cam/" + fol + "/"
video = "/home/pi/html/cam/" + fol + ".mp4"

print "get files from"
print folder

create_video = "ffmpeg -framerate 24 -f image2 -pattern_type glob -i '" + folder + "*.jpg' " + video
print create_video

pipe = call(create_video, shell=True)
print "Video created"
add_log("timelapse", video)

shutil.rmtree(folder)
print "Removed files"
