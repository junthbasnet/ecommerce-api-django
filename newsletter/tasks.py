from celery import shared_task

from common.tasks import send_email


@shared_task
def send_subscription_email(subscribers, newsletter):
    content = newsletter['content']
    subject = newsletter['email_subject']
    for subscriber in subscribers:
        email = subscriber['email']
        code = subscriber['code']
        html_content = content + f'<br><a style="display:block;background:black;color:white;text-align:center" href=http://localhost:8000/api/newsletter/unsubscribe/?email={email}&code={code}>unsubscribe</a>'
        send_email.delay(subject=subject, message=None, from_mail='akku@mail.akku.gg', to_mail=[email, ],
                         html_content=html_content)
