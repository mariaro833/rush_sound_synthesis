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
# font2 = pg.font.SysFont("Impact", 48)
# screen = pg.display.set_mode((1280, 720))
# pg.display.set_caption("FinFET Synth - replay txt" )

a_file = open("noteslist.txt")
file_contents = a_file.read(); a_file.close()
noteslist = file_contents.splitlines()
keymod = '0-='
notes = {}
# posx, posy = 25, 25 #start position
freq = 16.3516 #starting frequency

# save gamma in wave
for i in range(len(noteslist)):
    mod = int(i/36)
    key = noteslist[i]
    sample = synth(freq)
    # color = np.array([np.sin(i/25+1.7)*130+125,np.sin(i/30-0.21)*215+40, np.sin(i/25+3.7)*130+125])
    # color = np.clip(color, 0, 255)
    notes[key] = [freq, sample]
    notes[key][1].set_volume(0.33)
    freq = freq * 2 ** (1/12)
    # posx = posx + 140
    # if posx > 1220:
    #     posx, posy = 25, posy+56

    # screen.blit(font2.render(notes[key][4], 0, notes[key][3]), notes[key][2])
    # pg.display.update()

# open and pars file
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
for line in tracks:
	note = line.split()
	track.append(note)
for notes1 in track:
    for note in notes1:
        test.append(note.split('/'))
notes_short = np.delete(notes1, 0, 0)
for play_note in notes_short:
    keypresses = play_note.split('/')
    # duration = float(keypresses[1])
    # keypresses = int(keypresses[i][2])
print(keypresses)
# for i in range(len(tracks)):
# with open("SuperMario.txt", "r") as file:

    # keypresses = [eval(line.rstrip()) for tracks in arr]
    # tracks[1] = keypresses
    # tracks[2] = keypresses
    # print (tracks[1][1][1])
# file.close()

running = 1
for i in range(len(keypresses)):
    if not running:
        break
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            running = False

    # key = keypresses[i][1]
    key = keypresses[i]
    print(key)

    # pg.time.wait(keypresses[i][2])
    # if keypresses[i][0]:
    notes[key][1].play()
    pg.time.wait(800)
        # notes[keypresses[i + 10][1]][1].play()
    # screen.blit(font2.render(notes[key][4], 0, (255,255,255)), notes[key][1])
    # else:
    notes[key][1].fadeout(100)
        # screen.blit(font2.render(notes[key][4], 0, notes[key][3]), notes[key][2])

    # pg.display.update()

pg.time.wait(500)
pg.quit()
