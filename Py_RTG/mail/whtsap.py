# from twilio.rest import Client
#
# account_sid = 'AC8f1b58407645f4df360b8aaafe556cca'
# auth_token = '8ce9263b19b34f9dc7ba3758d49a35df'
# client = Client(account_sid, auth_token)
#
# message = client.messages.create(
#     from_='+12057828801',
# body='teste',
#     to='+972542082450'
# )
#
# print(message.sid)

from twilio.rest import Client

account_sid = 'AC8f1b58407645f4df360b8aaafe556cca'
auth_token = '8ce9263b19b34f9dc7ba3758d49a35df'
client = Client(account_sid, auth_token)

def send(tel,text):
    tel = '+972'+tel[-9:]
    print(tel)
    message = client.messages.create(
        from_='whatsapp:+12057828801',
        body=text,
        to='whatsapp:'+tel
    )

    print(message.sid)
send("0542083950",'ha ha Natan')