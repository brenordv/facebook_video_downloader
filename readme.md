# Facebook video downloader
This script will try to download a public video from an url.

# Usage
## Download video to current folder, using default name (timestamp) and resolution (hd)
```shell
python facebook.py https://facebook.com/link/to/video
```

## Download video to current folder, using using custom name and resolution 
```shell
python facebook.py https://facebook.com/link/to/video output "c:\\temp\\my_video.mp4" resolution hd
```

## Download video and enabling logging. 
```shell
python facebook.py https://facebook.com/link/to/video log debug
```

## Help
```shell
python facebook.py help
```

# Notes
- This script relies on the current Facebook page format. If they change it, this will break.
- Tried to use as few external dependencies as possible. Just enough to add a little swag here.
- Worked for every video i tried to download, but I must confess: I made this script during my lunch break and haven't really tested it the way i should. :)