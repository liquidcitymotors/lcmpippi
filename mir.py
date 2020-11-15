from pippi import dsp
from pippi import mir
from pippi import tune
from pippi import fx
from pippi import oscs
from pippi import rhythm
import lcm
import numpy as np

splices = mir.segments(lcm.random_splice_sound("loop", maxlength=60))
numsounds = len(splices)

out = dsp.buffer(length=.125 * numsounds)

for sound in splices:
	snd = sound.adsr(.01, .1, .25, .1)
	if dsp.rand() > .8:
		snd.reverse()
	out.dub(snd, dsp.randint(0, numsounds) * .125)

mod = oscs.Osc('sine', [0, 1000]).play(out.dur)
# mod2 = oscs.Osc('sine', freq=440, amp=1).play(5)

(out, mod) = lcm.match_length(out, mod)

rm = mod * out

lcm.spectrogram(rm)

print(out.dur)
print(mod.dur)

