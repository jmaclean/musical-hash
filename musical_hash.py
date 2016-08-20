#!/usr/local/bin/python
"""Musical Hash.

Usage:
  musical_hash.py
  musical_hash.py <string>

Options:
  -h --help     Show this screen.

No args will generate random hashes.
If an argument is provided, it will be hashed.
"""
from docopt import docopt
import audiogen
import csv
import time
import itertools
import numpy as np
from random import randint
import hashlib

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
    # char_list = map(lambda c: int(c, 16), list(hash))
    char_list = list(hash)
    tones = []
    for i in range(0, len(char_list), 3):
        if i > len(char_list) - 3:
            break
        freq_string = ''.join([char_list[i], char_list[i + 1]])
        freq = tone_dict[int(freq_string, 16) % len(tone_dict)]
        length = length_dict[int(char_list[i + 2], 16)]
        tones += [(freq, length, freq_string)]
    return tones

def gen_rand_hash(length):
    return ''.join(['%x' % randint(0, 15) for i in range(length)])

def read_csv(filename):
    tones = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            name = row[0]
            freq = float(row[1])
            tones += [(name, freq)]
    return tones

if __name__ == '__main__':
    args = docopt(__doc__, version='Musical Hash 0.1')

    file_tones = read_csv('./note_mappings.csv')
    tone_dict = {}
    for i, f in enumerate(file_tones):
        tone_dict[i] = f[1]

    # tone_dict = generate_tone_dict(255, 350, 2000)
    length_dict = generate_length_dict(16, .1, .4)
    if args['<string>']:
        m = hashlib.md5()
        m.update(args['<string>'])
        hash = m.hexdigest()
    else:
        hash = gen_rand_hash(32)
    print "Hash: {}".format(hash)
    tones = hash_to_tones(hash, tone_dict, length_dict)
    tone_chain = []
    print 'Frequency\tLength'
    for f in tones:
        print "{0}\t\t{1:.2f}s".format(f[0], f[1])
        tone_chain += audiogen.beep(f[0], f[1])
    start = time.time()
    audiogen.sampler.play(itertools.chain(tone_chain))
    print "Time to play: {0:.2f}s".format(time.time() - start)

