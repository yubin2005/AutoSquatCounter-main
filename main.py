import argparse, time, csv, logging
import cv2
import mediapipe as mp

from config        import *
from utils         import compute_angle, rotate_frame, select_backend
from renderer      import draw_hud, draw_feedback
from counter       import SquatCounter

# logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--source', default=DEFAULT_SOURCE)
    p.add_argument('--rotate', choices=['none','cw','ccw','180'], default=DEFAULT_ROTATE)
    p.add_argument('--scale', type=float, default=DEFAULT_SCALE)
    p.add_argument('--output', default=DEFAULT_OUTPUT)
    p.add_argument('--fps',    type=float, default=DEFAULT_FPS)
    p.add_argument('--csv',    default=DEFAULT_CSV)
    return p.parse_args()

def main():
    args = parse_args()
    cap = cv2.VideoCapture(int(args.source) if str(args.source).isdigit() else args.source,
                           select_backend())
    if not cap.isOpened():
        logger.error(f"Cannot open source {args.source}"); return

    # get frame size
    ok, frame = cap.read()
    if not ok: logger.error("No frame"); return
    frame = rotate_frame(frame, args.rotate)
    h,w = frame.shape[:2]
    cv2.namedWindow('Squat Counter', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Squat Counter', w, h)
    writer = cv2.VideoWriter(args.output,
                             cv2.VideoWriter_fourcc(*'mp4v'),
                             args.fps, (w,h))

    pose = mp.solutions.pose.Pose(model_complexity=0,
                                  smooth_landmarks=True,
                                  min_detection_confidence=0.5,
                                  min_tracking_confidence=0.5)

    left_idxs  = (mp.solutions.pose.PoseLandmark.LEFT_HIP,
                  mp.solutions.pose.PoseLandmark.LEFT_KNEE,
                  mp.solutions.pose.PoseLandmark.LEFT_ANKLE)
    right_idxs = (mp.solutions.pose.PoseLandmark.RIGHT_HIP,
                  mp.solutions.pose.PoseLandmark.RIGHT_KNEE,
                  mp.solutions.pose.PoseLandmark.RIGHT_ANKLE)

    counter = SquatCounter()
    prev_ang = None
    paused = False
    frame_idx = 0
    t0 = time.time()

    with open(args.csv, 'w', newline='') as f:
        writer_csv = csv.writer(f)
        writer_csv.writerow(['timestamp','frame_idx','rep_count','angle'])

        while True:
            ret, frame = cap.read()
            if not ret: break
            frame = rotate_frame(frame, args.rotate)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('p'):
                paused = not paused; logger.info('Paused' if paused else 'Resumed')
            if key == ord('r'):
                counter = SquatCounter(); logger.info('Reset')
            if paused:
                disp = cv2.resize(frame, None, fx=args.scale, fy=args.scale)
                cv2.imshow('Squat Counter', disp)
                continue

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res = pose.process(rgb)
            angle_text = 'N/A'

            if res.pose_landmarks:
                lm = res.pose_landmarks.landmark
                angles = []
                for idxs in (left_idxs, right_idxs):
                    if all(lm[i].visibility > VISIBILITY_TH for i in idxs):
                        pts = [(int(lm[i].x*w), int(lm[i].y*h)) for i in idxs]
                        angles.append(compute_angle(*pts))

                if angles:
                    raw = sum(angles)/len(angles)
                    ang = raw if prev_ang is None else (SMOOTH_ALPHA*raw + (1-SMOOTH_ALPHA)*prev_ang)
                    prev_ang = ang
                    angle_text = f"{ang:.1f}"
                    if counter.update(ang):
                        logger.info(f"Rep {counter.rep_count} @ {ang:.1f}°")

                mp.solutions.drawing_utils.draw_landmarks(frame, res.pose_landmarks,
                                                          mp.solutions.pose.POSE_CONNECTIONS)

            draw_hud(frame, counter.rep_count, angle_text)
            try:
                a = float(angle_text)
                draw_feedback(frame, a)
            except:
                pass

            # write out
            ts = time.time()-t0
            writer.write(frame)
            writer_csv.writerow([f"{ts:.2f}", frame_idx,
                                 counter.rep_count, angle_text])
            frame_idx += 1

            disp = cv2.resize(frame, None, fx=args.scale, fy=args.scale)
            cv2.imshow('Squat Counter', disp)
            if key == ord('q'): break

    cap.release()
    writer.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()