# Import necessary libraries
import cv2  # Library for computer vision tasks
import mediapipe as mp  # Library for applying machine learning models on media data

# Define a function for face detection and landmark mapping
def face_detection_and_mapping(image):
    """
    Detects faces in the provided image and returns the original image with bounding boxes around
    the faces and the cropped faces.

    Args:
        image (numpy.ndarray): The input image in BGR format.

    Returns:
        Tuple[numpy.ndarray, numpy.ndarray]: A tuple containing the original image with bounding boxes around
        the faces and the cropped faces.
    """

    # Initialize MediaPipe Face Detection
    mp_face_detection = mp.solutions.face_detection  # Face detection module
    mp_drawing = mp.solutions.drawing_utils  # Drawing utilities
    face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)  # Face detection model

    # Convert the image to RGB format (required by MediaPipe)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform face detection on the RGB image
    results = face_detection.process(image_rgb)

    # If faces are detected
    if results.detections:
        # Loop through each detected face
        for detection in results.detections:
            # Extract the bounding box coordinates of the detected face
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = image.shape
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

            # Draw a green bounding box around the detected face on the original image
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Crop the detected face from the original image
            cropped_face = image[y:y+h, x:x+w]

            # Convert the cropped face to RGB format for facial landmark detection
            cropped_face_rgb = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB)

            # Initialize MediaPipe Face Mesh for facial landmark detection
            mp_face_mesh = mp.solutions.face_mesh  # Face mesh module
            face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)  # Face mesh model

            # Perform facial landmark detection on the cropped face
            landmarks = face_mesh.process(cropped_face_rgb)
            # If landmarks are detected
            if landmarks.multi_face_landmarks:
                # Loop through each detected face landmarks
                for face_landmarks in landmarks.multi_face_landmarks:
                    # Loop through each landmark point
                    for landmark in face_landmarks.landmark:
                        # Calculate the pixel coordinates of the landmarks relative to the cropped face
                        x_lm, y_lm = int(landmark.x * w), int(landmark.y * h)
                        # Draw blue circles on the cropped face at the locations of the detected landmarks
                        cv2.circle(cropped_face, (x_lm, y_lm), 2, (255, 0, 0), -1)

    # Return the original image with bounding boxes around the faces and the cropped faces
    return image, cropped_face
