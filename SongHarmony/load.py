from xml.dom import minidom
import ast
from SongHarmony.song import Song
from SongHarmony.measure import Measure
from SongHarmony.chord import Chord

def load_song_from_xml(xml_path):
    song = Song()
    dom = minidom.parse(xml_path)
    
    song.title = dom.getElementsByTagName('title')[0].childNodes[0].data
    song.composer = dom.getElementsByTagName('composer')[0].childNodes[0].data
    song.chords_per_measure = int(dom.getElementsByTagName('chords_per_measure')[0].childNodes[0].data)
    song.measure_per_line = int(dom.getElementsByTagName('measures_per_line')[0].childNodes[0].data)
    
    measures = dom.getElementsByTagName('measure')
    for m in measures:
        measure = Measure()
        chords = m.getElementsByTagName('chord')
        for c in chords:
            root = c.getElementsByTagName('root')[0].childNodes[0].data
            specie = c.getElementsByTagName('specie')[0].childNodes[0].data
            grade = c.getElementsByTagName('grade')[0].childNodes[0].data
            chord = Chord(root, specie, grade)
            
            # Setting additional chord attributes if they exist
            for attr in ['new_key', 'old_key', 'down_comment', 'up_comment']:
                elements = c.getElementsByTagName(attr)
                if elements:
                    setattr(chord, attr, elements[0].childNodes[0].data)

            # Setting additional chord attributes if they exist
            for attr in ['ii_bracket', 'subii_bracket', 'v_i_arrow', 'subv_i_arrow']:
                elements = c.getElementsByTagName(attr)
                if elements:
                    setattr(chord, attr, ast.literal_eval(elements[0].childNodes[0].data))
            
            measure.chords.append(chord)
        
        if m.getElementsByTagName('end_bar'):
            measure.end_bar = True

        song.measures.append(measure)
    
    return song