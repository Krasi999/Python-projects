import numpy as np
import psutil
import os
import tracemalloc
from skimage.metrics import structural_similarity as ssim
 
# ──────────────────────────────────────────────
# RAM измерване
# ──────────────────────────────────────────────
 
def get_memory_usage():
    """Returns current RSS RAM usage of the process in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)
 
def measure_peak_memory(func, *args, **kwargs):
    """
    Executes func(*args) and returns (result, peak_RAM_in_KB).
    Uses tracemalloc for accurate peak memory allocation tracking.
    """
    tracemalloc.start()
    result = func(*args, **kwargs)
    _, peak = tracemalloc.get_traced_memory()  # peak в bytes
    tracemalloc.stop()
    return result, peak / 1024  # връщаме в KB
 
# ──────────────────────────────────────────────
# CPU измерване
# ──────────────────────────────────────────────
 
def measure_cpu_during(func, *args, **kwargs):
    """
    Executes func(*args) and returns (result, cpu_percent).
    Calculates CPU load specifically during the operation.
    """
    process = psutil.Process(os.getpid())
    process.cpu_percent(interval=None)   # reset — изчистване на брояча
    result = func(*args, **kwargs)
    cpu = process.cpu_percent(interval=None)  # измерване след операцията
    return result, cpu
 
def calculate_psnr(original, compressed):
    """Calculates Peak Signal-to-Noise Ratio (PSNR) in dB."""
    mse = np.mean((original.astype(np.float64) - compressed.astype(np.float64)) ** 2)
    if mse == 0:
        return 100.0  # Идентични изображения
    return 20 * np.log10(255.0 / np.sqrt(mse))
 
def calculate_ssim(original, compressed):
    """Calculates Structural Similarity Index (SSIM)."""
    return ssim(original, compressed, channel_axis=2, win_size=7)