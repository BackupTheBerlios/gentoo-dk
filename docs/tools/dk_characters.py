#!/usr/bin/python
## Made by Arne Mejlholm, to easily exchange wrong characters


import sys

def to_dk_characters(input, output, ae, oe, aa):
	for line in input:
		charnr = -1
		for character in line:
			charnr = charnr + 1
			if line[charnr] == ae[0] and line[charnr + 1] == ae[1]:
				output.write('æ')
				continue
			elif line[charnr] == oe[0] and line[charnr + 1] == oe[1]:
				output.write('ø')
				continue
			elif line[charnr] == aa[0] and line[charnr + 1] == aa[1]:
				output.write('å')
				continue
			elif line[charnr] == ae[1] and line[charnr - 1] == ae[0]:
				continue
			elif line[charnr] == oe[1] and line[charnr - 1] == oe[0]:
				continue
			elif line[charnr] == aa[1] and line[charnr - 1] == aa[0]:
				continue
			else:
				output.write(character)

input = open(sys.argv[1], 'r')
output = open(str(sys.argv[1]) + '.new', 'w')
if len(sys.argv) != 5:
	print "Brug: ./dk_characters.py outputfil 1 2 3"
	print "hvor 1 2 3 er henholdvis den først, anden og trejde character der skal udskiftes med æ ø og å"
else:
	ae = sys.argv[2]
	oe = sys.argv[3]
	aa = sys.argv[4]
	to_dk_characters(input, output, ae, oe, aa)

