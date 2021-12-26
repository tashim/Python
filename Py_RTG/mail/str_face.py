import datetime
import re

def from_face(mail,n,email_message,dic):
    for part in email_message.walk():
        if part.get_content_type() != "text/plain":# text/html
            print("html/plain")
            body =part.get_payload(decode="utf-8")
            # print(type(body))
            if (isinstance(body,bytes)):
                body = body.decode()
            # print(body)
            if type(body) != type(str()) : continue
            body = body.replace('<br />','')
            body = body.replace('<p>','')
            body = body.replace('</p>','')
        else:
            body = part.get_payload(decode=False)
            print('text/plain')
        if not body:                            continue
        if type(body) != type(''):              continue
        # mail.store(n, '-FLAGS', '\\Seen')
        print("=======================RTG==========================================")
        dic['From'] = dic['From'].replace('"','')
        dic['comment'] = 'Lid from '+ dic['source']+' '+ dic['subject']+' '+ datetime.date.today().strftime('%d/%m/%y')
        dic['telefon'] = ''
        dic['domain'] = ''
        dic['city'] = ''
        dic['email'] = ''

        for text in body.replace('\r','').split('\n'):
            if text.split(':')[0] == 'name':
                dic['fname'] = ' '
                dic['name'] = ' '
                txt = re.findall(r'\w+', text.split(':')[1])
                if len(txt)>0:
                    dic['name'] = txt[0]
                    for x in txt[1:] : dic['fname'] +=x+' '
                    dic['fname']=dic['fname'].strip(' ')
            elif text.split(':')[0] == 'phone':
                dic['telefon'] = text.split(':')[1].strip(' ').replace('-','')
                if len(dic['telefon']) < 7: dic['telefon']=None
                else:
                    if re.findall(r'^[\+]?972',dic['telefon']):
                        dic['telefon'] = '0'+dic['telefon'][-9:]
            elif text.split(':')[0] == 'branch':
                dic['city'] = text.split(':')[1].strip(' ')
            elif text.split(':')[0] == 'product':
                dic['domain'] = text[text.find(':',0)+1:].strip(' ')
            elif text.split(':')[0] == 'email':
                dic['email'] = text.split(':')[1].strip(' ')
        print("str_facse read:",dic)

