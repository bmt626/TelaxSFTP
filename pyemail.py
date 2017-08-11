import smtplib

from email.mime.text import MIMEText


def sendemail(logfile, statuscode):
    FROM = FROM_USER_EMAIL
    TO = TO_USER_EMAIL

    msg = MIMEText(createmsg(logfile))

    msg['Subject'] = statuscode + ': ' + 'EMAIL_SUBJECT_HERE'
    msg['From'] = FROM
    msg['To'] = TO

    s = smtplib.SMTP(SERVER_IP_ADDRESS_HERE)
    s.sendmail(FROM, [TO], msg.as_string())
    s.quit()


def createmsg(logfile):
    with open(logfile, 'rb') as fp:
        msg = ''
        for line in fp:
            msg += str(line, "utf-8")
            # add a new line to the text doc as some mail clients will
            # ignore the line breaks with out this (ie - outlook)
            msg += '\n-'
    return msg
