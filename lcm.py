import os
from pippi import dsp
from pippi import fx
from tkinter import filedialog
import glob
import time
import math

def spectrogram(out, name='scripts/lcm/renders/untitled'):
	out_path = name
	out.write(out_path+'.wav')
	os.system('sox '+out_path+'.wav -n spectrogram -o '+out_path+'.png')
	os.system('open '+out_path+'.png')
	os.system('afplay '+out_path+'.wav')

def get_file():
	return filedialog.askopenfilename()

def random_splice_sound(key="kick", maxlength=6, base_path="/Users/willmitchell/Splice/sounds/packs"):
	return random_splice_sound_path(key, maxlength, base_path)[0]

def random_splice_sound_path(key="kick", maxlength=6, base_path="/Users/willmitchell/Splice/sounds/packs"):
	sounds = glob.glob(base_path + "/**/*.wav", recursive=True)
	selections = []
	for sound in sounds:
		if key.upper() in sound.upper():
			selections.append(sound)
	seed = time.time() - int(time.time())
	file = selections[int(seed * len(selections))]
	selection = dsp.read(file)
	while selection.dur > maxlength:
		seed = time.time() - int(time.time())
		file = selections[int(seed * len(selections))]
		selection = dsp.read(file)
	return (selection, file)

def match_length(snd1, snd2):
	if snd1.dur > snd2.dur:
		snd2 = snd2.pad(end=len(snd1) - len(snd2), samples=True)
	elif snd2.dur > snd1.dur:
		snd1 = snd1.pad(end=len(snd2) - len(snd1), samples=True)

	return snd1, snd2

def dub_mono(snd1, snd2, pos):
	# if snd1.dur > pos:
	snd1 = snd1.cut(0, pos)
	snd1.adsr(0, 0, 1, .03)
	snd1.dub(snd2, pos)
	return snd1

class CompositionAction:

	def get_state(self):
		pass
	def show_state(self):
		pass
	def action_prompt(self):
		return 1
	def do_action(self, action):
		pass
	def show_result(self):
		pass
	def reaction_prompt(self):
		return 1
	def review_result(self, reaction):
		pass

	def iterate(self):
		self.show_state()
		action = self.action_prompt()
		self.do_action(action)
		self.show_result()
		reaction = self.reaction_prompt()
		self.review_result(reaction)

class MultitrackAction(CompositionAction):

	stem_folder = ""
	tracks = {}
	result = {}

	def update_track(self, name, sound):
		self.result[self.stem_folder + "/" + name + ".wav"] = sound

	def get_track(self, name, sound):
		key = self.stem_folder + "/" + name + ".wav"
		if key in self.result:
			return self.result[key]
		else: 
			return dsp.buffer([0])

	def get_state(self):
		self.files = glob.glob(self.stem_folder + "/*.wav", recursive=True)
		for file in self.files:
			if "compositiontemp" not in file:
				self.tracks[file] = dsp.read(file)

	def show_state(self):
		self.get_state()
		mix = dsp.buffer([])
		for file in self.tracks:
			mix &= self.tracks[file]
		spectrogram(mix, self.stem_folder + "/compositiontemp")

	def show_result(self):
		mix = dsp.buffer([])
		for file in self.result:
			mix &= self.result[file]
		spectrogram(mix, self.stem_folder + "/compositiontemp")
		
	def reaction_prompt(self):
		return input("What shall we do?")

	def review_result(self, reaction):

		replay = [""]
		play_original = [" "]
		keep = ["y"]
		skip = ["n"]
		discard = ["x"]

		if reaction in replay:
			self.show_result()
			self.review_result(self.reaction_prompt())
		if reaction in play_original:
			self.show_state()
			self.review_result(self.reaction_prompt())
		if reaction in keep:
			print(self.result)
			for file in self.result:
				self.result[file].write(file)
		if reaction in discard:
			self.iterate()
		elif reaction in skip:
			pass

















