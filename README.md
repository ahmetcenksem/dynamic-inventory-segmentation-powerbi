# 📊 Dinamik Stok Segmentasyonu (ABC-XYZ) & Emniyet Stoğu Karar Destek Sistemi

Bu proje, imalat ve yedek parça operasyonlarında stok optimizasyonu, maliyet minimizasyonu ve tedarik güvenliği sağlamak amacıyla geliştirilmiş uçtan uca bir analitik karar destek sistemidir.

**Pareto Analizi (ABC)**, **Talep Değişkenliği (XYZ)** ve **Stokastik Emniyet Stoğu** formülasyonlarını entegre ederek sipariş tetikleme mekanizmasını (*Reorder Point - ROP*) dinamik hale getirir ve sonuçları interaktif bir **Power BI** yönetim kokpitinde sunar.

---

## 📌 Problem Tanımı & İş Hedefi
Geleneksel stok yönetimi yaklaşımları genellikle tüm ürün çeşitlerine (SKU) tek tip stok kontrol kuralları uygular. Bu durum iki temel operasyonel soruna yol açar:
* **Sermaye Bağlanması:** Düşük talep gören veya öngörülebilir ürünlere gereksiz yere aşırı emniyet stoğu yatırımı yapılması.
* **Stoksuz Kalma (Stockout) Riski:** Yüksek cirolu kritik bileşenlerde tedarik süresi (Lead Time) ve talep dalgalanmalarının yanlış modellenmesi sonucu yaşanan hat duruşları.
* **🎯 Hedef:** **%95 hizmet seviyesi** ($Z = 1.65$) korunurken, sipariş süreçlerini ROP tabanlı otomatik karar kurallarına bağlamak ve satın alma/planlama ekiplerine tek ekranda aksiyon aldıracak bir karar destek mekanizması kurmak.

---

## 🛠️ Metodoloji & Matematiksel Modelleme

### 1. ABC Segmentasyonu (Kümülatif Ciro Katkısı - Pareto İlkesi)
Ürünler toplam yıllık cirolarına göre büyükten küçüğe sıralanmış ve kümülatif gelir katkılarına göre ayrıştırılmıştır:
* **A Grubu:** Toplam cironun ilk **%70**'ini oluşturan kritik ve yüksek değerli stratejik ürünler.
* **B Grubu:** Kümülatif cironun **%70 - %90** aralığını oluşturan orta segment ürünler.
* **C Grubu:** Cironun son **%10**'luk dilimini temsil eden düşük maliyetli sarf ürünleri.

### 2. XYZ Segmentasyonu (Talep Değişkenliği ve Öngörülebilirlik)
12 aylık talep geçmişi üzerinden her ürün için **Varyasyon Katsayısı ($CV$)** hesaplanmıştır:

$$CV = \frac{\sigma}{\mu}$$

* **X Sınıfı ($CV \le 0.20$):** Düzenli, kararlı ve yüksek öngörülebilir talep.
* **Y Sınıfı ($0.20 < CV \le 0.50$):** Sezonsal veya orta düzeyde değişkenlik gösteren talep.
* **Z Sınıfı ($CV > 0.50$):** Düzensiz, kesikli ve tahmin edilmesi güç yüksek riskli talep.

### 3. Stokastik Emniyet Stoğu ($SS$) & Yeniden Sipariş Noktası ($ROP$)
Tedarik süresi boyunca stoksuz kalma riskini **%95 güven düzeyinde** tutmak için normal dağılım kabulü ile stokastik modelleme kullanılmıştır:

$$SS = Z \times \sigma_{günlük} \times \sqrt{L}$$

$$ROP = (d \times L) + SS$$

* **$Z$:** Hizmet seviyesi faktörü (%95 servis seviyesi için $Z_{0.95} = 1.65$)
* **$\sigma_{günlük}$:** Günlük talep standart sapması ($\sigma_{aylık} / \sqrt{30}$)
* **$L$:** Tedarik süresi (*Lead Time* - Gün)
* **$d$:** Günlük ortalama talep

### 4. Operasyonel Karar Kuralı (DAX & Logic)
$$\text{Sipariş Durumu} = \begin{cases} \text{"Siparis Ver"}, & \text{Mevcut Stok} \le ROP \\ \text{"Stok Yeterli"}, & \text{Mevcut Stok} > ROP \end{cases}$$

---

## 🖥️ Karar Destek Kokpiti (Power BI)

![Power BI Dashboard](dashboard.png)

Proje kapsamında **Dark/Modern UI** konseptiyle geliştirilen yönetim paneli aşağıdaki bileşenleri içerir:
1. **Yönetici Özet Kartları (Executive KPIs):** Toplam Stok Tutarı (`648B TL`), Anlık Sipariş Alarmı Veren Kritik SKU Sayısı (`5 Adet`) ve Toplam Ürün Çeşidi (`15 SKU`).
2. **ABC Ciro Dağılımı (Donut Chart):** Portföyün gelir yoğunlaşmasını gösteren Pareto dağılım grafiği.
3. **9'lu ABC-XYZ Karar Matrisi:** Portföy risk ve değer profilinin 3x3 matris üzerinde çapraz filtrelenebilir şekilde izlenmesi.
4. **Mevcut Stok vs. ROP Kıyaslaması:** Güvenli sınırın altına inen bileşenlerin çubuk grafik üzerinde görsel tespiti.
5. **Sipariş & Aksiyon Tablosu:** Satın alma ekipleri için acil sipariş verilmesi gereken ürünleri (Kırmızı Alarm) ve önerilen sipariş miktarlarını listeleyen dinamik tablo.

---

## 📈 Kazanımlar & Sağlanan Katma Değer
* **Üretim Duruş Riskinin Minimize Edilmesi:** Talep belirsizliği yüksek ve kritik öneme sahip ürünlerde dinamik tampon stok ayrılarak *stockout* riski kontrol altına alındı.
* **İşletme Sermayesi Optimizasyonu:** Düzenli talep yapısına sahip X grubu ürünlerde gereksiz stok şişkinliğinin önüne geçildi.
* **Kural Tabanlı Satın Alma Tetiği:** Manuel takip hatalarını ortadan kaldıran, doğrudan ERP/MRP sistemlerine entegre edilebilir matematiksel bir sipariş tetikleme altyapısı oluşturuldu.

---

## 📂 Dosya Yapısı

```text
├── dashboard.png                # Power BI karar destek kokpiti ekran görüntüsü
├── Stok_Karar_Destek.pbix       # Power BI interaktif rapor dosyası
├── calculate_rop.py             # Matematiksel modelleme ve optimizasyon kodu
├── stok_verisi.csv              # 12 aylık ham talep ve operasyon parametre verisi
├── stok_analizi_sonuc.csv       # Hesaplanmış segmentler, ROP ve sipariş karar tablosu
└── README.md                    # Proje teknik dokümantasyonu

Kurulum & Çalıştırma
Python ortamında veri analizi ve ROP hesaplamalarını çalıştırmak için gerekli kütüphaneleri yükleyin:

Bash
pip install pandas numpy
Modelleme betiğini çalıştırın:

Bash
python calculate_rop.py
İnteraktif görselleştirmeleri ve DAX ölçülerini incelemek için Stok_Karar_Destek.pbix dosyasını Power BI Desktop ile açmanız yeterlidir.
