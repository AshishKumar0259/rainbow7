import cv2
import numpy as np
from keras.models import load_model

model = load_model('D:\GitHub_Projects\SmartCameraDetection\web\CODE\dataset.h5')


faceDetect=cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')

labels_dict={0:'Human',1:'cats', 2:'dogs'}



class Video(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        global value
        ret,frame = self.video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 3)

        for x, y, w, h in faces:
            sub_face_img = gray[y:y + h, x:x + w]
            resized = cv2.resize(sub_face_img, (50, 50))
            normalize = resized / 255.0
            reshaped = np.reshape(normalize, (1, 50, 50, 1))
            result = model.predict(reshaped)
            label = np.argmax(result, axis=1)[0]
            print(label)

            print(labels_dict[label])



            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
            cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
            cv2.putText(frame, labels_dict[label], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        ret,jpg = cv2.imencode('.jpg',frame)
        return jpg.tobytes()
