from ultralytics import YOLO

# Load YOLO model
yolo = YOLO("../yolo11n.pt")

print("YOLO модель загружена")


def check_image(image):
    results = yolo(image)
    return any(
        cls == 15 and conf > 0.7
        for cls, conf in zip(results[0].boxes.cls, results[0].boxes.conf)
    )
