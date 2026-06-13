# NiceM Query Rendering — Türkçe v0.1

**Durum:** NiceM v0.1 kıyaslama testi için 36 Türkçe sorgu metni
**Rol:** Üç eşdeğer sorgu renderinginden biri (EN/NL/TR). Her sorgu, İngilizce renderingden çevrilmek yerine niyet spesifikasyonu ve beklenen gerçek eşlemesinden bağımsız olarak hazırlanmıştır.
**Sürüm:** qr-tr-v0.1.0 (henüz dondurulmadı)
**Bağımlı:** `query-rendering-plan.md` (qr-plan-v0.1.0), `intent-set.md` (intent-v0.1.0), `expected-fact-mapping.md` (efm-v0.1.0)
**Besler:** Stage 1 tokenizer sanity gate (sorguları tokenize et; TR token sayılarını hesapla)
**İnceleme durumu:** Taslak — Stage 1 başlamadan önce proje sahibi (ana Türkçe konuşan) tarafından incelenmesi zorunludur (QR9)

**Not:** İngilizce, kanonik sorgu kaynağı değildir. Bu sorgular niyet spesifikasyonlarından bağımsız olarak hazırlanmıştır.

---

## Basit olgusal niyetler (INT-001–INT-012)

---

## INT-001

- **intent_id:** INT-001
- **language:** tr
- **query_text:** "NiceHome cihazlarında garanti süresi ne kadardır?"
- **linked_fact_ids:** [F0201]
- **expected_fact_set_id:** INT-001
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Doğrudan garanti sorgulama. Cihaz türü belirtilmemiş — "tüm cihazlar" kapsamını test eder. AC7: yanlış yanıt 30 gün (iade süresi).

---

## INT-002

- **intent_id:** INT-002
- **language:** tr
- **query_text:** "NiceHome cihazını iade etmek için kaç günüm var?"
- **linked_fact_ids:** [F0301]
- **expected_fact_set_id:** INT-002
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** İade penceresi sorgulama. AC7: yanlış yanıt 2 yıl (garanti). AC1: Buradaki 30 gün iade süresidir, bulut depolama değil.

---

## INT-003

- **intent_id:** INT-003
- **language:** tr
- **query_text:** "NiceHome Sensor ne ölçer?"
- **linked_fact_ids:** [F0102]
- **expected_fact_set_id:** INT-003
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Üç ölçüm de gerekli (sıcaklık, nem, hareket). Sorgu yanıtı ima etmeden ne ölçüldüğünü sorar.

---

## INT-004

- **intent_id:** INT-004
- **language:** tr
- **query_text:** "Cihazımı iade ettikten sonra ücret iadesi nereye yapılır?"
- **linked_fact_ids:** [F0307]
- **expected_fact_set_id:** INT-004
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Yalnızca iade hedefi sorgulanıyor. İşlem süresi sorgulanmıyor (INT-011 onu kapsar).

---

## INT-005

- **intent_id:** INT-005
- **language:** tr
- **query_text:** "Camera Plus Plan'ım var. Bulut video kayıtlarım ne kadar süre saklanır?"
- **linked_fact_ids:** [F0402]
- **expected_fact_set_id:** INT-005
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Aktif abonelik bağlamı açıkça belirtilmiş. AC1: Buradaki 30 gün depolama süresidir, iade süresi değil. AC3: Yanlış yanıt 14 gün (deneme süresi).

---

## INT-006

- **intent_id:** INT-006
- **language:** tr
- **query_text:** "Camera Plus Plan'ın ücretsiz deneme süresi ne kadar?"
- **linked_fact_ids:** [F0405]
- **expected_fact_set_id:** INT-006
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Yalnızca deneme süresi. AC3: Yanlış yanıt 30 gün (depolama süresi).

---

## INT-007

- **intent_id:** INT-007
- **language:** tr
- **query_text:** "Standart kargo ne kadar sürer?"
- **linked_fact_ids:** [F0502]
- **expected_fact_set_id:** INT-007
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** "Standart" açıkça belirtilmiş. Beklenen yanıt: 5-7 iş günü. Yanlış yanıt: ekspres kargo (2 iş günü).

---

## INT-008

- **intent_id:** INT-008
- **language:** tr
- **query_text:** "NiceHome Camera'yı dışarıda kullanabilir miyim?"
- **linked_fact_ids:** [F0104]
- **expected_fact_set_id:** INT-008
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** "Yalnızca iç mekan" kısıtlamasını test eder. Evet/hayır sorusu kısıtlama gerçeğini tetikler.

---

## INT-009

- **intent_id:** INT-009
- **language:** tr
- **query_text:** "NiceHome cihazının tamiri genellikle ne kadar sürer?"
- **linked_fact_ids:** [F0707]
- **expected_fact_set_id:** INT-009
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** "Genellikle" gerçek formülasyonuyla uyumlu. Yanıtta "teslim alındıktan sonra" bağlantı noktası gerekli. Yanlış yanıt: 14 iş günü (iade işlem süresi).

---

## INT-010

- **intent_id:** INT-010
- **language:** tr
- **query_text:** "NiceHome bir bulut aboneliği sunuyor mu? Sunuyorsa adı nedir?"
- **linked_fact_ids:** [F0401]
- **expected_fact_set_id:** INT-010
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Abonelik adı doğrulama testi. "Camera Plus Plan" kontrollü terimdir; uydurulmuş adlar = FAIL.

---

## INT-011

- **intent_id:** INT-011
- **language:** tr
- **query_text:** "Cihazımı iade ettikten sonra para iademi almam ne kadar sürer?"
- **linked_fact_ids:** [F0308]
- **expected_fact_set_id:** INT-011
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Para iadesi işlem süresi. "İş günü" ve "teslim alındıktan sonra" gerekli. Yanlış yanıt: 10 iş günü (tamir süresi).

---

## INT-012

- **intent_id:** INT-012
- **language:** tr
- **query_text:** "Hub olmadan NiceHome Plug'ımı uzaktan açıp kapatabilir miyim?"
- **linked_fact_ids:** [F0107]
- **expected_fact_set_id:** INT-012
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Kısmi istisna gerçeğini test eder. Her iki bölüm gerekli: açma/kapatma Hub olmadan çalışır VE otomasyon Hub gerektirir.

---

## Koşullu politika niyetleri (INT-013–INT-024)

---

## INT-013

- **intent_id:** INT-013
- **language:** tr
- **query_text:** "Birinci nesil bir Hub'ım var. Buna ikinci nesil bir NiceHome Sensor bağlayabilir miyim?"
- **linked_fact_ids:** [F0108, F0109]
- **expected_fact_set_id:** INT-013
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** Her iki koşul belirtilmiş: Gen 1 Hub, Gen 2 Sensor. AC1 uyumluluk asimetrisi. Beklenen: UYUMLU DEĞİL; Gen 2 Hub gerekli.

---

## INT-014

- **intent_id:** INT-014
- **language:** tr
- **query_text:** "NiceHome Plug'ımın kutusunu açtım ama artık istemiyorum. Cihaz hasarsız ve iade sürem dolmadı. İade edebilir miyim? İade kargosu kimin sorumluluğunda?"
- **linked_fact_ids:** [F0302, F0303]
- **expected_fact_set_id:** INT-014
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** Üç koşul belirtilmiş: açılmış, hasarsız, iade süresi içinde. Üç bölümlü yanıt gerekli: iade kabul edildi + tam para iadesi + müşteri kargo ücretini öder.

---

## INT-015

- **intent_id:** INT-015
- **language:** tr
- **query_text:** "NiceHome Camera'mı düşürdüm ve çalışmıyor. Bu durum garanti kapsamında mı?"
- **linked_fact_ids:** [F0202, F0203]
- **expected_fact_set_id:** INT-015
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** "Düşürdüm" kazara hasar koşulunu net hale getirir. Beklenen: GARANTİ KAPSAMINDA DEĞİL. İstisnayı uygulamadan genel kapsam uygulamak = FAIL.

---

## INT-016

- **intent_id:** INT-016
- **language:** tr
- **query_text:** "NiceHome Hub'ımın kasasını açarak içindeki bazı parçaları değiştirdim. Şimdi çalışmıyor. Garanti hâlâ geçerli mi?"
- **linked_fact_ids:** [F0202, F0204]
- **expected_fact_set_id:** INT-016
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** Yetkisiz değişiklik açıkça belirtilmiş. Beklenen: değişiklikten kaynaklanan hasar için garanti geçersiz. Her iki gerçek gerekli.

---

## INT-017

- **intent_id:** INT-017
- **language:** tr
- **query_text:** "Camera Plus Plan'ımı faturalandırma döneminin ortasında iptal edersem, dönem sonuna kadar bulut depolama erişimim devam eder mi? Kısmi para iadesi alır mıyım?"
- **linked_fact_ids:** [F0407, F0408]
- **expected_fact_set_id:** INT-017
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** Her iki alt soru birlikte sorulmuş. Her iki bölüm gerekli: erişim dönem sonuna kadar devam eder + kısmi para iadesi yok.

---

## INT-018

- **intent_id:** INT-018
- **language:** tr
- **query_text:** "NiceHome Hub'ım üç yaşında ve donanım arızası var. Hâlâ tamir ettirilebilir mi? Ne kadar ödemem gerekir?"
- **linked_fact_ids:** [F0702, F0706]
- **expected_fact_set_id:** INT-018
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** "Üç yaşında" garanti dışı koşulunu net hale getirir (garanti 2 yıl). Her iki bölüm gerekli: servis ücreti + müşteri her iki yön kargo ücretini öder.

---

## INT-019

- **intent_id:** INT-019
- **language:** tr
- **query_text:** "Cihazım garanti kapsamında değiştiriliyor ve yerine yenilenmiş bir cihaz gönderileceğini öğrendim. Bu yenilenmiş cihazın garanti süresi ne kadar olacak?"
- **linked_fact_ids:** [F0704, F0705]
- **expected_fact_set_id:** INT-019
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** AC8 niyeti. Üç FAIL deseni önceden kaydedilmiş: sabit 90 gün, tam 2 yıllık sıfırlama, garanti yok. Gerekli: "orijinal garantinin kalan süresi veya 90 gün, hangisi uzunsa".

---

## INT-020

- **intent_id:** INT-020
- **language:** tr
- **query_text:** "Dört saat önce bir sipariş verdim ve kargoya verilmeden iptal etmek istiyorum. Bu hâlâ mümkün mü?"
- **linked_fact_ids:** [F0505, F0506]
- **expected_fact_set_id:** INT-020
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** "Dört saat önce" pencere sonrası koşulunu açık hale getirir. Her iki bölüm gerekli: iptal artık mümkün değil + teslimattan sonra iade seçeneği mevcut.

---

## INT-021

- **intent_id:** INT-021
- **language:** tr
- **query_text:** "Stokta olmayan bir NiceHome Camera için ekspres kargo seçmek istiyorum. Bu mümkün mü?"
- **linked_fact_ids:** [F0503, F0504]
- **expected_fact_set_id:** INT-021
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** "Stokta olmayan" koşulunu net hale getirir. Beklenen: stokta olmayan ürünler için ekspres kargo MEVCUT DEĞİL.

---

## INT-022

- **intent_id:** INT-022
- **language:** tr
- **query_text:** "Camera Plus Plan için ödeme yaptım ve abonelik bedelimi cihaz iade süreci aracılığıyla geri almak istiyorum. Bu mümkün mü?"
- **linked_fact_ids:** [F0306, F0408]
- **expected_fact_set_id:** INT-022
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** Abonelik iadesi, iade süreci üzerinden — çapraz belge istisnası. Beklenen: abonelikler iade kapsamında değil; iptal ayrı bir süreçtir.

---

## INT-023

- **intent_id:** INT-023
- **language:** tr
- **query_text:** "NiceHome Camera'mın ekranını kendi elimle çatlattım. İade edip para alabilir miyim?"
- **linked_fact_ids:** [F0304]
- **expected_fact_set_id:** INT-023
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** "Kendi elimle" müşteriden kaynaklanan hasarı net hale getirir. Beklenen: iade para iadesi için uygun değil.

---

## INT-024

- **intent_id:** INT-024
- **language:** tr
- **query_text:** "Camera Plus Plan'ımı faturalandırma döneminin ortasında yükselttim. Yeni plan ne zaman geçerli olur?"
- **linked_fact_ids:** [F0409]
- **expected_fact_set_id:** INT-024
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** Yükseltme belirtilmiş (yükseltme ve indirgeme F0409'a göre aynı kuralı izler). Beklenen: bir sonraki faturalandırma döneminin başında.

---

## Sorun giderme ve süreç niyetleri (INT-025–INT-036)

---

## INT-025

- **intent_id:** INT-025
- **language:** tr
- **query_text:** "Tüm NiceHome cihazlarım çevrimdışı görünüyor. Bağlantı sorununu teşhis etmek ve gidermek için hangi adımları izlemeliyim?"
- **linked_fact_ids:** [F0601, F0602, F0603, F0604]
- **expected_fact_set_id:** INT-025
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Önceki adım belirtilmemiş. Dört adımlı tam tanılama gerekli. AC5: 3. adım "yeniden başlat" olmalı, "fabrika ayarlarına sıfırla" değil.

---

## INT-026

- **intent_id:** INT-026
- **language:** tr
- **query_text:** "Sisteme yeni bir NiceHome Sensor'u nasıl eklerim?"
- **linked_fact_ids:** [F0606, F0607, F0608]
- **expected_fact_set_id:** INT-026
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** AC2: "5 saniye" gerekli, 10 değil. Üç sıralı adım gerekli. Uygulamada "Cihaz ekle" ilk adımdır.

---

## INT-027

- **intent_id:** INT-027
- **language:** tr
- **query_text:** "Eşleştirme adımlarını uyguladım ama cihaz eşleşmedi. Ne yapmam gerekiyor?"
- **linked_fact_ids:** [F0606, F0607, F0608, F0609]
- **expected_fact_set_id:** INT-027
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Eşleştirme başarısızlığı belirtilmiş. Beklenen: cihazın Hub'ın kapsama alanında olup olmadığını kontrol et. İlk adım fabrika sıfırlaması olmamalı.

---

## INT-028

- **intent_id:** INT-028
- **language:** tr
- **query_text:** "NiceHome Sensor'um garanti kapsamında ve çalışmıyor. Garanti talebinde nasıl bulunurum?"
- **linked_fact_ids:** [F0205, F0206, F0207, F0208]
- **expected_fact_set_id:** INT-028
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Garanti dahilinde olduğu belirtilmiş. Dört sıralı adım gerekli; ön ödemeli kargo etiketi gerekli (müşteri kargo ücreti ödemez).

---

## INT-029

- **intent_id:** INT-029
- **language:** tr
- **query_text:** "Açılmamış NiceHome Hub'ımı iade etmek istiyorum ve iade sürem içindeyim. Hangi adımları izlemeliyim?"
- **linked_fact_ids:** [F0309, F0310, F0311]
- **expected_fact_set_id:** INT-029
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Açılmamış + iade süresi içinde belirtilmiş. Üç sıralı adım gerekli; yetkilendirme adımı kritik; yetkilendirmesiz gönderi = FAIL.

---

## INT-030

- **intent_id:** INT-030
- **language:** tr
- **query_text:** "Şifremi unuttum ve hesabıma giriş yapamıyorum. Şifremi nasıl sıfırlayabilirim?"
- **linked_fact_ids:** [F0801, F0802, F0803]
- **expected_fact_set_id:** INT-030
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Üç sıralı adım gerekli. E-posta bağlantısı mekanizması gerekli. Telefon ile sıfırlama = FAIL.

---

## INT-031

- **intent_id:** INT-031
- **language:** tr
- **query_text:** "NiceHome Hub'ımı fabrika ayarlarına nasıl sıfırlarım? Sıfırladıktan sonra ne yapmam gerekiyor?"
- **linked_fact_ids:** [F0806, F0807]
- **expected_fact_set_id:** INT-031
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** AC2: "10 saniye" gerekli (5 değil). AC9: yeniden eşleştirme zorunluluğu belirtilmeli (F0807, D08-S4'ten). İki chunk dahil (D08-S3 + D08-S4).

---

## INT-032

- **intent_id:** INT-032
- **language:** tr
- **query_text:** "NiceHome Camera'mı fabrika ayarlarına sıfırlamak üzereyim ve bulut video kayıtlarım konusunda endişeleniyorum. Fabrika sıfırlaması bu kayıtları siler mi?"
- **linked_fact_ids:** [F0804, F0805, F0809]
- **expected_fact_set_id:** INT-032
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** AC9: Bulut video fabrika sıfırlamasıyla SİLİNMEZ (F0809). Her iki bölüm gerekli: ayarlar/hesap bağlantısı silindi + bulut video silinmedi. AC5: Fabrika sıfırlama bağlamı açık.

---

## INT-033

- **intent_id:** INT-033
- **language:** tr
- **query_text:** "NiceHome Plug'ım hiçbir komuta yanıt vermiyor — açılmıyor ve uygulamayı da görmüyor. Ne yapmalıyım?"
- **linked_fact_ids:** [F0610, F0611]
- **expected_fact_set_id:** INT-033
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Tam yanıtsızlık belirtilmiş. İki sıralı adım: (1) uygulamadan aç/kapat, (2) yumuşak sıfırlama. AC5: 2. adım yumuşak sıfırlama, fabrika sıfırlaması değil.

---

## INT-034

- **intent_id:** INT-034
- **language:** tr
- **query_text:** "NiceHome Hub'ımın ışığı kırmızı yanıp sönüyor. Bu ne anlama geliyor ve ne yapmalıyım?"
- **linked_fact_ids:** [F0605, F0603, F0604]
- **expected_fact_set_id:** INT-034
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Gösterge belirtisi tanımlanmış. Anlam (ağ bağlantısı kesildi) gerekli; sonraki adım (ağ/yönlendirici kontrolü) bekleniyor. Donanım arızası olarak yanlış tanımlama = FAIL.

---

## INT-035

- **intent_id:** INT-035
- **language:** tr
- **query_text:** "Siparişim tahmini teslimat penceresini çoktan geçti ama kayıp olduğu doğrulanmadı. Ne hakkım var — tam para iadesi mi, yeni ürün mü, yoksa başka bir şey mi?"
- **linked_fact_ids:** [F0507, F0508]
- **expected_fact_set_id:** INT-035
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Gecikmeli kargo açıkça belirtilmiş (pencere geçti, kayıp doğrulanmadı). AC6: Kargo ücreti iadesi geçerli çözümdür, ürün değişimi değil. Sorgu her iki seçeneği de sunar.

---

## INT-036

- **intent_id:** INT-036
- **language:** tr
- **query_text:** "NiceHome Camera'm kayboldu ya da çalındı. Yetkisiz kullanımı önlemek için hesabımdan uzaktan kaldırabilir miyim?"
- **linked_fact_ids:** [F0808]
- **expected_fact_set_id:** INT-036
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Kayıp/çalıntı belirtilmiş. Beklenen: uygulama aracılığıyla uzaktan kaldırma mümkün. Fiziksel erişim gerekli = FAIL.

---

## Kalite kontrolü

| Kontrol | Sonuç |
|---|---|
| Tam olarak 36 girdi | PASS — INT-001'den INT-036'ya kadar |
| query_text içinde fact ID yok | PASS — doğrulandı |
| query_text içinde belge/chunk ID yok | PASS — doğrulandı |
| query_text içinde yanıt ipucu yok | PASS — sorgular sorar, yönlendirmez |
| Koşullu niyetler için tüm koşullar korunmuş | PASS — her girdi kontrol edildi |
| Sorun giderme niyetleri sorun durumunu koruyor | PASS — her girdi kontrol edildi |
| İngilizce'den doğrudan çeviri yapılmamış | PASS — niyet spesifikasyonlarından bağımsız hazırlandı |
| Kontrollü ürün adları doğru kullanılmış | PASS — NiceHome Hub/Sensor/Plug/Camera; Camera Plus Plan |
| Yabancı özel isim eklerinde kesme işareti | PASS — Hub'ım, Hub'ı, Camera'mı, Plan'ımı vb. |
| query_text içinde TODO_REVIEW işareti | YOK |

**İnceleme bağımlılığı:** Bu Türkçe sorgular, ana Türkçe konuşan olan proje sahibi tarafından Stage 1 başlamadan önce incelenmelidir (QR9). Dil doğruluk, doğal ifade ve kontrollü terim tutarlılığı açısından tam okuma gereklidir.

---

*Sürüm: qr-tr-v0.1.0. Türkçe, eşdeğer bir renderingdir; İngilizce sorguların çevirisi değildir.*
