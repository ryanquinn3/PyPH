PyPH
====
A command line tool for making power hour playlists in python.

##Installation

PyPH requires a few libraries to run properly. On OSX run:
```
$> pip install pydub
$> pip install click
```
and 
```
$> brew install ffmpeg --with-libvorbis --with-ffplay --with-theora
```
and to pull PyPH
```
$> git clone https://github.com/ryanquinn3/PyPH
```


##Usage

After installation, navigate to the directory where ph.py lives and run:
```
mkdir Songs
```
Add any songs you want to include in your power hour to the Songs directory you just created. When all your songs have been added run:
```
python ph.py template
```
This will scan your Songs directory and generate a JSON file. In this JSON file, you'll want to specify the start time for each song. Remember that the start time must not be after 1 minute before the end of the song!

Once you're satisfied with the start times of each song, run:

```
python ph.py generate
```

If you PyPH doesn't spit any errors, you should have a file named 'power_hour.mp3' in your current directory. Enjoy!


##Known Limitations
1. Songs must be .mp3 files
2. Start times of songs must be under 9 minutes 59 seconds

