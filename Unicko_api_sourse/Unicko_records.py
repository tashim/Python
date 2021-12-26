import time
from datetime import datetime
from unicko_api import UnickoApi
from database import Database
import os
from file import File
from Keywords import downloads_folder, upload_folder, unicko_user


class Download:
    def __init__(self):
        self.api = None
        self.db = None
        self.file = None
        self.downloads_folder = downloads_folder
        self.upload_folder = upload_folder
        self.start_time = 0
        self.course_set = set()

    def run(self):
        self.start_time = time.time()
        self.api = UnickoApi()
        self.db = Database()
        self.file = File()
        self.db.connect()
        self.load_courses_from_db()
        self.download_all_recordings()

    def download_handler(self, recording):
        file_path = self.downloads_folder + "/" + "recording_" + recording["id"] + ".mp4"
        recording_size = recording["file_size"]
        course_name = self.api.get_specific_meeting_name(recording["meeting"])['name']

        # Checking if file has finished downloading
        file_stats = os.stat(file_path)
        if file_stats.st_size != recording_size:
            print("File is corrupted!")
            return
        print("Recording:", recording["id"], "has finished downloading.")

        # Renaming and moving file
        new_file_path = self.file.move_file_to_folder(file_path, recording, course_name, self.upload_folder)
        if new_file_path == '':
            return

        # Getting proper format for db duration
        date, duration = self.file.date_for_db(recording)

        # Inserting file to database
        self.db.insert(unicko_user, recording['meeting'], course_name, date, duration, recording["id"], new_file_path)
        print("Recording inserted to database.",recording['id'])

        # TODO: delete record from Unicko
        # print('delete ',recording['id'])
        # self.api.delete_recording(recording['id'])

    def download_all_recordings(self):
        recordings = self.api.list_all_recordings()
        for recording in recordings:
            # print(recording)
            if not self.db.recording_exists(int(recording["id"])):
                try:
                    self.api.download_recording(recording, self.downloads_folder)
                    # download & insert into DB
                    self.download_handler(recording)
                except KeyError:
                    print("ALl other recording files are still processing.")
            else:
                # TODO:: delete from unicko
                print('delete ', recording['id'])
                self.api.delete_recording(recording['id'])

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(f"All available recordings for today ({dt_string}) have been downloaded!")
        self.update_all_lesson_numbers()

    def load_courses_from_db(self):
        self.course_set.update(self.db.get_course_ids())

    def update_all_lesson_numbers(self):
        for course_id in self.course_set:
            recording_dates = self.db.get_course_recording_dates(course_id)
            recording_times = [(recording_id, self.date_to_time(date)) for recording_id, date in recording_dates]
            recording_times.sort(key=lambda i: i[1])

            lesson_number = 1
            for recording_id, _ in recording_times:
                self.db.update_recording_lesson_number(lesson_number, recording_id)
                lesson_number += 1

    def date_to_time(self, date_string):
        # Getting date from SQL for lessons count.
        time_struct = datetime.strptime(date_string, "%m/%d/%y - %H:%M")
        time_struct = datetime.strftime(time_struct, "%m/%d/%y - %H:%M")
        return time_struct


if __name__ == '__main__':
    download = Download()
    download.run()
