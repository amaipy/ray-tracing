class Light:
    def __init__(self, position, color, atenuation):
        self.position = position
        self.color = color
        self.co_atenuation = atenuation[0]
        self.pos_atenuation = atenuation[1]
        self.co_square_pos = atenuation[2]