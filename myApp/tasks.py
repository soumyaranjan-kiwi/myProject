from myProject.celery import app
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime, timedelta
from .models import UserFile


@app.task(name='send_notification')
def send_notification():
    try:

        time_threshold = datetime.now() + timedelta(days=1)

        user_files = UserFile.objects.filter(start_date__lte=time_threshold, status=UserFile.EpicStatus.NON_REVIEWED)
        for user_file in user_files:
            subject = "Reminder: Your Epic's Start Date Tomorrow"
            message = (f"Dear {user_file.user.email},\n\nThis is a reminder that the start date of your Epic is "
                       f"tomorrow.\n\nBest regards,\nYour Project Team")
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user_file.user.email]
            send_mail(subject, message, email_from, recipient_list)
            user_file.status = UserFile.EpicStatus.REVIEWED
            user_file.save()
    except Exception as e:
        print(e)
