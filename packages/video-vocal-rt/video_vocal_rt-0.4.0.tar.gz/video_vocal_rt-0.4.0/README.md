# video-vocal-RT
A minimal package to record vocal response to video stimuli. Useful for vocal reaction time research with video stimuli instead of pictures. Uses open CV for video playing, among other things.

# Usage
I will provide more information soon 😉

## Installation with pip
```
pip install video-vocal-rt
```

## Installation with poetry
First, clone the repository
```
git clone https://github.com/LoonanChauvette/video-vocal-RT.git
```
Then, inside the package folder, install the dependencies with poetry
```
cd video-vocal-RT
poetry install
```
Poetry creates a virtual environment, you should be able to activate it using : 
```
poetry shell
```
Then you can run the script using : 
```
poetry run python video_vocal_rt/main.py
```

## How-to 
Place your video files in the VIDEO_FILES directory (only supports .avi files for now). For the moment, you need to go inside video_vocal_rt/main.py before running the experiement. There you should make sure to set the audio recording duration in seconds (default is 6 seconds, but should be the typical length of your videos). You also need to set the PARTICIPANT_ID to the desired value. 

You can also set fixation parameters with FIXATION_DUR for the duration (default is 1000 ms). You can provide change the file "fixation.png" to customize the fixation. By default, there is a whiteout period after the video, its duration can be changed with WHITEN_DUR (default is 1000 ms).

# Citation
 
```
Chauvette, L. (2023). Video-Vocal-RT: a minimal package for vocal response to video.
https://github.com/LoonanChauvette/video-vocal-RT
````

Bibtex:
```
@manual{Video-Vocal-RT,
  title={{Video-Vocal-RT: a minimal package for vocal response to video}},
  author={{Chauvette, Loonan}},
  year={2023},
  url={https://github.com/LoonanChauvette/video-vocal-RT},
}
```