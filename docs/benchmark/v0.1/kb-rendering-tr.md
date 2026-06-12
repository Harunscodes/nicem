# NiceHome Knowledge Base — Turkish Rendering (v0.1)

**Rendering ID:** kb-tr-v0.1.0 (not yet frozen)
**Language:** Turkish (Türkçe) — peer rendering, not a translation of the English or Dutch rendering
**Authored from:** `canonical-fact-set.md` (fs-v0.1.0) + `document-plan.md` (kb-plan-v0.1.0) + `language-rendering-plan.md` (lr-plan-v0.1.0)
**Structure:** 8 documents, 39 sections/chunks. Chunk IDs and fact IDs are metadata; they are stripped before the content is served to an agent.
**Register:** Neutral, clear product-support Turkish; impersonal imperative for procedural steps; not bureaucratic. Case suffixes attach to product names with an apostrophe (e.g., NiceHome Hub'ı) where natural.
**Controlled terminology (resolved TODOs):** live view = canlı görüntü; replacement = değişim; refurbished replacement = yenilenmiş değişim cihazı.
**Review status:** Project-owner (native Turkish speaker) review pending. This rendering introduces no policy facts beyond the canonical fact-set.

---

## D01 — Ürüne genel bakış ve cihaz uyumluluğu

### D01-S1 — Cihazlara genel bakış
```
chunk_id: D01-S1
fact_ids: [F0101, F0102, F0103, F0104]
document_id: D01
section_title: Cihazlara genel bakış
```
NiceHome Hub, diğer tüm NiceHome cihazlarını yöneten merkezi cihazdır. NiceHome Sensor sıcaklık, nem ve hareketi ölçer. NiceHome Plug, uzaktan açma/kapama ve enerji ölçümü sunan akıllı bir prizdir. NiceHome Camera, hareket bildirimleri ve canlı görüntü sunan bir iç mekân güvenlik kamerasıdır.

### D01-S2 — Hub gerekliliği ve bağımsız çalışma
```
chunk_id: D01-S2
fact_ids: [F0105, F0106, F0107]
document_id: D01
section_title: Hub gerekliliği ve bağımsız çalışma
```
NiceHome Sensor'ün çalışması için bir NiceHome Hub gerekir ve Sensor, Hub olmadan çalışmaz. NiceHome Camera'nın çalışması için de bir NiceHome Hub gerekir. NiceHome Plug, Hub olmadan temel uzaktan açma/kapama işlevini destekler; ancak otomasyon özellikleri olan zamanlama ve enerji ölçümü için bir Hub gerekir.

### D01-S3 — Nesil uyumluluğu
```
chunk_id: D01-S3
fact_ids: [F0108, F0109]
document_id: D01
section_title: Nesil uyumluluğu
```
NiceHome cihazları Gen 1 ve Gen 2 olmak üzere iki nesilde bulunur. Gen 2 cihazlar için bir Gen 2 Hub gerekir; bir Gen 1 Hub, Gen 2 cihazları desteklemez. Bir Gen 2 Hub geriye dönük uyumludur ve hem Gen 1 hem de Gen 2 cihazları destekler.

### D01-S4 — Canlı görüntü kullanılabilirliği
```
chunk_id: D01-S4
fact_ids: [F0110]
document_id: D01
section_title: Canlı görüntü kullanılabilirliği
```
Hub çevrimdışıyken Camera'nın canlı görüntüsü kullanılamaz.

---

## D02 — Garanti politikası

### D02-S1 — Garanti süresi
```
chunk_id: D02-S1
fact_ids: [F0201]
document_id: D02
section_title: Garanti süresi
```
Tüm NiceHome cihazları, satın alma tarihinden itibaren 2 yıllık standart garanti içerir.

### D02-S2 — Nelerin kapsandığı
```
chunk_id: D02-S2
fact_ids: [F0202]
document_id: D02
section_title: Nelerin kapsandığı
```
Garanti, normal kullanım sırasında ortaya çıkan üretim hatalarını ve donanım arızalarını kapsar.

### D02-S3 — Nelerin kapsanmadığı
```
chunk_id: D02-S3
fact_ids: [F0203, F0204]
document_id: D02
section_title: Nelerin kapsanmadığı
```
Garanti, kaza sonucu hasarı kapsamaz. Garanti ayrıca yanlış kullanımdan veya cihazın yetkisiz olarak değiştirilmesinden kaynaklanan hasarı da kapsamaz.

### D02-S4 — Garanti talebi oluşturma
```
chunk_id: D02-S4
fact_ids: [F0205, F0206, F0207, F0208]
document_id: D02
section_title: Garanti talebi oluşturma
```
Garanti talebi oluşturmak için satın alma belgesi sunmanız gerekir. Talep üç adımdan oluşur. Önce cihazın seri numarasıyla NiceHome destek birimine başvurun. Ardından destek birimi bir garanti talebi referansı ve önceden ödenmiş bir gönderi etiketi verir. Son olarak cihazı önceden ödenmiş etiketle gönderin ve talep referansını ekleyin.

### D02-S5 — Talebin sonucu
```
chunk_id: D02-S5
fact_ids: [F0209]
document_id: D02
section_title: Talebin sonucu
```
Kapsanan bir arıza doğrulanırsa, cihaz ücretsiz olarak onarılır veya değiştirilir.

---

## D03 — İade ve geri ödeme politikası

### D03-S1 — İade süresi
```
chunk_id: D03-S1
fact_ids: [F0301, F0305]
document_id: D03
section_title: İade süresi
```
İade süresi, satın alma tarihinden itibaren 30 gündür. Satın almadan 30 gün sonra yapılan iadeler kabul edilmez.

### D03-S2 — Cihaz durumuna göre geri ödeme
```
chunk_id: D03-S2
fact_ids: [F0302, F0303]
document_id: D03
section_title: Cihaz durumuna göre geri ödeme
```
30 gün içinde iade edilen açılmamış bir cihaz, ücretsiz iade gönderimiyle birlikte tam geri ödeme alır. 30 gün içinde iade edilen, açılmış ancak hasarsız bir cihaz da tam geri ödeme alır; ancak bu durumda iade gönderim ücretini siz ödersiniz.

### D03-S3 — İade istisnaları
```
chunk_id: D03-S3
fact_ids: [F0304, F0306]
document_id: D03
section_title: İade istisnaları
```
Müşteri tarafından hasar verilen bir cihaz, hasar garanti kapsamında olmadıkça geri ödemeye uygun değildir. Abonelik planları, cihaz iade süreci üzerinden geri ödenmez; abonelik iptali ayrı olarak ele alınır.

### D03-S4 — Geri ödemelerin işlenmesi
```
chunk_id: D03-S4
fact_ids: [F0307, F0308]
document_id: D03
section_title: Geri ödemelerin işlenmesi
```
Geri ödemeler, asıl ödeme yöntemine yapılır. Geri ödemeler, iade edilen cihaz teslim alındıktan sonra 14 iş günü içinde işleme alınır.

### D03-S5 — İade süreci
```
chunk_id: D03-S5
fact_ids: [F0309, F0310, F0311]
document_id: D03
section_title: İade süreci
```
İade üç adımdan oluşur. Önce NiceHome destek biriminden bir iade onayı isteyin. Ardından bir iade onay numarası ve gönderim talimatları alırsınız. Son olarak cihazı, iade onay numarasını ekleyerek gönderin.

---

## D04 — Abonelik planı kuralları

### D04-S1 — Plana genel bakış
```
chunk_id: D04-S1
fact_ids: [F0401]
document_id: D04
section_title: Plana genel bakış
```
NiceHome, Camera Plus Plan adında bir bulut aboneliği sunar.

### D04-S2 — Planın sunduğu özellikler
```
chunk_id: D04-S2
fact_ids: [F0402, F0403]
document_id: D04
section_title: Planın sunduğu özellikler
```
Camera Plus Plan, NiceHome Camera için 30 günlük bulut video depolama sunar. Abonelik olmadan NiceHome Camera yine de canlı görüntüyü destekler, ancak bulut video depolama sunmaz.

### D04-S3 — Plan gereksinimleri
```
chunk_id: D04-S3
fact_ids: [F0404]
document_id: D04
section_title: Plan gereksinimleri
```
Camera Plus Plan için bir NiceHome Camera ve bir NiceHome Hub gerekir.

### D04-S4 — Ücretsiz deneme süresi
```
chunk_id: D04-S4
fact_ids: [F0405, F0406]
document_id: D04
section_title: Ücretsiz deneme süresi
```
Camera Plus Plan, 14 gün süren ücretsiz bir deneme içerir. Ücretsiz deneme, hesap başına yalnızca bir kez kullanılabilir.

### D04-S5 — İptal ve değişiklikler
```
chunk_id: D04-S5
fact_ids: [F0407, F0408, F0409]
document_id: D04
section_title: İptal ve değişiklikler
```
Aboneliği iptal ederseniz, bulut depolama erişimi mevcut faturalandırma döneminin sonuna kadar devam eder. İptal edilen bir abonelik, mevcut faturalandırma dönemi için orantılı bir geri ödeme almaz. Abonelik plan değişiklikleri, yükseltme veya düşürme olsun, bir sonraki faturalandırma döneminin başında geçerli olur.

---

## D05 — Gönderim ve teslimat politikası

### D05-S1 — Gönderim yöntemleri ve süreleri
```
chunk_id: D05-S1
fact_ids: [F0501, F0502, F0503]
document_id: D05
section_title: Gönderim yöntemleri ve süreleri
```
İki gönderim yöntemi mevcuttur: Standard ve Express. Standard gönderim 5 ila 7 iş günü içinde teslim edilir. Express gönderim 2 iş günü içinde teslim edilir.

### D05-S2 — Express uygunluğu
```
chunk_id: D05-S2
fact_ids: [F0504]
document_id: D05
section_title: Express uygunluğu
```
Express gönderim yalnızca stokta bulunan ürünler için kullanılabilir.

### D05-S3 — Bir siparişi değiştirme veya iptal etme
```
chunk_id: D05-S3
fact_ids: [F0505, F0506]
document_id: D05
section_title: Bir siparişi değiştirme veya iptal etme
```
Bir siparişi, verdikten sonra 2 saat içinde değiştirebilir veya iptal edebilirsiniz. 2 saat sonra sipariş iptal edilemez; ancak cihazı teslimattan sonra iade politikası kapsamında iade edebilirsiniz.

### D05-S4 — Geciken veya kaybolan gönderiler
```
chunk_id: D05-S4
fact_ids: [F0507, F0508]
document_id: D05
section_title: Geciken veya kaybolan gönderiler
```
Bir gönderi, tahmini teslimat süresinin ötesinde gecikirse, gönderim ücretinin geri ödenmesini talep edebilirsiniz. Bir gönderi taşıma sırasında kaybolursa, ek ücret olmadan bir değişim gönderilir.

---

## D06 — Sorun giderme kılavuzu

### D06-S1 — Bağlantı sorunlarını giderme
```
chunk_id: D06-S1
fact_ids: [F0601, F0602, F0603, F0604]
document_id: D06
section_title: Bağlantı sorunlarını giderme
```
Bağlantı sorunlarında şu adımları izleyin. Önce Hub güç ışığının yanıp yanmadığını kontrol edin. Işık kapalıysa güç kablosunu ve prizi kontrol edin. Işık yanıyor ancak cihazlar çevrimdışıysa Hub'ı yeniden başlatın. Hub'ı yeniden başlattıktan sonra cihazlar çevrimdışı kalmaya devam ediyorsa ev ağını ve yönlendiriciyi kontrol edin.

### D06-S2 — Hub durum göstergeleri
```
chunk_id: D06-S2
fact_ids: [F0605]
document_id: D06
section_title: Hub durum göstergeleri
```
Hub'ın yanıp sönen kırmızı ışığı, Hub'ın ağ bağlantısını kaybettiğini gösterir.

### D06-S3 — Bir cihazı eşleştirme
```
chunk_id: D06-S3
fact_ids: [F0606, F0607, F0608, F0609]
document_id: D06
section_title: Bir cihazı eşleştirme
```
Yeni bir cihazı eşleştirmek için şu adımları izleyin. Önce NiceHome uygulamasını açın ve "Cihaz ekle" seçeneğini seçin. Ardından kurulum düğmesini 5 saniye basılı tutarak cihazı eşleştirme moduna alın. Son olarak eşleştirmeyi tamamlamak için uygulamadaki yönergeleri izleyin. Eşleştirme başarısız olursa, cihazın Hub'ın menzili içinde olduğundan emin olun.

### D06-S4 — Yanıt vermeyen Plug
```
chunk_id: D06-S4
fact_ids: [F0610, F0611]
document_id: D06
section_title: Yanıt vermeyen Plug
```
Bir NiceHome Plug yanıt vermiyorsa, önce uygulamadan kapatıp tekrar açın. Plug bundan sonra hâlâ yanıt vermiyorsa, Plug'a yumuşak sıfırlama uygulayın.

### D06-S5 — Sensor'ün hatalı ölçümleri
```
chunk_id: D06-S5
fact_ids: [F0612]
document_id: D06
section_title: Sensor'ün hatalı ölçümleri
```
NiceHome Sensor ölçümleri hatalı görünüyorsa, Sensor'ü uygulama ayarlarından yeniden kalibre edin.

### D06-S6 — Ne zaman desteğe başvurmalı
```
chunk_id: D06-S6
fact_ids: [F0613]
document_id: D06
section_title: Ne zaman desteğe başvurmalı
```
Bu sorun giderme adımları sorunu çözmezse, NiceHome destek birimine başvurun.

---

## D07 — Onarım ve değişim politikası

### D07-S1 — Garanti kapsamında onarım ve değişim
```
chunk_id: D07-S1
fact_ids: [F0701, F0703]
document_id: D07
section_title: Garanti kapsamında onarım ve değişim
```
Garanti kapsamındaki, kapsanan bir arızaya sahip cihaz ücretsiz olarak onarılır veya değiştirilir. Garanti kapsamındaki bir cihaz onarılamıyorsa, değiştirilir.

### D07-S2 — Garanti dışı onarım
```
chunk_id: D07-S2
fact_ids: [F0702, F0706]
document_id: D07
section_title: Garanti dışı onarım
```
Garanti dışı bir cihaz, bir servis ücreti karşılığında onarılabilir. Garanti dışı onarımlarda gönderim ücretini her iki yönde de siz ödersiniz.

### D07-S3 — Değişim cihazları
```
chunk_id: D07-S3
fact_ids: [F0704, F0705]
document_id: D07
section_title: Değişim cihazları
```
Bir değişim cihazı yeni veya yenilenmiş olabilir. Yenilenmiş değişim cihazı, asıl garantinin kalan süresini, en az 90 gün olmak üzere taşır; başka bir deyişle, asıl garantinin kalan süresi ile 90 günden hangisi daha uzunsa onu alırsınız.

### D07-S4 — Hasar istisnaları
```
chunk_id: D07-S4
fact_ids: [F0708]
document_id: D07
section_title: Hasar istisnaları
```
Kaza sonucu hasar veya sıvı hasarı bulunan cihazlar standart onarıma uygun değildir ve garanti dışı bir servis teklifi gerektirir.

### D07-S5 — Süre ve nasıl talep edilir
```
chunk_id: D07-S5
fact_ids: [F0707, F0709]
document_id: D07
section_title: Süre ve nasıl talep edilir
```
Onarım süresi, cihaz teslim alındıktan sonra genellikle 10 iş günüdür. Onarım talep etmek için NiceHome destek birimine başvurun ve sorunu açıklayın; destek birimi ardından bir onarım referansı ve gönderim talimatları verir.

---

## D08 — Hesap erişimi ve cihaz sıfırlama politikası

### D08-S1 — Şifre kurtarma
```
chunk_id: D08-S1
fact_ids: [F0801, F0802, F0803]
document_id: D08
section_title: Şifre kurtarma
```
Şifrenizi kurtarmak için şu adımları izleyin. Önce oturum açma ekranında "Şifremi unuttum" seçeneğini seçin. Ardından bir sıfırlama bağlantısı almak için hesap e-postasını girin. Son olarak yeni bir şifre belirlemek için sıfırlama bağlantısını izleyin.

### D08-S2 — Yumuşak sıfırlama ile fabrika ayarlarına sıfırlama
```
chunk_id: D08-S2
fact_ids: [F0804, F0805]
document_id: D08
section_title: Yumuşak sıfırlama ile fabrika ayarlarına sıfırlama
```
Yumuşak sıfırlama, bir cihazı ayarlarını silmeden yeniden başlatır. Fabrika ayarlarına sıfırlama, tüm cihaz ayarlarını siler ve cihazın hesapla bağlantısını kaldırır.

### D08-S3 — Hub'ı fabrika ayarlarına sıfırlama
```
chunk_id: D08-S3
fact_ids: [F0806, F0807]
document_id: D08
section_title: Hub'ı fabrika ayarlarına sıfırlama
```
Hub'ı fabrika ayarlarına sıfırlamak için Hub sıfırlama düğmesini 10 saniye basılı tutun. Hub ışığının yanıp sönmesini bekleyin; bu, sıfırlamanın tamamlandığını gösterir. Sıfırlama tamamlandıktan sonra cihazın yeniden eşleştirilmesi gerekir; bu, bir sonraki bölümde açıklanmıştır.

### D08-S4 — Fabrika ayarlarına sıfırlamadan sonra
```
chunk_id: D08-S4
fact_ids: [F0807, F0809]
document_id: D08
section_title: Fabrika ayarlarına sıfırlamadan sonra
```
Fabrika ayarlarına sıfırlamadan sonra, cihazın yeniden kullanılabilmesi için uygulama üzerinden yeniden eşleştirilmesi gerekir. Fabrika ayarlarına sıfırlama, bulutta depolanan videoyu silmez; bulut videosu cihaz tarafından değil, abonelik tarafından yönetilir.

### D08-S5 — Kaybolan bir cihazı yönetme
```
chunk_id: D08-S5
fact_ids: [F0808]
document_id: D08
section_title: Kaybolan bir cihazı yönetme
```
Bir cihaz kaybolursa, uygulama üzerinden uzaktan hesaptan kaldırılabilir.

---

*End of Turkish rendering. 8 documents, 39 chunks. kb-tr-v0.1.0, not yet frozen. Project-owner review pending.*
