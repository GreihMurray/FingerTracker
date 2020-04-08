## Three important keys,
# q: will quit the application
# c: will start tracking mouse to finger
# r: will stop tracking mouse
#Keys may need to be pressed several times to take affect

import cv2
import pyautogui

#path to xml
fingerPath = "cascade.xml"
fingerCascade = cv2.CascadeClassifier(fingerPath)

#Start capturing webcam
video_capture = cv2.VideoCapture(0)

#Get size of screen
width, height = pyautogui.size()
#Size for video display
size = (width, height)

calib = False

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    #resize to 200 px lower than screen
    frame = cv2.resize(frame, size, interpolation= cv2.INTER_NEAREST)

    #Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Use cascade
    fingers = fingerCascade.detectMultiScale(
        gray,
        scaleFactor=1.4,
        minNeighbors=5,
        minSize=(100, 100),
        maxSize=(150, 150),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    #For each detected finger outlines, then checks if conditions
    for (x, y, w, h) in fingers:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, "Finger", (x - 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 255))

        #If c is pressed, considered calibrated, will start to track fingers
        if cv2.waitKey(1) & 0xFF == ord('c'):
            calib = True

        #If r is pressed reset calibration
        if cv2.waitKey(1) & 0xFF == ord('r'):
            calib = False

        #If calibrated, tracks mouse to finger
        if calib is True:
            #If the coordinates are onscreen move to inverted x, y
            if pyautogui.onScreen(x, y):
                pyautogui.moveTo(width - x, y)
            #Otherwise, go to predefined location
            else:
                pyautogui.moveTo(width/2, height/2)

    # Display the resulting frame
    if frame.shape[0] > 0 and frame.shape[1] > 0:
        cv2.imshow('Video', frame)
        cv2.moveWindow('Video', 0, 0)

    #Checks for user pressing q and quits if so
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #Checks for user pressing r and resets calibration if so
    if cv2.waitKey(1) & 0xFF == ord('r'):
        calib = False

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
