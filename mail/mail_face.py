import imaplib
import email
import email.header
import re

from DB import set_to_db
from ole_post import send_to_oleg
from str_face import  from_face

EMAIL_ACCOUNT = "job.mai.rtg@gmail.com"
EMAIL_PASSWORD = '3309318rt'

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
        result, email_data = mail.fetch( n, '(RFC822)')
        if not email_data[0] :              continue
        raw_email = email_data[0][1]
        if type(raw_email) == type(1):      continue
        try:
            raw_email_string = raw_email.decode('utf-8')
        except:
            raw_email_string = raw_email.decode('windows-1255')
        email_message = email.message_from_string(raw_email_string)
                    # ########### Header Details
        print('read new mail:<-----------------------------')
        subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
        email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
        dic = {'From':email_from.split(' ')[0],'subject':subject,'ContactType':110}
                    # ########### check mail from?
        print(' mail:', email_from)
        if 'job.mai.rtg' in email_from:
            dic['source'] = 'SNL'
            from_face(mail,n,email_message,dic)
            id = set_to_db(dic)  # dic = {'From':email_from.split(' ')[0],'subject':subject,'ContactType':110}
            print(dic)
            print("Send oleg")
            send_to_oleg(id,dic['domain'],'SNL')

        resp, data = mail.fetch(n, "(UID)")
        msg_uid = parse_uid(data[0].decode())
        result = mail.uid('COPY', msg_uid, 'readed')
        if result[0] == 'OK':
            mail.store(n, '+FLAGS', '\\Seen')
            mail.store(n, '+FLAGS', '\\Deleted')
            mail.expunge()

    mail.expunge()
if __name__=='__main__':

    read_mail()
