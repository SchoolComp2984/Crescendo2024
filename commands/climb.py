class Climb:
    def __init__(self, _arm):
        # pass in reference to arm
        self.arm = _arm

    def climb(self):
        # move the arm to the position we want it to be at for climbing
        self.arm.arm_to_angle(30)

        # maybe hold it there or engage something else?
