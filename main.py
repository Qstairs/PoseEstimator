import os
import time
import csv

import numpy as np
import cv2
import mediapipe as mp

from draw.draw_world_landmarks import plot_landmarks

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# For static images:
IMAGE_FILES = []

def capture(video_path, mask_path=None):
    mask = None
    if mask_path is not None:
        mask = cv2.imread(mask_path)

    cap = cv2.VideoCapture(video_path)
    while True:
        ret, img = cap.read()
        if not ret:
            break

        if mask is not None:
            img = cv2.bitwise_and(img, mask)
            
        yield img

    cap.release()

def output_landmark_to_csv(pose_landmarks, size, writer, correct_aspect=False):
    pose_landmarks = [[lmk.x, lmk.y, lmk.z] for lmk in pose_landmarks.landmark]

    # Map pose landmarks from [0, 1] range to absolute coordinates to get
    # correct aspect ratio.
    if correct_aspect:
        frame_height, frame_width = size
        pose_landmarks *= np.array([frame_width, frame_height, frame_width])

    # Write pose sample to CSV.
    pose_landmarks = np.around(pose_landmarks, 5).flatten().astype(np.str).tolist()
    writer.writerow([idx] + pose_landmarks)

if __name__ == "__main__":
    # video_path = "./sample.mp4"
    video_path = "./videos/home1.mp4"
    # mask_path = "./masks/walking_3.png"
    mask_path = None

    output_folder = os.path.join("outputs", os.path.basename(video_path).split(".")[0])
    os.makedirs(output_folder, exist_ok=True)

    csv_out_path = os.path.join("outputs", os.path.basename(video_path).split(".")[0]+".csv")
    csv_out_file = open(csv_out_path, 'w')
    csv_out_writer = csv.writer(csv_out_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    csv_world_out_path = os.path.join("outputs", os.path.basename(video_path).split(".")[0]+"_world.csv")
    csv_world_out_file = open(csv_world_out_path, 'w')
    csv_world_out_writer = csv.writer(csv_world_out_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:

        for idx, image in enumerate(capture(video_path, mask_path=mask_path)):
            time_s = time.time()
            image = cv2.resize(image, None, fx=.5, fy=.5)
            image_height, image_width, _ = image.shape
            # Convert the BGR image to RGB before processing.
            results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            print(time.time() - time_s)
            # continue

            if not results.pose_landmarks:
                concat = cv2.hconcat([cv2.resize(image, None, fx=.5, fy=.5), cv2.resize(image, None, fx=.5, fy=.5)])
                cv2.imwrite(os.path.join(output_folder, f"{idx:08d}.jpg"), concat)
                continue
            print(
                f'Nose coordinates: ('
                f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width}, '
                f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height})'
            )
            # Draw pose landmarks on the image.
            annotated_image = image.copy()
            mp_drawing.draw_landmarks(
                annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            # cv2.imwrite('./tmp/annotated_image' + str(idx) + '.png', annotated_image)
            concat = cv2.hconcat([cv2.resize(image, None, fx=.5, fy=.5), cv2.resize(annotated_image, None, fx=.5, fy=.5)])
            cv2.imwrite(os.path.join(output_folder, f"{idx:08d}.jpg"), concat)
            # cv2.imshow("image", cv2.resize(annotated_image, None, fx=.5, fy=.5))
            # key = cv2.waitKey(1)
            # if key == ord("q"):
            #     break

            # # Plot pose world landmarks.
            # mp_drawing.plot_landmarks(
            dst_path = os.path.join(output_folder, f"{idx:08d}.html")
            plot_landmarks(
                dst_path, results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

            output_landmark_to_csv(results.pose_landmarks, image.shape[:2], csv_out_writer, correct_aspect=True)
            output_landmark_to_csv(results.pose_world_landmarks, image.shape[:2], csv_world_out_writer)

    csv_out_file.close()
    csv_world_out_file.close()