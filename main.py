import logging
from queue import SimpleQueue as Queue
from time import sleep

from gpiozero import Servo, Motor

SERVO_PIN=17
MOTOR_FORWARD_PIN=27
MOTOR_BACKWARD_PIN=22
MOTOR_HAS_PWM=True


class Car():
    """
    Class repreenting the car.
    """
    def __init__(self):
        self.commands = Queue()
        self.servo = Servo(SERVO_PIN)
        self.servo.value = 0
        self.motor = Motor(forward=MOTOR_FORWARD_PIN, backward=MOTOR_BACKWARD_PIN, pwm=MOTOR_HAS_PWM)

    def accelerate(self, until=1):
        """
        Gradually accelerates the motor.
        """
        speed = 0.1
        while speed < until:
            self.motor.forward(speed)
            speed += 0.1
            sleep(0.2)

    def deaccelerate(self, until=0):
        """
        Gradually deaccelerates the motor.
        """
        speed = self.motor.value
        while speed > until:
            self.motor.forward(speed)
            speed -= 0.1
            sleep(0.2)

    def turn_right(self):
        self.turn('right')

    def turn_left(self):
        self.turn('left')

    def set_straight(self):
        """
        Puts servo on the mid position.
        """
        self.servo.mid()
        sleep(0.5)

    def stop(self):
        """
        Stops the motor and set the servo to mid position.
        """
        self.motor.stop()
        self.set_straight()

    def turn(self, left_right):
        """
        Make turns.
        """
        start_speed = self.motor.value
        self.deaccelerate(0.4)
        if left_right == 'left':
            self.servo.max()
        else:
            self.servo.min()
        sleep(1)
        self.accelerate(start_speed)


def demo_right_left(c):
    """Just turns the servo direction from right to left."""
    c.servo.mid()
    sleep(1.5)
    c.turn_right()
    sleep(1.5)
    c.turn_left()


def demo_square(c):
    """Makes the card make a "square" like way."""
    for _ in range(3):
        c.set_straight()
        sleep(1)
        c.accelerate(0.6)
        sleep(1)
        c.turn_right()
        sleep(1)
    c.stop()
    

def main():
    c = Car()
    demo_square(c)

if __name__ == '__main__':
    main()
