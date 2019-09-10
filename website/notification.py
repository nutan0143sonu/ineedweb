#----------------Import local packages------------
from app.models import *
from website.models import *

#-------------------Notification for both jobseeker and employement---------------------------
def userNotification(sender,receiver,job,title,type_of_notification):
    notification=Notification.objects.create(sender=sender,receiver=receiver,job=job,title=title,type_of_notification=type_of_notification)
    print("notification",notification)
    return notification