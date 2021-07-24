import time

import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# For static images:
IMAGE_FILES = []

def capture(video_path):

    cap = cv2.VideoCapture(video_path)
    while True:
        ret, img = cap.read()
        if not ret:
            break
        yield img

    cap.release()

if __name__ == "__main__":
    video_path = "./sample.mp4"

    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:

        for idx, image in enumerate(capture(video_path)):
            time_s = time.time()
            image = cv2.resize(image, None, fx=.5, fy=.5)
            image_height, image_width, _ = image.shape
            # Convert the BGR image to RGB before processing.
            results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            print(time.time() - time_s)
            # continue

            if not results.pose_landmarks:
                continue
            print(
                f'Nose coordinates: ('
                f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width}, '
                f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height})'
            )
            # Draw pose landmarks on the image.
            annotated_image = image.copy()
            mp_drawing.draw_landmarks(
                annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            # cv2.imwrite('./tmp/annotated_image' + str(idx) + '.png', annotated_image)
            concat = cv2.hconcat([cv2.resize(image, None, fx=.5, fy=.5), cv2.resize(annotated_image, None, fx=.5, fy=.5)])
            cv2.imwrite("sample.jpg", concat)
            cv2.imshow("image", cv2.resize(annotated_image, None, fx=.5, fy=.5))
            key = cv2.waitKey(1)
            if key == ord("q"):
                break

            # # Plot pose world landmarks.
            # mp_drawing.plot_landmarks(
            #     results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)