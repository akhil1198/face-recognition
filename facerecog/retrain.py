import face_recognition
import pickle
import cv2
import os
from datetime import datetime
from backend.settings import BASE_DIR, MEDIA_ROOT, MODEL_ROOT


#define paths
USER_PIC_DIR = MEDIA_ROOT
MODEL_DIR =  os.path.join(MODEL_ROOT,"user_face_encodings") 

def retrain():
	start = datetime.now()
	#load existing models to check changes
	# CHANGE 2 roadBlock 2
	prev_users_count = 0
	if os.path.exists(MODEL_DIR + "/encodings.pickle"):
		with (open(os.path.join(MODEL_DIR,"encodings.pickle"), "rb")) as openfile:
			while True:
				try:
					users_data = pickle.load(openfile)
				except EOFError:
					break
		prev_users_count = len(set(users_data['names']))
	# initialize the list of known encodings and known names
	knownEncodings = []
	knownNames = []

	#get names and update encoding lists
	for users in os.listdir(USER_PIC_DIR):
		#get ENcodings
		user_path = os.path.join(USER_PIC_DIR,users)
		for user_image_path in os.listdir(user_path):
			if user_image_path.endswith(".jpg") or user_image_path.endswith(".jpeg") :
				image = cv2.imread(os.path.join(user_path,user_image_path))
				rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
				# detect the (x, y)-coordinates of the bounding boxes
				# corresponding to each face in the input image
				boxes = face_recognition.face_locations(rgb,model='hog')
				# compute the facial embedding for the face
				encodings = face_recognition.face_encodings(rgb, boxes)
				for encoding in encodings:
					if len(encoding)>0:
						#update encodings
						knownEncodings.append(encoding)
						#update user names
						knownNames.append(users)

	reg_users_face_encodings = {"encodings": knownEncodings, "names": knownNames}
	f = open(os.path.join(MODEL_DIR,"encodings.pickle"), "wb")
	f.write(pickle.dumps(reg_users_face_encodings))
	f.close()


	updated_users_count = len(set(reg_users_face_encodings['names']))
	print("{0} New users added".format(updated_users_count-prev_users_count))
	print("Retrained {0} users and updated {1} encodings in {2}".format(updated_users_count, len(knownEncodings), datetime.now()-start))
	return ("Retrained {0} users and updated {1} encodings in {2}".format(updated_users_count, len(knownEncodings), datetime.now()-start))
