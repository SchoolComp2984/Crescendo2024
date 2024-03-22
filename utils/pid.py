class PID:
    #intializing the PID by making references to the values that are getting passed in
    def __init__(self, kp, ki, kd, val):
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
        proportional_term = error * self.kp

        #proportion can cause the value to go over the target
        #if the integral passes over the target either from the bottom and going over or from the top and going under
        #we bring the integral back at zero to prevent it from going up infinitely
        if self.integral > 0 and error*self.ki < 0:
            self.integral = 0
        if self.integral < 0 and error*self.ki > 0: 
            self.integral = 0

        #adding to the integral value
        self.integral += error * self.ki
        
        integral_term = 0
        #if error is close enough to the target, we will use the integral
        if error > -20 and error < 20: 
            integral_term = self.integral
        #if not, the integral should go back to zero 
        else: self.integral = 0

        #find the speed of the variation of the error through the derivative
        derivative_term = self.kd * (error - self.previous_error) 

        # set the previous error to the current error from this function call
        self.previous_error = error
       
        # add up the p, i, and d terms and return the sum
        power = proportional_term + integral_term + derivative_term
        return power
    
    def keep_integral(self, error):
        #a pid that keeps the integral which will probably be used for spinning the motor
        #may not even need this but might as well have one.
        #basically the same as the other PID we have.
        #not turning so no need to clear integral.
        proportional_term = error * self.kp

        self.integral += error * self.ki
        integral_term = 0
        if error > -20 and error < 20:
            integral_term += self.integral
        else: self.integral = 0

        derivative_term = self.kd * (error - self.previous_error)

        self.previous_error = error

        power = proportional_term + integral_term + derivative_term

        return power
