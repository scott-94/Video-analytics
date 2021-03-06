# Video-analytics
# Import the required modules 
import dlib
import cv2
import argparse as ap
import get_points_v2
import numpy as np


def run(source=0, dispLoc=False):
    # Create the VideoCapture object
    cam = cv2.VideoCapture(source)
    cam.set(0,20000)

    # If Camera Device is not opened, exit the program
#    if not cam.isOpened():
#        print "Video device or file couldn't be opened"
#        exit()
#    
#    print "Press key `p` to pause the video to start tracking"
#    while True:
#        # Retrieve an image and Display it.
#        retval, img = cam.read()
#        if not retval:
#            print "Cannot capture frame device"
#            exit()
#        if(cv2.waitKey(10)==ord('p')):
#            break
#        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
#        cv2.imshow("Image", img)
#    cv2.destroyWindow("Image")

    # Co-ordinates of objects to be tracked 
    # will be stored in a list named `points`
    retval, img = cam.read()
    points = get_points_v2.run(img, multi=True) 

    if not points:
        print "ERROR: No object to be tracked."
        exit()

    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.imshow("Image", img)

    # Initial co-ordinates of the object to be tracked 
    # Create the tracker object
    tracker = [dlib.correlation_tracker() for _ in xrange(len(points))]
    # Provide the tracker the initial position of the object
    [tracker[i].start_track(img, dlib.rectangle(*rect)) for i, rect in enumerate(points)]
    i=1
    j=1
    dist=[]
    temp=[]
    # j will be used for reading text file of coordinates
    frm=2
    mean_pt_detect=0
    mean_pt=0
    while True:
        dist=[]
        # Read frame from device or file
        retval, img = cam.read()
        if not retval:
            print "Cannot capture frame device | CODE TERMINATION :( "
            exit()
        # Update the tracker  
        for i in xrange(len(tracker)):
            dist=[]
            tracker[i].update(img)
            # Get the position of th object, draw a 
            # bounding box around it and display it.
            rect = tracker[i].get_position()
            pt1 = (int(rect.left()), int(rect.top()))
            pt2 = (int(rect.right()), int(rect.bottom()))
            mean_pt = ((int(rect.right())+int(rect.left()))/2,(int(rect.top())+int(rect.bottom()))/2)
#            print pt1
#            print pt2            
#            print mean_pt
            
            #getting points, need to take other points
            points = open("points/points_detect"+str(frm)+".txt","r")
            all_points = points.read().split(',')
            for i in range(len(all_points)-1) :
                all_points[i]=int(all_points[i])
            for j in range(0,len(all_points)-1,4):
                x1=all_points[j]
                y1=all_points[j+1]
                x2=all_points[j+2]
                y2=all_points[j+3]
                mean_pt_detect = ((x1+x2)/2,(y1+y2)/2)
                dist.append(np.sqrt(np.square(mean_pt_detect[0]-mean_pt[0]) + np.square(mean_pt_detect[1]-mean_pt[1])))
                print dist
            ind=np.argmin(dist)
            print dist[ind]
            temp.append(dist[ind])
#            if dist[ind]<5 :
#                pt1=((int(all_points[ind])+int(rect.left()))/2,(int(rect.top())+int(all_points[ind+1]))/2)
#                pt2=((int(rect.right())+int(all_points[ind+2]))/2,(int(all_points[ind+3])+int(rect.bottom()))/2)
            pt1=(int(all_points[ind]),int(all_points[ind+1]))
            pt2=(int(all_points[ind+2]),int(all_points[ind+3]))          
            
            # compare pts_1 and pts_2 pt1 and pt2
            cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)
            #print "Object {} tracked at [{}, {}] \r".format(i, pt1, pt2),
            if dispLoc:
                loc = (int(rect.left()), int(rect.top()-20))
	        txt = "Object tracked at [{}, {}]".format(pt1, pt2)
	        cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 1)
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Image", img)
        # Continue until the user presses ESC key
        if cv2.waitKey(1) == 27:
            break
        frm+=1

    # Relase the VideoCapture object
    cam.release()

if __name__ == "__main__":
    # Parse command line arguments
    parser = ap.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', "--deviceID", help="Device ID")
    group.add_argument('-v', "--videoFile", help="Path to Video File")
    parser.add_argument('-l', "--dispLoc", dest="dispLoc", action="store_true")
    args = vars(parser.parse_args())

    # Get the source of video
    if args["videoFile"]:
        source = args["videoFile"]
    else:
        source = int(args["deviceID"])
    run(source, args["dispLoc"])
