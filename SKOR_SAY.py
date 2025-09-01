from setuptools.command.build_ext import use_stubs
class Skor_Ayarla:
    sayi=[0,0]
    _sayi=0
    alt_sinir=0
    ust_sinir=0

    def __init__(self, _sayi,alt_sinir,ust_sinir):
        self.sayi = _sayi
        self.alt_sinir = alt_sinir
        self.ust_sinir = ust_sinir

    def sayi_ayarla(self,durum, oran):
        self.sayi.clear()
        # durum=0 ise azaltma
        # durum=1 ise arttırma
        # oran kaç sayi artacak veya azalacak
        if durum==0:
            if self._sayi>self.alt_sinir :
                self._sayi = self._sayi-oran
                if self._sayi<self.alt_sinir:self._sayi=self.alt_sinir
        else:
            if self._sayi<self.ust_sinir:
                self._sayi = self._sayi+oran
                if self._sayi>self.ust_sinir:self._sayi=self.ust_sinir
        if self._sayi<10:
            self.sayi.append(0)
            self.sayi.append(self._sayi)
        elif self._sayi<100:
            self.sayi=[int(x) for x in str(self._sayi)]
        else:
            self.sayi=[0,0]
        print(self._sayi)

    def skor_Goster(self)->[int,int]:
        return self.sayi
