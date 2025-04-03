import RPi.GPIO as GPIO
import time
import keyboard

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define the GPIO pins for the servo motors
servo_1_pin = 17
servo_2_pin = 12

# Set up the GPIO pins as outputs
GPIO.setup(servo_1_pin, GPIO.OUT)
GPIO.setup(servo_2_pin, GPIO.OUT)

# Set up PWM for the servos with a frequency of 50 Hz (standard for servos)
servo_1_pwm = GPIO.PWM(servo_1_pin, 50)
servo_2_pwm = GPIO.PWM(servo_2_pin, 50)

# Start the PWM on both servos with a duty cycle of 0 (this ensures they are in their neutral position)
servo_1_pwm.start(0)
servo_2_pwm.start(0)

# Function to set the servo angle
def set_servo_angle(servo_pwm, angle):
    # Map the angle to a PWM duty cycle
    duty_cycle = (angle / 18) + 2
    servo_pwm.ChangeDutyCycle(duty_cycle)

# Function to stop PWM signals and clean up GPIO
def cleanup():
    servo_1_pwm.stop()
    servo_2_pwm.stop()
    GPIO.cleanup()

# Main loop for testing the servos with keybinds
try:
    print("Press 'w' to rotate Servo 1 up, 's' to rotate Servo 1 down")
    print("Press 'a' to rotate Servo 2 up, 'd' to rotate Servo 2 down")
    print("Press 'q' to quit.")
    
    while True:
        if keyboard.is_pressed('w'):  # Rotate Servo 1 up
            print("Rotating Servo 1 up")
            set_servo_angle(servo_1_pwm, 90)  # Rotate 90 degrees
            time.sleep(0.5)
        elif keyboard.is_pressed('s'):  # Rotate Servo 1 down
            print("Rotating Servo 1 down")
            set_servo_angle(servo_1_pwm, 0)  # Rotate 0 degrees (down)
            time.sleep(0.5)
        elif keyboard.is_pressed('a'):  # Rotate Servo 2 up
            print("Rotating Servo 2 up")
            set_servo_angle(servo_2_pwm, 90)  # Rotate 90 degrees
            time.sleep(0.5)
        elif keyboard.is_pressed('d'):  # Rotate Servo 2 down
            print("Rotating Servo 2 down")
            set_servo_angle(servo_2_pwm, 0)  # Rotate 0 degrees (down)
            time.sleep(0.5)
        elif keyboard.is_pressed('q'):  # Quit the program
            print("Exiting program...")
            break

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    cleanup()
