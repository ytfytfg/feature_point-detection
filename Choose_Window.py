import cv2
import numpy as np

class windows:

    keyboard = None
    font = None

    def Basic_Setting():

        global keyboard, font

        # Heigh, Weigth
        keyboard = np.zeros((400, 1000, 3), np.uint8)
        cv2.rectangle(keyboard, (0, 0), (1000,200), (255, 255, 255), -1)
        font = cv2.FONT_HERSHEY_PLAIN

    def draw_menu():

        rows, cols, _ = keyboard.shape
        th_lines = 4 # thickness lines

        print("row = ", rows)
        print("cols = ", cols)

        #

        # Central Line Vertial
        cv2.line(keyboard, (int(cols/2) - int(th_lines/2), int(rows/2)),(int(cols/2) - int(th_lines/2), rows),
                (51, 51, 51), th_lines)
        
        # Central Line Heroizen
        cv2.line(keyboard, (0, int(rows/2)),(cols, int(rows/2)),
                (51, 51, 51), th_lines)
        
        cv2.putText(keyboard, "True", (100, rows - 100), font, 6, (255, 255, 255), 5)
        cv2.putText(keyboard, "False", (100 + int(cols/2), rows - 100), font, 6, (255, 255, 255), 5)

        print("Menu being Drew!")


    def draw_content():

        rows, cols, _ = keyboard.shape
        th_lines = 4 # thickness lines

        cv2.putText(keyboard, "Question", (250, 100), font, 6, (0, 0, 0), 5)
        print("Content being Drew!")


if __name__ == "__main__":

    windows.Basic_Setting()
    windows.draw_menu()
    windows.draw_content()

    cv2.imshow("Virtual keyboard", keyboard)
    cv2.waitKey(0)

    cv2.destroyAllWindows()
    