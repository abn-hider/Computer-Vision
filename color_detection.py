
import cv2
import numpy as np

# تعريف ألوان BGR تقريبة مع اسمائها
colors = {
    "Red": (0,0,255),
    "Green": (0,255,0),
    "Blue": (255,0,0),
    "Yellow": (0,255,255),
    "Orange": (0,165,255),
    "Cyan": (255,255,0),
    "Magenta": (255,0,255),
    "White": (255,255,255),
    "Black": (0,0,0),
    "Gray": (128,128,128)
}

def get_closest_color(bgr):
    min_dist = float('inf')
    closest_color = "Unknown"
    for name, (b,g,r) in colors.items():
        dist = ((b - bgr[0])**2 + (g - bgr[1])**2 + (r - bgr[2])**2)**0.5
        if dist < min_dist:
            min_dist = dist
            closest_color = name
    return closest_color

# رابط كاميرا الهاتف
url = "http://192.168.0.100:8080/video"
cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    if not ret:
        print("لا يوجد فيديو!")
        break

    h, w, _ = frame.shape
    cx, cy, size = w//2, h//2, 30  # حجم مربع صغير في المنتصف
    roi = frame[cy-size:cy+size, cx-size:cx+size]

    # متوسط اللون في المربع
    avg_color = np.mean(roi, axis=(0,1))  # BGR
    color_name = get_closest_color(avg_color)

    # رسم مربع وكتابة اسم اللون
    cv2.rectangle(frame, (cx-size, cy-size), (cx+size, cy+size), (0,0,0), 2)
    cv2.putText(frame, color_name, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

    cv2.imshow("Color Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
