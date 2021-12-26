import os
from os.path import exists
import shutil
from datetime import datetime
from pathlib import Path

from dateutil.relativedelta import relativedelta


class File:
    def __init__(self): pass

    @staticmethod
    def create_folder(upload_folder):
        Path(upload_folder).mkdir(parents=True, exist_ok=True)

    def move_file_to_folder(self, file_path, recording, course_name, upload_folder) -> str:
        if not exists(file_path):
            print(f"{file_path} does not exist! Maybe the File / Date / Course name in "
                  "Unicko contains illegal characters.")
            return ''

        new_name = File.new_name_for_file(recording, course_name)

        # Create directories
        self.create_folder(upload_folder)
        course_folder = os.path.join(upload_folder, course_name)
        self.create_folder(course_folder)

        # Does a file with the same name already exist in the destination folder?
        new_file_path = os.path.join(course_folder, new_name)
        print(new_file_path)

        # Moving files to new folder
        try:
            shutil.move(file_path, new_file_path)
            return new_file_path
        except shutil.Error as e:   print(e)
        return ''

    @staticmethod
    def new_name_for_file(recording, course_name):
        recording_date = recording['end_time'].split('T')[0]
        recording_date = recording_date.replace('-', '_')
        # String concatenation for name change.
        new_name = recording["id"] + '_' + \
                   course_name + '_' + \
                   recording_date + '.mp4'
        return new_name

    @staticmethod
    def date_for_db(recording):
        recording_date = recording['end_time'].split('T')[0]
        recording_date = recording_date.replace('-', '/')

        recording_hour = recording['end_time'].split('T')
        recording_hour = recording_hour[1].split("Z")

        recording_hour2 = recording['start_time'].split('T')
        recording_hour2 = recording_hour2[1].split("Z")

        recording_date_hour = recording_date + " " + "-" + " " + recording_hour[0]
        date = datetime.strptime(recording_date_hour, "%Y/%m/%d - %H:%M:%S")
        date = datetime.strftime(date, "%m/%d/%y - %H:%M")

        # Calculating duration
        end_time = recording_hour[0]
        start_time = recording_hour2[0]
        start_time = datetime.strptime(start_time, "%H:%M:%S")
        end_time = datetime.strptime(end_time, "%H:%M:%S")
        difference = end_time - start_time
        difference = int(difference.total_seconds() / 60)
        attrs = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']

        human_readable = lambda delta: [
            '%d %s' % (getattr(delta, attr), getattr(delta, attr) > 1 and attr or attr[:-1])
            for attr in attrs if getattr(delta, attr)
        ]

        duration = human_readable(relativedelta(minutes=difference))
        duration = ', '.join(duration)
        return date, duration
