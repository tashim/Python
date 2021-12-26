import re

import dbMan
import post


def html_to_list(str,dic):
    d = {'telefon': '', 'city': '', 'email': '', 'fname': '', 'name':'','domain': '','comment':''}
    dic.update(d)
    print('\n toStudy:\n',dic['From'])
    while str.find('  ')!=-1:
        str = str.replace('  ',' ')
    str = str.replace('\n','')
    str = str.replace('\r','')
    print(str, '\n::::::html to study::::::')

    ll = str.split('>')
    l2 = []
    for l in ll:
        if l[:1].find('<') != -1:
            ll.remove(l)
        else:
            n = l.find('<');
            if n >= 0:
                l = l[:n]
            n = l.find('>');
            if n >= 0:
                l = l[n:]
            if l !='' and l != ' ':
                l2.append(l)
    start =0
    end = len(l2)
    step = 2
    ll.clear()
    while start < end:
        if not ':' in l2[start]:
            start+=1
            continue

        if 'body' in l2[start] or 'leadDetails' in l2[start]:
            start+=1
            continue
        line = l2[start]
        lbody = l2[start+1]
        lbody.strip()
        if line.find("טל") != -1:
            lbody = lbody.replace('-', '')
            lbody = lbody.replace('+', '')
            dic.update({"telefon": lbody})
        elif line.find('עיר') != -1:
            dic.update({"city": lbody})
        elif line.find('דוא') != -1 or line.find('מייל') != -1:
            dic.update({"email": lbody})
        elif line.find('שם') != -1:

            if 'shimmonn@yoram' in dic['From']:
                name = lbody.split(' ')
                dic.update({"name": name[0]})
                dic.update({"fname": name[1]})
            else:
                lbody = lbody.split(' ')[0]
                if line.find('פרט') != -1:
                    dic.update({'name': lbody})
                if line.find('משפחה') != -1:
                    dic.update({"fname": lbody})
        elif line.find('קורס') != -1 or line.find('מסלול') != -1:
            lbody = lbody.replace('קורס','')
            dic.update({'domain': lbody})

        elif line.find('תואר') != -1 or line.find('תחום') != -1 or line.find('קטגוריה') != -1:
            dic.update({'comment': dic['comment'] + lbody + '\n'})

        start += step;
    return dic
    # exit(1)
#
# from info rtg
def from_rtg(mail,n,email_message,dic):
    for part in email_message.walk():
        mail.store(n, '+FLAGS', '\\Seen')
        if part.get_content_type() == "text/plain": pass
        else:  # text/html
            body = part.get_payload(decode=False)
            if not body:   continue
            if type(body) != type(''): continue
                # print('info rtg call html_to_list')
                # print(dic)
            # print("=======================RTG==========================================")
            # print("subject:", dic["subject"])
            # print("from:", dic["From"])
            dic = rt_html_to_list(body, dic)
            if dic:
                dbMan.set(dic)
                post.mail_post\
                            (
                            Phone = dic['telefon'],
                            Fname = dic['fname'],
                            Lname = dic['name'],
                            Address = dic['city'],
                            Comments = dic['comment'],
                            ProductTitle = dic['domain'],
                            Email = dic['email'],
                            )
            #  print(dic)
            # for d in dic:  print(d,':',dic[d])
            # print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")

def rt_html_to_list(str,dic):
    d = {'telefon': '', 'city': '', 'email': '', 'fname': '', 'name':'','domain': '','comment':''}
    dic.update(d)
    # print('\n----===',dic['From'])
    lfrom = dic['From'].split(' ')
    dic['From'] = lfrom[len(lfrom) -1]
    if len(lfrom) > 1:
        dic['name'] = lfrom[0]
        for i in range(1,len(lfrom)-1):
            # print(i)
            dic['fname'] += lfrom[i] + ' '
    # elif len(lfrom) == 2:
    #     dic['name'] = lfrom[0]
    # else:
    #     print("dic no")
### find email
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str)
    if len(emails) > 0:
        dic['email'] = emails[0]
### find telefon
    tel = re.findall(r"([\d]+[- \d]?\d{3}[- \d]?\d{3})", str)
    if len(tel) > 0:
        dic['telefon'] = tel[0]
        while '-' in dic['telefon']: dic['telefon']= dic['telefon'].replace('-','')
    else:
        # print('No telefon')
        return  None

    while str.find('  ')!=-1:
        str = str.replace('  ',' ')
    while 1:
        s1 = str.find('<')
        s2 = str.find('>')
        if s1 == -1 or s2 == -1: break
        srt_t = str[:s1]
        str = srt_t + str[s2+1:]
    str = str.replace('\r', '')
    str = str.strip('\n ')
    sl = str.split('\n')
    while '' in sl: sl.remove('')
    if 'Syllabus' in dic['subject'] :
        sl = sl[0].split('הסלבוס')
        dic['comment'] = sl[0]
        sl = sl[1].split(':')
        dom = sl[1].split('.')[0]
        if '&' in dom:   dom = dom[:dom.find('&')] + dom[dom.find(';') + 1:]
        dic['domain'] = dom.replace('-', '')
    else:
        for l in sl:
            if l == dic['subject']: continue
            if not ':' in l or 'הודעה' in l:
                while 'POPUP' in l : l = l.replace('POPUP','')
                dic['comment'] += l + '\n'
            if 'עמוד עניין' in l:
                dom = l.split(':')[1]
                if 'Contact' in dom or 'Home' in dom:
                    dic['domain']=''
                    continue
                if '&' in dom:    dom = dom[:dom.find('&')] + dom[dom.find(';')+1:]
                dic['domain'] = dom.replace('-','')

    return  dic

def TELESERVICE(mail,n,email_message,dic):
    d = {'telefon': '', 'city': '', 'email': '', 'fname': '', 'name':'','domain': '','comment':''}
    dic.update(d)
    for part in email_message.walk():
        mail.store(n, '+FLAGS', '\\Seen')
        if part.get_content_type() == "text/plain": pass
        else:  # text/html
            body = part.get_payload(decode=False)
            if not body:   continue
            if type(body) != type(''): continue
            # print('body====================================================================')
            # print(body)
            # print('body====================================================================')
            ls = body.split('\n')
            for l in ls:
                if not ':' in l: continue
                l = l.split('<')[0]
                if 'מסלול:' in l:
                    dic['domain'] = l.split(':')[1].strip().replace('-','')
                if 'בארץ:' in l:
                    dic['city'] = (l.split(':')[1]).strip().replace('-','')
                if 'שם:' in l:
                    dic['name'] = (l.split(':')[1]).strip()
                if 'משפחה:' in l:
                    dic['fname'] = (l.split(':')[1]).strip()
                if 'פניה:' in l:
                    dic['comment'] = 'lid TELEService:'+(l.split(':')[1]).strip()
                if 'טלפון:' in l:
                    dic['telefon'] = (l.split(':')[1]).strip().replace('-','')
            if len(dic["telefon"]) < 7:
                print('Not get telefon number')
                return

            # dic = rt_html_to_list(body, dic)
            # for d in dic: print(d,'::',dic[d],'::')
            if dic:
                dbMan.set(dic)
                post.mail_post\
                            (
                            Phone = dic['telefon'],
                            Fname = dic['fname'],
                            Lname = dic['name'],
                            Address = dic['city'],
                            Comments = dic['comment'],
                            ProductTitle = dic['domain'],
                            Email = dic['email'],
                            )
            print("end---------------------------------------------------------------------------------")