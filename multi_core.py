import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from processing import full_pipeline

_executor = None

def get_executor():
    global _executor
    if _executor is None:
        _executor = ThreadPoolExecutor(max_workers=4)
    return _executor

def process_multi(frame):
    start = time.perf_counter()

    h, w = frame.shape[:2]
    h4 = h // 4
    regions = [
        frame[0:h4, :],
        frame[h4:2*h4, :],
        frame[2*h4:3*h4, :],
        frame[3*h4:h, :],
    ]

    executor = get_executor()
    futures  = [executor.submit(full_pipeline, r) for r in regions]
    results  = [f.result() for f in futures]

    output = np.vstack(results)

    elapsed = time.perf_counter() - start
    fps = 1.0 / elapsed if elapsed > 0 else 0
    return output, fps
