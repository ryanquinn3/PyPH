from pydub import AudioSegment
from glob import glob
import sys, os, click, json, re

song_dir = 'Songs/'
start_times_file = 'start_times.json'
power_hour_song = 'power_hour.mp3'

@click.group()
def cli():
    pass

@cli.command()
def template():
    if(not os.path.isdir(song_dir)):
        click.echo('Song directory not present. Run "mkdir Songs" and fill with .mp3 files, then rerun')
        sys.exit(2)

    playlist_songs = [mp3_file for mp3_file in glob(song_dir+"*.mp3")]

    if len(playlist_songs) == 0:
        click.echo('Songs directory is empty. Add .mp3 files and rerun');
        sys.exit(2)

    template = {}
    for song in playlist_songs:
        template[song[6:]] = "0:00"
    template_string = json.dumps(template, indent=4,
                                separators=(',', ': '))

    with open(start_times_file, "w") as text_file:
        text_file.write(template_string)

    click.echo("Wrote start time template as " + start_times_file)

@cli.command()
def generate():
    if not os.path.exists(start_times_file):
        click.echo("Start time file doesn't exist. run python ph.py template")
        sys.exit(2)
    with open(start_times_file) as json_file:
        try:
            json_data = json.load(json_file)
        except:
            click.echo("Template file couldn't be parsed. re-run python ph.py template")
            sys.exit(2)

        errors = []
        for name in json_data:
             re_match = re.match(r'^(\d):(\d{2})$', json_data[name])
             if not re_match:
                  errors.append(name)
             else:
              mins, secs = re_match.group(1), re_match.group(2)
              total_msecs = (int(mins)*60 + int(secs))
              json_data[name] = total_msecs # <SongName> : <length in sec>

        if not len(errors) == 0:
            error_str = 'The following files have invalid start times: [must be X:XX]\n'
            for e in errors:
              error_str += ("*** "+e + '\n')
            click.echo(error_str)
            sys.exit(2)
        song_data = {}
        for mp3_file in glob(song_dir+"*.mp3"):
            song_data[mp3_file[6:]] = AudioSegment.from_mp3(mp3_file)


        unfound_songs, overrun_times = [], []
        for name in song_data:
            if name not in json_data:
                unfound_songs.append(name)
            elif song_data[name].duration_seconds - 60 < json_data[name]:
                overrun_times.append(name)
        errors = len(unfound_songs) > 0 or len(overrun_times) > 0
        err_str = ''
        if len(unfound_songs) > 0:
            err_str += "The following files did not have entries in "+start_times_file+". Re-rerun python ph.py template.\n"
            for song in unfound_songs:
                err_str += "*** " + song + "\n"
            err_str += "\n"

        if len(overrun_times) > 0:
            err_str += "The following files had entries in "+start_times_file+" that were beyond 1 minute before the end of the song:\n"
            for song in overrun_times:
                err_str += "*** " + song + "\n"
            err_str += "\n"

        if errors:
            click.echo(err_str)
            sys.exit(2)

        first_song = True
        for name in song_data:
            strt = json_data[name]*1000
            end = strt + 60*1000
            song_data[name] = song_data[name][strt:end]
            if first_song:
              power_hour = song_data[name]
              first_song = False
            else:
              power_hour = power_hour.append(song_data[name].fade_in(250).fade_out(250))


        try:
            power_hour
        except NameError:
            click.echo('Power hour is empty..')
            sys.exit(2)
        else:
          power_hour.export(power_hour_song,format="mp3")
          click.echo("Enjoy!")
          sys.exit(2)





if __name__ == '__main__':
  cli()

