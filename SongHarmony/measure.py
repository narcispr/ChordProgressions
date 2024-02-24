class Measure:
    def __init__(self) -> None:
        self.chords = []
        self.end_bar = False
        self.init_bar = False
        self.first_end = False
        self.second_end = False
        self.repeat_bar = False
    
    def get_str(self, chords_per_measure) -> str:
        ret = '| '
        if len(self.chords) == 0:
            ret += '% '
        else:
            for i in range(chords_per_measure):
                if i < len(self.chords):
                    ret += str(self.chords[i])
                else:
                    ret += '  '
        if self.end_bar:
            ret += '||'
        return ret