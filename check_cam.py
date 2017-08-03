from subprocess import call, Popen, PIPE
import time
import datetime
from config import cam_path
from schedule import get_light
import os
from db import add_log

light_mode = get_light()
if not light_mode:
  print "No Light: No Photo"
  exit(0)

# Create file name / folder / title
folder = datetime.datetime.now().strftime("%Y%m%d")
num = datetime.datetime.now().strftime("%H%M")
path = cam_path + folder + "/" + num + ".jpg"
title = datetime.datetime.now().strftime("%d%b")

# Create folder if needed
directory = os.path.dirname(path)
if not os.path.exists(directory):
    os.makedirs(directory)
    print "Created folder: %s" % (directory)

stop = True
get_img = ["fswebcam", "-q", "-r 1280x960", "--no-banner", path]

# Try to take a photo
while stop:
  pipe = Popen(get_img, stdout=PIPE, stderr=PIPE)
  output, error = pipe.communicate()
  stop = False
  if "Error" in error:
    stop = True
    print "Camera access failed: %s" % (error)
    time.sleep(7)
  else:
    print "Photo taken: %s" % (path)
    add_log('cam', folder + "/" + num + ".jpg")

