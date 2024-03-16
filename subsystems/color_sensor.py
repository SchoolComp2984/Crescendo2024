from rev import ColorSensorV3

class ColorSensor:
    def __init__(self, _color_sensor : ColorSensorV3):
        self.color_sensor = _color_sensor

    def sees_note(self):
        if self.color_sensor.getProximity() > 230:
            return True
        
        return False
