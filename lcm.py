import os
from pippi import dsp
from pippi import fx
from tkinter import filedialog
import glob
import time
import math

def spectrogram(out, name='untitled'):
	out_path = 'scripts/lcm/renders/' + name
	out.write(out_path+'.wav')
	os.system('sox '+out_path+'.wav -n spectrogram -o '+out_path+'.png')
	os.system('open '+out_path+'.png')
	os.system('afplay '+out_path+'.wav')

def get_file():
	return filedialog.askopenfilename()

def random_splice_sound(key="kick", maxlength=1, base_path="/Users/willmitchell/Splice/sounds/packs"):
	sounds = glob.glob(base_path + "/**/*.wav", recursive=True)
	selections = []
	for sound in sounds:
		if key.upper() in sound.upper():
			selections.append(sound)
	seed = time.time() - int(time.time())
	selection = dsp.read(selections[int(seed * len(selections))])
	while selection.dur > maxlength:
		seed = time.time() - int(time.time())
		selection = dsp.read(selections[int(seed * len(selections))])
	return selection

