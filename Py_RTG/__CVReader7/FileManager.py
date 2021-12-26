"""Function to parse the right document type
    and convert it to a readable list to work with the text"""
import os
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
        try:
            data = [line.strip() for line in codecs.open(file_path + fileName, 'r', encoding='utf-8')]
            # moveFile(fileName, file_path, save_path)
            # print data
            # return data
            return ['.txt', data]
        except:
            return "Bad"

    elif fileName[-4:] == ".doc":
        my_file = Path(temp_path + 'Result.txt')
        if my_file.is_file():
               os.remove( temp_path + 'Result.txt')
        # os.system('set HOME=c/:antiword')
        # cmd = ['c:/antiword/antiword.exe', '-mUTF-8.txt', file_path + fileName]
        # p = Popen(cmd, stdout=PIPE)
        # stdout, stderr = p.communicate()

        os.system('set HOME='+temp_path+' & '+temp_path+'antiword.exe '+'-mUTF-8.txt '+file_path+fileName +' >>'+temp_path + "Result.txt")
        # target = open(temp_path + "Result.txt", 'w')

        # try:
        #     for line in stdout.split('|'):
        #
        #         line = line.strip()
        #         target.write(line + '\n')
        #     target.close()
        # except:
        #     return "Bad"
        try:
            data = [line.strip() for line in codecs.open(temp_path + "Result.txt", 'r', encoding='utf-8')]
            # print data
            # moveFile(fileName, file_path, save_path)
            # return data
            return ['.doc', data]
        except :
            # print("bad")
            return "Bad"


    elif fileName[-5:] == ".docx":
        data2 = ''
        data = []
        text = docx2txt.process(file_path + fileName)

        target = codecs.open(temp_path + "Result.txt", 'w', encoding='utf-8')

        for line in text.splitlines():
            target.write(line + '\n')
        target.close()

        try:
            data = [line.strip() for line in codecs.open(temp_path + "Result.txt", 'r', encoding='utf-8')]
            # print data
            # moveFile(fileName, file_path, save_path)
            return ['.docx', data]
        except:
            return "Bad"


    elif fileName[-4:] == ".pdf":
        text = convert_pdf_to_txt(file_path + fileName)
        readytext = get_display(text)
        data = []
        for line in readytext.splitlines():
            if line != '' and line != ' ':
                line = line.strip()
                data.append(line)
        # moveFile(fileName, file_path, save_path)
        # print data
        return ['.pdf', data]

    else:
        return "Bad"
