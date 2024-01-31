from subsystems.arm import Arm
#Making a class for the shooter mechanism on the robot.
#the shooter motor is a neo.
#move arm to angle to shoot
#right speed for the wheel?
#some sorta sensor for distance? either apriltag or ultrasound
#some sorta function to calculate arm angle and then motor speed to shoot
#probably a different code in commands for shoot instead of shooting it here.
class Shooter:
    #intiating the shooter
    def shooter_init(self, _shooter_motor):
        #creating a reference to our shooter motor
        self.shooter_motor = _shooter_motor

   
    #spins the shooting motors
    def shooter_spin(self, speed):
        self.shooter_motor.set(speed)


"""
pseudo coding?
use sensors. get measurement of distance from the speaker
maybe find the angle as well to rotate the robot
math it in
calculate optimal arm angle, motor power needed
move arm to angle
spin motor at right speed
fire
move arm back to before? do we need that?


we need the apriltags to:
tell us distance, angle
so we can allign robot directly at the center using the bearing of the apriltag
get distance from the apriltag to shoot

1. get distance from apriltag (camera most likely)
2. get current arm angle
3. calculate desired arm angle
4. get location of apriltag
5. turn robot so that we are angled directly at the april tag and the center of the speaker
6. spin shooter motors for 1 second
7. feed the note into the shooter
8. end shooting (stop motor)
"""