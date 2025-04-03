import cv2
from picamera2 import Picamera2

# Initialize the camera using picamera2
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))  # Set resolution to 640x480
picam2.start()

# Load the Haar Cascade for face detection from OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start capturing frames
try:
    while True:
        # Capture a frame from the camera
        frame = picam2.capture_array()

        # Convert the frame to grayscale (necessary for face detection)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Display the frame with faces highlighted
        cv2.imshow("Facial Recognition", frame)

        # Wait for the 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    # Clean up and close the camera
    picam2.stop()
    cv2.destroyAllWindows()
