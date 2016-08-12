#!/usr/local/bin/python
"""Musical Hash.

Usage:
  musical_hash.py

Options:
  -h --help     Show this screen.

"""
from docopt import docopt
import audiogen
import time
import itertools
import numpy as np
from random import randint

def generate_tone_dict(num_tones, freq_min, freq_max):
    dict = {}
    for i, f in enumerate(range(freq_min, freq_max, (freq_max - freq_min) / num_tones)):
        dict[i] = f
    return dict


def generate_length_dict(num_lengths, min, max):
    dict = {}
    for i, f in enumerate(np.arange(min, max, (max - min) / num_lengths)):
        dict[i] = f
    return dict

def hash_to_tones(hash, tone_dict, length_dict):
    char_list = map(lambda c: int(c, 16), list(hash))
    tones = []
    for i in range(0, len(char_list), 3):
        if i > len(char_list) - 3:
            break
        # tones += [(tone_dict[char_list[i] + char_list[i+1]], length_dict[char_list[i + 2]])]
        tones += [(tone_dict[char_list[i]], tone_dict[char_list[i + 1]], length_dict[char_list[i + 2]])]
    return tones

def gen_hash(length):
    return ''.join(['%x' % randint(0, 15) for i in range(length)])

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Musical Hash 0.1')
    # print(arguments)
    tone_dict = generate_tone_dict(16, 300, 1800)
    length_dict = generate_length_dict(16, .1, .6)
    hash = gen_hash(64)
    print hash
    tones = hash_to_tones(hash, tone_dict, length_dict)
    tone_chain = []
    for f in tones:
    # for f in tone_dict.values():
        print f
        length = f[2]
        mix = audiogen.crop(audiogen.util.mixer((audiogen.tone(f[0]), audiogen.beep(f[1])),
                                  [(audiogen.util.constant(1), audiogen.util.constant(1))]
                                  ), length)
        tone_chain += mix
        # time.sleep(.1)
    start = time.time()
    audiogen.sampler.play(itertools.chain(tone_chain))
    print time.time() - start

