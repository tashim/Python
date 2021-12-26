import imaplib
import email
import email.header
from datetime import datetime

import dbMan
import post
from str_mail import html_to_list, from_rtg, TELESERVICE

EMAIL_ACCOUNT = "lidimrtg@gmail.com"
EMAIL_PASSWORD = '0503309318rt'

def read_mail():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    # maillist=mail.list()
    mail.select('inbox')
    rv, data = mail.search(None, "UNSEEN")
    num = data[0].split()
    for n in num:
        result, email_data = mail.fetch( n, '(RFC822)')
        if not email_data[0] :
            print('no data')
            continue
        raw_email = email_data[0][1]
        print(raw_email)
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
        dic = {'From':email_from,'subject':subject}

# ########### check mail from?
        print("=======================HTML==========================================")
        print(' mail:', email_from)
        if  'info@rt-ed.co.il' in email_from :
            from_rtg(mail,n,email_message,dic)
            # continue
        elif  'TELESERVICE' in email_from :
            TELESERVICE(mail,n,email_message,dic)
            # continue
        elif  'info@tostudy' in email_from  or '@yoram' in email_from :
            for part in email_message.walk():
                mail.store(n, '+FLAGS', '\\Seen')
                if part.get_content_type() == "text/plain": pass
                else:  # text/html
                    body = part.get_payload(decode=True)
                    if not body:   continue
                    ls = str(body.decode('utf-8'))
                    print('info tostudy call html_to_list')
                    dic = html_to_list(ls, dic)
        else:
            dic = None
            print('no need mail:', email_from)
            mail.store(n, '+FLAGS', '\\Seen')
        if dic:
            dbMan.set(dic,0)
            dbMan.set(dic,1)
            post.mail_post \
                    (
                    Phone=dic['telefon'],
                    Fname=dic['fname'],
                    Lname=dic['name'],
                    Address=dic['city'],
                    Comments=dic['comment'],
                    ProductTitle=dic['domain'],
                    Email=dic['email'],
                )

        # print('mail no rtg', email_from)
        print('dic = ',dic)

# ########## Body details
#
                 # dbMan.set(dic)
    mail.expunge()
if __name__=='__main__':
    try:

        read_mail()
        print('start', datetime.now())
    except:
        print("exept error read mail")
    finally:
        print('end',datetime.now())
