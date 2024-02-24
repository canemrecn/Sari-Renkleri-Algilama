import cv2
import numpy as np
#Gerekli kütüphaneleri import et
altRenk = (10, 100, 100)
ustRenk = (40, 255, 255)
# Belirlenen renk aralığı
RENK = 'SARI'
# Nesne rengi
kamera = cv2.VideoCapture(0)
# Kamerayı başlat
cember = True
# Nesne algılama şekli
while True:
    if not kamera.isOpened(): break
# Kamera açıksa devam et
    _,kare = kamera.read()
# Kameradan bir kare al
    hsv = cv2.cvtColor(kare, cv2.COLOR_BGR2HSV)
# Kareyi HSV renk uzayına dönüştür
    maske = cv2.inRange(hsv,altRenk,ustRenk)
# Belirlenen renk aralığına göre maske oluştur
    kernel = np.ones((5,5),'int')
    maske = cv2.dilate(maske,kernel)
# Maskeyi genişletmek için kernel kullan
    res = cv2.bitwise_and(kare,kare,mask=maske)
# Orijinal kare ile maskeyi birleştir
    konturlar = cv2.findContours(maske.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
# Konturları bul
    say = 0
# Sayacı sıfırla
    for kontur in konturlar:
        alan = cv2.contourArea(kontur)
# Kontur alanını hesapla
        if alan > 600:
            say+=1
# Belirlenen alandan büyük konturları işle
            (x,y,w,h)=cv2.boundingRect(kontur)
            cv2.rectangle(kare, (x, y), (x + w, y + h), (0, 255, 0), 2)
# Konturun sınırlayıcı dikdörtgenini çiz
            if cember:
                (x, y), ycap = cv2.minEnclosingCircle(kontur)
                merkez = (int(x), int(y))
                ycap = int(ycap)
                img = cv2.circle(kare, merkez, ycap, (255, 0, 0), 2)
# Konturun çevreleyen en küçük daireyi çiz
    if say > 0:
        cv2.putText(kare, f'{say} {RENK} nesne bulundu', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, 1)
# Bulunan nesne sayısını ekrana yazdır
    cv2.imshow('kare', kare)
# Kareyi ekranda göster
    k = cv2.waitKey(4) & 0xFF
    if k == 27: break
# Klavyeden ESC tuşuna basılırsa döngüyü sonlandır
if kamera.isOpened():
    kamera.release()
# Kamera açıksa kapat
cv2.destroyAllWindows()
# Tüm pencereleri kapat