# coding=utf-8
"""Function to scan every needed type of files
    and extract the needed info like Name, Date, Phone, Email and Skills

The Function mainly uses RegEx and string manipulations in a loop to get the results
"""

# Imports
import re

# Function to extract name from the file
# Run throughout every line and search combinations of "Name"/"First Name" and its hebrew versions as-well
# if Found the script returns the name to the main function
def scanName(data):
    name = "No Name"

    for line in data:
        match = re.search(r'(?i)Name[ -:](.*)', line)
        match4 = re.search(u'\u05e9\u05dd\u05de\u05dc\u05d0[ -:](.*)', line)
        match2 = re.search(u'\u05e9\u05dd[ -:](.*)', line)
        match3 = re.search(r'\xd7\xa9\xd7\x9d[ -:](.*)', line)

        if match:
            try:
                name = str(match.group(1))
            except UnicodeEncodeError as e:
                print (e)
                continue
            name = re.sub(r'\W', " ", name)
            if len(name.split()) == 4:
                name = name[0] + ' ' + name[1] + ' ' + name[2] + ' ' + name[3]
                return name.replace(':', '').replace('-', '').strip()
            elif 0 < len(name.split()) <= 3:
                return name.replace(':', '').replace('-', '').strip()
            else:
                name = "No Name"

        elif match2:
            name = match2.group(1)
            print (name.split())
            name = name.replace(':', '').replace('-', '').strip()
            if len(name.split()) == 4:
                # name2 = name.split(' ')
                # print name2
                # name = name2[0] + ' ' + name2[1] + ' ' + name2[2] + ' ' + name2[3]
                name = name[0] + ' ' + name[1] + ' ' + name[2] + ' ' + name[3]
                return name  # .replace(':', '').replace('-', '').strip()
            elif 0 < len(name.split()) <= 3:
                return name.replace(':', '').replace('-', '').strip()
            else:
                name = "No Name"

        elif match3:
            name = match3.group(1)
            name = name.replace(':', '').replace('-', '').strip()
            if len(name.split()) == 4:
                name2 = name.split(' ')
                name = name2[0] + ' ' + name2[1] + ' ' + name2[2] + ' ' + name2[3]
                return name  # .replace(':', '').replace('-', '').strip()
            elif 0 < len(name.split()) <= 3:
                return name.replace(':', '').replace('-', '').strip()
            else:
                name = "No Name"

        elif match4:
            name = match4.group(1)
            name = name.replace(':', '').replace('-', '').strip()
            if len(name.split()) == 4:
                name2 = name.split(' ')
                name = name2[0] + ' ' + name2[1] + ' ' + name2[2] + ' ' + name2[3]
                return name  # .replace(':', '').replace('-', '').strip()
            elif 0 < len(name.split()) <= 3:
                return name.replace(':', '').replace('-', '').strip()
            else:
                name = "No Name"

    if name == "No Name":
        try:
            if 1 < len(data[0].split()) < 5:
                name = data[0] + "?"
                name = name.replace(':', '').replace('-', '').strip()
            elif 1 < len(data[1].split()) < 5:
                name = data[1] + "?"
                name = name.replace(':', '').replace('-', '').strip()
                # elif 1 < len(data[2].split()) < 3:
                #     name = data[2] + "?"

        except:
            print ("No Name Found")

    return name


# Function to extract birth date from the file
# # Run throughout every line and search combinations of "2Digits/2Digits/4Digits"
# if Found the script returns the date to the main function
def scanDate(data):
    for line in data:
        match = re.search(r'(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})', line)

        if match:
            return match.group()

    return "No Date"


# Function to extract phone number from the file
# def scanPhone(data):
#     for line in data:
#         line = line.replace(' ', '')
#
#         cellMatch = re.search(r'(\d{10})', line)
#         cellMatch2 = re.search(r'(\d{3})[-](\d{7})', line)
#         cellMatch3 = re.search(r'(\d{3})[-](\d{3}[-](\d{4}))', line)
#         cellMatch5 = re.search(r'(\d{4})[-](\d{6})', line)
#         cellMatch6 = re.search(r'(\d{6})[-](\d{4})', line)
#         cellMatch4 = re.search(r'(\d{7})[-](\d{3})', line)
#         # homeMatch = re.search(r'(\d{2})[ -](\d{7})', line)
#
#         if cellMatch:
#             return cellMatch.group()
#         if cellMatch2:
#             return ''.join(e for e in cellMatch2.group() if e.isalnum())
#         if cellMatch3:
#             return ''.join(e for e in cellMatch3.group() if e.isalnum())
#         if cellMatch4:
#             return ''.join(e for e in cellMatch4.group() if e.isalnum())
#         if cellMatch5:
#             return ''.join(e for e in cellMatch5.group() if e.isalnum())
#         if cellMatch6:
#             return ''.join(e for e in cellMatch6.group() if e.isalnum())
#
#     return 'No Number'


# Function to extract phone number from the file
# Run throughout every line and search combinations of "10Digits" as a phone number
# if Found the script returns the number to the main function
def scanPhone(text):
    data = {"TZ":'',"Phone":'',"Email":''}
    readytext = text.replace('\n',' ')
    readytext = readytext.replace('\r',' ')
    readytext = re.sub('[^A-Za-z0-9\-@_\. ]+', '|', readytext)
    readytext = readytext.replace('  ',' ')
    readytext = readytext.replace('|-','|')
    readytext = readytext.replace('-|','|')
    readytext = readytext.replace('| ','|')
    readytext = readytext.replace(' |','|')
    readytext = readytext.replace('- ','-')
    readytext = readytext.replace(' -','-')
    while readytext.find('  ')>=0: readytext = readytext.replace('  ',' ')
    print(readytext)
    emails = re.findall(r"[A-Za-z0-9\.\-+_]+@[A-Za-z0-9\.\-+_]+\.[A-Za-z]{2}[A-Za-z]?\.?c?o?\.?i?l?", readytext)

    tel = re.findall(r"([09]\d+\d\d[ \-]?\d{6})", readytext)
    print('1',tel)
    telt = re.findall(r'[09]\d?\d?[ |\-]?\d\d[ \-\+|\.\)]?\d{7}', readytext)
    print('2',telt)
    for t in telt: tel.append(t)
    # telt = re.findall(r"([09][\d]+[ ]?[- ]?[ ]?\d?\d?\d{2}[ -]?[- ]?\d?\d?\d{2}[ -]?[- \d]?\d?\d{2})", readytext)
    # print('3',telt)
    # for t in telt: tel.append(t)
    telt = re.findall(r"[09]\d?\d?[ |\-]?\d\d[ \-\+|\.\)]?\d{4}[ \-\+|\.\)]?\d{3}", readytext)
    print('4',telt)
    for t in telt: tel.append(t)
    telt = re.findall(r"[09]\d?\d?[ |\-]?\d\d[ \-\+|\.\)]?\d{3}[ \-\+|\.\)]?\d{4}", readytext)
    print('5',telt)
    for t in telt: tel.append(t)
    telt = re.findall(r"[09]\d?\d?[ |\-]?\d\d[ \-|\.]?\d{3}[ \-\+|\.\)]?\d{2}[ \-|\.]?\d{2}", readytext)
    print('6x',telt)
    for t in telt: tel.append(t)
    telt = re.findall(r"[09]\d?\d?[ |\-]?\d\d[ \-|\.]?\d{2}[ \-\+|\.\)]?\d{2}[ \-\+|\.\)]?\d{3}", readytext)
    print('6',telt)
    for t in telt: tel.append(t)
    telt = re.findall(r"([\-,: |]\d{7}[|\- ]?[- |][- |]?\d\d{2}[^\d])", readytext)
    print('7',telt)
    for t in telt: tel.append(t)
    if telt:
            kid = re.findall(r'[^\d]\d{3}[^\d]',telt[0])
            print(kid)
            print(tel)
            kid = kid[0]
            telt[0] = kid + re.findall(r'\d{7}',telt[0])[0]
    for t in telt: tel.append(t)
    telt = re.findall(r"[| \d\-]{19}[|\d\-]?", readytext)
    print('8',telt)
    for t in telt: tel.append(t)
    telt = re.findall(r'[|][09]\d{2}\d?[-|]\d{2}\d?\d?[-|]\d{2}\d?\d?', readytext)
    print('9',telt)
    for t in telt: tel.append(t)
    telt = re.findall(r"([^\d][09][\d]+[|\. ]?\d?\d{2}[- \d]?[\. |]?\d?\d{3}[-| \.]?\d]?\d{3})",readytext)
    print('10',telt)
    for t in telt: tel.append(t)
    print('e',tel)
    tz = re.findall(r"([^\d]\d{9}[^\d])", readytext)

    for t in range(len(tz)):
        tz[t]=tz[t].replace('-','')
        tz[t] = tz[t].replace('|','')
        tz[t] = tz[t].replace(',','')
        tz[t] = tz[t].replace(' ','')
    for t in range(len(tel)):
        tel[t]=tel[t].replace('-','')
        tel[t] = tel[t].replace('|','')
        tel[t] = tel[t].replace(',','')
        tel[t] = tel[t].replace(' ','')
        tel[t] = tel[t].replace('.','')
        if not tel[0].isdigit():
            tel[0] = tel[0][1:]
    print(tel)
    for t in tel:
        if len(t) < 10 : continue
        # if not tel.isdigit(): continue
        if t[0] == '9' or t[0] == '0':
            data['Phone'] = t
    for t in tz:
        data['TZ'] = t
        break
    if emails:
        data['Email'] = emails[0]
    text = text.replace('  ',' ')
    # print(text)
    dtext = []
    for line in text.splitlines():
        line = line.strip()
        if line != '' and len(line)>1:
            # print('line>>',line)
            dtext.append(line)
    data['Name'] = scanName(dtext)
    print(data)
    if len(tel) < 1: return None
    if len(tel[0]) < 8: return  None
    return data


# Function to extract email address from the file
# Run throughout every line and search combinations of "string@string.string" as an email
# if Found the script returns the email to the main function
def scanEmail(data):
    for line in data:
        match = re.search(r'[\w\.-]+@[\w\.-]+', line)

        if match:
            return match.group()

    return "No Email"


# Function to extract skills from the file
# Run throughout every line and search combinations of "Skill name" as a Skills
# if Found the script returns the skills to the main function
# def scanEducation(data):
#     education = []
#     qualities = ["python",
#                  u"ג'אווה",
#                  "java",
#                  "sql",
#                  "mysql",
#                  "sqlite",
#                  "c#",
#                  "c++",
#                  "c",
#                  "javascript",
#                  "pascal",
#                  "html",
#                  "css",
#                  "jquery",
#                  "linux",
#                  ".net",
#                  "asp.net",
#                  "winforms",
#                  "j2ee",
#                  "j2me",
#                  "android",
#                  "ios",
#                  "visual basic",
#                  "qa",
#                  "windows"]
#
#     for line in data:
#         for word in line.split():
#             word = word.strip(',')
#             # word = word.strip(' ,')
#             if word.lower() in qualities and word not in education:
#                 # if word in education:
#                 #     continue
#                 # else:
#                 #     education += word + " "
#                 education.append(word)
#
#     return education


# Added counters for statistics in the end of the work
Ucounter = 0
Acounter = 0

def addUCounter(num):
    global Ucounter
    Ucounter += num


def setCounter():
    global Ucounter, Acounter
    Ucounter = 0
    Acounter = 0


def addACounter(num):
    global Acounter
    Acounter += num

def getCounter():
    global Ucounter, Acounter
    return 'Summary: (' + str(Ucounter) + ') Updated, (' + str(Acounter) + ') Added.'
