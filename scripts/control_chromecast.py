import pychromecast
import os
import sys

# --------------------------------------------
# CONFIGURATION
# --------------------------------------------
CHROMECAST_NAME = "Jamie"
MPD_HTTPD_PORT = "8000"
MPD_HTTPD_AUDIO_FORMAT = "audio/ogg"



# --------------------------------------------
# DO NOT EDIT BELOW
# --------------------------------------------

def usage():
	print("Usage: control_chromecast.py command")
	print("")
	print("possible commands: play/pause/stop")
	sys.exit(1)



# check arguments
if len(sys.argv) != 2:
	usage()

COMMAND = sys.argv[1]

# determine phoniebox' IP address and MPD's httpd URL
IPADDRESS = os.popen('hostname -I').readline().replace("\n", "").strip()
MPD_HTTPD_URL = "http://" + IPADDRESS + ":" + MPD_HTTPD_PORT

# fetch chromecasts in the network and choose the one defined above
print("Searching for chromecast " + CHROMECAST_NAME + "...")
chromecasts = pychromecast.get_chromecasts()
cast = None
for _cast in chromecasts:
	if _cast.name == CHROMECAST_NAME:
		cast = _cast
		break

if not cast:
	print(" > Could not find a chromecast called " + CHROMECAST_NAME + " in your network!")
	print(" > Discovered chromecasts:")
	print("{}".format(chromecasts))
	sys.exit(1)

# wait for connection to the chromecast
print("Waiting for connection to " + CHROMECAST_NAME + "...")
cast.wait()

# initialize media controller
mc = cast.media_controller

# react upon command
if (COMMAND == "play"):
	print("Playing MPD's http stream via URL: " + MPD_HTTPD_URL)
	mc.play_media(MPD_HTTPD_URL, MPD_HTTPD_AUDIO_FORMAT, "Phoniebox", None, 0, True, "LIVE")
	mc.block_until_active()
	mc.play()
elif (COMMAND == "pause"):
	print("Pausing stream")
	mc.pause()
elif (COMMAND == "stop"):
	print("Stopping playback on " + CHROMECAST_NAME)
	mc.stop()
else:
	usage()
