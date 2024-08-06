# camera.py

import cv2
import PIL.Image
from PIL import Image
import argparse
import shutil
class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        
        self.video = cv2.VideoCapture(0)
        self.k=1
        #cap = self.video
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        #self.video = cv2.VideoCapture('video.mp4')

        # Check if camera opened successfully
        #if (cap.isOpened() == False): 
        #  print("Unable to read camera feed")

        # Default resolutions of the frame are obtained.The default resolutions are system dependent.
        # We convert the resolutions from float to integer.
        #frame_width = int(cap.get(3))
        #frame_height = int(cap.get(4))

        # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
        #self.out = cv2.VideoWriter('video.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))


        
    
    def __del__(self):
        self.video.release()
        
    
    def get_frame(self):
        success, image = self.video.read()
        #self.out.write(image)

        cv2.imwrite("getimg.jpg", image)
        
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # Read the frame
        #_, img = cap.read()

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Draw the rectangle around each face
        j = 1

        ff=open("user.txt","r")
        uu=ff.read()
        ff.close()

        ff1=open("photo.txt","r")
        uu1=ff1.read()
        ff1.close()

        ###
        if self.k<=40:
            self.k+=1
            fnn=""
            fnn=uu+"_"+str(self.k)+".jpg"
            

            ff2=open("det.txt","w")
            ff2.write(str(self.k))
            ff2.close()
            if uu1=="2":
                mm3 = PIL.Image.open('getimg.jpg')
                rz3 = mm3.resize((300,300), PIL.Image.ANTIALIAS)
                rz3.save("image.jpg")
                shutil.copy('image.jpg', 'static/frame/'+fnn)
            
            
        
        ###########################################
        ###########################################
        
        '''for (x, y, w, h) in faces:
            mm=cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imwrite("myface.jpg", mm)

            
            image = cv2.imread("myface.jpg")
            cropped = image[y:y+h, x:x+w]
            gg="f"+str(j)+".jpg"
            cv2.imwrite("faces/"+gg, cropped)

            ###
            if self.k<=40:
                self.k+=1
                fnn=""
                fnn=uu+"_"+str(self.k)+".jpg"
                

                ff2=open("det.txt","w")
                ff2.write(str(self.k))
                ff2.close()
                if uu1=="2":
                    cv2.imwrite("static/frame/"+fnn, cropped)
                
                mm2 = PIL.Image.open('faces/'+gg)
                rz = mm2.resize((100,100), PIL.Image.ANTIALIAS)
                rz.save('faces/'+gg)
                
            j += 1

        ff4=open("img.txt","w")
        ff4.write(str(j))
        ff4.close()  '''  

            

        

            
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
