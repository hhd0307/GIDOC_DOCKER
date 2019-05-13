#!/usr/bin/env python3
# This script generates full-context label for an input text file.
# The file may consist of several utterances.

from .uniproc import DetectLettersAndTone
from .let2snd import ConvertLettersToSounds
from .label_format import Utterance
import argparse
import codecs

##### Util for transfrom text into list of utterances
def transform_text(text):
    utterances = []
    raw_utterances = []

    dot_split = text.split(".")
    dot_split = [x.encode('utf8', 'surrogateescape').decode('utf8') for x in dot_split]

    for utterance in dot_split:
        if len(utterance):
            raw_utterances.append(utterance)

    for raw_utterance in raw_utterances:
        utterance = []
        comma_split = raw_utterance.split(",")
        for raw_phrase in comma_split:
            phrase_list = raw_phrase.split()
            if len(phrase_list):
                utterance.append(phrase_list)
        utterances.append(utterance)

    return utterances


def main():
	parser = argparse.ArgumentParser(description='Generates full-context label from an Unicode-encoded text file.')
	parser.add_argument('inFile', metavar='inFile', type=str, action='store',
					help='input text file')
	args = parser.parse_args()

	with codecs.open(args.inFile, "r", encoding='utf-8', errors='ignore') as f:
		text = f.read()
	text = text.strip()
	
	utterances = []
	utterance_list = transform_text(text)

	# Loop through raw utterances
	for utterance in utterance_list:
		new_utterance = []
		for phrase in utterance:
			new_phrase = []
			for word in phrase:
				word = DetectLettersAndTone(word)
				word = ConvertLettersToSounds(word)
				new_phrase.append(word)
			new_utterance.append(new_phrase)
		utterances.append(new_utterance)

	for utterance in utterances:
		utterance_ins = Utterance(utterance)
		utterance_ins.create_label()
		print(utterance_ins.label)

	f.close()

if __name__ == "__main__":
	main()
