# import libraries
import cv2
import face_recognition

# Get a reference to webcam 
video_capture = cv2.VideoCapture(0)

#Rescaling the window size of the video
def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

# Initialize variables
face_locations = []
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
gender_list = ['Male', 'Female']

gender_net = cv2.dnn.readNetFromCaffe('A:\Aadharsh\Repo\Face_Recognition\deploy_gender.prototxt', 'A:\Aadharsh\Repo\Face_Recognition\gender_net.caffemodel')

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    # Find all the faces in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)

    # Display the results
    for top, right, bottom, left in face_locations:
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 0), 2)

        #Get Face 
        face_img = frame[top:bottom, left:right].copy()
        blob = cv2.dnn.blobFromImage(face_img, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

        #Predict Gender
        gender_net.setInput(blob)
        gender_preds = gender_net.forward()
        gender = gender_list[gender_preds[0].argmax()]
        print("Gender : " + gender)

        overlay_text = "%s" % (gender)
        cv2.putText(frame, overlay_text, (left, top), 1, 1, (255, 255, 255), 2, cv2.LINE_AA)
       
    #Rescaling function call
    frame150 = rescale_frame(frame, percent=150)

    # Display the resulting image
    cv2.imshow('Video', frame150)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()