import cv2
import numpy as np
from single_core import process_single
from multi_core  import process_multi

def draw_overlay(frame, label, fps, color):
    h, w = frame.shape[:2]
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 60), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.9, color, 2, cv2.LINE_AA)
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
    return frame

def make_test_pattern(h, w):
    xv, yv = np.meshgrid(np.arange(w), np.arange(h))
    r = 128 + 127 * np.sin(xv / 50)
    g = 128 + 127 * np.sin(yv / 50)
    b = 128 + 127 * np.sin((xv + yv) / 50)
    return np.stack([r, g, b], axis=2).astype(np.uint8)

def main():
    print("Membuka kamera...", flush=True)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    use_camera = cap.isOpened()
    if use_camera:
        print(f"Kamera OK: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}", flush=True)
    else:
        print("Kamera tidak ditemukan, pakai test pattern", flush=True)

    print("Tekan 'Q' untuk keluar", flush=True)

    test_pattern = make_test_pattern(480, 640)
    frame_count = 0

    while True:
        if use_camera:
            ret, frame_read = cap.read()
            if not ret or frame_read is None:
                break
            frame = frame_read
        else:
            frame = test_pattern.copy()

        frame_count += 1

        try:
            left_frame,  fps_single = process_single(frame.copy())
            right_frame, fps_multi  = process_multi(frame.copy())
        except Exception as e:
            import traceback
            print(f"Error: {e}", flush=True)
            traceback.print_exc()
            continue

        if frame_count <= 3:
            print(f"Frame {frame_count} - single FPS: {fps_single:.1f}, multi FPS: {fps_multi:.1f}", flush=True)

        target_h, target_w = frame.shape[:2]
        left_frame  = cv2.resize(left_frame,  (target_w, target_h))
        right_frame = cv2.resize(right_frame, (target_w, target_h))

        left_frame  = draw_overlay(left_frame, "SINGLE CORE", fps_single, (0, 200, 255))
        right_frame = draw_overlay(right_frame, "MULTI CORE (4x)", fps_multi, (0, 255, 100))

        combined = np.hstack([
            left_frame,
            np.full((target_h, 4, 3), (200, 200, 200), dtype=np.uint8),
            right_frame
        ])

        title_bar = np.zeros((40, combined.shape[1], 3), dtype=np.uint8)
        cv2.putText(title_bar, "Parallel Computing Demo -- Single vs Multi Core",
                    (20, 28), cv2.FONT_HERSHEY_DUPLEX, 0.7, (220, 220, 220), 1, cv2.LINE_AA)
        combined_v = np.vstack([title_bar, combined])

        cv2.imshow("Parallel Camera", combined_v)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if use_camera:
        cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
