import sys,time
from rpi_ws281x import *# LED için
from PySide6.QtWidgets import QApplication, QMainWindow
from main import Ui_Form  # Designer'dan gelen dosya
from RakamAyarla_2digit_skor import ScoreBoard_Ayarla
from SKOR_SAY import Skor_Ayarla

#      4  5  6  7
#   3              8
#   2              9
#   1              10
#   0              11
#      15 14 13 12
#   16             27
#   17             26
#   18             25
#   19             24
#       20 21 22 23

class MyWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # LED strip configuration:
        LED_COUNT      = 120   # Number of LED pixels.
        LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
        #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
        LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
        LED_BRIGHTNESS = 65      # Set to 0 for darkest and 255 for brightest
        LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
        
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()
        
        # Home skor nesneleri
        self.home_skor = ScoreBoard_Ayarla([0, 0], 4)
        self.home_skor_ayarla = Skor_Ayarla([0, 0], 0, 100)

        # Guest skor nesneleri
        self.guest_skor = ScoreBoard_Ayarla([0, 0], 4)
        self.guest_skor_ayarla = Skor_Ayarla([0, 0], 0, 100)

        # Home skor LED bağlantıları
        self.home_skor.led_ekle([i for i in range(28)])
        self.home_skor.led_ekle([i for i in range(28,57)])

        # Guest skor LED bağlantıları
        self.guest_skor.led_ekle([i for i in range(57,85)])
        self.guest_skor.led_ekle([i for i in range(85,113)])

        # Buton bağlantıları (dinamik hale getirildi)
        self.btn_homeskor_azalt3.clicked.connect(
            lambda: self.sayac_ayarla(self.home_skor_ayarla, self.home_skor, 0, 3)
        )
        self.btn_homeskor_arttir3.clicked.connect(
            lambda: self.sayac_ayarla(self.home_skor_ayarla, self.home_skor, 1, 3)
        )
        self.btn_homeskor_azalt2.clicked.connect(
            lambda: self.sayac_ayarla(self.home_skor_ayarla, self.home_skor, 0, 2)
        )
        self.btn_homeskor_arttir2.clicked.connect(
            lambda: self.sayac_ayarla(self.home_skor_ayarla, self.home_skor, 1, 2)
        )
        self.btn_homeskor_azalt1.clicked.connect(
            lambda: self.sayac_ayarla(self.home_skor_ayarla, self.home_skor, 0, 1)
        )
        self.btn_homeskor_arttir1.clicked.connect(
            lambda: self.sayac_ayarla(self.home_skor_ayarla, self.home_skor, 1, 1)
        )

        self.btn_guestskor_azalt3.clicked.connect(
            lambda: self.sayac_ayarla(self.guest_skor_ayarla, self.guest_skor, 0, 3)
        )
        self.btn_guestskor_arttir3.clicked.connect(
            lambda: self.sayac_ayarla(self.guest_skor_ayarla, self.guest_skor, 1, 3)
        )
        self.btn_guestskor_azalt2.clicked.connect(
            lambda: self.sayac_ayarla(self.guest_skor_ayarla, self.guest_skor, 0, 2)
        )
        self.btn_guestskor_arttir2.clicked.connect(
            lambda: self.sayac_ayarla(self.guest_skor_ayarla, self.guest_skor, 1, 2)
        )
        self.btn_guestskor_azalt1.clicked.connect(
            lambda: self.sayac_ayarla(self.guest_skor_ayarla, self.guest_skor, 0, 1)

        )
        self.btn_guestskor_arttir1.clicked.connect(
            lambda: self.sayac_ayarla(self.guest_skor_ayarla, self.guest_skor, 1, 1)
        )

        # Başlangıçta skorları sıfırla
        self.rakam_goster(self.home_skor, [0, 0])
        self.rakam_goster(self.guest_skor, [0, 0])
    
    def sayac_ayarla(self, _skor_ayarla, _skor, durum, oran):
        """ Skoru güncelle ve LED’lere yansıt """
        _skor_ayarla.sayi_ayarla(durum, oran)
        self.rakam_goster(_skor, _skor_ayarla.skor_Goster())

        
    def rakam_goster(self, _skor, rakam):
        '''self.strip.setPixelColor(119,Color(0,255,0))
        self.strip.setPixelColor(113,Color(0,0,255))
        self.strip.show()
        time.sleep(2000/1000)'''
        print(_skor.leds)
        # Önce tüm LED'leri kapat
        for i in range(_skor.digit_sayisi()):# kaç adet takımın skoru tutuluyorsa
            for k in _skor.leds[i]:
                #print("{0}-{1}".format(i,k))
                self.strip.setPixelColor(k,Color(0,0,0))
                self.strip.show()
            #time.sleep(1/1000)
                

        if _skor==self.home_skor:
            self.label_homeskor.setText(str(rakam[0]) + str(rakam[1]))
        else:
            self.label_guestskor.setText(str(rakam[0]) + str(rakam[1]))
        # İlgili rakamları yak
        
        for i in range(_skor.digit_sayisi()):# kaç adet takımın skoru tutuluyorsa
            #print(_skor.rakams[rakam[i]])
            for k in _skor.rakams[rakam[i]]:
                if _skor.leds[i][k]==55:
                    print('55 nolu led {0}-{1}'.format(i,k))
                self.strip.setPixelColor(_skor.leds[i][k],Color(255,0,0))
                self.strip.show()
            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
