#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
import threading,serial,time
from cStringIO import StringIO
import os,math,locale,requests,urllib,sys#语音相关
reload(sys)  
sys.setdefaultencoding('utf8')#二维码识别相关

class mxBot():


    def __init__(self):
        self.Serial = serial.Serial(port = "/dev/arduino", baudrate = 115200, timeout = 1)

        self._KeepRunning = True
        self._ReceiverThread = threading.Thread(target=self._Listen)
        self._ReceiverThread.setDaemon(True)
        self._ReceiverThread.start()
        self.args = 0
        self.turn_speed = 5
        self.encode_line = 1320
        self.speak_language = "zh"
        self.speak_path = "/home/intel/Music/tts.mp3"
        self.speak_ID = "15237082"
        self.speak_KEY = "BLYTwp1ex3Tcvd0vaNGpjG64"
        self.speak_SECRET_KEY = '4RfNN4l6s0GnrAjViEfMomZIpN5Vn0Gw'
        self.delay(2)
        pass


    def motor(self,pwm1,pwm2):
        self.Serial.write('m '+str(pwm1)+ ' ' + str(pwm2) + '\r')
        pass

    def delay(self,second):#延时函数
        time.sleep(second)
        pass

    def stop(self):
        self.motor(0,0)
        pass

    def ping(self, pin):
        self.Serial.write('p '+str(pin) + '\r')
        time.sleep(0.2)
        return int(self.args[0])

    def getEncode(self):
        self.Serial.write('e' + '\r')
        time.sleep(0.2)
        return long(self.args[0]),long(self.args[1])

    def digitalWrite(self,pin,state):
        self.Serial.write('w '+str(pin)+ ' ' + str(state) + '\r')

    def _Listen(self):
        stringIO = StringIO()
        while self._KeepRunning:
            data = self.Serial.read()
            if data == '\r':
                pass
            if data == '\n':
                self.ReceivedLineHandler(stringIO.getvalue())
                stringIO.close()
                stringIO = StringIO()
            else:
                stringIO.write(data)

    def ReceivedLineHandler(self,line):
        if(len(line) > 0):
            lineParts = line.split(' ')
            self.args = lineParts

    def reset_encode(self):
        self.Serial.write('r' + '\r')

    def turn(self,angle,direction):
        vel_encode = 8.3 * angle
        left = right = 0

        if(direction == 0):
            while(left < vel_encode):
                left,right = self.getEncode()
                self.motor(self.turn_speed,-self.turn_speed)
            self.reset_encode()
            # print(left)
        elif(direction == 1):
            while(right < vel_encode):
                left,right = self.getEncode()
                self.motor(-self.turn_speed,self.turn_speed)
            self.reset_encode()
            # print(right)

    def forward(self,cm,speed):
        vel_cm = cm * 38.21
        left = right = 0
        print(vel_cm)
        while(left <= vel_cm):
            left,right = self.getEncode()
            self.motor(speed,speed)
            if left > right:
                err_pwm = (left - right)/20
                self.motor(speed,speed+err_pwm)
            elif right > left:
                err_pwm = (right - left)/20
                self.motor(speed + err_pwm,speed)
            else:
                self.motor(speed,speed)
        self.stop
        self.reset_encode() #重置编码器


    # #语音相关
    # def make_message(self,message):
    #     s = requests.Session()
    #     mes="http://tts.baidu.com/text2audio?lan=zh&per=4&pid=101&vol=9&per=6&ie=UTF-8&text="
    #     s.get(mes + urllib.quote(message))
    #     res = s.get(mes + urllib.quote(message)).content
    #     f = open(self.speak_path,"w")
    #     f.write(res)
    #     f.close
    # def speak(self,message):
    #     self.make_message(message)
    #     os.system("play "+ self.speak_path)
    #     os.system("rm" + self.speak_path)


    def speak(self,message):
        from aip import AipSpeech
        import os
        client = AipSpeech(self.speak_ID, self.speak_KEY, self.speak_SECRET_KEY)

        result  = client.synthesis(message, 'zh', 1, {
            'vol': 15,
            'per': 4,
            'pit': 6,
            'spd': 3
        })

        if not isinstance(result, dict):
            with open('/home/intel/Music/auido.mp3', 'wb') as f:
                f.write(result)
        os.system("play  ~/Music/auido.mp3")
        return 0

    def play(self,path):
        os.system("play " + path)

    def qrcode_rt(self):
        import cv2 
        import pyzbar.pyzbar as pyzbar
        import Image,ImageEnhance
        cap = cv2.VideoCapture(2)
        while(1):
            ret,frame = cap.read()
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            cv2.imwrite('qrcode.jpg',gray)
            image = 'qrcode.jpg'    
            img = Image.open(image)    
            barcodes = pyzbar.decode(img)
            barcodesData = 0
            for barcode in barcodes:
                barcodeData = barcode.data.decode("utf-8")
                time.sleep(2)
                if len(barcodeData) >= 1:
                    return barcodeData
                    break


    
        




# if __name__ == "__main__":
#     mx_bot = mxBot()
#     while(True):
# #         distance = mx_bot.ping(9)
# #         print(distance)
# #         if distance > 3 and distance <= 15:
# #             mx_bot.play("~/Music/test.mp3")
#         data = mx_bot.qrcode_rt()
#         print(data)
#         mx_bot.speak(data)
