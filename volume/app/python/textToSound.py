import os
import argparse
from subprocess import call
from functools import partial

from lib.uniproc import DetectLettersAndTone
from lib.let2snd import ConvertLettersToSounds
from lib.generate_label import transform_text
from lib.label_format import Utterance

DEFAULT_LABEL_OUTPUT = 'output/out.lab'
DEFAULT_SOUND_OUTPUT = '../output/out.wav'
DEFAULT_HTS_VOICES = 'voices/20170428.htsvoice'
DEFAULT_SOUND_INTENSITY = 10
DEFAULT_SPEECH_SPEED = 1

def generate_speech(lab_file_path=DEFAULT_LABEL_OUTPUT, 
                    out_speech_path=DEFAULT_SOUND_OUTPUT,
                    sound_intensity=DEFAULT_SOUND_INTENSITY, 
                    speech_speed=DEFAULT_SPEECH_SPEED,
                    voice=DEFAULT_HTS_VOICES):

        call(['./hts_engine', '-m', voice, '-b', '0.4', '-ow', out_speech_path, lab_file_path, '-g', str(sound_intensity), '-r', str(speech_speed)])
        # Change back to defaut text

def write_text(text, output_text=DEFAULT_LABEL_OUTPUT):
    text = text.strip()
    utterances = []
    utterance_list = transform_text(text)
    output_label = ''

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
        output_label = output_label + utterance_ins.label + '\n'

    with open(output_text, "w") as f:
        f.write(output_label)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', dest='text', help='Input text')
    parser.add_argument('-v', dest='voice', help='HTS_voice')
    parser.add_argument('-o', dest='output', help='Output sound file')
    parser.add_argument('-l', dest='label', help='Label file path')
    
    input_argv = parser.parse_args()
    label_file = input_argv.label
    if (input_argv.label != None) and (os.path.isfile(label_file)):
        generate_speech(lab_file_path=label_file, out_speech_path=input_argv.output, voice=input_argv.voice)
    else:
        write_text(input_argv.text)
        generate_speech(out_speech_path=input_argv.output, voice=input_argv.voice)

    print('success')

    




