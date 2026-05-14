import cv2
import time
 
# Конфигурации за двата режима на компресия
# JPG: стандартен формат, широка поддръжка, добро съотношение скорост/качество
# WebP: по-добра компресия (~25-35% по-малък размер от JPG при същото качество)
COMPRESSION_CONFIGS = {
    "high": {
        "jpg_quality": 95,       # Висококачествен JPG — минимални артефакти
        "webp_quality": 90,      # Висококачествен WebP — почти без загуби
        "webp_method": 6         # Най-добра компресия (CPU интензивно)
    },
    "fast": {
        "jpg_quality": 20,       # Нисък JPG — бързо, но видими артефакти
        "webp_quality": 40,      # Нисък WebP — компактен файл, бърза обработка
        "webp_method": 0         # Най-бърза компресия — подходящо за IoT/real-time
    }
}
 
def compress_image(image, mode="high", format="jpg"):
    """
    Compresses an image using the selected mode and format.
 
    Args:
        image: BGR image (OpenCV numpy array)
        mode: "high" (quality) or "fast" (speed/IoT)
        format: "jpg" or "webp"
 
    Returns:
        (encoded_image, duration_seconds)
    """
    start_time = time.perf_counter()
    config = COMPRESSION_CONFIGS.get(mode, COMPRESSION_CONFIGS["high"])
 
    if format == "webp":
        params = [int(cv2.IMWRITE_WEBP_QUALITY), config["webp_quality"]]
    else:
        params = [int(cv2.IMWRITE_JPEG_QUALITY), config["jpg_quality"]]
 
    ext = f".{format}"
    success, encoded_image = cv2.imencode(ext, image, params)
 
    duration = time.perf_counter() - start_time
    return encoded_image, duration
 
def decompress_image(encoded_image):
    """
    Decompresses an image from a buffer.
 
    Returns:
        (decoded_image, duration_seconds)
    """
    start_time = time.perf_counter()
    decoded = cv2.imdecode(encoded_image, cv2.IMREAD_COLOR)
    duration = time.perf_counter() - start_time
    return decoded, duration