import sys
import re
from pyparsing import line_end

# instruments[] =
song = input('Enter the path of your song: ')
with open(song, 'r') as filin:
	for line in filin:
		if line[0] == '#':
			continue
		if line == '\n':
			continue
		if 'tempo' in line:
			# temp variables
			temp = re.findall('[0-9]+', line)
			print(temp)
		if 'tracks' in line:
			# instrments arrange
			instruments = (re.split('\W+|,', line))
			print (instruments[25])
filin.close()
sys.exit

# words_with_numbers = []

# f = open('file.txt', 'r')
# for line in f:
#   line = line.strip()
#   words = line.split(' ')
#   for w in words:
#     if any(c.isdigit() for c in w):
#       words_with_numbers.append(w)
# f.close()