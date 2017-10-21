from subprocess import call, Popen, PIPE
import time
import datetime

from schedule import get_light, get_sol
import os
import shutil
from db import add_pin, get_config

config = get_config()
cam_path = config['general.path.cam']

light_mode = get_light()

if not light_mode:
  print "No Light: No Photo"
  exit(0)

# Create file name / folder
date_name = datetime.datetime.now().strftime("%Y%m%d")
file_name = datetime.datetime.now().strftime("%H%M")
file_path = cam_path + date_name + "/" + file_name + ".jpg"

# Create folder if needed
directory = os.path.dirname(file_path)
if not os.path.exists(directory):
  os.makedirs(directory)
  print "Created folder: %s" % (directory)

stop = True
get_img = ["fswebcam", "-q", "-r 1280x960", "--no-banner", file_path]

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
    print "Photo taken: %s" % (file_path)
    add_pin('CAM', file_name)

    min = datetime.datetime.now().strftime("%M")
    if int(min) % 5 == 0:
      sol = get_sol()
      sol_name = "sol-" + str(sol)
      sol_file_name = datetime.datetime.now().strftime("%Y%m%d%H%M")
      sol_path = cam_path + sol_name + "/" + sol_file_name + ".jpg"

      # Create folder if needed
      directory = os.path.dirname(sol_path)
      if not os.path.exists(directory):
        os.makedirs(directory)
        print "Created folder: %s" % (directory)

      shutil.copyfile(file_path, sol_path)
      print "Copy to Sol: %s => %s" % (file_path, sol_path)
