# pilapse
simple timelapse recorder written in python for raspberry pi

**note: this has only been tested with python3, please use this version**

## Setup

There really isn't all that much to setup, just make sure to install screen (or your preferred terminal multiplexer) using `sudo apt-get update && sudo apt-get install screen`.

Make sure you have python3 by running `python3 --version`, if you don't get the version, run `sudo apt-get install python3`.

## How to Use

If you haven't already, run `screen -S pilapse`.

`cd` into the directory with the script in it, and run `python3 pilapse.py --help`, and use the help page to help set the required arguments.

Once it is running, you can detach from the screen by pressing ctrl+a, and then d. To reattach, run `screen -r pilapse`.


If you run it with `--eternal` or `-e`, then you will have to stop it using ctrl+c, and run `ffmpeg -framerate 10 -i images/%08d.jpg output.mp4`, making sure to set the framerate, image folder, and output file to the required values.

To stream, find the start_stream.sh file and run `./start_stream.sh your_youtube_streamkey`. If you get a 'permission denied' error, run `chmod +x start_stream.sh`
