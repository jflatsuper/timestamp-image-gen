import ast
import logging
import os
import cv2
import csv
from app.upload_to_s3 import upload_to_s3
from werkzeug.datastructures import FileStorage


def handle_capture_time(capture_time: str):
    time_in_seconds, capture_time = 0, capture_time.split(".")
    for i in range(len(capture_time)):
        if len(capture_time) - 1 == i and len(capture_time[i]) == 1:
            time_in_seconds += int(f"{capture_time[i]}0")
        else:
            time_in_seconds += int(capture_time[i]) * (
                60 ** (len(capture_time) - i - 1)
            )
    return time_in_seconds


handle_capture_time("17.56")


def video_to_frames(
    video_path,
    dir_name,
    hotspots,
    frame_rate=15,
):
    print(hotspots)
    cap = cv2.VideoCapture(video_path)
    record_name = video_path.split("/")[-1].split("_")[0]
    if not cap.isOpened():
        logging.error(f"Failed to open video: {video_path}")
        return
    for i in hotspots:
        for j in range(0, 60, frame_rate):
            v = i + (j * 0.01)
            print(v)
            cap.set(cv2.CAP_PROP_POS_MSEC, v * 1000)
            ret, frame = cap.read()
            if not ret:
                logging.warning(f"Failed to read frame from  {v} second")
                continue
            image_id = f"{dir_name}_{record_name}_{v}.jpg"
            success, encoded_image = cv2.imencode(".jpg", frame)
            if not success:
                logging.error("Could not encode image")
                continue

            # Convert to bytes
            image_bytes = encoded_image.tobytes()

            try:
                written = upload_to_s3(
                    f"nail/pr_nail_images_{dir_name}/" + image_id, image_bytes
                )
            except Exception as e:
                print(e)

            if not written:
                logging.warning(f"Failed to save frame to bucket")
                continue
    cap.release()


def read_csv_file(file, file_name):
    error_list = []
    logging.info("Video frames extraction completed")
    logging.info(file)
    csvreader = csv.reader(file)
    logging.info(
        "Reading CSV file",
    )
    print(csvreader)
    headers = next(csvreader)
    print(headers)
    dir_name = file_name.split(".")[0]
    csv_arr = []
    for row in csvreader:
        print(row[-1])
        video_path = row[5]
        print(video_path)
        try:
            hotspots = [
                handle_capture_time(str(item))
                for item in ast.literal_eval(row[-1].replace(":", "."))
            ]
            csv_arr.append((video_path, hotspots))
            print(hotspots, video_path)
        except Exception as e:
            error_list.append(row[1])
            print(e)
            continue

    if len(error_list) > 0:
        print("Error list", error_list)
        return error_list

    for x in csv_arr:
        video_to_frames(x[0], dir_name, x[1], frame_rate=60)


def upload_files(files: list[FileStorage], s3_folder=""):

    for file in files:
        print(file)
        file_name = file.filename
        if file_name.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
            local_path = file_name
            print(local_path)

            try:
                written = upload_to_s3(f"blood/5-spot/{file_name}", file)

                print(f"Successfully uploaded {local_path}")
            except FileNotFoundError:
                print(f"The file was not found: {local_path}")
