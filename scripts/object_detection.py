# scripts/object_detection.py
import os
import pandas as pd
from ultralytics import YOLO
from pathlib import Path

# Load YOLOv8 model (YOLOv8n, YOLOv8s, etc.)
model = YOLO("yolov8n.pt")  # Small and fast. Replace with yolov8s/YOLOv8m if needed.

def run_object_detection(image_dir="data/images", output_csv="detections/predictions.csv"):
    rows = []
    image_dir = Path(image_dir)
    for channel_dir in image_dir.iterdir():
        if channel_dir.is_dir():
            for image_file in channel_dir.glob("*.jpg"):
                try:
                    if os.path.getsize(image_file) == 0:
                        print(f"⚠️ Skipping empty file: {image_file}")
                        continue

                    results = model(image_file)
                    for r in results:
                        for box in r.boxes:
                            cls = int(box.cls[0])
                            conf = float(box.conf[0])
                            label = model.names[cls]
                            message_id = image_file.name.split("_")[1]  # assumes <channel>_<msgid>_<timestamp>.jpg
                            rows.append({
                                "message_id": message_id,
                                "detected_object_class": label,
                                "confidence_score": conf,
                                "channel": channel_dir.name,
                                "image_path": str(image_file)
                            })
                except Exception as e:
                    print(f"❌ Error processing {image_file}: {e}")
                    continue

    os.makedirs("detections", exist_ok=True)
    pd.DataFrame(rows).to_csv(output_csv, index=False)
    print(f"✅ YOLO predictions saved to: {output_csv}")
