# Gorsel-Format-Donusturucu[README (1).md](https://github.com/user-attachments/files/22995504/README.1.md)
# 🎨 Görsel Format Dönüştürücü

Bu uygulama, modern ve sezgisel bir arayüzle **görsellerinizi farklı formatlara (PNG, JPG, WebP, AVIF, vb.) dönüştürmenizi** sağlar.  
Sürükle-bırak desteği, kalite ayarı ve toplu dönüştürme özellikleriyle profesyonel bir deneyim sunar.

---

## 🚀 Özellikler

- 📂 Sürükle-bırak desteği (dosyaları doğrudan pencereye bırakabilirsiniz)  
- 🖼️ Toplu görsel dönüştürme desteği  
- 🧩 Desteklenen formatlar: **PNG, JPG, JPEG, WebP, AVIF, BMP, GIF, TIFF, HEIC**  
- ⭐ Kalite kontrolü (JPG/WebP/AVIF için 1–100 arası)  
- 💾 Farklı kaydetme seçenekleri:
  - Klasör seç ve kaydet  
  - Orijinal konuma kaydet  
  - Aynı konumda `converted_images` klasörüne kaydet  
- 🌈 Modern karanlık arayüz (Custom renkler, animasyonlar, sekmeli yapı)  
- 🪄 Canlı ilerleme çubuğu ve durum bildirimi  
- 🗑️ Seçilen dosyaları kolayca temizleme  
- ✅ Başarılı ve hatalı işlemler için ayrıntılı sonuç mesajları

---

## 📦 Gereksinimler

- Python **3.9 veya üzeri**

---

## 🔧 Kurulum

### 1️⃣ Gerekli kütüphaneleri yükleyin:
```bash
pip install pillow pillow-heif tkinterdnd2
```

> 💡 `tkinter` zaten Python ile birlikte gelir, ek kurulum gerektirmez.  

---

### 2️⃣ Dosya yapısı:
```
convert.py
```

---

## ▶️ Çalıştırma

```bash
python convert.py
```

Uygulama açıldıktan sonra:

1. Görselleri doğrudan pencereye **sürükleyip bırakın** veya “📂 Dosya Seç” butonuyla seçin.  
2. “⚙️ Ayarlar” sekmesinden:
   - Hedef formatı (örn. PNG, JPG, WebP) seçin  
   - Kalite değerini belirleyin (varsayılan 90)  
   - Kaydetme konumunu ayarlayın  
3. “✨ Dönüştürmeyi Başlat” butonuna tıklayın.  
4. İşlem ilerleme çubuğunda anlık olarak görüntülenir.  

---

## 💡 İpuçları

- `HEIC` ve `AVIF` dosyaları için **pillow-heif** kütüphanesi desteği bulunur.  
- Aynı isimde bir dosya zaten varsa, otomatik olarak `_1`, `_2` eklenerek kaydedilir.  
- Görsellerin küçük önizlemeleri (thumbnail) otomatik olarak oluşturulur.  
- `converted_images` klasörü otomatik oluşturulur (gerekirse).  
- Dönüştürme tamamlandığında detaylı sonuç mesajı görüntülenir.  

---

## 🧱 Teknik Bilgiler

- Arayüz: **Tkinter + ttk (Custom Stil)**  
- Görsel işleme: **Pillow (PIL)**  
- HEIC/AVIF desteği: **pillow-heif**  
- Sürükle-bırak sistemi: **tkinterdnd2**  
- Dosya işlemleri: **os**, **filedialog**, **messagebox**  

---

## 🪪 Lisans

Bu proje kişisel kullanım içindir.  
Görsellerin telif hakları kullanıcıya aittir.  
Kod açık kaynaklı olup öğrenme ve geliştirme amaçlı kullanılabilir.

---

## 👨‍💻 Geliştirici

**Hüseyin Eray Özdemir**  

---

> 💬 Projeyi faydalı bulduysanız GitHub üzerinde bir ⭐ bırakmayı unutmayın!
