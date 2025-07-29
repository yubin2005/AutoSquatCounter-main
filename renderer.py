import cv2
from config import FONT_SCALE, FONT_THICKNESS, CARD_COLOR, SHADOW_COLOR, STATE_DELAY

def draw_rounded_rect(img, pt1, pt2, color, radius, thickness=-1):
    x1, y1 = pt1; x2, y2 = pt2
    cv2.rectangle(img, (x1+radius, y1), (x2-radius, y2), color, thickness)
    cv2.rectangle(img, (x1, y1+radius), (x2, y2-radius), color, thickness)
    for dx in (radius, x2-radius):
        for dy in (radius, y2-radius):
            cv2.circle(img, (dx, dy), radius, color, thickness)

def draw_hud(frame, rep_count, angle_text):
    # shadow
    shadow = frame.copy()
    draw_rounded_rect(shadow, (8,8), (403,203), SHADOW_COLOR, 20)
    shadow = cv2.GaussianBlur(shadow, (21,21), 0)
    cv2.addWeighted(shadow, 0.5, frame, 0.5, 0, frame)
    # card
    overlay = frame.copy()
    draw_rounded_rect(overlay, (5,5), (400,200), CARD_COLOR, 20)
    cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
    # text
    cv2.putText(frame, f"Reps: {rep_count}", (15,65),
                cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, (255,255,255), FONT_THICKNESS)
    cv2.putText(frame, f"Angle: {angle_text}", (15,125),
                cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, (255,255,255), FONT_THICKNESS)

def draw_feedback(frame, angle):
    # Real Time Feedbacks
    if angle > 170:
        fb = "Good extension!"
    elif angle < 90:
        fb = "Good depth!"
    else:
        fb = "Keep going"
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale, thick = FONT_SCALE, FONT_THICKNESS
    (w,h), _ = cv2.getTextSize(fb, font, scale, thick)
    max_w = 380
    while w > max_w and scale > 0.5:
        scale *= 0.9
        (w,h), _ = cv2.getTextSize(fb, font, scale, thick)
    pos = (10,185)
    # outline
    cv2.putText(frame, fb, pos, font, scale, (0,0,0), thick+2, cv2.LINE_AA)
    cv2.putText(frame, fb, pos, font, scale, (255,255,255), thick, cv2.LINE_AA)
