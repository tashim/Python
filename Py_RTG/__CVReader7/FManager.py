"""Function to parse the right document type
    and convert it to a readable list to work with the text"""
import os
import re
from pathlib import Path
# Imports
from subprocess import Popen, PIPE
import shutil  # os directory library
import docx2txt  # docx reader library
from PDF2txt import convert_pdf_to_txt
import codecs
from bidi.algorithm import get_display

# File type and corresponding text processing function
# run throughout the given file if it matches right type
# every line is then redirected to a simple txt file for better gain of the information needed
# the script returns Bad if the file is not in a supported list
# otherwise return txt file ready for scanning
def makeItRain(fileName, file_path, save_path, temp_path):
    if fileName[-4:] == ".txt":
        text = ''
        try:
            for line in codecs.open(file_path + fileName, 'r', encoding='utf-8'):
                text = text + line
            return ['.txt', text]
        except:
            return ['Bad']

    elif fileName[-4:] == ".doc":
        my_file = Path(temp_path + 'Result.txt')
        if my_file.is_file():
               os.remove( temp_path + 'Result.txt')
        print('OS')
        os.system('set HOME='+temp_path+' & '+temp_path+'antiword.exe '+'-mUTF-8.txt '+file_path+fileName +' >>'+temp_path + "Result.txt")
        print('OS')
        try:
            text = ''
            for line in codecs.open(temp_path + "Result.txt", 'r', encoding='utf-8'):
                text = text + line
            return ['.doc', text]
        except:
            return ['Bad']


    elif fileName[-5:] == ".docx":
        print('dox1')
        data2 = ''
        data = []
        my_file = Path(temp_path + 'Result.txt')
        if my_file.is_file():
            os.remove(temp_path + 'Result.txt')
        text = docx2txt.process(file_path + fileName)

        target = codecs.open(temp_path + "Result.txt", 'w', encoding='utf-8')

        for line in text.splitlines():
            target.write(line + '\n')
        target.close()
        try:
            text = ''
            for line in codecs.open(temp_path + "Result.txt", 'r', encoding='utf-8'):
                text = text + line
            return ['.docx', text]
        except:
            return ['Bad']


    elif fileName[-4:] == ".pdf":
        print('pdf:::',fileName)
        text = get_display( convert_pdf_to_txt(file_path + fileName) )
        return ['.pdf', text]

    else:
        return ['Bad']

