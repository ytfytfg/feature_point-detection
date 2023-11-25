import cv2
import numpy as np
import time

class windows:

    question = None
    G_result = None

    global Q_List, shift, picture, control

    control = "Default"
    Q_List = ["EAT   ", "WATER ", "TOILET", "OTHER   "]
    shift = [47, 74, 75, 75]

    picture = None
    font = None
    images = []

    def __init__(self, blinked = None, result = G_result):
            
            self.blinked = blinked
            self.result = result

    def Basic_Setting(self):

        global question, font

        # Heigh, Weigth
        question = np.zeros((400, 1000, 3), np.uint8)
        #cv2.rectangle(question, (0, 0), (1000,200), (255, 255, 255), -1)
        font = cv2.FONT_HERSHEY_PLAIN

    def Gengrate_coor_Vertial(self, l):

        pivot = 0
        array = []
        center = []
        array.append(pivot)

        length = l
        piece = l / len(Q_List)
        vcenter = int((pivot + piece) / 2)
        center.append(vcenter)

        while length > 0:
            
            pivot = pivot + piece
            array.append(int(pivot))
            center.append(int(pivot + vcenter))
            length -= piece
            

        return array, center
            
    def draw_menu(self):

        global picture

        rows, cols, _ = question.shape
        th_lines = 4 # thickness lines

        print("row = ", rows)
        print("cols = ", cols)

        vertial_Line_coors, picture = self.Gengrate_coor_Vertial(cols)

        print(vertial_Line_coors, picture)

        for i in range (0, len(vertial_Line_coors)):

            # Central Line Heroizen
            cv2.line(question, (vertial_Line_coors[i], 0),(vertial_Line_coors[i], rows),
                    (51, 51, 51), th_lines)
        
        
        
        #cv2.putText(question, "True", (100, rows - 100), font, 6, (255, 255, 255), 5)

        print("Menu being Drew!")
        self.put_content(picture)

    def put_content(self, picture_coor):

        global Q_List

        rows, cols, _ = question.shape
        th_lines = 4 # thickness lines

        for i in range(0, len(Q_List)):

            cv2.putText(question, Q_List[i], (picture_coor[i] - shift[i], 200), font, 3, (255, 255, 255), 5)


        print("Content being Drew!")
        #self.image_Read()

    def image_Read(self):

        rows, cols, _ = question.shape
        python_logo = cv2.imread("python_Logo.png")
        #overlay_pythonlogo = np.ones(python_logo.shape,np.uint8)

        question[rows:rows, cols:cols ] = python_logo

    def Jump_block(self, i):

        if i == 0:
            old = 3
        else:
            old = i - 1

        time.sleep(0.5)
        cv2.putText(question, Q_List[old], (picture[old] - shift[i - 1], 200), font, 3, (255, 255, 255), 5)
        cv2.putText(question, Q_List[i], (picture[i] - shift[i], 200), font, 3, (0, 255, 0), 5)
    
    def from_threading(self):

        self.blinked = True

        print(G_result)
        

        print("Windows Recieved Signal")

        return
    
    
    def Control(self, signal):
        
        global G_result

        print("Blink Eyes to stop or Enter ESC to stop")
        self = windows()
        control = signal
        self.Basic_Setting()
        self.draw_menu()
        pivot = 0
        stop_pivot = 0
        print("Windows receive signal: ", signal)

        while control == "start":

            self.Jump_block(pivot)
            cv2.imshow("Questions", question)
            time.sleep(0.5)
            key = cv2.waitKey(1)

            temp = pivot
            G_result = Q_List[temp]

            if self.blinked == True or key == 27:
                stop_pivot = pivot - 1
                print("You choose: ", Q_List[stop_pivot])
                #control = "stop"
                cv2.destroyWindow("Questions")
                #time.sleep(0.5)
                self.result = Q_List[stop_pivot]
                break
                #return True, Q_List[stop_pivot]
            else:
                print("not getting blink")

            #print(Q_List[pivot])
        
            if pivot == 3:
                pivot = 0
            else:
                pivot += 1
        
        print("Windows stop")
        
        return False, "unexpected"

if __name__ == "__main__":

    Question = windows()
    choosen = Question.Control("start")

    print("************************You choose: " + choosen + "************************")


    