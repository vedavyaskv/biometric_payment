import cv2

def authenticate_face():
    model = cv2.face.LBPHFaceRecognizer_create()
    model.read("model/face_model.yml")

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cam = cv2.VideoCapture(0)
    verified = False

    while True:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            _, confidence = model.predict(gray[y:y+h, x:x+w])
            if confidence < 50:
                verified = True
                cv2.putText(frame, "Verified", (x,y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        cv2.imshow("Face Authentication", frame)
        if verified or cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()
    return verified
