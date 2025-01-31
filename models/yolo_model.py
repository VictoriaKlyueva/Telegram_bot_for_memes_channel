from ultralytics import YOLO

# Load YOLO model
yolo = YOLO("../yolo11n.pt")

print("YOLO модель загружена")


def check_image(image):
    results = yolo(image)

    classes = results[0].boxes.cls
    confidences = results[0].boxes.conf

    cls_15_count = sum(1 for cls in classes if cls == 15)

    has_cls_15 = any(
        cls == 15 and conf > 0.5
        for cls, conf in zip(classes, confidences)
    )

    return has_cls_15 and cls_15_count <= 3
