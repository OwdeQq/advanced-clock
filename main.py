from machine import Pin, ADC
from machine import Pin, PWM
from time import sleep
import utime
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from dht import  DHT11

led = Pin(25, Pin.OUT)
pin = Pin(15,Pin.IN,Pin.PULL_UP)
dht11 = DHT11(pin,None,dht11=True)
buzzer = PWM(Pin(3))


#LCD
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

#serowanie joystick
osX = ADC(Pin(27))
osY = ADC(Pin(26))
srodek = Pin(17,Pin.IN, Pin.PULL_UP)

zmiana = Pin(2, Pin.IN, Pin.PULL_UP)

#ANIMACJA:
#1 klataka
krop1 = bytearray([0x10,0x11,0x05,0x14,0x11,0x05,0x14,0x10])
ter1 = bytearray([0x04,0x0A,0x0A,0x0A,0x0A,0x11,0x11,0x0E])
#2 klataka
krop2 = bytearray([0x02,0x10,0x11,0x05,0x14,0x11,0x05,0x14])
ter2 = bytearray([0x04,0x0A,0x0A,0x0A,0x0A,0x1F,0x1F,0x0E])
#3 klataka
krop3 = bytearray([0x0A,0x02,0x10,0x11,0x05,0x14,0x11,0x05])
ter3 = bytearray([0x04,0x0A,0x0A,0x0A,0x0E,0x1F,0x1F,0x0E])
#4 klataka
krop4 = bytearray([0x08,0x0A,0x02,0x10,0x11,0x05,0x14,0x11])
ter4 = bytearray([0x04,0x0A,0x0A,0x0E,0x0E,0x1F,0x1F,0x0E])

#ZMIENNE
m=0
#mieciac
d=0
#dzien
g=0
#godzina
mi=0
#minuta
s=0
#sekunda
w=1
#wybur
e=1
#ekran

while True:
    buzzer.value(1)
  
    
    xValue = osX.read_u16()
    yValue = osY.read_u16()
    buttonValue = srodek.value()

    if zmiana.value() == 0:
        e=e+1
    
 
    if e <= 5:
        
        if xValue >= 60000:
            w=w+1  
        if xValue <= 600:
            w=w-1 
        
        if w==-1:
            w=5
        if w>=6:
            w=0

    #1       
        if yValue <= 600 and w == 1:
            m=m+1  
        if yValue >= 60000 and w == 1:
            m=m-1 
    #2
        if yValue <= 600 and w == 2:
            d=d+1  
        if yValue >= 60000 and w == 2:    
            d=d-1 
    #3
        if yValue <= 600 and w == 3:
            g=g+1  
        if yValue >= 60000 and w == 3:    
            g=g-1 
    #4
        if yValue <= 600 and w == 4:
            mi=mi+1  
        if yValue >= 60000 and w == 4:    
            mi=mi-1 
    #5        
        if yValue <= 600 and w == 5:
            s=s+1  
        if yValue >= 60000 and w == 5:    
            s=s-1     

    #limity
        if m >= 12:
            m = m*0         
        if d >= 31:
            d = d*0     
        if g >= 24:
            g = g*0       
        if mi >= 60:
            mi = mi*0    
        if s >= 60:
            s = s*0

        T,H = dht11.read()
        if T is None:
            lcd.move_to(0,0)
            lcd.putstr(" sensor error!  ")
            led.toggle()

        else:
            led.on()
            (year, month, day, hour, minute, second, millis, _tzinfo)=utime.localtime()
            
            lcd.move_to(3,1)
            lcd.putstr(":{}C".format(T))
            lcd.move_to(10,1)
            lcd.putstr(":{}%".format(H))

    #miesiace        
            if w == 1:
                lcd.move_to(0,0)
                lcd.putstr("[%02d]%02d %02d:%02d:%02d" % (month+m, day+d, hour+g, minute+mi, second+s))        
    #dni    
            if w == 2:
                lcd.move_to(0,0)
                lcd.putstr(" %02d[%02d]%02d:%02d:%02d" % (month+m, day+d, hour+g, minute+mi, second+s))     
    #godz    
            if w == 3:
                lcd.move_to(1,0)
                lcd.putstr("%02d-%02d[%02d]%02d:%02d " % (month+m, day+d, hour+g, minute+mi, second+s))     
    #min
            if w == 4:
                lcd.move_to(1,0)
                lcd.putstr("%02d-%02d %02d[%02d]%02d " % (month+m, day+d, hour+g, minute+mi, second+s)) 
    #sekundy
            if w == 5:
                lcd.move_to(1,0)
                lcd.putstr("%02d-%02d %02d:%02d[%02d]" % (month+m, day+d, hour+g, minute+mi, second+s)) 
            if w == 0:
                lcd.move_to(0,0)
                lcd.putstr(" %02d-%02d %02d:%02d:%02d " % (month+m, day+d, hour+g, minute+mi, second+s))
                
    #ANIMACJA
    #1 klatka        
            lcd.custom_char(0, ter1)
            lcd.move_to(2,1)
            lcd.custom_char(0, ter1)
            lcd.putstr(chr(0))
            
            lcd.custom_char(4, krop1)
            lcd.move_to(9,1)
            lcd.custom_char(4, krop1)
            lcd.putstr(chr(4))        
    #2 klatka          
            lcd.custom_char(1, ter2)
            lcd.move_to(2,1)
            lcd.custom_char(1, ter2)
            lcd.putstr(chr(1))        
            
            lcd.custom_char(5, krop2)
            lcd.move_to(9,1)
            lcd.custom_char(5, krop2)
            lcd.putstr(chr(5))        
    #3 klatka           
            lcd.custom_char(2, ter3)
            lcd.move_to(2,1)
            lcd.custom_char(2, ter3)
            lcd.putstr(chr(2))
                    
            lcd.custom_char(6, krop3)
            lcd.move_to(9,1)
            lcd.custom_char(6, krop3)
            lcd.putstr(chr(6))       
    #4 klatka          
            lcd.custom_char(3, ter4)
            lcd.move_to(2,1)
            lcd.custom_char(3, ter4)
            lcd.putstr(chr(3))

            lcd.custom_char(7, krop4)
            lcd.move_to(9,1)
            lcd.custom_char(7, krop4)
            lcd.putstr(chr(7))
    buzzer.value(0)  00
    #if e <= 6:
        #lcd.clear()
    #print("ez {}".format(e))