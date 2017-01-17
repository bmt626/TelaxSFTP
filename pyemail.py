import smtplib

from email.mime.text import MIMEText

def sendEmail(logfile, statuscode):
    FROM = FROM_USER_EMAIL
    TO = TO_USER_EMAIL

    fp = open(logfile, 'rb')
    msg = MIMEText(fp.read())
    fp.close()

    msg['Subject'] = statuscode + ': ' + 'EMAIL_SUBJECT_HERE'
    msg['From'] = FROM
    msg['To'] = TO

    s = smtplib.SMTP(SERVER_IP_ADDRESS_HERE)
    s.sendmail(FROM, [TO], msg.as_string())
    s.quit()
