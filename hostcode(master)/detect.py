import cv2
import numpy as np
import torch
from PIL import Image
from transformers import YolosForObjectDetection, YolosImageProcessor

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = YolosForObjectDetection.from_pretrained('hustvl/yolos-small').to(device)
image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-small")

cap = cv2.VideoCapture("http://<ip-address>:5000/video_feed", cv2.CAP_FFMPEG)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)  # Increase the buffer size to reduce latency

detected_objects = set()

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_AREA)
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    inputs = image_processor(images=image, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}  # Move the inputs tensor to the device
    outputs = model(**inputs)

    logits = outputs.logits
    bboxes = outputs.pred_boxes

    target_sizes = torch.tensor([image.size[::-1]])
    results = image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]
    objects = set([model.config.id2label[label.item()] for label in results["labels"]])
    new_objects = objects.difference(detected_objects)
    detected_objects = detected_objects.union(objects)
    if len(new_objects) > 0:
        print(f"Detected {len(new_objects)} new objects: {', '.join(new_objects)}")

    frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)
    for box in results["boxes"]:
        box = [int(i) for i in box.tolist()]
        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()