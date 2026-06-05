import cv2
import numpy as np
from single_core import process_single
from multi_core  import process_multi

def draw_overlay(frame, label, fps, color):
    """Tambahkan label dan FPS ke frame."""
    h, w = frame.shape[:2]

    # Background semi-transparan
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 60), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    # Teks label
    cv2.putText(frame, label,
                (10, 30), cv2.FONT_HERSHEY_DUPLEX,
                0.9, color, 2, cv2.LINE_AA)

    # Teks FPS
    fps_text = f"FPS: {fps:.1f}"
    cv2.putText(frame, fps_text,
                (10, 55), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 1, cv2.LINE_AA)
    return frame

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("❌ Kamera tidak ditemukan!")
        return

    print("✅ Tekan 'Q' untuk keluar")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Proses kedua pipeline
        left_frame,  fps_single = process_single(frame.copy())
        right_frame, fps_multi  = process_multi(frame.copy())

        # Resize agar sama
        target_h, target_w = frame.shape[:2]
        left_frame  = cv2.resize(left_frame,  (target_w, target_h))
        right_frame = cv2.resize(right_frame, (target_w, target_h))

        # Tambah overlay
        left_frame  = draw_overlay(left_frame,
                                   "SINGLE CORE", fps_single,
                                   (0, 200, 255))   # oranye
        right_frame = draw_overlay(right_frame,
                                   "MULTI CORE (4x)", fps_multi,
                                   (0, 255, 100))   # hijau

        # Garis pemisah
        divider = np.zeros((target_h, 4, 3), dtype=np.uint8)
        divider[:] = (200, 200, 200)

        # Gabung side-by-side
        combined = np.hstack([left_frame, divider, right_frame])

        # Judul atas
        title_bar = np.zeros((40, combined.shape[1], 3), dtype=np.uint8)
        cv2.putText(title_bar,
                    "Parallel Computing Demo — Single vs Multi Core",
                    (20, 28), cv2.FONT_HERSHEY_DUPLEX,
                    0.7, (220, 220, 220), 1, cv2.LINE_AA)
        combined = np.vstack([title_bar, combined])

        cv2.imshow("Parallel Camera", combined)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()