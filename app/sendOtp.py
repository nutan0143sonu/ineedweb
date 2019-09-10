from django.core.mail import send_mail
from django.conf import settings
from templated_email import send_templated_mail

def send_OTP(otp, email):
    """Fuction of Sending Otp Through email"""
    subject = "Otp For Verification."
    user =  settings.EMAIL_HOST_USER
    message = "The Otp Verication  Email"+"\n\n"+str(otp)
    send_mail(subject, message, user, [email])

def send_link(link, email):
    """Function of Sending link through email"""
    subject = "This is link for email verification of User"
    user = settings.EMAIL_HOST_USER
    message = "Click here to verify your credential or Email for changing Your Password" + "\n" + link
    send_mail(subject, message, user, [email])

def send_template_reference(link,sender,receiver,user):
    """Fuction of sending template Email """
    send_templated_mail(
        template_name='invite',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[receiver],
        context={
            'receiver':receiver,
            'Message':user+" has invited you. So, click on given link below",
            'link':link
        })

