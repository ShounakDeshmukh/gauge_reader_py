import cv2

# Initialize the camera
camera = cv2.VideoCapture(0)  # 0 represents the default camera (usually the built-in webcam)

if not camera.isOpened():
    print("Error: Could not access the camera.")
else:
    while True:
        # Read a frame from the camera
        ret, frame = camera.read()

        if not ret:
            print("Error: Could not capture a frame.")
            break

        # Display the frame in a window
        cv2.imshow("Live Video Stream", frame)

        # Check for the 'q' key to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the OpenCV window
    camera.release()
    cv2.destroyAllWindows()
