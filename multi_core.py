import time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from processing import full_pipeline

# Pool global agar tidak respawn tiap frame
_executor = None

def get_executor():
    global _executor
    if _executor is None:
        _executor = ProcessPoolExecutor(max_workers=4)
    return _executor

def process_multi(frame):
    """
    Proses 4 region frame secara PARALEL (4 core).
    """
    start = time.perf_counter()

    h, w = frame.shape[:2]
    regions = [
        frame[0:h//2, 0:w//2].copy(),
        frame[0:h//2, w//2:w].copy(),
        frame[h//2:h, 0:w//2].copy(),
        frame[h//2:h, w//2:w].copy(),
    ]

    executor = get_executor()
    futures  = [executor.submit(full_pipeline, r) for r in regions]
    results  = [f.result() for f in futures]

    top    = np.hstack([results[0], results[1]])
    bottom = np.hstack([results[2], results[3]])
    output = np.vstack([top, bottom])

    elapsed = time.perf_counter() - start
    fps = 1.0 / elapsed if elapsed > 0 else 0
    return output, fps