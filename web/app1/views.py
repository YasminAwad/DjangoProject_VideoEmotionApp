from django.shortcuts import render, redirect
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponse

from .models import Video, Emotion, Client, Statistics

from timeit import default_timer as timer
from django.template import loader
import sys
from pkg_resources import resource_filename
import numpy as np
import cv2
from keras.preprocessing import image
import time
from keras.models import model_from_json
from keras import backend as K
from django.db.models import Count
from django.core import serializers
import json



def start(request):

    request.session.create()
    sk = request.session.session_key

    #print(request.session.session_key)

    new_client = Client(client_id = sk)
    new_client.save()
    context = {'Client': new_client}

    return render(request, "start.html", context)

def home(request):
    video = Video.objects.all()
    context = {
        'Video' : video}
    request.session['emotion'] = 'error';  # variabile di sessione dove ci salvo emozione
    print(request.session.session_key)

    return render(request, "home.html", context)


def videoDet(request, pk):
    video = Video.objects.get(pk = pk)
    context = {'Video' : video}
    return render(request, "video_detail.html", context)


def emotion(request):
    duration = int(request.GET.get('duration', 0))
    time = 0
    sum = 0
    start = timer()
    K.clear_session()
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

    model = model_from_json(open("./facial_expression_model_structure.json", "r").read())
    model.load_weights('./facial_expression_model_weights.h5')


    #face_cascade = cv2.CascadeClassifier('C:/Users/yasmi/PPM/tensorflow-101-master/model/haarcascade_frontalface_default.xml')

    #model = model_from_json(open("C:/Users/yasmi/PPM/tensorflow-101-master/model/facial_expression_model_structure.json", "r").read())
    #model.load_weights('C:/Users/yasmi/PPM/tensorflow-101-master/model/facial_expression_model_weights.h5')

    emotions = ('arrabbiato', 'disgustato', 'impaurito', 'felice', 'triste', 'sorpreso', 'annoiato')



    frame = 0

    time = 0

    angry = 0
    disgust = 0
    fear = 0
    happy = 0
    sad = 0
    surprise = 0
    neutral = 0

    m_emotion = {
        "arrabbiato" : 0,
        "disgustato" : 0,
        "impaurito" : 0,
        "felice" : 0,
        "triste" : 0,
        "sorpreso" : 0,
        "annoiato" : 0
    }


    finito = timer()

    # 0 angry, 1 disgust, 2 fear, 3 happy, 4 sad, 5 surprise, 6 neutral
    while(True):
        currentTime = int(request.GET.get('currentTime', 0))

        #pausa = int(request.GET.get('g', None))
        #print(currentTime)
        ret, img = cap.read()

        img = cv2.resize(img, (640, 360))
        img = img[0:308,:]

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)



        for(x,y,w,h) in faces:
            if w > 130:

                detected_face = img[int(y):int(y+h), int(x):int(x+w)]
                detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY)
                detected_face = cv2.resize(detected_face, (48,48))

                img_pixels = image.img_to_array(detected_face)
                img_pixels = np.expand_dims(img_pixels, axis = 0)

                img_pixels /= 255 #pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]

                predictions = model.predict(img_pixels) #store probabilities of 7 expressions
                max_index = np.argmax(predictions[0])

                overlay = img.copy()
                opacity = 0.4
                cv2.rectangle(img,(x+w+10,y-25),(x+w+150,y+115),(64,64,64),cv2.FILLED)
                cv2.addWeighted(overlay, opacity, img, 1 - opacity, 0, img)

                cv2.line(img,(int((x+x+w)/2),y+15),(x+w,y-20),(255,255,255),1)
                cv2.line(img,(x+w,y-20),(x+w+10,y-20),(255,255,255),1)

                emotion = ""

                for i in range(len(predictions[0])):
                    emotion = "%s %s%s" % (emotions[i], round(predictions[0][i]*100, 2), '%')

                    color = (255,255,255)

                    cv2.putText(img, emotion, (int(x+w+15), int(y-12+i*20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                    #print(emotion)


                #print('-----------------------')

                angry = angry + round(predictions[0][0]*100, 2)
                disgust = disgust + round(predictions[0][1]*100, 2)
                fear = fear + round(predictions[0][2]*100, 2)
                happy = happy + round(predictions[0][3]*100, 2)
                sad = sad + round(predictions[0][4]*100, 2)
                surprise = surprise + round(predictions[0][5]*100, 2)
                neutral = neutral + round(predictions[0][6]*100, 2)
                sum = sum +1
                #print(sum, disgust)
                #print(angry, disgust, fear, happy, sad, surprise, neutral)'''

        #cv2.imshow('img',img)
        #K.clear_session()

        frame = frame + 1
        end = timer()
        time = end - start

        if (time > 10):
            if(sum != 0):
                m_emotion['arrabbiato'] = round(angry/sum, 0)
                m_emotion['disgustato'] = round(disgust/sum, 0)
                m_emotion['impaurito'] = round(fear/sum, 0)
                m_emotion['felice'] = round(happy/sum, 0)
                m_emotion['triste'] = round(sad/sum, 0)
                m_emotion['sorpreso'] = round(surprise/sum, 0)
                m_emotion['annoiato'] = round(neutral/sum, 0)


            e_m = {}
            for key, value in sorted(m_emotion.items(), key=lambda item: item[1], reverse= True):
                e_m[key] = value
            #max_emotion = max(m_emotion, key=m_emotion.get)


            request.session['emotion'] = e_m
            request.session.save()

            sum = 0
            angry = 0
            disgust = 0
            fear = 0
            happy = 0
            sad = 0
            surprise = 0
            neutral = 0
            x = 0
            time = 0
            start = timer()


        finitoEnd = timer()
        esci = finitoEnd - finito + currentTime

        if cv2.waitKey(0) and esci >= duration:
            print('break')
        #    K.clear_session()
            break
    #    if cv2.waitKey(1) & 0xFF == ord('q'):
    #        K.clear_session()
    #        break

    cap.release()

    cv2.destroyAllWindows()
    K.clear_session()
    return HttpResponse(m_emotion)



def emotionReading(request):
    em = request.session.get('emotion');
    with open('e_m.json', 'w') as out:
        data = json.dump(em, out)
    v = open('e_m.json', 'r')
    return HttpResponse(v)

def saveData(request):
    client = Client.objects.last()
    sk = client.pk
    cl = Client.objects.get(pk = sk)
    video = request.GET.get('idV', None)

    #time= request.GET.get('time', None)
    response= request.GET.get('response', None)
    titleV = request.GET.get('titleV', None)

    sequence= request.GET.get('sequence', None)

    new_data = Emotion(client = cl, video_id = video, response = response, titleV = titleV, sequence = sequence )
    new_data.save()

    return HttpResponse(new_data)


def getData(request, pk):
    client = Client.objects.last()
    video = Video.objects.get(pk = pk)
    em = Emotion.objects.filter(client = (client)).values('emotion', 'response', 'titleV', 'sequence')
    context = {'em': em,
               'Video' : video}
    return render(request, "saveData.html", context)


def saveStat(request):

    sequence = request.GET.get('sequence', 0)
    response = request.GET.get('response', None)
    pk = int(request.GET.get('idV', None))

    print(sequence)

    stat_control = Statistics.objects.filter(video_id = pk, sequence = sequence)

    if stat_control.exists():
        stat = Statistics.objects.get(video_id = pk, sequence = sequence)
        if(response == "arrabbiato"):
            stat.arrabbiato = stat.arrabbiato + 1
        if(response == "felice"):
            stat.felice = stat.felice + 1
        if(response == "triste"):
            stat.triste = stat.triste + 1
        if(response == "disgustato"):
            stat.disgustato = stat.disgustato + 1
        if(response == "sorpreso"):
            stat.sorpreso = stat.sorpreso + 1
        if(response == "annoiato"):
            stat.annoiato = stat.annoiato + 1
        if(response == "impaurito"):
            stat.impaurito = stat.impaurito + 1

        stat.save()

    else:
        stat = Statistics(video_id = pk, arrabbiato = 0, felice = 0, triste = 0, disgustato = 0, sorpreso = 0, annoiato = 0, impaurito = 0, sequence = sequence)
        stat.save()

        if(response == "arrabbiato"):
            stat.arrabbiato = stat.arrabbiato + 1
        if(response == "felice"):
            stat.felice = stat.felice + 1
        if(response == "triste"):
            stat.triste = stat.triste + 1
        if(response == "disgustato"):
            stat.disgustato = stat.disgustato + 1
        if(response == "sorpreso"):
            stat.sorpreso = stat.sorpreso + 1
        if(response == "annoiato"):
            stat.annoiato = stat.annoiato + 1
        if(response == "impaurito"):
            stat.impaurito = stat.impaurito + 1
        stat.save()

    print(stat)

    return HttpResponse(stat)


def getStat(request, pk):
    video = Video.objects.get(pk = pk)
    stat = Statistics.objects.filter(video_id = pk)
    context = {
        'Stat' : stat,
        'Video' : video,
    }

    return render(request, "getStat.html", context)
