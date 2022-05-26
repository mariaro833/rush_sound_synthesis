import pygame as pg
import numpy as np
import sys

# just tryings to read a file in required format. Not works since there are single characters without '/' in the lines

file_inp = open("Imperial_March.synth", 'r')
all_text = file_inp.readlines()
file_inp.close()
tracks = []

for line in all_text:
    if line[0].isdigit():
        seq_of_notes = line.split()[1:]
        for i in range(len(seq_of_notes)):
            if len(seq_of_notes[i]) == 1:
                pass
            else:
                note, dur = seq_of_notes[i].split('/')
            seq_of_notes[i] = (note.capitalize(), float(dur))
        seq_of_notes = [tuple(note.split('/')) for note in seq_of_notes]
        tracks.append(seq_of_notes)
sys.exit
