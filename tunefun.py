from pippi import tune
from pippi import fx
from pippi import dsp
from pippi.oscs import Osc
from pippi import wavetables
import os
import numpy as np
import lcm

chord1 = tune.chord('i7', key='a', octave=3)
chord2 = tune.chord('iv7', key='a', octave=2)
chord3 = tune.chord('v7', key='a', octave=4)
chords = [chord1, chord2, chord3]

sr = 48000

length = 1024
beat = .1

print("Rendering filter")

pulse = dsp.buffer([.1]*100)
beat_pulse = dsp.buffer(length=beat*16)
beat_pulse.dub(pulse, 0)
pings = dsp.buffer(length=length*beat)

for i in range((length*3)//4):
	if (i//3)%2 == 0:
		onset = i * (beat/3) * 4
		pings.dub(pulse * (((i%3)/3) + .33333), onset)

cvl = []
cvr = []
key = dsp.choice(chords)
res = []
res_gabmit = [1, .95, .85, .9]
for note in range(length):
	if (note % 3) == 0:
		key = dsp.choice(chords)

	notel = key[note % len(chord1)]
	noter = key[(note + 1) % len(chord1)]
	res.append(dsp.choice(res_gabmit))
	for i in range(1000):
		cvl.append(notel)
		cvr.append(noter)

pings = fx.lpf(pings, [cvl, cvr], res)

wavetable = dsp.win('sine', -2, 2)
wavetable.repeat(length * 220)
warp1 = fx.vspeed2(pings, wavetable, quality=6, normalize=True)
warp2 = warp1.reversed()
pings &= warp1
pings &= warp2 * .50

print("Rendering closed hat")

main = 'x...x...'
variations = ['x.x.x...', 'x...x...', 'x.x.x.x.']
hat = lcm.random_splice_sound("closed")
# hat = dsp.read(lcm.get_file())
velocities = [1, .75, .85, .75]

hatdub = dsp.buffer(length=length*beat)

for note in range(length):
	if ((note//16) % 8) == 3:
		pattern = dsp.choice(variations)
	else:
		pattern = main
	if pattern[note % len(pattern)] == "x":
		jitter = (dsp.rand() - .5) * .0001
		hatdub.dub(hat * velocities[note % len(velocities)], note * beat + jitter)

print("Rendering snares")

main = '..x.............'
variations = ['..x.x...', 'x..', 'x....']
snare = lcm.random_splice_sound("snare")
snare.cut(0, int(snare.dur/beat) * beat)
revflipflop = 1
snaredub = dsp.buffer(length=beat * length)

for note in range(length):
	if ((note//4) % 4) == 3:
		pattern = dsp.choice(variations)
	else:
		pattern = main
	if (pattern[note % len(pattern)] == "x") and (dsp.rand() > .5):
		sound = fx.vspeed2(snare, [dsp.rand() * 2 + .5, 1], 6)
		if revflipflop > .5: 
			sound.reverse()
			revflipflop = 0
		else:
			revflipflop = 1
		snaredub.dub(sound, note * beat)

print("Rendering 808")

bass = lcm.random_splice_sound("MURDA_808")
bassdub = dsp.buffer(length=length * beat)
for note in range(length):
	if (note % 16) == 0:
		bassdub.dub(bass, note * beat)

print("Rendering Perc")

perc = lcm.random_splice_sound("perc")
percdub = dsp.buffer(length=length * beat)
for note in range(length):
	if (note % 16) == 8:
		percdub.dub(perc, note * beat)

print("Clipping")

out = bassdub & (snaredub * .75) & pings & hatdub & percdub
out *= .25
out = fx.upsample(out, 2)
out.softclip()
out = fx.decimate(out, 2)

print("Chopping")

pullups = [[1,-1], [0, -1], [-1, 1], [1, 0], [0, 1], [-1, 0]] 
for eightbar in range(length//(16*8)):
	last_bar = ((eightbar + 1) * (16 * 8) - 16) * beat
	bar = 16 * beat
	first_part = out.cut(0, last_bar)
	chop = out.cut(last_bar, bar)
	chop = fx.vspeed2(chop, dsp.choice(pullups), 20, True)
	end = out.cut(last_bar + bar, max(out.dur - (last_bar + bar), 0))
	out = first_part + chop + end




lcm.spectrogram(out)
