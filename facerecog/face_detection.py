#import essentials
import cv2
import os
import pickle
import numpy as np
# from PIL import Image
import face_recognition
from datetime import datetime
# from mtcnn.mtcnn import MTCNN
# from keras.models import load_model
# from keras.preprocessing import image
# from keras.preprocessing.image import img_to_array
from backend.settings import BASE_DIR, MODEL_ROOT, MEDIA_ROOT


start = datetime.now()

# create the detector, using default weights
# detector = MTCNN()

# define paths
BASE_DIR = MEDIA_ROOT
MODEL_DIR =  os.path.join(MODEL_ROOT,"user_face_encodings") 
print(MODEL_DIR)
if os.path.isdir(MODEL_DIR):
    pass
else:
    os.mkdir(MODEL_DIR)


#load existing models

if os.path.exists(MODEL_DIR + "/encodings.pickle"):
    with (open(os.path.join(MODEL_DIR,"encodings.pickle"), "rb")) as openfile:
        while True:
            try:
                users_data = pickle.load(openfile)
                known_face_encodings = users_data["encodings"]
                known_face_names  = users_data["names"]
                print("*"*20, "Model LOADED successfully", "*"*20)
            except EOFError:
                break

            
#function to match faces
def recognise_face(roi, faces):
    """this function checks the faces and returns detected users
    face_recognition api is used here"""
    face_locations = []
    face_locations.append(faces)
    #print(face_locations)
    face_encodings = face_recognition.face_encodings(roi, face_locations)
    # print("This is face_encodings", face_encodings)
    face_names = []
    det_user=[]
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        # print("this is kfe", known_face_encodings)

        #compare if all value of match is true
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        best_match_index = np.argmin(face_distances)

        if matches[best_match_index] and face_distances[best_match_index] <= 0.45:
            name = known_face_names[best_match_index]
            print("Name:-->", name)              #Check: detected users
            return name
        else:
            return "Unknown"    
   
    #     # print("This is matches[best_mactch_index] -- >", matches[best_match_index])
    #     if matches[best_match_index]:
    #         name = known_face_names[best_match_index]
    #         det_user.append(name)
    #         print("Name:-->", name)              #Check: detected users
    
    # return det_user[0]
    

def det_recog_engine(frame, recog = True):
    """This function will detect faces and returns bounding boxes
    if the boolean of recog is set true then detected faces are returned
    with name"""
    detected_users_list = []   
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb, model = 'hog')
    #print("Faces detected, ", len(faces))   #chcek for number of faces detected
    for face in face_locations:
            try:
                #print(face, type(face))
                y,width,height,x= face   
                if recog==True:
                    detected_user = recognise_face(rgb, face)
                    detected_users_list.append(detected_user)
                    cv2.putText(frame, detected_user, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)    
                # get coordinates
                frame = cv2.rectangle(frame, (x,y), (width, height), (255,0,0), 1)
                # cv2.imwrite("recognized.jpg", frame)  #check for image output
                # cv2.imshow("recog", frame)   #check for knowing detected faces
            except:
                # cv2.imwrite("recognized.jpg", frame)
                return frame, detected_users_list
    print("here")            
    return frame, detected_users_list