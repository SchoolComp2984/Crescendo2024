#PID
class PID:
    #intializing the PID by making references to the values that are getting passed in
    def pid_init(self, kp, ki, kd, val):
        #initializing the three constants in the PID
        #p = proportional constant
        self.kp = kp
        #i = integral
        self.ki = ki
        #d = derivative
        self.kd = kd
        #setting the previous error to the 
        self.previous_error = val
        #initializing the integral that is used to calculate the distance between the current value and target value
        self.integral = 0
    
    #pid for steering
    def steer_pid(self, error):
        #PID is basically the sum of three. Proportion + Integral + Derivative
        #proportion = error times the proportion constant
        proportion = error*self.kp

        #proportion can cause the value to go over the target
        #if the integral passes over the target either from the bottom and going over or from the top and going under
        #we bring the integral back at zero to prevent it from going up infinitely
        if self.integral>0 and (error*self.i<0): self.integral = 0
        if self.integral<0 and (error*self.i>0): self.integral = 0
        #adding to the integral value
        self.integral += error * self.ki
        #if error is close enough to the target, we will use the integral
        if(-20<error<20): integral = self.integral
        #if not, the integral should go back to zero 
        else: self.integral = 0

        #find the speed of the variation of the error through the derivative
        derivative = self.kd * (error-self.previous_error)  
        power = proportion + integral + derivative
        previous_error  = error
        return power
