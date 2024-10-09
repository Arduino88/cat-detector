import cv2

def init():
    global cam_port
    cam_port = 1
     


def take_photo():
    
    # reading the input using the camera
    cam = cv2.VideoCapture(cam_port)
    result, image = cam.read() 

    # If image will detected without any error,  
    # show result 
    if result:
        cv2.imwrite('cat-detector/data/cats-photos/test/unknown/image.jpg', image) # MAKE DUPLICATE FILE TO TAKE PHOTOS OF CATS WITH WEBCAM
        cam.release()

    else:
        print("No image")

if __name__ == "__main__":
    take_photo()
  