#PID
class PID:
    #intializing the PID by making references to the values that are getting passed in
    def pid_init(self, p, i, d, val):
        #initializing the three main values in PID
        #p = proportion
        self.p = p
        #i = integral
        self.i = i
        #d = derivative
        self.d = d
        #setting the previous error to the 
        self.previous_error = val
        #initializing the integral that is used to calculate the distance between the current value and target value
        self.integral = 0
    