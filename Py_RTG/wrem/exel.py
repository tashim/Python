"""
    read exel file from bmby

"""
import dbMan


def read_file(fileName):
    try:
        # print('try')
        file = open(fileName, 'r')
        text = file.read()
        # print(text)
        return text
    except:
        print('error open file',fileName)
        return None

def getlist(filename):
    text = read_file(filename)
    if not text:
        exit(2)
    txt = text
    list = []
    txt = txt[txt.find('StyleID'):]
    txt = txt[:txt.find('<Cell ss:MergeAcross')].strip()
    text = txt.split('<Row')
    # print(text)
    tt = text[0].split('<Data')
    keys=[]
    for t in tt:
        l =  t[t.find('>') + 1:t.find('<')]
        if l == '':l ='null'
        if 'דוא' in l: l='email'
        if 'טלפון ראשי' in l: l='telefon2'
        if 'טלפון נוסף' in l: l='telefon2'
        if 'סלולרי' in l: l='telefon'
        if 'פרטי' in l: l='name'
        if 'איזור' in l: l='city'
        if 'תאריך' in l: l='date'
        if 'משפחה' in l: l='fname'
        if 'התעניינות' in l: l='domain'
        if 'מקור' in l: l='ContactType'
        keys.append(l )
    # print(keys)
    m_list = []
    for n in range(1,len(text)):
        tt = text[n]
        list = []
        for t in tt.split('<Data'):
            l = t[t.find('>')+1:t.find('<')].strip()
            # if l == '': continue
            list .append(l)
            # print('====',list)
        # print(len(list),len(keys))
        dic =  dict(zip(keys,list) )
        # for d in dic:
        #     print( d,":",dic[d] )
        if len(dic)< 3:continue
        if 'telefon2' in dic:
            if dic['telefon'] == '':
                dic['telefon'] = dic['telefon2']
        m_list.append(dic)
    for m in m_list:
        m['telefon'] = m['telefon'].replace('-','')
        if 'telefon2' in dic:
            m['telefon2'] = m['telefon2'].replace('-','')
        # print(m)
    return m_list


if __name__ == "__main__":
    if not dbMan.connnect():
        print("error connection")
        exit(1)
    list = getlist('C:\Projects\Python\wrem\File1.xls')
    for l in list:
        # print(l)
        dbMan.input(l)
    print(len(list))
    dbMan.con_close()





