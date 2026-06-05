import time
from processing import full_pipeline

def process_single(frame):
    """
    Proses frame secara sequential (1 core).
    Dibuat 'berat' dengan memproses 4x ukuran berbeda lalu digabung.
    """
    start = time.perf_counter()

    # Simulasi beban: proses 4 region frame secara berurutan
    h, w = frame.shape[:2]
    results = []
    for region in [
        frame[0:h//2, 0:w//2],
        frame[0:h//2, w//2:w],
        frame[h//2:h, 0:w//2],
        frame[h//2:h, w//2:w],
    ]:
        results.append(full_pipeline(region))

    # Gabungkan 4 quadrant
    top    = __import__('numpy').hstack([results[0], results[1]])
    bottom = __import__('numpy').hstack([results[2], results[3]])
    output = __import__('numpy').vstack([top, bottom])

    elapsed = time.perf_counter() - start
    fps = 1.0 / elapsed if elapsed > 0 else 0
    return output, fps