class Chord():
    def __init__(self, root:str, specie:str, grade:str) -> None:
        super().__init__()
        self.root = root
        self.type = specie
        self.grade = grade
        self.new_key = None
        self.old_key = None
        self.ii_bracket = None
        self.subii_bracket = None
        self.v_i_arrow = None
        self.subv_i_arrow = None
        self.scale = []
        
    def __str__(self):
        return "{}{} ".format(self.root, self.type)