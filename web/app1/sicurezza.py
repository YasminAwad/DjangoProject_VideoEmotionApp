from django.shortcuts import render, redirect
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponse

from .models import Video, Emotion, Client

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


def start(request):

    request.session.create()
    sk = request.session.session_key

    print(request.session.session_key)

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
    duration = float(request.GET.get('duration', None))
    time = 0

    start = timer()
    K.clear_session()

    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

    model = model_from_json(open("./facial_expression_model_structure.json", "r").read())
    model.load_weights('./facial_expression_model_weights.h5')

    #face_cascade = cv2.CascadeClassifier('C:/Users/Yasmin/Ppm/tensorflow-101-master/model/haarcascade_frontalface_default.xml')

    #model = model_from_json(open("C:/Users/Yasmin/Ppm/tensorflow-101-master/model/facial_expression_model_structure.json", "r").read())
    #model.load_weights('C:/Users/Yasmin/Ppm/tensorflow-101-master/model/facial_expression_model_weights.h5'

    emotions = ('arrabbiato', 'disgustato', 'impaurito', 'felice', 'triste', 'sorpreso', 'annoiato')

    cap = cv2.VideoCapture(0)

    frame = 0
    x = 0
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
        currentTime = float(request.GET.get('currentTime', None))
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
                x = x+1
                print(x)

                #print('-----------------------')

                angry = angry + round(predictions[0][0]*100, 2)
                disgust = disgust + round(predictions[0][1]*100, 2)
                fear = fear + round(predictions[0][2]*100, 2)
                happy = happy + round(predictions[0][3]*100, 2)
                sad = sad + round(predictions[0][4]*100, 2)
                surprise = surprise + round(predictions[0][5]*100, 2)
                neutral = neutral + round(predictions[0][6]*100, 2)
                '''print(angry, disgust, fear, happy, sad, surprise, neutral)'''

        #cv2.imshow('img',img)
        #K.clear_session()

        frame = frame + 1
        end = timer()
        time = end - start

        if (time > 10):
            m_emotion['arrabbiato'] = angry
            m_emotion['disgustato'] = disgust
            m_emotion['impaurito'] = fear
            m_emotion['felice'] = happy
            m_emotion['triste'] = sad
            m_emotion['sorpreso'] = surprise
            m_emotion['annoiato'] = neutral

            max_emotion = max(m_emotion, key=m_emotion.get)
            request.session['emotion'] = max_emotion
            request.session.save()

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

        if esci >= duration:
            K.clear_session()
            break
    #    if cv2.waitKey(1) & 0xFF == ord('q'):
    #        K.clear_session()
    #        break
    print('vai'+ currentTime)
    cap.release()
    cv2.destroyAllWindows()
    K.clear_session()
    return HttpResponse()

def emotionReading(request):
    em = request.session['emotion'];
    return HttpResponse(em)

def saveData(request):
    client = Client.objects.last()
    video = request.GET.get('idV', None)
    emotion = request.GET.get('data', None)
    time= request.GET.get('time', None)
    response= request.GET.get('response', None)
    titleV = request.GET.get('titleV', None)

    new_data = Emotion(client = client, time = time, video_id = video, response = response, emotion = emotion, titleV = titleV)
    new_data.save()

    print("emotion salvata")

    return HttpResponse(new_data)


def getData(request, pk):
    video = Video.objects.get(pk = pk)
    client = Client.objects.last()
    em = Emotion.objects.filter(client = (client)).values('emotion', 'response','time', 'titleV')
    context = {
        'em': em,
        'Video': video,
    }
    return render(request, "saveData.html", context)

def jsonData(request, pk):

    nClient = Emotion.objects.filter(video_id = pk, sequence = 1).values('sequence').annotate(nC=Count('sequence'))   #Conta il numero di Utenti
    em = Emotion.objects.filter(video_id = pk).values('emotion', 'sequence').annotate(nEmotion=Count('emotion'))    #Seleziona emozioni in base al video
    seq = Emotion.objects.filter(video_id = pk).values('sequence').distinct()   #mi dice quante sequenze ci sono
      #users_list = list(users)  # important: convert the QuerySet to a list object
    context = {'em': em, 'seq':seq, 'nClient': nClient}

    for n in nClient:     #Numero utenti
        nC ='Utenti', n['nC']

    with open("file.json", "w") as out:

            with open("file.json", "w") as out:
                                      #      1       2        3        4
                    json.dump(nC, out)   # 0 - 20, 20- 40, 40 - 60, 60 - 80
                    count = 0
                    for s in seq:
                        count = count
                        nS = 'Sequenza: ' + str( s['sequence']*20 - 20)+ '-' + str(s['sequence']*20), 'Emozioni:'
                        json.dump(nS, out, indent=4)

                        for e in em:
                            if s['sequence'] == e['sequence']:
                                emo =e['emotion'], e['nEmotion']
                                json.dump(emo, out)
#    out = open("file.json", "r")
    return render(request, "jsonData.html", context)
#    response(out, content_type='application/json')
    #return HttpResponse(out)
