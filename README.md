# KISISEL-ASISTAN
Yüz tanıma ve duygu tespitini anlık yaparak kişiyi müzik,film,oyun önerileri alabileceği sistem
(bunun içine pythonda Open-Cv face_recognition deepface(duygu tespiti için,önce dlipin yüklenmesi gerkiyor) kullandıldı ve ayrıca apılerin kullanımı için requests kütüphanesinin olması gerkiyor.)

Flask uygulaması, gerçek zamanlı yüz tanıma ve duygu tespiti yaparak size kişiselleştirilmiş öneriler sunar. Duygu durumunuza göre sizi bir asistana yönlendirir ve burada oyun, müzik ve film önerileri alınabilir. Müzik önerileri için Spotify API'si  ve diğer özellikler için çeşitli API'ler entegre edilmiştir.

Özellikler
Gerçek zamanlı yüz tanıma ve duygu tespiti.
Asistan sayfasında üç ana bölüm:
Oyunlar (Steam API kullanarak kişiselleştirilmiş oyun önerileri)
Müzik (Spotify API kullanarak kişiselleştirilmiş müzik önerileri)
Filmler (IMDB API kullanarak kişiselleştirilmiş film önerileri)
Farklı API entegrasyonları ile özelleştirilmiş öneriler.
