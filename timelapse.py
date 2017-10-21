
import os
import datetime
import subprocess
import shutil
from db import add_log,get_config

from schedule import get_sol, get_sol_delta

config = get_config()
cam_path = config['general.path.cam']

sol = get_sol()
sol_folder = cam_path + "sol-" + str(sol) + "/"
# sol_video_tmp = cam_path + "/sol-" + str(sol) + "-tmp.mp4"
sol_video = cam_path + "sol-" + str(sol) + ".mp4"
sol_video_html = "/cam/sol-" + str(sol) + ".mp4"

sol_prev_video = cam_path + "/sol-" + str(sol-1) + ".mp4"


live_video = cam_path + "/live.mp4"
live_tmp_video = cam_path + "/live-tmp.mp4"

# Drop yesterday date
yesterday =  datetime.datetime.now() + datetime.timedelta(days=-1)
yesterday_folder = cam_path + yesterday.strftime("%Y%m%d") + "/"
directory = os.path.dirname(yesterday_folder)
if os.path.exists(directory):
    # shutil.rmtree(yesterday_folder)
    print "Remove (%s)" % (yesterday_folder)


# Create current sol video
create_sol_video = "ffmpeg -y -framerate 24 -f image2 -pattern_type glob -i '" + sol_folder + "*.jpg' -vf drawtext=\"fontfile=/home/pi/clima/font/karla.ttf: text='SOL " + str(sol) + "': fontcolor=white: fontsize=24: box=1: boxcolor=black@0.5: boxborderw=5: x=20: y=text_h*2\" " + sol_video
print create_sol_video

out = subprocess.call(create_sol_video, shell=True)
# add_log("timelapse", sol_video_html)

# print "Drop SOL tmp"

# if os.path.isfile(sol_prev_video):
    # concat live with prev sol

