from celery import shared_task
from decouple import config
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

@shared_task(name="sum_two_numbers")
def add(x, y):
    return x + y


@shared_task
def send_email(subject,message,html_content,to_mail,from_mail):
    username=from_mail
    if from_mail=="order@mail.akku.gg":
        password=config('ORDER_MAIL_PASSWORD',cast=str)
    elif from_mail=='payment@mail.akku.gg':
        password=config('PAYMENT_MAIL_PASSWORD',cast=str)
    elif from_mail=='code@mail.akku.gg':
        password=config('CODE_MAIL_PASSWORD',cast=str)
    elif from_mail=='system@mail.akku.gg':
        password=config('SYSTEM_MAIL_PASSWORD',cast=str)
    else:
        username='akku@mail.akku.gg'
        password=config('DEFAULT_MAIL_PASSWORD')

    rcptto=to_mail
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f"AKKU<{username}>"

    msg['To'] = ", ".join(rcptto)
    msg['Message-id'] = email.utils.make_msgid()
    msg['Date'] = email.utils.formatdate() 
    textplain = MIMEText(message, _subtype='plain', _charset='UTF-8')
    msg.attach(textplain)
    texthtml = MIMEText(html_content, _subtype='html', _charset='UTF-8')
    msg.attach(texthtml)
    try:
        client = smtplib.SMTP()
        client.connect('smtpdm-ap-southeast-1.aliyun.com', 80)
        client.set_debuglevel(0)
        client.login(username, password)
        client.sendmail(username, rcptto, msg.as_string())
        client.quit()
    except smtplib.SMTPConnectError as e:
        print('Mail delivery fails, the connection fails:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPAuthenticationError as e:
        print('Mail delivery failure, certification error:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPSenderRefused as e:
        print('Send mail failed, the sender is rejected:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPRecipientsRefused as e:
        print('Send mail failed, the recipient was rejected:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPDataError as e:
        print('Send mail failed, data reception to refuse:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPException as e:
        print('Send mail failed, ', e.message)
    except Exception as e:
        print('Send mail abnormal, ', str(e))