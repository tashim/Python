import email
import email.header
import imaplib
import re

import dbMan
from DB import set_to_db
from ole_post import send_to_oleg
from str_mail import html_to_list, TELESERVICE, omnitelecom

EMAIL_ACCOUNT = "lidimrtg@gmail.com"
EMAIL_PASSWORD = '0503309318rtg'

pattern_uid = re.compile('\d+ \(UID (?P<uid>\d+)\)')
def parse_uid(data):
    match = pattern_uid.match(data)
    return match.group('uid')


def read_mail():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    # maillist=mail.list()
    mail.select('inbox')
    rv, data = mail.search(None, "ALL")
    # rv, data = mail.search(None, "UNSEEN")
    num = data[0].split()
    for n in num:
        result, email_data = mail.fetch(n, '(RFC822)')
        if not email_data[0]:                continue
        raw_email = email_data[0][1]
        if type(raw_email) == type(1):        continue
        try:
            raw_email_string = raw_email.decode('utf-8')
        except:
            raw_email_string = raw_email.decode('windows-1255')
        email_message = email.message_from_string(raw_email_string)
        # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',raw_email_string,'\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')

        # ########### Header Details
        print('read new mail:')
        subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
        email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
        dic = {'From': email_from, 'subject': subject}
        dic['source'] = 'SEO'
        if 'PPC' in subject: dic['source'] = 'PPC'

        # ########### check mail from?
        dir = 'noneed'
        #         print("=======================HTML==========================================")
        print(' mail:', email_from)
        if '@rt-ed' in email_from:
            # from_rtg(mail,n,email_message,dic)
            from str_face import from_face
            from_face(mail, n, email_message, dic)
            dir = 'Info'
        elif 'TELESERVICE' in email_from:
            TELESERVICE(mail, n, email_message, dic)
            dir = 'Tele'
            # continue
        elif 'info@tostudy' in email_from or '@yoram' in email_from:
            for part in email_message.walk():
                mail.store(n, '+FLAGS', '\\Seen')
                if part.get_content_type() == "text/plain":
                    pass
                else:  # text/html
                    body = part.get_payload(decode=True)
                    if not body:   continue
                    ls = str(body.decode('utf-8'))
                    print('info tostudy call html_to_list')
                    dic = html_to_list(ls, dic)
                    dir = 'tostudy'
        elif 'omnitelecom' in email_from:
            omnitelecom(mail, n, email_message, dic)
            mail.store(n, "+FLAGS", "(\Seen)")
            dir = 'omnitelecom'
            if (dbMan.is_student(dic["telefon"])):
                print("is student")
                dir="omnistud"
                mail.store(n, '+FLAGS', '\\Seen')
                mail.store(n, '+FLAGS', '\\Deleted')
                continue
            # else:
            #     print("new")
            #     continue
        else:
            dic = None
        if dic :
            id = set_to_db(dic)
            if id and  dir!="omnistud":
                send_to_oleg(id, dic['domain'], dic['source'])
                print('send ', dic['source'])
            else:
                dir='noread'
        else:
            dir = 'noread'
        #
        resp, data = mail.fetch(n, "(UID)")
        msg_uid = parse_uid(data[0].decode())
        try:
            result = mail.uid('COPY', msg_uid, dir)
        except:
            print('exept copy mail ',msg_uid)
            result= mail.uid('COPY', msg_uid, 'error')
        # print(dir)
        if result[0] == 'OK':
            try:
                mail.store(n, '+FLAGS', '\\Seen')
                mail.store(n, '+FLAGS', '\\Deleted')
            except:
                print('error copy')
            mail.expunge()
        mail.expunge()


##########################################################################################
if __name__ == '__main__':
    read_mail()
