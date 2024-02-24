import drawsvg as draw

from SongHarmony.song import Song
from SongHarmony.measure import Measure
from SongHarmony.chord import Chord


class Render:
    def __init__(self, song:Song) -> None:
        self.song = song
        self.chord_size = 90
        self.y_size = 120
        self.text_size = 20
        self.type_offset = 5
        self.grade_offset = 50
        self.measure_size = 25
        self.bracket_offset_x = 12
        self.bracket_offset_y = 30
        self.arrow_offset_y = -30
        self.new_key_offset = -20
        
        
        self.d = draw.Drawing((song.measure_per_line+1)*self.chord_size*song.chords_per_measure, 
                              (2+len(song.measures)//song.measure_per_line)*self.y_size)
        

    def __drawHorizontalBracket__(self, x_, y_, offset, type=0, is_dashed=False): # type 0: normal, type 1: start, type 2: end
        y_offset = 10  # Adjust based on your coordinate system
        x1 = x_ + self.bracket_offset_x
        x2 = x_ + offset + self.bracket_offset_x
        y = y_ + self.bracket_offset_y

        if type == 0 or type == 1:
            self.d.append(draw.Line(x1, y, x1, y+y_offset, stroke='black', stroke_width=1))
        if is_dashed:
            self.d.append(draw.Line(x1, y+y_offset, x2, y+y_offset, stroke='black', stroke_width=1, stroke_dasharray='5, 5'))
        else:
            self.d.append(draw.Line(x1, y+y_offset, x2, y+y_offset, stroke='black', stroke_width=1))
        if type == 0 or type == 2:
            self.d.append(draw.Line(x2, y+y_offset, x2, y, stroke='black', stroke_width=1))

    def __drawCurvedArrow__(self, x_, y_, offset, type=0, is_dashed=False):
        # Draw arrows
        y_offset = 30 
        arrow = draw.Marker(-0.1, -0.51, 0.9, 0.5, scale=4, orient='auto')
        arrow.append(draw.Lines(-0.1, 0.5, -0.1, -0.5, 0.9, 0, fill='black', close=True))

        x1 = x_ + self.text_size/2
        x2 = x_ + offset
        if type == 0 or type == 1:
            y1 = y_ + self.arrow_offset_y
        else:
            y1 = y_ + self.arrow_offset_y - y_offset/2
        
        if type == 0 or type == 2:
            y2 = y_ + self.arrow_offset_y
        else:
            y2 = y_ + self.arrow_offset_y - y_offset/2
        
        if type == 0:
            y_half = y1-y_offset
        elif type == 1:
            y_half = y2
        else:
            y_half = y1

        # Draw an arbitrary path (a triangle in this case)
        if is_dashed:
            p = draw.Path(stroke_width=1, stroke='black', fill_opacity=0.0, marker_end=arrow, stroke_dasharray='5, 5')
        else:
            p = draw.Path(stroke_width=1, stroke='black', fill_opacity=0.0, marker_end=arrow)
        p.M(x1, y1)  # Start path 
        p.C(x1, y1, x1 + (x2-x1)/2, y_half, x2, y2)  # Draw a curve 
        self.d.append(p)
    
    def get_distance(self, current, next):
        line_offset = (next[0] // self.song.measure_per_line) - (current[0] // self.song.measure_per_line)
        if line_offset == 0:
            chords_offset = ((next[0] - current[0]) * self.song.chords_per_measure + next[1] - current[1])
        elif line_offset == 1:
            chords_offset = (next[0] % self.song.measure_per_line ) * self.song.chords_per_measure + next[1] 
        else:
            print("Error: more than 1 line offset!")
            exit(-1)
        return line_offset, chords_offset
    
    def __draw_title__(self, x, y, title, composer):
        self.d.append(draw.Text(title, int(self.text_size*1.5), x, y, font_weight='bold', stroke='black', center=True))
        self.d.append(draw.Text(composer, int(self.text_size), x, y + self.text_size*1.5, stroke='grey', center=True))

    def __draw_init_bar__(self, x, y, init_bar=False):
        self.d.append(draw.Line(x-self.chord_size/4, y-self.measure_size, 
                                x-self.chord_size/4, y+self.measure_size/4, 
                                stroke='black', stroke_width=2))
        if init_bar:
            self.d.append(draw.Text(":", int(self.text_size), 
                                    x-self.chord_size/4 + self.text_size/2, y-self.measure_size/2, 
                                    stroke='black', center=True))
    
        
    def __draw__root__(self, x, y, root):
        self.d.append(draw.Text(root, self.text_size, x, y, font_weight='bold', center=False))
    
    def __draw_chord_type__(self, x, y, chord_type, root):
        self.d.append(draw.Text(chord_type, int(self.text_size/1.5),
                                x + int(self.text_size/1.5)*len(root) + self.type_offset, 
                                y - self.text_size/2, center=False))
                    
    def __draw_grade__(self, x, y, grade):
        self.d.append(draw.Text(grade, int(self.text_size/1.25),
                                x + int(self.text_size/2) + len(grade), 
                                y + self.text_size, center=True))
    def __draw_bracket__(self, x, y, current, next, is_dashed):
        line_offset, chords_offset = self.get_distance(current, next)
    
        if line_offset == 0:
            offset = chords_offset * self.chord_size
            self.__drawHorizontalBracket__(x, y, offset, type=0, is_dashed=is_dashed)
        else:
            
            offset =  ((self.song.measure_per_line * self.song.chords_per_measure) - (current[0] % self.song.measure_per_line) * self.song.chords_per_measure + current[1]) * self.chord_size - self.chord_size/4
            self.__drawHorizontalBracket__(x, y, offset, type=1, is_dashed=is_dashed)
            offset = chords_offset * self.chord_size + self.chord_size/2
            self.__drawHorizontalBracket__(self.chord_size/2, y + self.y_size, offset, type=2, is_dashed=is_dashed)

    def __draw_arrow__(self, x, y, current, next, is_dashed):
        line_offset, chords_offset = self.get_distance(current, next)
        
        if line_offset == 0:
            offset = chords_offset * self.chord_size
            self.__drawCurvedArrow__(x, y, offset, type=0, is_dashed=is_dashed)
        elif line_offset == 1:
            offset = ((self.song.measure_per_line * self.song.chords_per_measure) - (current[0] * self.song.chords_per_measure + current[1])) * self.chord_size - self.chord_size/4
            self.__drawCurvedArrow__(x, y, offset, type=1, is_dashed=is_dashed)
            offset = chords_offset * self.chord_size + self.chord_size/2
            self.__drawCurvedArrow__(self.chord_size/2, y + self.y_size, offset, type=2, is_dashed=is_dashed)
    
    def __draw_new_key__(self, x, y, new_key):
        self.d.append(draw.Text(new_key+":", int(self.text_size/1.75),
                                x + self.new_key_offset, 
                                y + self.text_size, stroke='grey', center=True))
        self.d.append(draw.Line(x + 2*self.new_key_offset, y + self.text_size*1.5, x, y + self.text_size*1.5, stroke='grey', stroke_width=1))
        self.d.append(draw.Line(x + 2*self.new_key_offset, y + self.text_size*1.5, x + 2*self.new_key_offset, y + self.text_size*0.75, stroke='grey', stroke_width=1))

    def __draw_old_key__(self, x, y, old_key):
        self.d.append(draw.Text(old_key, int(self.text_size/1.75),
                                x + self.new_key_offset, 
                                y + 2*self.text_size, stroke='grey', center=True))
        self.d.append(draw.Line(x, y + self.text_size*1.5, x, y + 2.4*self.text_size, stroke='grey', stroke_width=1))
    
    def __draw_end_bar__(self, x, y):
        self.d.append(draw.Line(x-self.chord_size/4, y-self.measure_size, 
                                        x-self.chord_size/4, y+self.measure_size/4, 
                                        stroke='black', stroke_width=2))
        self.d.append(draw.Line(x-self.chord_size/4 + 5, y-self.measure_size, 
                                x-self.chord_size/4 + 5, y+self.measure_size/4, 
                                stroke='black', stroke_width=4))
    
    def __draw_repeat_bar__(self, x, y):
        self.d.append(draw.Line(x-self.chord_size/4, y-self.measure_size, 
                                        x-self.chord_size/4, y+self.measure_size/4, 
                                        stroke='black', stroke_width=2))
        self.d.append(draw.Line(x-self.chord_size/4 + 5, y-self.measure_size, 
                                x-self.chord_size/4 + 5, y+self.measure_size/4, 
                                stroke='black', stroke_width=2))
        self.d.append(draw.Text(":", int(self.text_size),
                                x - self.chord_size/4 - self.text_size/2, 
                                y - self.measure_size/2, center=True))
    
    def __draw_n_ending__(self, x, y, n):
        self.d.append(draw.Line(x - self.chord_size/4, y-self.measure_size*1.1,  
                                x - self.chord_size/4, y-self.measure_size*1.25 - self.text_size, 
                                stroke='grey', stroke_width=2))
        
        self.d.append(draw.Line(x - self.chord_size/4, y-self.measure_size*1.25 - self.text_size,  
                                x + self.chord_size/4, y-self.measure_size*1.25 - self.text_size, 
                                stroke='grey', stroke_width=2))
        
        self.d.append(draw.Text(str(n)+".", int(self.text_size)*0.75,
                                x - self.chord_size/4 + self.text_size/2, y-self.measure_size*1.25, 
                                stroke='grey', font_weight='bold', center=False))
        
    def draw(self, out_name='out'):
        self.__draw_title__((self.song.measure_per_line+1)*self.chord_size*self.song.chords_per_measure/2, self.y_size/2, 
                            self.song.title, self.song.composer)
        x = self.chord_size
        y = 1.5*self.y_size
        for i, m in enumerate(self.song.measures):
            self.__draw_init_bar__(x, y, m.init_bar)
            
            if m.first_end:
                self.__draw_n_ending__(x, y, 1) 
            elif m.second_end:
                self.__draw_n_ending__(x, y, 2)
            
            if len(m.chords) == 0:
                self.__draw__root__(x, y, '%')
                x += self.chord_size * self.song.chords_per_measure
            else:
                for c in range(self.song.chords_per_measure):
                    if c < len(m.chords):
                        # Root text
                        self.__draw__root__(x, y, m.chords[c].root)
                        # Chord type text
                        self.__draw_chord_type__(x, y, m.chords[c].type, m.chords[c].root)
                        # Chord grade text
                        self.__draw_grade__(x, y, m.chords[c].grade)
                        # Draw brackets
                        if m.chords[c].ii_bracket is not None:
                            self.__draw_bracket__(x, y, (i, c), m.chords[c].ii_bracket, False)
                        if m.chords[c].subii_bracket is not None:
                            self.__draw_bracket__(x, y, (i, c), m.chords[c].subii_bracket, True)
                        # Draw arrows
                        if m.chords[c].v_i_arrow is not None:
                            self.__draw_arrow__(x, y, (i, c), m.chords[c].v_i_arrow, False)
                        if m.chords[c].subv_i_arrow is not None:
                            self.__draw_arrow__(x, y, (i, c), m.chords[c].subv_i_arrow, True)
                        # New key
                        if m.chords[c].new_key is not None:
                            self.__draw_new_key__(x, y, m.chords[c].new_key)
                        # Old key
                        if m.chords[c].old_key is not None:
                            self.__draw_old_key__(x, y, m.chords[c].old_key)

                    x += self.chord_size

            if m.end_bar:
                self.__draw_end_bar__(x, y)
            elif m.repeat_bar:
                self.__draw_repeat_bar__(x, y)
            
            if (i+1) % self.song.measure_per_line == 0:
                # Draw init measure line
                self.d.append(draw.Line(x-self.chord_size/4, y-self.measure_size, 
                                        x-self.chord_size/4, y+self.measure_size/4, 
                                        stroke='black', stroke_width=2))
                x = self.chord_size
                y += self.y_size
                
        self.d.set_pixel_scale(2)  # Set number of pixels per geometry unit
        self.d.save_svg(out_name + '.svg')
        self.d.save_png(out_name + '.png')