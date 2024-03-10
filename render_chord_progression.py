#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ChordProgressions.load import load_song_from_xml 
from ChordProgressions.render import Render
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: test.py <xml file> <scale default=1>")
        sys.exit(1)
    song = load_song_from_xml(sys.argv[1])
    ds = Render(song)
    if len(sys.argv) == 3:
        ds.draw(out_name=sys.argv[1].split('.')[0], scale=float(sys.argv[2]))
    else:
        ds.draw(out_name=sys.argv[1].split('.')[0])
   
    