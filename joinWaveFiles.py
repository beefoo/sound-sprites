# -*- coding: utf-8 -*-

import argparse
import csv
import json
import os
import sys
import wave

# input
parser = argparse.ArgumentParser()
parser.add_argument('-manifest', dest="MANIFEST_FILE", default="manifest/orchestral_harp.csv", help="CSV manifest input file")
parser.add_argument('-out', dest="OUTPUT_FILE", default="wav/orchestral_harp.wav", help="Wav file output")
parser.add_argument('-sprite', dest="SPRITE_FILE", default="sprites/orchestral_harp.json", help="Wav file output")

args = parser.parse_args()
MANIFEST_FILE = args.MANIFEST_FILE
OUTPUT_FILE = args.OUTPUT_FILE
SPRITE_FILE = args.SPRITE_FILE

notes = []
with open(MANIFEST_FILE, 'rb') as f:
    reader = csv.DictReader(f)
    notes = list(reader)

duration = sum([int(n["duration"]) for n in notes])
print "Target duration: %ss" % round(1.0*duration/1000, 3)

data = []
sprites = {}
start = 0
for note in notes:
    duration = int(note["duration"])

    w = wave.open(note["file"], 'rb')
    data.append([w.getparams(), w.readframes(w.getnframes())])
    w.close()

    sprites[note["name"]] = [start, duration]
    start += duration

# Write to sprite file
with open(SPRITE_FILE, 'w') as f:
    json.dump(sprites, f, indent=2)
    print "Wrote sprites to %s" % SPRITE_FILE

# Write to wave file
output = wave.open(OUTPUT_FILE, 'wb')
output.setparams(data[0][0])
for d in data:
    output.writeframes(d[1])
output.close()
print "Wrote wave file %s" % OUTPUT_FILE
