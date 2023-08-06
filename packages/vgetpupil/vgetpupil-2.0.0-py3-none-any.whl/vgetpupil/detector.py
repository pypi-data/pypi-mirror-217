import cv2
from pupil_detectors import Detector2D

detector = Detector2D()

input_file = r"C:\Users\zlin341\Documents\GitHub\vgetpupil\pnm_eye_video.mp4"
print("Input file name:", input_file)
# print("Output file name:", output_file)
input_video = cv2.VideoCapture(input_file)
frame_width = input_video.get(cv2.CAP_PROP_FRAME_WIDTH)
print("Input frame width:", frame_width)
frame_height = input_video.get(cv2.CAP_PROP_FRAME_HEIGHT)
print("Input frame height:", frame_height)
frame_rate = input_video.get(cv2.CAP_PROP_FPS)
print("Input frame rate:", frame_rate)
frame_count = input_video.get(cv2.CAP_PROP_FRAME_COUNT)
print("Input frame count:", frame_count)

while True:
    # r_start = time.time()
    ret, frame = input_video.read()
    # r_stop = time.time()
    # print(f"read time {(r_stop - r_start) * 1000}")

    # When there is frame to read
    if ret:
        height, width, channels = frame.shape
        half_width = width // 2

        left_section = frame[:, :half_width]
        right_section = frame[:, half_width:]
        gray = cv2.cvtColor(left_section, cv2.COLOR_BGR2GRAY)
        # d_start = time.time()
        result = detector.detect(gray)
        ellipse = result["ellipse"]
        ellipse_center = tuple(int(v) for v in ellipse["center"])
        ellipse_axis = tuple(int(v / 2) for v in ellipse["axes"])
        ellipse_angle = ellipse["angle"]
        confidence = result['confidence']
        # print(confidence)
        if confidence >= 0.8:
            left_section = cv2.ellipse(
                left_section,
                ellipse_center,
                ellipse_axis,
                ellipse_angle,
                0, 360,
                (0, 0, 255)
            )
        cv2.imshow('Left', left_section)
        cv2.imshow('Right', right_section)

        if cv2.waitKey(1) & 0xFF == 27:
            break
