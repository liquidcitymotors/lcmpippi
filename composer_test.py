from lcm import MultitrackAction
import lcm
from pippi import dsp
import os

name = "composer_test"

stem_dir = "scripts/lcm/renders/" + name

if  not os.path.isdir(stem_dir):
	os.mkdir(stem_dir)

class AddDrum(MultitrackAction):
	def __init__(self, name="drums", key="kick", pattern="x", beat=.25):
		self.name = name
		self.key = key
		self.pattern = pattern
		self.beat = beat
	stem_folder = stem_dir

	def do_action(self, prompt):
		new_sound = lcm.random_splice_sound(self.key)
		out = dsp.buffer()
		for index, note in enumerate(self.pattern):
			if note=="x":
				out = lcm.dub_mono(out, new_sound, self.beat * index)

		self.update_track(self.name, out)
		print(self.result)

boom = AddDrum("808", "808", "x..x..x.x..x..x.")

boom.iterate()
