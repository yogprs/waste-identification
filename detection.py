import cv2
import torch
import numpy as np
import tensorflow as tf

# Load model SEKALI
model_yolo = torch.hub.load(
    'ultralytics/yolov5',
    'yolov5n',
    pretrained=True,
    trust_repo=True
)

model_yolo.classes = [39, 41, 44, 46, 47]
model_yolo.conf = 0.3
model_yolo.max_det = 2

model_cls = tf.keras.models.load_model("model/trash_model.h5")

CLASS_NAMES = ["Non-Organik", "Organik"]
IMG_SIZE = 224
CONF_THRESHOLD = 0.6

def detect_trash(frame):
    results = model_yolo(frame)
    detections = results.xyxy[0]

    label = "Tidak Ada Deteksi"

    if len(detections) > 0:
        detections = detections[detections[:, 4].argsort(descending=True)]

    for det in detections[:2]:  # batasi langsung
        x1, y1, x2, y2, conf, cls = det
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        crop = frame[y1:y2, x1:x2]
        if crop.size == 0:
            continue

        img = cv2.resize(crop, (IMG_SIZE, IMG_SIZE))
        img = img / 255.0
        img = np.expand_dims(img, axis=0)

        prediction = model_cls.predict(img, verbose=0)[0]
        idx = np.argmax(prediction)
        conf_model = prediction[idx]

        if conf_model >= CONF_THRESHOLD:
            label = f"{CLASS_NAMES[idx]} ({conf_model*100:.1f}%)"
            color = (0,255,0)
        else:
            label = "Tidak Yakin"
            color = (0,255,255)

        cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)
        cv2.putText(frame, label, (x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    return frame, label