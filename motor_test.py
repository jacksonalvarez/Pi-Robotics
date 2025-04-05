import pygame
import time
import RPi.GPIO as GPIO

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define the GPIO pins for the servo motors
servo_1_pin = 23  # Changed to GPIO 13 for left-right movement
servo_2_pin = 12  # Kept the same as in original code
servo_3_pin = 17  # Using the original servo_1_pin for the third motor

# Set up the GPIO pins as outputs
GPIO.setup(servo_1_pin, GPIO.OUT)
GPIO.setup(servo_2_pin, GPIO.OUT)
GPIO.setup(servo_3_pin, GPIO.OUT)

# Set up PWM for the servos with a frequency of 50 Hz (standard for servos)
servo_1_pwm = GPIO.PWM(servo_1_pin, 50)
servo_2_pwm = GPIO.PWM(servo_2_pin, 50)
servo_3_pwm = GPIO.PWM(servo_3_pin, 50)

# Start the PWM on all servos with a duty cycle that corresponds to middle position
servo_1_pwm.start(7.5)  # 7.5% duty cycle typically corresponds to 90 degrees (middle)
servo_2_pwm.start(7.5)
servo_3_pwm.start(7.5)

# Current position of each servo (in degrees, 0-180)
servo_positions = {
    1: 90,  # Start in middle position
    2: 90,
    3: 90
}

# Step size for smooth movement (smaller steps make smoother movement)
STEP_SIZE = 2  # Degrees per step

# Function to smoothly set the servo angle
def set_servo_angle(servo_pwm, servo_num, target_angle):
    # Ensure angle is within bounds
    target_angle = max(0, min(180, target_angle))
    
    # Get current position
    current_angle = servo_positions[servo_num]
    
    # Move in small steps to reduce glitching
    if current_angle != target_angle:
        if current_angle < target_angle:
            for angle in range(current_angle, target_angle + 1, STEP_SIZE):
                duty_cycle = (angle / 18) + 2
                servo_pwm.ChangeDutyCycle(duty_cycle)
                time.sleep(0.01)  # Short delay between steps
        else:
            for angle in range(current_angle, target_angle - 1, -STEP_SIZE):
                duty_cycle = (angle / 18) + 2
                servo_pwm.ChangeDutyCycle(duty_cycle)
                time.sleep(0.01)  # Short delay between steps
        
        # Update the current position
        servo_positions[servo_num] = target_angle
        
        # Turn off PWM after movement to reduce jitter
        time.sleep(0.1)
        servo_pwm.ChangeDutyCycle(0)

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Three Servo Control')

# Define font for displaying servo positions
font = pygame.font.Font(None, 36)

# Key mappings for the servos
key_mappings = {
    # Motor 1 (left-right) controls - A/D keys
    pygame.K_a: (1, -10),  # Servo 1, decrease angle
    pygame.K_d: (1, 10),   # Servo 1, increase angle
    
    # Motor 2 controls - W/S keys
    pygame.K_w: (2, 10),   # Servo 2, increase angle
    pygame.K_s: (2, -10),  # Servo 2, decrease angle
    
    # Motor 3 controls - Q/E keys
    pygame.K_q: (3, -10),  # Servo 3, decrease angle
    pygame.K_e: (3, 10)    # Servo 3, increase angle
}

# Main loop
running = True
try:
    while running:
        # Fill screen with a light gray color
        screen.fill((200, 200, 200))
        
        # Display current servo positions
        position_text = f"Servo 1: {servo_positions[1]}°  Servo 2: {servo_positions[2]}°  Servo 3: {servo_positions[3]}°"
        text_surface = font.render(position_text, True, (0, 0, 0))
        screen.blit(text_surface, (10, 20))
        
        # Display controls
        controls_text = "Controls: A/D (Servo 1), W/S (Servo 2), Q/E (Servo 3), ESC (Quit)"
        controls_surface = font.render(controls_text, True, (0, 0, 0))
        screen.blit(controls_surface, (10, 60))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC key to quit
                    print("Exiting program...")
                    running = False
                elif event.key in key_mappings:
                    servo_num, change = key_mappings[event.key]
                    new_angle = servo_positions[servo_num] + change
                    new_angle = max(0, min(180, new_angle))  # Ensure angle stays within bounds
                    
                    # Map to the correct servo PWM
                    if servo_num == 1:
                        print(f"Moving Servo 1 to {new_angle}°")
                        set_servo_angle(servo_1_pwm, 1, new_angle)
                    elif servo_num == 2:
                        print(f"Moving Servo 2 to {new_angle}°")
                        set_servo_angle(servo_2_pwm, 2, new_angle)
                    elif servo_num == 3:
                        print(f"Moving Servo 3 to {new_angle}°")
                        set_servo_angle(servo_3_pwm, 3, new_angle)
                    
        pygame.display.update()
        time.sleep(0.01)  # Small delay to prevent CPU hogging
        
except KeyboardInterrupt:
    print("Program interrupted")
finally:
    # Move servos to neutral position before cleanup
    for pwm, servo_num in [(servo_1_pwm, 1), (servo_2_pwm, 2), (servo_3_pwm, 3)]:
        set_servo_angle(pwm, servo_num, 90)
    
    time.sleep(0.5)
    
    # Cleanup
    servo_1_pwm.stop()
    servo_2_pwm.stop()
    servo_3_pwm.stop()
    GPIO.cleanup()
    pygame.quit()
