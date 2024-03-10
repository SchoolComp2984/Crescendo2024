# import the networktables library for python
import ntcore

# create a reciever class for the roboRIO to access network tables
class NetworkReciever():
    def __init__(self):
        # create an reference to the network table data from the smart dashboard
        self.dashboard = ntcore.NetworkTableInstance.getDefault().getTable("SmartDashboard")


    # method to retrieve the x and y position of an april tag from the camera
    # (0, 0) is in the center of the screen
    # we can use the fact that if the x position of the apriltag is positive, then it is to our right
    # we can use this to center our robot and aim towards the speaker
    def get_apriltag_data(self):
        # store the x and y positions of the apriltag as variables and set them to None if the data cannot be found
        apriltag_x = self.dashboard.getNumber("tagcenterx", None)
        apriltag_y = self.dashboard.getNumber("tagcentery", None)
        apriltag_distance = self.dashboard.getNumber("Distance", None)

        # return the position in an array
        return [apriltag_x, apriltag_y, apriltag_distance]
    
    # method to retrieve the x and y positions of the note from the camera
    # same as apriltags where (0, 0) is in th center of the screen
    # we can use the same fact to aim the robot towards the note, which is useful for auto intake
    def get_note_data(self):
        note_x = self.dashboard.getNumber("note_x", None)
        note_y = self.dashboard.getNumber("note_y", None)
        note_distance = self.dashboard.getNumber("note_distance", None)

        # return the x and y positions of the note in an array
        return [note_x, note_y, note_distance]