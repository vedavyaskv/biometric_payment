# import cv2
# import time

# def blink_verification():
#     # Load cascades
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
#     eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

#     cam = cv2.VideoCapture(0)
#     if not cam.isOpened():
#         return False

#     blink_count = 0
#     consecutive_closed_frames = 0
#     EYE_CLOSED_THRESHOLD = 2  # Must be closed for at least 2 frames
#     EYE_OPEN_REQUIRED = True  # Flag to ensure eyes were open before counting a blink
    
#     start_time = time.time()
#     timeout = 20 # Give user 20 seconds to blink properly

#     while True:
#         ret, frame = cam.read()
#         if not ret: break

#         frame = cv2.flip(frame, 1)
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#         eyes_detected = False

#         for (x, y, w, h) in faces:
#             roi_gray = gray[y:y+h, x:x+w]
#             # Precise eye detection
#             eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 10) 

#             if len(eyes) >= 2:
#                 eyes_detected = True
            
#             cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)

#         # -------- SECURE BLINK LOGIC --------
#         if eyes_detected:
#             # If eyes are open and we previously met the closed threshold, count the blink
#             if consecutive_closed_frames >= EYE_CLOSED_THRESHOLD:
#                 blink_count += 1
#                 # Reset closed frames counter
#                 consecutive_closed_frames = 0
#             EYE_OPEN_REQUIRED = True 
#         else:
#             # If eyes are NOT detected (closed), increment counter
#             if EYE_OPEN_REQUIRED:
#                 consecutive_closed_frames += 1

#         # --- UI FEEDBACK ---
#         # Show status
#         status_color = (0, 255, 0) if eyes_detected else (0, 0, 255)
#         status_text = "EYES OPEN" if eyes_detected else "EYES CLOSED (BLINKING)"
        
#         cv2.putText(frame, f"STATUS: {status_text}", (30, 40), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        
#         cv2.putText(frame, f"Proper Blinks: {blink_count}/2", (30, 80), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
        
#         cv2.putText(frame, "Look into the camera and blink naturally", (30, 450), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

#         cv2.imshow("Secure Liveness Verification", frame)

#         # Break on success
#         if blink_count >= 2:
#             # Visual confirmation before closing
#             cv2.putText(frame, "LIVENESS VERIFIED!", (150, 250), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 4)
#             cv2.imshow("Secure Liveness Verification", frame)
#             cv2.waitKey(1000) # Wait 1 second so user sees success
#             break

#         # Break on timeout or ESC
#         if time.time() - start_time > timeout or cv2.waitKey(1) == 27:
#             cam.release()
#             cv2.destroyAllWindows()
#             return False

#     cam.release()
#     cv2.destroyAllWindows()
#     return True if blink_count >= 2 else False
import cv2, time

def blink_verification():
    face_cas = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eye_cas = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
    cam = cv2.VideoCapture(0)
    blinks, closed_f = 0, 0
    start = time.time()
    
    while time.time() - start < 20:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cas.detectMultiScale(gray, 1.3, 5)
        eyes_seen = False
        for (x,y,w,h) in faces:
            roi = gray[y:y+h, x:x+w]
            eyes = eye_cas.detectMultiScale(roi, 1.1, 10)
            if len(eyes) >= 2: eyes_seen = True
        
        if not eyes_seen: closed_f += 1
        else:
            if closed_f >= 2: blinks += 1
            closed_f = 0
            
        cv2.putText(frame, f"Blinks: {blinks}/2", (30,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.imshow("Liveness Test", frame)
        if blinks >= 2: 
            cam.release(); cv2.destroyAllWindows(); return True
        if cv2.waitKey(1) == 27: break
    cam.release(); cv2.destroyAllWindows(); return False