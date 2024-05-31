# app.py
import logging
import os
from flask import Flask, request, render_template

from app.upload_to_s3 import upload_to_s3
from app.read_frames_from_csv import read_csv_file, upload_files

app = Flask(__name__)

# AWS S3 configuration


@app.route("/", methods=["GET", "POST"])
def upload_csv():
    if request.method == "POST":
        if "files[]" not in request.files:
            return redirect(request.url)

        files = request.files.getlist("files[]")
        upload_files(files)

        return render_template("dir_upload.html")
    return render_template("dir_upload.html")


# def upload_csv():
#     if request.method == "POST":
#         # Check if the post request has the file part
#         if "file" not in request.files:
#             return render_template("index.html", message="No file part")

#         file = request.files["file"]

#         # If user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == "":
#             return render_template("index.html", message="No selected file")

#         if file:
#             # Read CSV data
#             csv_data = file.stream.read().decode("utf-8")

#             # Process CSV data (Here you can add your processing logic)

#             # Upload processed data to S3
#             logging.info("Uploading file to S3", file)

#             value = read_csv_file(csv_data.splitlines(), file.filename)
#             print(len(value))
#             if value:
#                 return render_template("index.html", message=value)
#             if upload_to_s3("quantisal/quantisal_csv/" + file.filename, csv_data):
#                 return render_template(
#                     "index.html", message="File uploaded successfully"
#                 )
#             else:
#                 return render_template(
#                     "index.html", message="Failed to upload file to S3"
#                 )

#     return render_template("index.html")


# if __name__ == "__main__":
#     app.run(debug=True)
