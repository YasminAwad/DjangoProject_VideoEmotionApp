# DjangoProject_VideoEmotionApp

This project was carried out in 2019 toghether with [Niki Di Costanzo](https://github.com/NikiDicostanzo).

## Goals:
- allow video playback
- detect users facial expressions when viewing videos
- suggest feelings to the user based on what has been detected
- save the feeling detected and the user's response in a database (associating the relative time moment of the video)
- allow access to multiple sessions
- allow the visualization of the statistics of each video and the download of its json file

#### To carry out the project were used:
- [Django](https://www.djangoproject.com/)
- [Expression Detector](https://github.com/serengil/tensorflow-101/)

### Views realized:
- __emotion__: contains the code to detect facial expressions. Triggered via an Ajax call after pressing the play button. This view saves in a session variable (emotion) the average of the emotions detected every 10 seconds.
- __emotionReading__: allows the exchange of information with javascript (video_detail.js), in particular to pass the detected emotions. This is done through the use of a json file (dictionary).
- __videoDet__: allows you to view a specific video.
- __saveStat__: updates the database by adding a row in the Statistics model. It is called when the user answers a question.
- __getStat__: allows you to view the contents of the Statistics model.

### Images of the final product
<img src="https://github.com/YasminAwad/DjangoProject_VideoEmotionApp/blob/main/final_images/start.PNG" width="400" /> <img src="https://github.com/YasminAwad/DjangoProject_VideoEmotionApp/blob/main/final_images/home.PNG" width="400" />
<img src="https://github.com/YasminAwad/DjangoProject_VideoEmotionApp/blob/main/final_images/video1.PNG" width="400" /> <img src="https://github.com/YasminAwad/DjangoProject_VideoEmotionApp/blob/main/final_images/video2.PNG" width="400" />
<img src="https://github.com/YasminAwad/DjangoProject_VideoEmotionApp/blob/main/final_images/statistics.PNG" width="400" />
