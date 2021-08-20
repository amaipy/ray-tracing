class Camera:
    def __init__(self, position, center, direction, orientation, y_opening):
        self.position = position
        self.center = center
        self.direction = direction
        self.up = orientation
        self.y_opening = y_opening
