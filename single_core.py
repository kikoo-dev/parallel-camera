import time
import numpy as np
from processing import full_pipeline

def process_single(frame):
    """
    Proses frame secara sequential (1 core).
    Dibuat 'berat' dengan memproses 4x ukuran berbeda lalu digabung.
    """
    start = time.perf_counter()

    # Simulasi beban: proses 4 region frame secara berurutan
    h, w = frame.shape[:2]
    h4 = h // 4
    results = []
    for region in [
        frame[0:h4, :],
        frame[h4:2*h4, :],
        frame[2*h4:3*h4, :],
        frame[3*h4:h, :],
    ]:
        results.append(full_pipeline(region))

    output = np.vstack(results)

    elapsed = time.perf_counter() - start
    fps = 1.0 / elapsed if elapsed > 0 else 0
    return output, fps