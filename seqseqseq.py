from pippi import dsp
from pippi import rhythm
import lcm

beat = [60 / 150, 60 / 80, 60 / 150]
dm = rhythm.Seq(beat)

hat1pat = rhythm.eu(8, 3)
hat2pat = 'x'
snarepat = rhythm.eu(16, 5)
kickpat = rhythm.eu(16, 7)

kick = lcm.random_splice_sound()
snare = lcm.random_splice_sound("snare")
hat1 = lcm.random_splice_sound("open")
hat2 = lcm.random_splice_sound("closed")

def makehat1(ctx):
	return hat1

def makehat2(ctx):
	return hat2

def makesnare(ctx):
	return snare

def makekick(ctx):
	return kick

dm.add('h1', hat1pat, makehat1, div=4)
dm.add('h2', hat2pat, makehat2, div=4)
dm.add('k', kickpat, makekick, div=4)
dm.add('c', snarepat, makesnare, div=4)

out = dm.play(32)
lcm.spectrogram(out)