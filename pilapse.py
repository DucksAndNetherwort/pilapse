from picamera import PiCamera
from io import BytesIO
import PIL
from PIL import Image
import time
from fractions import Fraction
import os
import getopt
import sys
import subprocess as sp

startTime = int(time.time())

imageCount = 30 #number of total frames
framerate = 10 #fps of output video
captureRate = 1 #time in seconds between taking stills
outputFile = 'output.mp4' #destination file for the video
tempFolder = 'images' #folder where the still frames are stored
highQuality = False #whether to let the camera do a self calibration before locking in values
eternal = False #whether to run forever
dontRun = False #determines if the main part should run
longExposure = False #enables long exposures if true

arguments = sys.argv[1:] #this block defines possible arguments, and fetches the ones passed to the script
options = 'hi:f:c:o:t:qel'
longOptions = ['help', 'images=', 'framerate=', 'capturerate=', 'output=', 'tempfolder=', 'highquality', 'eternal', 'longexposure']

try:
	args, values = getopt.getopt(arguments, options, longOptions) #this entire section is for parsing arguments, refer to help page
	for currentArgument, currentValue in args:
		if currentArgument in ('-h', '--help'):
			dontRun = True
			print(f"""creates a timelapse, written by Ducks And Netherwort\n
-h, --help: prints this message. takes no arguments
-i, --images: set the number of frames to capture. Default: {imageCount}
-f, --framerate: select the desired output video frame rate, in frames per second. Default: {framerate}
-c, --capturerate: rate at which to capture images, in seconds per frame. Default: {captureRate}
-o, --output: destination file, relative to current location. Default: {outputFile}
-t, --tempfolder: folder in which to store stills for later conversion to video. Default: {tempFolder}
-q, --highquality: if present, will have the camera spend some time and lock the settings it generates. takes no arguments
-e, --eternal: run forever. takes no arguments
-l, --longexposure: makes the exposures as long as possible""")

		elif currentArgument in ('-i', '--images'):
			imageCount = int(currentValue)
			print(f'target image count: {imageCount}')

		elif currentArgument in ('-f', '--framerate'):
			framerate = currentValue
			print(f'framerate: {framerate}')

		elif currentArgument in ('-c', '--capturerate'):
			captureRate = int(currentValue)
			print(f'capture framerate: {captureRate}')

		elif currentArgument in ('-o', '--output'):
			outputFile = currentValue
			print(f'output file: {outputFile}')

		elif currentArgument in ('-t', '--tempfolder'):
			tempFolder = currentValue
			print(f'temporary image folder: {tempFolder}')

		elif currentArgument in ('-q', '--highquality'):
			highQuality = True
			print('high quality option set')

		elif currentArgument in ('-e', '--eternal'):
			eternal = True
			print('will run until stopped')

		elif currentArgument in ('-l', '--longexposure'):
			longExposure = True
			print('long exposures enabled')

except getopt.error as err:
    print(str(err))


if not dontRun: #main part of the script

	capturedFrames = 0

	print('starting camera')
	if (captureRate > 10) and longExposure:
		camera = PiCamera(sensor_mode=3, framerate=0.1)

	elif longExposure:
		camera = PiCamera(sensor_mode=3, framerate=(1/captureRate))

	else:
		camera = PiCamera(sensor_mode=3)


	if highQuality:
		print(f'will wait {captureRate * 10} seconds for calibration')
		if longExposure:
			if captureRate > 10:
				camera.shutter_speed = 10 * 1000000
			else:
				camera.shutter_speed = captureRate * 1000000

		time.sleep(captureRate * 10)

		if not longExposure:
			camera.shutter_speed = camera.exposure_speed

		camera.exposure_mode = 'off'
		(g1, g2) = camera.awb_gains
		camera.awb_mode = 'off'
		camera.awb_gains = (g1, g2)

	else:
		if longExposure:
                        if captureRate > 10:
                                camera.shutter_speed = 10 * 1000000
                        else:
                                camera.shutter_speed = captureRate * 1000000

		print(f'will wait {captureRate * 2} seconds for camera warmup')
		time.sleep(captureRate * 2)

	print('camera ready')
	stream = BytesIO() #get stream

	os.system(f'mkdir {tempFolder}')
	os.system(f'rm {tempFolder}/*')
	print(f'image folder {tempFolder} cleaned and ready')
	os.system(f'rm {outputFile}')
	print(f'output file {outputFile} removed')

	cameraReady = False

	while (capturedFrames < imageCount) or eternal:
		if (((startTime - time.time()) % captureRate) < 0.5) and (cameraReady == True):
			cameraReady = False
			camera.capture(stream, format='jpeg')
			stream.seek(0)
			imageFile = open(f'{tempFolder}/{capturedFrames:08}.jpg', 'wb')
			imageFile.write(stream.getvalue())
			print(f'image {capturedFrames:08} of {imageCount} captured')
			capturedFrames += 1

		if not (((startTime - time.time()) % captureRate) < 0.5):
			cameraReady = True

	print('running ffmpeg')
	print(os.system(f'ffmpeg -framerate {framerate} -i {tempFolder}/%08d.jpg {outputFile}')) #convert stills to output file

