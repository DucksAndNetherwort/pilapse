ffmpeg -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -framerate 6 -video_size 1920x1080 -i /dev/video1 -f flv -b 6000000 -r 24 -g 4 rtmp://a.rtmp.youtube.com/live2/"$1"
