# Standard imports
import cv2
import imutils
import numpy as np;

# Setup SimpleBlobDetector parameters.
#params = cv2.SimpleBlobDetector_Params()
 
 #Change thresholds
#params.minThreshold = 10000;
#params.maxThreshold = 20000;
 
#params.filterByColor=1
#params.blobColor = 0 
 
# Filter by Area.
#params.filterByArea = False
#params.minArea = 1
 
# Filter by Circularity
#params.filterByCircularity = False
#params.minCircularity = 0.1
 
# Filter by Convexity
#params.filterByConvexity = False
#params.minConvexity = 0.87
 
# Filter by Inertia
#params.filterByInertia = True
#params.minInertiaRatio = 0.01
 
# Create a detector with the parameters
#ver = (cv2.__version__).split('.')
#if int(ver[0]) < 3 :
    #detector = cv2.SimpleBlobDetector(params)
#else : 
    #detector = cv2.SimpleBlobDetector_create(params)

 
# Read image
im = cv2.VideoCapture("/home/musigma/Desktop/carnival.mp4")
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
im.set(0,130000)
ret = True
count = 0
cnt=0
while(ret):
	ret,frame = im.read()
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	ret,frame = cv2.threshold(frame,115,255,cv2.THRESH_TOZERO)
	#frame = cv2.adaptiveThreshold(frame,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
	frame = imutils.resize(frame, width=500)
# Set up the detector with default parameters.
        detector = cv2.SimpleBlobDetector()
# Detect blobs.
        m = 18/float(11)
        c = -5724/float(11)
        #print c
        #print m
        x = 1 
        l = []
        z = []
        while (x<500):
           y = 40
           while (y<205):
              if int(y) == int((m*x) + c):
                 l.append([x,y])
              y+=1
           x+=1
        m1 = 73/float(41)
        c1 = -22534/float(41)
        #print c
        #print m
        x1 = 1 
        l1 = []
        while (x1<489):
           y1 = 40
           while (y1<220):
              if int(y1) == int((m1*x1) + c1):
                 l1.append([x1,y1])
              y1+=1
           x1+=1

        keypoints = detector.detect(frame)
        for keyPoint in keypoints:
           c = len(keypoints)
           p = keyPoint.pt[0]
           q = keyPoint.pt[1]
           p =int(p)
           q =int(q)
           s=p
           t=q
           r=q
           while (p<(s+10)):
              q=r
              while (q<(t+4)) :
                 z.append([p,q])
                 #print (p,q)
                 #if [p,q] in l:
                    #print ("highalert")
                 q+=1
              p+=1
           zl=len(z)
           ll=len(l)   
           i = 1 
           j = 1
           while (i<zl):
              j = 1
              while (j<ll):
                 if z[i] == l[j]:
                    print (str(z[i])+"standing on edge")
                    cv2.putText(frame, "standing on edge", (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                 if z[i] ==l1[j] and z[i][0]!=366 and z[i][0]!=367 and z[i][0]!=368:
                    print (str(z[i])+"Falling down")
                    cv2.putText(frame, "Falling down", (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                 j+=1
              i+=1
        #print z
        #print l            
            
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
        im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        #img = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.line(im_with_keypoints, (348, 70), (430,216), (0,0,255), 2) 
        cv2.line(im_with_keypoints, (351, 54), (445,207), (0,255,0), 2)
        out.write(im_with_keypoints)
        cv2.imshow('IMG',im_with_keypoints)
        cv2.imwrite("img/frame_"+str(cnt)+".jpg",im_with_keypoints)
        cnt += 1
        #cv2.imshow('rgb',img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
           break           
out.release()
