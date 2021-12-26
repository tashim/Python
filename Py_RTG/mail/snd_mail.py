import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_ACCOUNT = "job.mai.rtg@gmail.com"
EMAIL_PASSWORD = '3309318rt'

receiver_email = ["tashim.te@gmail.com","info@rt-ed.co.il","bennyc1313@gmail.com"]

message = MIMEMultipart("alternative")
message["Subject"] = "errors scripts"
message["From"] = EMAIL_ACCOUNT
message["To"] = ",,,,"
for t in receiver_email: message["To"] +=t+','


def send_email(f_name,text):
    # Create the plain-text and HTML version of your message
    html = """
    <html>
      <body style="background-color:rgb(100,100,100,0,3);">
      <H2>Log from {} </H2>
        <pre style="border:2px solid Tomato;color:blue;">""" + text+ """ </pre>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    # part1 = MIMEText(text, "plain")
    part2 = MIMEText(html.format(f_name), "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    # message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        for receiver in receiver_email:
            server.sendmail(EMAIL_ACCOUNT, receiver, message.as_string())

def check(f_name):
    ttt = ''
    # f_name = 'log.log'
    try:
        with open(f_name, 'r') as f:
            ttt = f.read()
    except:
        pass
    if ttt != '':
        with open(f_name, 'w') as f:
            pass
            send_email(f_name,ttt)

if __name__=="__main__":
    check("/LOGS/mface.log")
    check("/LOGS/minfo.log")

