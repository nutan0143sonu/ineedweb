import time

from django.conf import settings
from pyfcm import FCMNotification

push_service = FCMNotification(
    api_key="AAAABwCcc5s:APA91bEz2Lp2Wk0wY7Dg7il5lJWTMz2cVWpQCtfuqJ8OSSmbQE1BwQzpqmhf0-J7uS4lH5u5bHzj0fX9DRdJzgxpkCwWEegPhuVKO-S3z9uixlufX8IbWtYe9_x6UwdMP_yJAytCyYOT"
    #api_key="AAAAN3Kc-Qk:APA91bFpIXgTyuEVn4thgFBNqZSqurPMxkWwI77KighU4LLzZYI5x_T8jAIcrf8QWJ2TB1CUfZ3kpf5Pzx2yrS7icHfllOm9HN1h5UynpPWvO9Xvv5Eb88R5056rYc000Eg3q8L8l75H"
    )

def send_notification(device_id):
    print("device id", device_id)
    message_title = "MVP update"
    message_body = "Hope you're having fun this weekend, don't forget to check today's news"
    result = push_service.notify_multiple_devices(registration_ids=[device_id], message_title=message_title,
                                                  message_body=message_body))
    return result