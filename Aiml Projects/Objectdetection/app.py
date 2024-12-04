import cv2
import numpy as np

# Load the pre-trained MobileNet-SSD model and the class labels
net = cv2.dnn.readNetFromCaffe('E:\Projects\Objectdetection\deploy.prototxt', 'E:\Projects\Objectdetection\mobilenet_iter_73000.caffemodel')
classes = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", 
           "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", 
           "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

# Load the input image
image = cv2.imread('E:\Projects\Objectdetection\project.jpg')  # Replace with your image file
(h, w) = image.shape[:2]

# Prepare the image for the model (resize to 300x300 pixels and mean subtraction)
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

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

        # Draw the prediction on the image
        label = "{}: {:.2f}%".format(classes[idx], confidence * 100)
        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
        y = startY - 15 if startY - 15 > 15 else startY + 15
        cv2.putText(image, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Show the output image with detected objects
cv2.imshow("Output", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
