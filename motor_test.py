import pygame
import time
import RPi.GPIO as GPIO
import cv2
import numpy as np

# Set up GPIO
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

# Initialize pygame
pygame.init()

# Set up the display (even though we won't show anything on screen)
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Servo Control')

# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 for the default Pi Camera, change it if using a different one

# Load the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Main loop
running = True
try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Quit the program
                    print("Exiting program...")
                    running = False

        # Capture video frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break
        
        # Convert the frame to grayscale (required for face detection)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) > 0:
            # Get the coordinates of the first detected face
            (x, y, w, h) = faces[0]
            # Draw a rectangle around the face (optional, for visualization)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Calculate the center of the face
            face_center_x = x + w / 2
            face_center_y = y + h / 2

            # Assume the screen center is at (200, 150)
            # Adjust the servo position based on the face position
            screen_center_x = 200  # Half of 400px width
            screen_center_y = 150  # Half of 300px height

            # Adjust Servo 1 (horizontal) based on face position
            angle_1 = (face_center_x - screen_center_x) / screen_center_x * 90  # Map to -90 to 90 degrees
            set_servo_angle(servo_1_pwm, 90 - angle_1)  # Servo range from 0 to 180 degrees

            # Adjust Servo 2 (vertical) based on face position
            angle_2 = (face_center_y - screen_center_y) / screen_center_y * 90  # Map to -90 to 90 degrees
            set_servo_angle(servo_2_pwm, 90 - angle_2)  # Servo range from 0 to 180 degrees

        # Display the frame (for debugging, if you want to see it in a window)
        cv2.imshow("Face Detection", frame)

        # Handle the exit key (press 'q' to exit the face detection window)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        pygame.display.update()

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    # Cleanup GPIO and close the camera
    servo_1_pwm.stop()
    servo_2_pwm.stop()
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()
