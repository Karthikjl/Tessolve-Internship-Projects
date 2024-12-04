import cv2
import numpy as np

# Load the pre-trained MobileNet-SSD model and the class labels
net = cv2.dnn.readNetFromCaffe('E:/Projects/Objectdetection/deploy.prototxt', 'E:/Projects/Objectdetection/mobilenet_iter_73000.caffemodel')
classes = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", 
           "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", 
           "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

# Initialize the video capture object for the inbuilt camera (usually device index 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Process video frames from the camera
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image.")
        break

    # Get the dimensions of the frame
    (h, w) = frame.shape[:2]

    # Prepare the frame for the model (resize to 300x300 pixels and mean subtraction)
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

    # Set the input to the pre-trained deep learning network and perform inference
    net.setInput(blob)
    detections = net.forward()

    # Loop over the detections
    for i in range(detections.shape[2]):
        # Extract the confidence (i.e., probability) associated with the prediction
        confidence = detections[0, 0, i, 2]

        # Filter out weak detections by ensuring the `confidence` is greater than a minimum threshold
        if confidence > 0.2:  # Adjust the threshold as needed
            # Extract the index of the class label from the `detections`, then compute
            # the (x, y)-coordinates of the bounding box for the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # Draw the prediction on the frame
            label = "{}: {:.2f}%".format(classes[idx], confidence * 100)
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show the output frame with detected objects
    cv2.imshow("Object Detection", frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
