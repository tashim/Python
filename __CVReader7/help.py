

# EMAIL_ACCOUNT = "Doron.rted@gmail.com"
# EMAIL_PASSWORD = 'Yokasta!'


#     result, data = mail.uid('search', None, "UNSEEN") # (ALL/UNSEEN)
#
#     i = len(data[0].split())
#     for x in range(i):
#         continue
#         latest_email_uid = data[0].split()[x]
#         result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
#         # result, email_data = conn.store(num,'-FLAGS','\\Seen')
#         # this might work to set flag to seen, if it doesn't already
#         raw_email = email_data[0][1]
#         raw_email_string = raw_email.decode('utf-8')
#         email_message = email.message_from_string(raw_email_string)
#         message_id = email_message.get('Message-ID')
#         print('mesId=',message_id)
# ########### Header Details
#         # date_tuple = email.utils.parsedate_tz(email_message['Date'])
#         # if date_tuple:
#          # local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
#          # local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
#         email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
#         # email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
#         subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
#         # print("From: %s\nTo:  %s\nSubject: %s\nendsubject" % (email_from, email_to, subject))
#         if email_from.find('shimmonn@yoram') == -1 and email_from.find('info@tostudy') == -1:
#             # store(num, '+FLAGS', '\\Deleted')
#             print('mail ', email_from)
#             # mail.expunge()
#             continue
#         dic = {'From':email_from,'subject':subject}
# ###### Body details
#
#         for part in email_message.walk():
#             if part.get_content_type() == "text/plain":
#                 body = part.get_payload(decode=True)
#                 # print(body)
#             else: # text/html
#                  body = part.get_payload(decode=True)
#                  if not body:
#                      continue
#                  ls = str(body.decode('utf-8'))
#                  # print(ls)
#                  lst = {}
#                  lst=str_to_list(ls,dic)
#                  dbMan.set(lst)
#                  # for l in lst:
#                  #    print(l,'\t:',lst[l])
