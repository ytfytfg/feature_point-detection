import cv2
import time
import dlib 

def video_init(is_2_write=False,save_path=None):
    writer = None
    cap = cv2.VideoCapture(0)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)#default 480
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)#default 640

    if is_2_write is True:
        fourcc = cv2.VideoWriter_fourcc(*'divx')
        if save_path is None:
            save_path = 'demo.avi'
        writer = cv2.VideoWriter(save_path, fourcc, 30, (int(width), int(height)))

    return cap,height,width,writer

def Dlib_face_detection(use_CUDA=True):
    #----var
    frame_count = 0
    FPS = "FaceDetect"
    no_face_str = "No faces detected"
    show_facial_points = False
    
    #----video streaming init
    cap, height, width, writer = video_init(is_2_write=False)

    #----Dlib init
    detector = dlib.get_frontal_face_detector()
    detector_cnn = dlib.cnn_face_detection_model_v1('mmod_human_face_detector.dat')
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    color = (0,255,0)

    #----video nonstop capture
    while (cap.isOpened()):

        #----get image
        ret, img = cap.read()

        if ret is True:
            #----img preprocess
            # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            #----face detection
            if use_CUDA is True:
                faces = detector_cnn(img, 0)#if the digit is 1, the img will be resized double. The detection speed will decline
            else:
                faces, scores, idx = detector.run(img, 0)

            #----face analysis
            if (len(faces) > 0):
                for k, d in enumerate(faces):
                    if use_CUDA is True:
                        d = d.rect
                    #----draw rectangles on faces
                    cv2.rectangle(img, (d.left(), d.top()), (d.right(), d.bottom()), color,2)
                    if use_CUDA is False:
                        cv2.rectangle(img, (d.left(), d.top()), (d.right(), d.bottom()), color,2)
                        cv2.putText(img, str('%6s %.2f %4s %1d'%('scores:',scores[k],'idx:',idx[k])), (d.left(), d.top()), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)


                    #----draw 68 points of face characteristics
                    if show_facial_points is True:
                        shape = predictor(img, d)
                        for i in range(68):
                            #cv2.circle(影像, 圓心座標, 半徑, 顏色, 線條寬度)
                            cv2.circle(img, (shape.part(i).x, shape.part(i).y), 2, (0, 255, 0), -1, 8)
                            #cv2.putText(影像, 文字, 座標, 字型, 大小, 顏色, 線條寬度, 線條種類)
                            cv2.putText(img, str(i), (shape.part(i).x, shape.part(i).y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                        (255, 2555, 255))
            #----no faces detected
            else:
                cv2.putText(img, no_face_str, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            #----FPS count and claculation
            if frame_count == 0:
                t_start = time.time()
            frame_count += 1
            if frame_count >= 10:
                FPS = "FPS=%1f" % (10 / (time.time() - t_start))
                frame_count = 0

            # cv2.putText(影像, 文字, 座標, 字型, 大小, 顏色, 線條寬度, 線條種類)
            cv2.putText(img, FPS, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            #----image display
            cv2.imshow("demo by JohnnyAI", img)

            #----'q' key pressed?
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('f'):
                show_facial_points = True
            elif key == ord('g'):
                show_facial_points = False
        else:
            print("get image failed")
            break

    #----release
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    Dlib_face_detection(use_CUDA=True)
