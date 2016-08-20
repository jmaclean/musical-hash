# What is this?

This project aims to allow for simple differentiation of hashes through the power of music!

It simply takes a hex string (from a hash) and uses that to generate a series of tones with varying frequencies and tones.

# Setup

Install `portaudio`:
```
brew install portaudio
```

Install pip requirements:
```
pip install -r requirements.txt
```

# Usage

Run without arguments to generate a psuedo-random hash.
```
python musical_hash.py
```

Run with some string input to hash and play it.
```
python musical_hash.py "Hello, World"
```

# The Future

I want to support the following:
- Various hashing algorithms
- Load from file
- Input already hashed string
- Output to music file
- Support playing two hashes at once (to diff them)
- Better concept of tone length
- A consistent (configurable?) tempo (relates to the above)
