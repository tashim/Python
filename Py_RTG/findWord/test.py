import codecs
import os
import re
from pathlib import Path
from shutil import copyfile

from bidi.algorithm import get_display
from docx2txt import docx2txt

from PDF2txt import convert_pdf_to_txt

def find(path,word):
    dir = os.listdir(path)
    for d in dir:
        if os.path.isdir(path+"/"+d):
            # print(d,' is dir')
            pass
            find(path+"/"+d,word)
        else:
            # print('[',d,']')
            file = path+"/"+d
            ext = file.split('.')[-1].lower()
            if ext != "txt" \
                    or ext != "doc" \
                    or ext != "docx" \
                    or ext != "pdf":

            # if ext == 'pdf':

                # print(file)
                try:
                    text = makeItRain(file,ext)
                except:
                    continue
                if text:
                    if re.search(r'{0}'.format(word),text,flags=re.IGNORECASE):
                        print('find ',file)
                        copyfile(file,'z:/lab_old/'+file.split('/')[-1])


def makeItRain(fileName, ext):
    temp_path = 'c:/antiword/'
    if ext == "txt":
        text = ''
        try:
            for line in codecs.open(fileName, 'r', encoding='utf-8'):
                text = text + line
            return  text
        except:
            return None

    elif ext == "doc":
        my_file = Path(temp_path + 'Result.txt')
        if my_file.is_file():   os.remove( temp_path + 'Result.txt')
        print('OS run antiword')
        os.system('set HOME='+temp_path+' & '+temp_path+'antiword.exe '+'-mUTF-8.txt '+fileName +' >>'+temp_path + "Result.txt")
        print('OS end antiword')
        try:
            text = ''
            for line in codecs.open(temp_path + "Result.txt", 'r', encoding='utf-8'):
                text = text + line
                # print(text)
            return  text
        except:
            return None


    elif ext == "docx":
        # print('dox1')
        my_file = Path(temp_path + 'Result.txt')
        if my_file.is_file():   os.remove(temp_path + 'Result.txt')
        text = docx2txt.process(fileName)

        target = codecs.open(temp_path + "Result.txt", 'w', encoding='utf-8')

        for line in text.splitlines():
            target.write(line + '\n')
        target.close()
        try:
            text = ''
            for line in codecs.open(temp_path + "Result.txt", 'r', encoding='utf-8'):
                text = text + line
            return text
        except:
            return None


    elif ext == "pdf":
        # print('pdf:::',fileName)
        try:
            text = get_display( convert_pdf_to_txt(fileName) )
            return  text
        except:
            return None


    else:
        return None



# count =0
# for dirname, dirnames, filenames in os.walk(path):
#     # print path to all subdirectories first.
#     # for subdirname in dirnames:
#     #     print(os.path.join(dirname, subdirname))
#
#     # print path to all filenames.
#     for filename in filenames:
#         print(os.path.join(dirname, filename))
#         count += 1
# print(count)

path = "z:/SmartCV"

find(path,'labview')

