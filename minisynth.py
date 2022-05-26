import pygame as pg
import numpy as np
import sys
import array as arr

def synth(frequency, duration=3, sampling_rate=44100):
    frames = int(duration*sampling_rate)
    arr = np.cos(2*np.pi*frequency*np.linspace(0, duration, frames))
    arr = arr + np.cos(4*np.pi*frequency*np.linspace(0, duration, frames)) # organ like
    arr = arr + np.cos(6*np.pi*frequency*np.linspace(0, duration, frames)) # organ like
##    arr = np.clip(arr*10, -1, 1) # squarish waves
##    arr = np.cumsum(np.clip(arr*10, -1, 1)) # triangularish waves pt1
##    arr = arr+np.sin(2*np.pi*frequency*np.linspace(0,duration, frames)) # triangularish waves pt1
    arr = arr/max(np.abs(arr)) # triangularish waves pt1
    sound = np.asarray([32767*arr,32767*arr]).T.astype(np.int16)
    sound = pg.sndarray.make_sound(sound.copy())

    return sound

pg.init()
pg.mixer.init()

a_file = open("noteslist.txt")
file_contents = a_file.read(); a_file.close()
noteslist = file_contents.splitlines()
keymod = '0-='
notes = {}
freq = 16.3516 #starting frequency

# save the notelist into a wave
for i in range(len(noteslist)):
    mod = int(i/36)
    key = noteslist[i]
    sample = synth(freq)

    notes[key] = [freq, sample]
    notes[key][1].set_volume(0.33)
    # tryineg to add a silence
    if 'r' in key:
        freq = 24
    else:
        freq = freq * 2 ** (1/12)

# open and parse a file
if len(sys.argv) > 2 or len(sys.argv) == 1:
    print("Usage: ./minsynth <filename>")
song = str(sys.argv[1])
tracks = []
with open(song, 'r') as filin:
    for line in filin:
        if 'tempo' in line:
            tempo = [int(temp) for temp in line.split() if temp.isdigit()]
            if tempo == 0 :
                print("Didn't found any tempo")
                sys.exit
        if ord(line[0]) >= 48 and ord(line[0]) <= 57:
            if ':' in line:
                tracks.append(line)
filin.close()
# tracks == List of all tracks
#  track == every tracks is list
track = []
test = []
keypresses = []
for line in tracks:
    note = line.split()
    track.append(note)
notes_short = np.delete(track[0], 0, 0)
for play_note in notes_short:
    keypresses.append(play_note.split('/'))
print(keypresses)

running = 1
for i in range(len(keypresses)):
    if not running:
        break
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            running = False
    key = keypresses[i][0]
    print("key: ")
    print(key)
    # if 'r' in keypresses[i][0]:
    #     notes[key][0] = 0
    notes[key][1].play()
    pg.time.wait(int((60000 * float(keypresses[i][1])) / tempo[0]))
    # print(int((60000 * float(keypresses[i][1])) / tempo[0]))
    notes[key][1].fadeout(0)

pg.time.wait(500)
pg.quit()
