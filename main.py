import cv2
from core.hand_tracker import HandTracker
from core.drawing_engine import DrawingEngine
from core.gestures import is_inside, is_draw_gesture, is_stop_gesture
import numpy as np

cap = cv2.VideoCapture(0)
w, h = 1280, 720
cap.set(3, w)
cap.set(4, h)

tracker = HandTracker()
engine = DrawingEngine(w, h)

# ---- UI CONFIG ----
btn_width, btn_height = 100, 60
gap = 25
corner_radius = 30  # more rounded pill-like
hover_thickness = 4


# Draw a pill-shaped rounded rectangle
def pill_rect(img, top_left, bottom_right, color, alpha=0.5, radius=30, border_color=(255, 255, 255), thickness=2):
    x1, y1 = top_left
    x2, y2 = bottom_right
    overlay = img.copy()

    # Central rectangle
    cv2.rectangle(overlay, (x1 + radius, y1), (x2 - radius, y2), color, -1)
    cv2.rectangle(overlay, (x1, y1 + radius), (x2, y2 - radius), color, -1)

    # Rounded corners
    cv2.ellipse(overlay, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, -1)
    cv2.ellipse(overlay, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, -1)
    cv2.ellipse(overlay, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, -1)
    cv2.ellipse(overlay, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, -1)

    # Border
    overlay = round_rect_border(overlay, (x1, y1), (x2, y2), border_color, radius, thickness)

    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
    return img


def round_rect_border(img, top_left, bottom_right, color, radius=30, thickness=2):
    x1, y1 = top_left
    x2, y2 = bottom_right
    cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y2), color, thickness)
    cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), color, thickness)
    cv2.ellipse(img, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, thickness)
    cv2.ellipse(img, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, thickness)
    cv2.ellipse(img, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, thickness)
    cv2.ellipse(img, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, thickness)
    return img


# ---------------- UI BUTTONS ----------------

# Colors
color_buttons = ["red", "blue", "green", "yellow", "cyan", "magenta", "orange", "pink"]
y_colors = h - 250
n_colors = len(color_buttons)
total_width_colors = n_colors * btn_width + (n_colors - 1) * gap
start_x_colors = (w - total_width_colors) // 2

buttons = {}
for i, name in enumerate(color_buttons):
    x1 = start_x_colors + i * (btn_width + gap)
    y1 = y_colors
    x2 = x1 + btn_width
    y2 = y1 + btn_height
    buttons[name] = (x1, y1, x2, y2)

# Brush sizes
brush_buttons = ["thin", "thick"]
y_brush = y_colors + btn_height + gap
total_width_brush = len(brush_buttons) * btn_width + gap
start_x_brush = (w - total_width_brush) // 2
for i, name in enumerate(brush_buttons):
    x1 = start_x_brush + i * (btn_width + gap)
    y1 = y_brush
    x2 = x1 + btn_width
    y2 = y1 + btn_height
    buttons[name] = (x1, y1, x2, y2)

# Eraser & Clear
special_buttons = ["eraser", "clear"]
btn_special_width = 90
btn_special_height = 60
y_special = y_brush + btn_height + gap
total_width_special = len(special_buttons) * btn_special_width + gap
start_x_special = (w - total_width_special) // 2
for i, name in enumerate(special_buttons):
    x1 = start_x_special + i * (btn_special_width + gap)
    y1 = y_special
    x2 = x1 + btn_special_width
    y2 = y1 + btn_special_height
    buttons[name] = (x1, y1, x2, y2)

# Button colors
button_colors = {
    "red": (0, 0, 255),
    "blue": (255, 0, 0),
    "green": (0, 255, 0),
    "yellow": (0, 255, 255),
    "cyan": (255, 255, 0),
    "magenta": (255, 0, 255),
    "orange": (0, 165, 255),
    "pink": (203, 192, 255),
    "thin": (200, 200, 200),
    "thick": (120, 120, 120),
    "eraser": (60, 60, 60),
    "clear": (0, 0, 200)
}

current_color = (255, 0, 255)
thickness = 5

# ---------------- MAIN LOOP ----------------
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    overlay = frame.copy()

    index_pos, lm_list = tracker.process(frame, draw=True)

    # Draw buttons
    for name, (x1, y1, x2, y2) in buttons.items():
        color = button_colors.get(name, (180, 180, 180))
        overlay = pill_rect(overlay, (x1, y1), (x2, y2), color, alpha=0.6, radius=corner_radius)

        # Shadowed text
        text_size = cv2.getTextSize(name.upper(), cv2.FONT_HERSHEY_DUPLEX, 0.6, 2)[0]
        text_x = x1 + (x2 - x1 - text_size[0]) // 2
        text_y = y1 + (y2 - y1 + text_size[1]) // 2
        cv2.putText(overlay, name.upper(), (text_x + 1, text_y + 1), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 3)
        cv2.putText(overlay, name.upper(), (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 2)

        # Hover highlight
        if index_pos and is_inside(index_pos[0], index_pos[1], (x1, y1, x2, y2)):
            overlay = pill_rect(overlay, (x1, y1), (x2, y2), (0, 255, 0), alpha=0.3, radius=corner_radius,
                                border_color=(0, 255, 0), thickness=hover_thickness)

    frame = cv2.addWeighted(overlay, 0.7, frame, 0.3, 0)

    # Draw fingertip dot smaller
    if index_pos:
        x, y = index_pos
        cv2.circle(frame, (x, y), 6, (0, 255, 0), -1)

        # Button interactions
        for name, box in buttons.items():
            if is_inside(x, y, box):
                if name in button_colors and name not in ["eraser", "clear", "thin", "thick"]:
                    current_color = button_colors[name]
                elif name == "thin":
                    thickness = 3
                elif name == "thick":
                    thickness = 10
                elif name == "eraser":
                    current_color = (0, 0, 0)
                    thickness = 30
                elif name == "clear":
                    engine.clear()

        # Gestures
        if is_draw_gesture(lm_list):
            if current_color == (0, 0, 0):
                engine.erase((x, y), size=thickness)
            else:
                engine.draw((x, y), color=current_color, thickness=thickness)
        elif is_stop_gesture(lm_list):
            engine.reset_prev()
    else:
        engine.reset_prev()

    merged = cv2.addWeighted(frame, 0.7, engine.canvas, 0.3, 0)
    cv2.imshow("Virtual Pen AI", merged)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
