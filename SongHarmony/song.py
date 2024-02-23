class Song:
    def __init__(self, title:str="", composer:str="") -> None:
        self.title = title
        self.composer = composer
        self.measures = []
        self.measure_per_line = 4
        self.chords_per_measure = 2
    
    def __str__(self) -> str:
        ret = "{} by {}\n".format(self.title, self.composer)
        for m in self.measures:
            ret += str(m.get_str(self.chords_per_measure))
        return ret