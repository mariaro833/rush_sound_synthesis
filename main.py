import sys
import re
from pyparsing import line_end

# instruments[] =
song = input('Enter the path of your song: ')
with open(song, 'r') as filin:
	for line in filin:
		if line[0] == '#' or line == '\n':
			continue
		if 'tempo' in line:
			# temp variables
			temp = re.findall('[0-9]+', line)
			print(temp)
		if 'tracks' in line:
			# instrments arrange
			instruments = (re.split('\W+|,', line))
			print (instruments[25])
		if line[0] == '#' or line == '\n':
			continue
		

filin.close()
sys.exit