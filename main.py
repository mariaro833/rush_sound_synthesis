from curses.ascii import isdigit
import sys
import array as arr
import numpy as np

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
# for notes1 in track:
#     for note in notes1:
#         test.append(note.split('/'))
notes_short = np.delete(track[0], 0, 0)
for play_note in notes_short:
    keypresses.append(play_note.split('/'))
    # duration = float(keypresses[1])
print("keypresses: ")
print(keypresses)
# print("duration: ")
# print(duration)
print("track: ")
print(track)