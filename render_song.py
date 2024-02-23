#!/usr/bin/env python
# -*- coding: utf-8 -*-

from SongHarmony.load import load_song_from_xml 
from SongHarmony.render import Render
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: test.py <xml file>")
        sys.exit(1)
    song = load_song_from_xml(sys.argv[1])
    ds = Render(song)
    ds.draw()
    ds.d  # Show the svg
