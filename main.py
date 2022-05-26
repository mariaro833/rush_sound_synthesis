import sys
import array as arr

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
sys.exit
