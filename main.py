import cat_detector as detect
import webcam_save as camera



def main():
    detect.init()
    camera.init()

    print('press enter to take a picture')
    _ = input()

    camera.take_photo()
    print(detect.isPittin())

if __name__ == '__main__':
    main()

