from pippi import fx
from pippi import dsp
from pippi.oscs import Osc
import numpy as np
import os

length = 4
oversample = 1
sweep = np.logspace(0, 9, 512 * length, base = 2) * 24
snd = Osc('sine', freq=sweep, samplerate=24000).play(length)
snd = fx.upsample(snd, oversample)
print(snd.samplerate)
# snd *= 2
# snd = fx.distort(snd)
# snd = fx.decimate(snd, oversample)


out_path = 'scripts/renders/test_up_downsample'
snd.write(out_path+'.wav')
os.system('sox '+out_path+'.wav -n spectrogram -o '+out_path+'.png')
os.system('open '+out_path+'.png')
os.system('afplay '+out_path+'.wav')