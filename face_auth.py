# # import cv2
# # import pickle
# # import os
# # import time

# # def authenticate(selected_user):
# #     # -------- SAFETY CHECKS --------
# #     if not os.path.exists("model/face_model.yml"):
# #         print("Error: Face model (yml) not found. Please train the model first.")
# #         return False

# #     if not os.path.exists("model/labels.pkl"):
# #         print("Error: Label mapping (pkl) not found.")
# #         return False

# #     # Initialize LBPH Recognizer
# #     model = cv2.face.LBPHFaceRecognizer_create()
# #     model.read("model/face_model.yml")

# #     # Load the label mapping {ID: folder_name}
# #     with open("model/labels.pkl", "rb") as f:
# #         label_map = pickle.load(f)

# #     face_cascade = cv2.CascadeClassifier(
# #         cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
# #     )

# #     cam = cv2.VideoCapture(0)
# #     verified = False
# #     start_time = time.time()
# #     timeout = 15  # 15 seconds to verify

# #     while True:
# #         ret, frame = cam.read()
# #         if not ret:
# #             break
            
# #         frame = cv2.flip(frame, 1)
# #         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# #         faces = face_cascade.detectMultiScale(gray, 1.3, 5)

# #         for (x, y, w, h) in faces:
# #             # Predict the face
# #             label_id, confidence = model.predict(gray[y:y+h, x:x+w])
            
# #             # Retrieve the folder name associated with the predicted ID
# #             predicted_user = label_map.get(label_id)

# #             # --- STRICT SECURITY LOGIC ---
# #             # 1. predicted_user MUST match the selected_user folder
# #             # 2. Confidence must be low (LBPH: < 55 is high accuracy, > 80 is likely a guess)
# #             if predicted_user == selected_user and confidence < 55:
# #                 verified = True
# #                 color = (0, 255, 0) # Green
# #                 status_text = f"Verified: {predicted_user}"
# #             else:
# #                 color = (0, 0, 255) # Red
# #                 status_text = "ACCESS DENIED: Identity Mismatch"

# #             # Visual Feedback
# #             cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
# #             cv2.putText(frame, status_text, (x, y-10),
# #                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
# #             # Show confidence for debugging (optional, remove for production)
# #             cv2.putText(frame, f"Conf: {round(confidence)}", (x, y+h+20),
# #                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

# #         cv2.imshow("Secure Face Authentication", frame)

# #         # Break if verified, ESC pressed, or timeout reached
# #         if verified:
# #             time.sleep(1) # Brief pause to show green box
# #             break
        
# #         if cv2.waitKey(1) == 27 or (time.time() - start_time) > timeout:
# #             break

# #     cam.release()
# #     cv2.destroyAllWindows()
    
# #     # Final console log for security audit
# #     if verified:
# #         print(f"✅ [AUTH SUCCESS] Identity matched for {selected_user}")
# #     else:
# #         print(f"❌ [AUTH FAILED] Identity could not be verified for {selected_user}")
        
# #     return verified

# import cv2, pickle, os, time

# def authenticate(selected_user):
#     if not os.path.exists("model/face_model.yml"): return False
#     model = cv2.face.LBPHFaceRecognizer_create()
#     model.read("model/face_model.yml")
#     with open("model/labels.pkl", "rb") as f: label_map = pickle.load(f)
#     detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
#     cam = cv2.VideoCapture(0)
#     start = time.time()
#     while time.time() - start < 15:
#         ret, frame = cam.read()
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = detector.detectMultiScale(gray, 1.3, 5)
#         for (x,y,w,h) in faces:
#             lab, conf = model.predict(gray[y:y+h, x:x+w])
#             if label_map.get(lab) == selected_user and conf < 55:
#                 cam.release(); cv2.destroyAllWindows(); return True
#         cv2.imshow("Authenticating...", frame)
#         if cv2.waitKey(1) == 27: break
#     cam.release(); cv2.destroyAllWindows(); return False
import cv2, pickle, os, time

def authenticate(selected_user):
    if not os.path.exists("model/face_model.yml"): return False
    
    model = cv2.face.LBPHFaceRecognizer_create()
    model.read("model/face_model.yml")
    
    with open("model/labels.pkl", "rb") as f: 
        label_map = pickle.load(f)
    
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    cam = cv2.VideoCapture(0)
    start = time.time()
    
    while time.time() - start < 15: # 15s timeout
        ret, frame = cam.read()
        if not ret: break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        
        for (x,y,w,h) in faces:
            # Predict returns (label_id, confidence)
            lab_id, conf = model.predict(gray[y:y+h, x:x+w])
            predicted_folder = label_map.get(lab_id)

            # SECURITY CHECK: Predicted folder must match the logged-in folder
            if predicted_folder == selected_user and conf < 50:
                cam.release()
                cv2.destroyAllWindows()
                return True
            else:
                # Visual feedback for mismatch
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2)
                cv2.putText(frame, "Identity Mismatch", (x, y-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

        cv2.imshow("Secure Face Verification", frame)
        if cv2.waitKey(1) == 27: break
        
    cam.release()
    cv2.destroyAllWindows()
    return False