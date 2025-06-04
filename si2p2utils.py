import datetime
from time import mktime
from django.utils import timezone
import json
from google.oauth2 import service_account
import google.auth.transport.requests
import requests

from server.backend.admin.models import Log
from server.backend.assistance.models import Assistance, ClassSession
from server.backend.assistance.serializers import AssistanceSerializer
from server.backend.core.models import Class, Student, Subject, User
from server.backend.grades.models import Score, ScoreTarget
from server.backend.grades.serializers import ScoreSerializer
from server.backend.participations.models import Participation
from server.backend.participations.serializers import ParticipationSerializer

service_account_file = './si2-p1-mobile-firebase-adminsdk-fbsvc-c39d103571.json'
credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=['https://www.googleapis.com/auth/cloud-platform'])

def get_access_token():
    print('reached get_access_token()')
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    print('finished get_access_token()')
    return credentials.token

def send_fcm_notification(device_token, title, body):
    print('reached send_fcm_notification()')
    fcm_url = 'https://fcm.googleapis.com/v1/projects/si2-p1-mobile/messages:send'
    message = {
        "message": {
            "token": device_token,
            "notification": {
                "title": title,
                "body": body
            }
        }
    }
    headers = {
        'Authorization': f'Bearer {get_access_token()}',
        'Content-Type': 'application/json; UTF-8'
    }
    response = requests.post(fcm_url, headers=headers, data=json.dumps(message))
    print('finished send_fcm_notification()')
    if response.status_code == 200:
        print('Notification sent!')
    else:
        print(f"Error sending notification: {response.status_code}, {response.text}")
        
def saveLog(request, action): 
    log = Log()
    user = User.objects.get(access_token=request.META['HTTP_AUTHORIZATION'].split()[1])
    if user.role == 'S':
        log.user = user.student.lname + " " + user.student.name
    if user.role == 'T':
        log.user = user.teacher.lname + " " + user.teacher.name
    if user.role == 'A':
        log.user = user.login
    log.role = user.role
    log.login = user.login
    log.action = action
    log.ip = request.META['REMOTE_ADDR']
    log.time = timezone.now().today()
    log.save()
        
def saveLogUser(request, action, user): 
    log = Log()
    if user.role == 'S':
        log.user = user.student.lname + " " + user.student.name
    if user.role == 'T':
        log.user = user.teacher.lname + " " + user.teacher.name
    if user.role == 'A':
        log.user = user.login
    log.role = user.role
    log.login = user.login
    log.action = action
    log.ip = request.META['REMOTE_ADDR']
    log.time = timezone.now().today()
    log.save()
    
def subjectPrediction(subject: Subject, _class: Class, student: Student):
    targets = ScoreTarget.objects.filter(_class=_class, subject=subject)
    scores = Score.objects.filter(student=student, target__in=targets)
    s = ScoreSerializer(data=scores, many=True)
    s.is_valid()
    scores = s.data
    sessions = ClassSession.objects.filter(_class=_class, subject=subject)
    sesscount = sessions.count()
    attendances = Assistance.objects.filter(student=student, session__in=sessions)
    a = AssistanceSerializer(data=attendances, many=True)
    a.is_valid()
    attendances = a.data
    participations = Participation.objects.filter(subject=subject, _class=_class, student=student)
    p = ParticipationSerializer(data=participations, many=True)
    p.is_valid()
    participations = p.data
    sumx, sumy, sumxy, sumx2, sumy2, ac = [0, 0, 0, 0, 0, 0]
    n = len(scores)
    for score in scores:
        x = (mktime(ScoreTarget.objects.get(pk=score['target']).date.timetuple())/86400) - 19500
        y = score['score']
        sumy += y
        sumx += x
        sumxy += x*y
        sumx2 += pow(x, 2)
        sumy2 += pow(y, 2)
    for participation in participations:
        x = (mktime(Participation.objects.get(pk=participation['id']).date.timetuple())/86400) - 19500
        y = participation['score']
        sumy += y
        sumx += x
        sumxy += x*y
        sumx2 += pow(x, 2)
        sumy2 += pow(y, 2)
    if sesscount > 0:
        for attendance in attendances:
            if attendance['status'] == 'present': ac += 1
            if attendance['status'] == 'late': ac += 0.5
    if sumy > 0:
        b = ((sumx*sumy)-(n*sumxy))/(-(n*sumx2)+pow(sumx, 2))
        a = (sumy-(b*sumx))/n
        x = (datetime.datetime(2025, 8, 7, 0, 0).timestamp()/86400) - 19500
        res = a+(b*x)
        if sesscount > 0:
            res += -5+10*(ac/sesscount)
        avg = sumy/n
        if res > 100: res = 100
        if res < 0: res = 0
        return {"average": round(avg, 2), "prediction": round(res, 2), "A": a, "B": b}
    return {"average": 0, "prediction": 0, "A": 0, "B": 0}