from pippi.soundbuffer import SoundBuffer
from pippi import wavetables
from pippi.wavetables import Wavetable
from pippi import dsp
from pippi.oscs import Osc
from pippi import fx

import numpy as np
import os

length = .5
oversample = 1
snd = dsp.read('tests/sounds/linux.wav')
snd = fx.vspeed2(snd, 'sine', 20)

out_path = 'scripts/renders/test'
snd.write(out_path+'.wav')
os.system('sox '+out_path+'.wav -n spectrogram -o '+out_path+'.png')
os.system('open '+out_path+'.png')
os.system('afplay '+out_path+'.wav')