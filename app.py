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
        
        SEGMENT_LED_SAYISI=4 # 7 segmentlı yapıda bir segmente bulunan led sayısı
        self.SEGMENT_LED_RENGI=Color(255,0,0) # scoreBoard un genel rengi
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
        """
        Bir takımın 2 haneden oluşan skoru (00..99) olduğundan
        skoru oluşturan herbir rakamın Şerit LED üzerinde kaç led ile
        ifade edilğini ayarllıyorum. bu örnekte 7 segmenten oluşan rakamın
        her segmentinde 4 led olduğundan 7x4=28, eğer 5 led den oluşsaydı 7x5=35 olacaktı
        """
        sg_led=SEGMENT_LED_SAYISI*7
        # Home skor LED bağlantıları
        self.home_skor.led_ekle([i for i in range(sg_led)])
        self.home_skor.led_ekle([i for i in range(sg_led,sg_led*2)])

        # Guest skor LED bağlantıları
        self.guest_skor.led_ekle([i for i in range(sg_led*2,sg_led*3)])
        self.guest_skor.led_ekle([i for i in range(sg_led*3,sg_led*4)])

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
    
    """
    _skor_ayarla hangi takımın       skorunu belirtilen oranda arttırıp,
    azaltmayı sağlar
    """
    def sayac_ayarla(self, _skor_ayarla, _skor, durum, oran):
        """ Skoru güncelle ve LED’lere yansıt """
        _skor_ayarla.sayi_ayarla(durum, oran)
        self.rakam_goster(_skor, _skor_ayarla.skor_Goster())

    """ _skor ile belirtilen takımın skorunun rakam ile belirtilen değere getiri"""   
    def rakam_goster(self, _skor, rakam):
        # Önce tüm LED'leri kapat
        for i in range(_skor.digit_sayisi()):# kaç adet takımın skoru tutuluyorsa
            for k in _skor.leds[i]:
                self.strip.setPixelColor(k,Color(0,0,0))
                self.strip.show()
            #time.sleep(1/1000)
                
        """Arayüzdeki Skorları değiştirmemi sağlıyor"""
        if _skor==self.home_skor:
            self.label_homeskor.setText(str(rakam[0]) + str(rakam[1]))
        else:
            self.label_guestskor.setText(str(rakam[0]) + str(rakam[1]))
        """
            _skor ile belirtilen takım için, skoru oluşturan rakamlar için teker teker,
            ilgili rakamı oluşturmak için hangi indexde bulunan ledleri yakması gerektiğini
            belirleyerek ilgili takımın led tablosundan o indexde bulunan led numarasına yanma
            komutu verir
        """
        for i in range(_skor.digit_sayisi()):# kaç adet takımın skoru tutuluyorsa
            for k in _skor.rakams[rakam[i]]:
                self.strip.setPixelColor(_skor.leds[i][k],self.SEGMENT_LED_RENGI)
                self.strip.show()
            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
