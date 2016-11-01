import numpy as np
import cv2
import pyttsx
import time

# Dado o raio da circunferencia obtida,
# como a distancia e fixa, retorna, em centavos,
# o valor da moeda
def r_to_value(r) :
    if (r > 28 and r < 35) :
        return 100
    elif (r > 27 and r <= 28) :
        return 25
    elif (r < 27 and r > 24) :
        return 50
    elif (r == 24) :
        return 5
    elif (r < 24 and r > 20) :
        return 10
    #elif (r == 1) :
    #    return 1

    return 0

def returnSpeech(prediction):

    prediction = int(prediction)
    reais = prediction/100
    centavos = prediction%100
    msg2 = ""
    if reais < 1:
        return str(centavos) + " centavos."
    else:
        if reais == 1:
            msg1 = str(1) + " real"
        else:
            msg1 = str(reais) + " reais"
        if prediction%100 != 0:
            msg2 = " e " + str(centavos) + " centavos"

    return msg1 + msg2


def run_main() :    
    cap = cv2.VideoCapture(1)
    engine = pyttsx.init()
    engine.setProperty('voice', "brazil")

     
    while(True) :
        ret, frame = cap.read()
        roi = frame[0:500, 0:500]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        gray_blur = cv2.GaussianBlur(gray, (15, 15), 0)
        thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 1)

        kernel = np.ones((3, 3), np.uint8)
        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,
        kernel, iterations=4)

        cont_img = closing.copy()
        contours, hierarchy = cv2.findContours(cont_img, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
        
        time.sleep(3)
        soma = 0
        for cnt in contours :
            area = cv2.contourArea(cnt)

            if area < 500 or area > 4000 :
                continue

            circle = cv2.minEnclosingCircle(cnt)            
            cv2.circle(roi, (int(circle[0][0]), int(circle[0][1])), int(circle[1]),(255,255,255), 2)
            soma += r_to_value(int(circle[1]))
            #soma += int(circle[1]) 
        
        #cv2.putText(roi, 'Valor total: R$ %.2f' %soma, (0,470), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,0))
        #cv2.imshow('Contagem de moedas', roi)

        #engine = pyttsx.init()
        
        #msg = returnSpeech(soma)
        #engine.say(msg)
        #engine.say(" ")
        #engine.runAndWait()
        #engine.stop()
        



        if cv2.waitKey(1) & 0xFF == ord('q') :
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_main()
