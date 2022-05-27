import pygame as pg
import numpy as np
import sys
import array as arr
import re
import threading
import time
import asyncio
from multiprocessing import Pool
from multiprocessing import Process
import random

#-----------------------------------
# sample generater

def synth(frequency, duration=1, sampling_rate=44100):
    frames = int(duration * sampling_rate)
    arr = np.cos(2 * np.pi * frequency * np.linspace(0, duration, frames)) #sine
    # arr = arr + np.cos(4*np.pi*frequency*np.linspace(0, duration, frames)) # organ like
    # arr = arr + np.cos(6*np.pi*frequency*np.linspace(0, duration, frames)) # organ like
##    arr = np.clip(arr*10, -1, 1) # square
##    arr = np.cumsum(np.clip(arr*10, -1, 1)) # saw
##    arr = arr+np.sin(2*np.pi*frequency*np.linspace(0,duration, frames)) # triangle_nice
    arr1 = arr/max(np.abs(arr)) # triangle

    sound1 = np.asarray([32767 * arr,32767 * arr1]).T.astype(np.int16)
    sound1 = pg.sndarray.make_sound(sound1.copy())

    arr2 = np.clip(arr*10, -1, 1) # square
    arr2 = arr/max(np.abs(arr2)) # triangle

    sound2 = np.asarray([32767 * arr,32767 * arr2]).T.astype(np.int16)
    sound2 = pg.sndarray.make_sound(sound2.copy())

    arr3 = np.cumsum(np.clip(arr*10, -1, 1)) # saw
    arr3 = arr/max(np.abs(arr3)) # triangle

    sound3 = np.asarray([32767 * arr,32767 * arr3]).T.astype(np.int16)
    sound3 = pg.sndarray.make_sound(sound3.copy())

    arr4 = arr+np.sin(2*np.pi*frequency*np.linspace(0,duration, frames)) # triangle_nice
    arr4 = arr/max(np.abs(arr4)) # triangle

    sound4 = np.asarray([32767 * arr,32767 * arr4]).T.astype(np.int16)
    sound4 = pg.sndarray.make_sound(sound4.copy())


    return [sound1, sound2, sound3, sound4]

#-----------------------------------
# save the notelist into a wave

pg.init()
pg.mixer.init()

a_file = open("noteslist.txt")
file_contents = a_file.read(); a_file.close()
noteslist = file_contents.splitlines()
keymod = '0-='
notes = {}
freq = 16.3516 #starting frequency

for i in range(len(noteslist)):
    mod = int(i/36)
    key = noteslist[i]
    sample = synth(freq)
    instrument = {}

    notes[key] = [freq, sample]
    notes[key][1][0].set_volume(0.33)
    notes[key][1][1].set_volume(0.33)
    notes[key][1][2].set_volume(0.33)
    notes[key][1][3].set_volume(0.33)
    freq = freq * 2 ** (1/12)

#-----------------------------------
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
        if 'tracks' in line:
            instruments = line[7:].split(',')
filin.close()

#-----------------------------------
# if there are equal number of tracks

dict_tracks_instruments = dict()
dict_tracks_0 = dict()
number_of_tracks = len(tracks)


for i in range(number_of_tracks):
    track_i = tracks[i]
    number_i = track_i[0 : track_i.find(':')]
    if number_i not in dict_tracks_0:
        dict_tracks_0[number_i] = track_i[track_i.find(':') + 1: ]
    else:
        dict_tracks_0[number_i] += track_i[track_i.find(':') + 1: ]
    dict_tracks_instruments[number_i] = instruments[i]

#-----------------------------------
# checker for the duration

dict_tracks = dict()

for n_track in dict_tracks_0:
    track = dict_tracks_0[n_track]
    list_of_notes = track.split()
    for i in range(len(list_of_notes)):
        note_dur = list_of_notes[i].split('/')
        if len(note_dur) == 1:
            list_of_notes[i] = note_dur
        else:
            if len(note_dur[1]) == 0:
                list_of_notes[i] = [note_dur[0]]
            else:
                list_of_notes[i] = note_dur
    dict_tracks[n_track] = list_of_notes

#-----------------------------------
# checker for the octave

for key in dict_tracks:
    keypresses = dict_tracks[key]
    # print(keypresses)

    actual_octave = '4'
    actual_duration = 1.0
    for i in range(len(keypresses)):
        if not re.findall(r'\d', keypresses[i][0]) and not 'r' in keypresses[i][0]:
            dict_tracks[key][i][0] = keypresses[i][0] + actual_octave
        elif not 'r' in keypresses[i][0]:
            actual_octave1 = (re.findall(r'\d', keypresses[i][0]))
            actual_octave = actual_octave1[0]
        if len(keypresses[i]) == 1:
            if i == 0:
                keypresses[i].append(str(actual_duration))
            else:
                keypresses[i].append(keypresses[i-1][1])
        dict_tracks[key][i][0] = dict_tracks[key][i][0].replace('c#', 'd').replace('g#', 'a').replace('ab', 'g').replace('bb', 'a#').replace('cb', 'b#').replace('db', 'c').replace('eb', 'd#').replace('fb', 'e#').replace('gb', 'e#')
        # print(dict_tracks[key][i][0])

#-----------------------------------
# running sound

def play_(keypresses_, instruments_):
    instrument = instruments_
    print(keypresses_)
    running = 1
    for i in range(len(keypresses_)):
        # if not running:
        #     break
        # for event in pg.event.get():
        #     if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
        #         running = False
        key = keypresses_[i][0]
    #-----------------------------------
    # checker for silent 'r'
        print(key)
        if not 'r' in key:
            print("play")
            notes[key][1][instrument].play()
            print("play1")

        pg.time.wait(int((60000 * float(keypresses_[i][1])) / tempo[0]))
        print("play2")
        # notes[key][1][instrument].fadeout(0)
        print("play3")


# processes = []

# def start():
#     for key in dict_tracks:
#         p = Process(target=play_, args=(dict_tracks[key], int(dict_tracks_instruments[key].replace('sine', '1').replace('square', '2').replace('saw', '3').replace('triangle', '4'))))
#         p.start()
#     for p in processes:
#         p.join()

# if __name__ == "__main__":
#     start()

# for key in dict_tracks:
#     play_(dict_tracks[key], 1)

def play__():
    print("что-")
    play_(dict_tracks['1'], 1)
    # for key in dict_tracks:
# t = threading.Thread(target=play__)
# t.start()
processes = []

def start():
    for i in str(dict_tracks['1']):
        p = Process(target = [play__])
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

if __name__ == '__main__':
    start()

# t1 = threading.Thread(target=play_, args=(dict_tracks['2'], 1))
# t1.start()


#     for key in dict_tracks:
#         play_(dict_tracks[key], int(dict_tracks_instruments[key].replace('sine', '1').replace('square', '2').replace('saw', '3').replace('triangle', '4')))

pg.time.wait(500)
pg.quit()
