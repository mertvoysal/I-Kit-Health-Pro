from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile


SOURCE_DOCX = Path(r"C:\Users\mertv\Downloads\2209-a_sonuc_raporu_formati (1).docx")
TARGET_DOCX = Path(r"C:\Users\mertv\Downloads\2209-a_sonuc_raporu_FORMATLI_UZUN_FINAL_v2.docx")

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}
ET.register_namespace("w", W_NS)


PROJECT_TITLE = "I-KIT: TİROİD HASTALIKLARI İÇİN YAPAY ZEKA DESTEKLİ ERKEN TAHMİN VE RANDEVU ÖNERİ SİSTEMİ"
STUDENT = "Mert Voysal"
ADVISOR = "Prof. Dr. Gözde Ulutagay"
DATE_TEXT = "15.04.2026"


INTRO_PARAGRAPHS = [
    "Bu sonuç raporu, 2209/A başvuru formunda tanımlanan hedeflerin proje uygulama döneminde hangi düzeyde gerçekleştirildiğini sistematik olarak sunmak amacıyla hazırlanmıştır. Çalışmanın merkezinde tiroid hastalıklarının erken aşamada güvenilir biçimde öngörülmesi ve kullanıcıyı uygun uzmana yönlendiren bir karar destek akışının oluşturulması yer almaktadır.",
    "Tiroid bozuklukları, klinik pratiğin sık karşılaşılan ancak çok parametreli değerlendirme gerektiren alanlarından biridir. Özellikle birinci basamakta, laboratuvar sonuçlarının birlikte yorumlanması zaman ve uzmanlık gerektirdiğinden, dijital karar destek araçlarına ihtiyaç duyulmaktadır. Proje bu ihtiyaca yanıt verecek şekilde tasarlanmıştır.",
    "I-Kit sistemi, yalnızca tek adımlı bir makine öğrenmesi modeli olarak değil, veri doğrulama, güvenlik kontrolleri, modelleme, sonuç açıklama ve uzman yönlendirme bileşenlerini bir araya getiren bütünleşik bir yazılım mimarisi olarak geliştirilmiştir.",
    "Başvuru formunda belirtilen özgün değer önerisi; düşük maliyetli, erişilebilir, ölçülebilir başarı metrikleri üreten ve son kullanıcı açısından anlaşılır bir çözüm geliştirmekti. Uygulama sürecinde bu yaklaşım korunmuş, model güvenliği ve sürdürülebilirlik başlıklarıyla kapsam genişletilmiştir.",
    "Sistemin etik konumlandırması proje boyunca net tutulmuştur: geliştirilen yapı tanı koyan bağımsız bir sistem değil, hekim kararını destekleyen bir dijital yardımcıdır. Raporda sunulan tüm teknik kazanımlar bu ilke ile uyumlu biçimde değerlendirilmiştir.",
    "Proje çerçevesinde analiz edilen klinik parametreler (TSH, FTI, T3/TT3, TT4, T4U), veri setinin sunduğu kapsam içinde modelleme açısından anlamlı değişkenler olarak kullanılmıştır. Bu parametreler üzerinden üretilen sınıflandırma çıktıları, karar destek katmanında uzman önerisiyle birlikte sunulmuştur.",
    "Bu yaklaşım sayesinde çalışma, hem akademik bir araştırma çıktısı hem de gösterilebilir bir dijital ürün çıktısı üretmiştir. Sonuç raporunda bu iki eksen birlikte ele alınmış, başvuru formu ile uyumlu bir değerlendirme çerçevesi kurulmuştur.",
]

WORK_PARAGRAPHS = [
    "Rapor döneminde ilk adım olarak literatür taraması ve problem sınırlarının netleştirilmesi gerçekleştirilmiştir. Tiroid hastalıklarında erken tahmin yaklaşımları, tabular veri üzerinde model seçimi, klinik karar destek sistemleri ve kullanıcı odaklı sağlık arayüzleri incelenmiştir.",
    "Literatür değerlendirmesi, yalnızca model doğruluğuna odaklanan yaklaşımların saha kullanımında sınırlı kaldığını göstermiştir. Bu nedenle proje planı doğrultusunda model katmanına ek olarak veri güvenliği, yönlendirme ve arayüz bileşenleri birlikte geliştirilmiştir.",
    "Veri hazırlama aşamasında eksik değerler, hedef değişken dönüşümü, kategorik alan kodlama ve alan bazlı tutarlılık kontrolü adımları tamamlanmıştır. Eksik numerik değerlerde medyan, kategorik alanlarda mod temelli yaklaşım tercih edilmiştir.",
    "Modelin gerçek kullanıcı girişlerinde kararlı çalışması amacıyla, API seviyesinde kapsamlı doğrulama katmanı uygulanmıştır. Yaş, hormon değerleri, enlem-boylam gibi girdiler için aralık denetimleri eklenmiş; geçersiz veri durumlarında açıklayıcı hata mesajları tanımlanmıştır.",
    "Algoritma seçimi aşamasında farklı yöntemler değerlendirilmiş; tabular ve kategorik veri davranışı açısından CatBoost yaklaşımı ana model olarak belirlenmiştir. Bu tercih, proje hedefleriyle uyumlu biçimde doğruluk ve kararlılık dengesi gözetilerek yapılmıştır.",
    "Model eğitimi sonrasında performans holdout test ve stratified çapraz doğrulama ile ölçülmüştür. Değerlendirme yalnızca tek metrikle sınırlı tutulmamış; accuracy yanında precision, recall ve F1 değerleri birlikte analiz edilmiştir.",
    "Sistemde güvenlik amaçlı biyolojik sınır kontrolleri uygulanmıştır. Eğitim verisindeki değer dağılımlarının dışına çıkan girişler için önleyici doğrulama mekanizması tanımlanmış, böylece yanlış veri girişi riskinin model kararını bozması engellenmiştir.",
    "Ayrıca belirli kritik paternlerde deterministik destek kuralları kullanılmıştır. Bu hibrit yaklaşım, model çıktısının klinik sezgi ile daha uyumlu görünmesini sağlamış ve uç senaryolarda karar kalitesini güçlendirmiştir.",
    "Projenin ayırt edici bileşenlerinden biri olan uzman yönlendirme modülü de rapor döneminde tamamlanmıştır. Bu modül, model çıktısını eyleme dönüştürerek kullanıcıya uygun branş ve uzman önerisi sunmaktadır.",
    "Yönlendirme algoritmasında branş uygunluğu, unvan/tecrübe katkısı, hasta memnuniyeti ve mesafe birlikte değerlendirilmiştir. Böylece öneri listesi yalnızca tek ölçüte dayanmayan çok boyutlu bir puanlama ile sıralanmıştır.",
    "Canlı konum bilgisinin kullanılabildiği senaryolarda rota temelli mesafe hesaplanmış, dış servis erişilemediğinde ilçe bazlı fallback yaklaşımı otomatik devreye alınmıştır. Bu tasarım, uygulamanın dış bağımlılıklar nedeniyle durmasını önlemektedir.",
    "Arayüz geliştirme sürecinde kullanıcı deneyimi odaklı birçok iyileştirme yapılmıştır. Mobil uyumluluk, yüklenme geri bildirimi, sonuç kartları, etik bilgilendirme metinleri ve tablo görünümü bu dönemde olgunlaştırılmıştır.",
    "Sistem metinlerinde tıbbi terminoloji standardizasyonu sağlanmış; kullanıcıya gösterilen uyarı ve açıklamalar sade, anlaşılır ve klinik sorumluluk sınırlarını vurgulayacak biçimde düzenlenmiştir.",
    "Değerlendirme altyapısı için tekrar üretilebilir betikler hazırlanmış; metriklerin yeniden hesaplanabilir olması sağlanmıştır. Model metadata kayıtları ile versiyon ve eğitim zamanı gibi bilgiler izlenebilir hale getirilmiştir.",
    "Bu süreçlerin tamamı proje yönetim planına paralel yürütülmüş, teknik riskler düzenli biçimde gözden geçirilmiş ve gerekli iyileştirmeler uygulanmıştır. Böylece çalışma planı yalnızca geliştirme değil kalite güvencesi bakış açısıyla da yönetilmiştir.",
    "Rapor döneminde yapılan çalışmalar sonucunda, proje başlangıcında öngörülen hedeflerin büyük çoğunluğu tamamlanmış, bazı başlıklarda başlangıç hedeflerinin ötesine geçilmiştir. Özellikle model çıktısının yönlendirme modülü ile birleştirilmesi, projeyi uygulama değeri yüksek bir noktaya taşımıştır.",
    "Model yükleme ve versiyonlama sürecinde eğitim çıktısının diskten çağrılması, metadata dosyalarının tutulması ve yeniden değerlendirme betiklerinin hazırlanması sayesinde proje çıktıları sürdürülebilir hale gelmiştir.",
    "Uygulama tarafında geliştirilen canlı konum yaklaşımı; yol mesafesi, tahmini varış süresi ve fallback mekanizması ile desteklenmiş; bu sayede öneri tablosunun gerçek hayata daha yakın davranması sağlanmıştır.",
    "Arayüzde yapılan kullanıcı deneyimi güncellemeleri sonucunda rapor edilen bulguların anlaşılabilirliği artmış, hekim ve kullanıcı açısından karar destek çıktılarının yorumlanması kolaylaştırılmıştır.",
]

RESULT_PARAGRAPHS = [
    "Proje sonunda geliştirilen modelin performansı güncel değerlendirmede güçlü sonuçlar üretmiştir. Holdout test sonuçlarında Accuracy 0.9858, Precision (macro) 0.9341, Recall (macro) 0.8823 ve F1 (macro) 0.9055 düzeyi elde edilmiştir.",
    "Stratified 5 katlı çapraz doğrulama sonuçları da modelin farklı veri bölmelerinde kararlı davrandığını göstermiştir. Bu durum, performansın tek bir test ayrımına bağımlı olmadığını desteklemektedir.",
    "Model başarısının yanında, sistemin güvenli kullanımını destekleyen doğrulama ve eşik kontrolleri devreye alınmıştır. Böylece hem performans hem güvenilirlik birlikte yönetilmiştir.",
    "Uzman yönlendirme katmanı sayesinde sistem yalnızca tahmin çıktısı üretmekle kalmamış, kullanıcıya eyleme dönük bir sonraki adımı da sunmuştur. Bu özellik, projenin uygulama etkisini artıran temel unsurlardan biridir.",
    "Etik açıdan karar destek sınırı korunmuş, nihai klinik sorumluluğun hekimde olduğu açık biçimde belirtilmiştir. Sonuç olarak proje, 2209/A kapsamında beklenen araştırma disiplini ve uygulama değeri kriterlerini karşılayan bir çıktıya ulaşmıştır.",
    "Genel değerlendirmede sistem; ölçülebilir, tekrar üretilebilir, geliştirilebilir ve saha koşullarına uyarlanabilir bir yapıda tamamlanmıştır. Bu yönüyle proje, ileri Ar-Ge adımlarına açık bir teknik temel oluşturmuştur.",
    "Başvuru formunda beyan edilen performans hedeflerinin aşılması, proje çıktısının nicel olarak güçlü olduğunu göstermektedir. Bununla birlikte ekip, metriklerin klinik anlamı üzerinde de değerlendirme yapmış ve yanlış sınıflandırma risklerini raporlamıştır.",
    "Modelin açıklanabilirliğini desteklemek amacıyla arayüz çıktıları sadeleştirilmiş, kullanıcının hangi parametrelerle karar verildiğini daha kolay yorumlayabilmesi hedeflenmiştir. Bu yaklaşım, proje çıktısının benimsenebilirliğini artırmaktadır.",
]

OUTPUT_PARAGRAPHS = [
    "Projenin temel çıktısı, web tabanlı çalışan I-Kit prototipidir. Sistem kullanıcıdan laboratuvar verisi alarak risk sınıflandırması yapmakta ve gerekli durumlarda uzman yönlendirmesi üretmektedir.",
    "Teknik çıktı olarak model dosyası, metadata dosyası, değerlendirme betiği ve metrik raporları oluşturulmuştur. Bu dosyalar proje sonrasında performansın yeniden doğrulanmasına olanak sağlamaktadır.",
    "Proje çıktısı aynı zamanda eğitim ve sunum amaçlı kullanılabilecek bir demonstrasyon altyapısı sunmaktadır. Uygulama arayüzü, karar destek çıktılarının anlaşılır biçimde aktarılmasını sağlamaktadır.",
    "Çalışmanın bilimsel çıktı potansiyeli de bulunmaktadır. Özellikle hibrit karar yapısı, eksik veri yönetimi ve yönlendirme katmanının birlikte ele alınması, bildiri/makale üretimi için uygun bir araştırma zemini oluşturmaktadır.",
    "Proje bulguları teknik sunumlarda paylaşılabilecek olgunluk seviyesine ulaşmış; yazılım, modelleme ve ürünleştirme başlıklarının aynı raporda birleştirilmesine olanak tanımıştır.",
    "Canlı prototipin dış kullanıcıya açılabilmesi, projenin yalnızca laboratuvar ortamında kalmadığını ve uygulama değerinin test edilebilir hale geldiğini göstermektedir.",
    "Hazırlanan teknik dokümantasyon ve profil raporları, proje sonuçlarının akademik ve profesyonel platformlarda temsil edilmesini kolaylaştıracak niteliktedir.",
]

EXPENSE_PARAGRAPHS = [
    "Proje yazılım geliştirme, veri işleme, model eğitimi ve prototip yayına alma faaliyetleri odaklı yürütülmüştür. Bu nedenle fiziksel ekipman giderleri sınırlı, yazılım ve işlem odaklı çalışma yükü ise yüksek olmuştur.",
    "Çalışmalarda açık kaynak teknolojiler ve mevcut akademik altyapı etkin biçimde kullanılmış; maliyet/çıktı dengesi gözetilmiştir. Bu yaklaşım, proje bütçesinin verimli kullanılmasına katkı sağlamıştır.",
    "Harcama planlaması, başvuru sürecinde belirtilen kapsam ve program kuralları doğrultusunda değerlendirilmiştir. Kaynaklar proje hedeflerini doğrudan destekleyecek biçimde önceliklendirilmiştir.",
    "Toplam çıktılar dikkate alındığında, yapılan harcamaların model geliştirme, doğrulama, arayüz uygulaması ve raporlama bileşenlerine somut katkı sağladığı görülmektedir.",
    "Sonuç olarak mali kullanım, proje hedefleri ile uyumlu, teknik üretkenliği yüksek ve sürdürülebilir geliştirme anlayışını destekleyen bir çizgide gerçekleşmiştir.",
    "Yazılım geliştirme odaklı projelerde en kritik kaynak insan emeği ve zaman yönetimi olduğundan, planlama adımlarında iş paketi bazlı önceliklendirme yapılmış ve çıktı kalitesi korunmuştur.",
    "Açık kaynak kütüphanelerin tercih edilmesi yalnızca maliyet avantajı sağlamamış; aynı zamanda projenin tekrar üretilebilirliğini ve sürdürülebilirliğini artırmıştır.",
]

WORK_PARAGRAPHS += [
    "Proje sürecinde yürütülen her geliştirme adımı, başvuru formunda tanımlanan iş paketleriyle ilişkilendirilerek takip edilmiştir. Bu yöntem, teknik ilerleme ile raporlama dilinin aynı çerçevede kalmasını sağlamış ve dönem sonunda ölçülebilir bir gerçekleşme tablosu oluşmasına katkı vermiştir.",
    "Modelleme sürecinde veri dengesizliği, sınıf ayrımı ve örneklem davranışı düzenli olarak gözlemlenmiştir. Sadece nihai skor odaklı yaklaşım yerine, sınıf bazlı davranış farkları da izlenmiş ve kritik sınıflarda hata maliyetinin olası etkileri ayrıca yorumlanmıştır.",
    "Sistem mimarisinin önemli adımlarından biri, modelin yeniden eğitilmeden diskten güvenli biçimde yüklenmesini sağlayan yapının kurulması olmuştur. Bu sayede uygulamanın açılış süresi ve çalışma kararlılığı iyileştirilmiş, sunum ve canlı kullanım sırasında teknik kesinti riski azaltılmıştır.",
    "API katmanında geliştirilen yanıt şeması, yalnızca tahmin sonucu değil etik uyarı, yönlendirme bilgisi, mesafe kaynağı ve olası fallback durumu gibi açıklayıcı alanları da içerecek biçimde düzenlenmiştir. Bu yaklaşım, sistemin çıktısını daha denetlenebilir ve daha okunur hale getirmiştir.",
    "Rapor dönemlerinde kullanıcı arayüzünün dili ve tıbbi terim standardı üzerine ek revizyonlar yapılmıştır. Böylece kullanıcı girişleri ile modelde kullanılan parametreler arasında anlam tutarlılığı korunmuş; olası yanlış anlamaların önüne geçilmiştir.",
    "Canlı rota servislerinin ağ gecikmesi, erişim sınırı veya geçici kesinti riskleri için uygulanan alternatif akış, proje yönetiminde risk azaltıcı ana unsur olarak değerlendirilmiştir. Bu mekanizma sayesinde tek bir dış servise bağımlı olmayan daha dayanıklı bir sistem elde edilmiştir.",
    "Doktor öneri sıralamasında kullanılan ağırlıkların tek bir sabit dağılım olarak kalmaması için raporlama notlarında güncellenebilir parametre yaklaşımı benimsenmiştir. Böylece ileriki fazlarda uzman geri bildirimi ile kalibrasyon yapılabilecek bir yapı korunmuştur.",
    "Veri güvenliği ve kullanıcı mahremiyeti perspektifinde, sistemde doğrudan kimlikleyici kişisel veri tutulmaması prensibi korunmuştur. Kullanım akışı, laboratuvar ve demografik girdilerin karar destek amacıyla anlık işlenmesine odaklanacak şekilde sınırlandırılmıştır.",
    "Projede geliştirilen test yaklaşımı, sadece mutlu akış senaryoları ile sınırlı tutulmamıştır. Geçersiz değer, eksik değer, sınır dışı konum bilgisi ve servis kesintisi gibi durumlar da test edilerek hata yönetimi olgunlaştırılmıştır.",
    "Sonuç ekranında görselleştirme ve metin birlikte kullanılarak kullanıcıya hem hızlı hem de açıklayıcı geri bildirim verilmesi sağlanmıştır. Bu sayede model çıktısının anlaşılması kolaylaşmış ve sistemin eğitim/demonstrasyon amaçlı kullanımı güçlenmiştir.",
]

RESULT_PARAGRAPHS += [
    "Performans değerlendirmesi yorumlanırken tek bir yüksek doğruluk değerine dayanılmamış, precision ve recall dengesine özellikle dikkat edilmiştir. Böylece özellikle klinik risk içeren sınıflarda yanlış negatif ve yanlış pozitif etkileri daha görünür hale getirilmiştir.",
    "Çapraz doğrulama bulguları, modelin veri bölünmesine duyarlılığının sınırlı olduğunu ve kararlı bir öğrenme davranışı sergilediğini göstermektedir. Bu durum, projenin ileri fazlarında dış doğrulama çalışmaları için güçlü bir başlangıç noktası sunmaktadır.",
    "Sistemin uygulama başarısı yalnızca model metrikleriyle değil, akış dayanıklılığıyla da değerlendirilmiştir. Giriş doğrulama, fallback mekanizması ve açıklayıcı hata yanıtları birlikte ele alındığında prototipin operasyonel güvenilirliği artmıştır.",
    "Yönlendirme katmanının eklenmesi, çalışmanın etki alanını genişletmiştir. Kullanıcı açısından sistem yalnızca bir sınıf etiketi üretmek yerine sonraki adımı belirgin hale getirerek pratik fayda üretmiştir.",
    "Etik çerçeve ve klinik sorumluluk sınırı korunarak geliştirilen bu yapı, proje çıktısının kamu yararı ve güvenli kullanım perspektifinde değerlendirilmesini kolaylaştırmıştır.",
    "Tüm bulgular birlikte değerlendirildiğinde, proje çıktısının hem akademik hem uygulamalı kriterler açısından olgun bir seviyeye ulaştığı görülmektedir.",
]

OUTPUT_PARAGRAPHS += [
    "Hazırlanan sonuç raporu, teknik dokümantasyon ve proje profili dosyaları birlikte değerlendirildiğinde çalışmanın farklı platformlarda temsil edilebilecek bir paket haline geldiği görülmektedir.",
    "Geliştirilen yazılım mimarisi, yeni veri ve yeni kullanıcı gereksinimlerine göre genişletilebilecek modüler bir temel sunmaktadır. Bu nedenle çıktı yalnızca tek dönemlik bir prototip değil, devam ettirilebilir bir Ar-Ge çekirdeği niteliğindedir.",
    "Canlı gösterim altyapısı sayesinde proje çıktısı paydaşlara doğrudan aktarılabilmekte, karar destek akışı son kullanıcı gözünden test edilebilmektedir. Bu özellik, çıktıların görünürlüğünü ve yaygın etki potansiyelini artırmaktadır.",
]

EXPENSE_PARAGRAPHS += [
    "Maliyet planlamasında öncelik, çıktı üretimini doğrudan artıran faaliyetlere verilmiştir. Model geliştirme, doğrulama, arayüz olgunlaştırma ve raporlama adımları mali etkinlik kriterine göre dengelenmiştir.",
    "Yazılım odaklı projelerde lisans maliyeti oluşturan kapalı çözümler yerine açık kaynak ekosisteminin tercih edilmesi, bütçe verimliliğini desteklemiş ve proje kapsamının genişletilebilmesine imkan tanımıştır.",
    "Dönem sonu değerlendirmede harcamaların büyük bölümünün proje hedefleriyle doğrudan ilişkili teknik faaliyetlere ayrıldığı görülmüş; bu durum kaynak kullanımının amaçla uyumlu olduğunu ortaya koymuştur.",
]

WORK_PARAGRAPHS += [
    "Geliştirme adımlarında kod kalitesi ve bakım kolaylığı da gözetilmiştir. Fonksiyonların ayrıştırılması, dosya düzeninin sadeleştirilmesi ve script tabanlı otomasyonların eklenmesi, proje sonrasında yapılacak güncellemelerin hızını artırmıştır.",
    "Model yönetimi kapsamında sürümleme yaklaşımı benimsenmiş, modelin ne zaman ve hangi koşullarda üretildiğini izlemeye yarayan metadata alanları tanımlanmıştır. Bu yaklaşım, araştırma şeffaflığı ve denetlenebilirlik açısından önemli bir kazanım sağlamıştır.",
    "Yönlendirme akışında kullanılan kurum ve uzman eşleme mantığı, kullanıcı deneyimi testleriyle birlikte gözden geçirilmiştir. Tablo yapısı, eylem butonları ve mesafe gösterim biçimi kullanıcıdan geri bildirim alınarak daha okunur hale getirilmiştir.",
    "Arayüzde kullanılan tıbbi alan adları, laboratuvar pratiğindeki karşılıklarıyla uyumlu hale getirilmiştir. Bu düzenleme, kullanıcı giriş hatalarını azaltmış ve proje çıktısının klinik bağlamda anlaşılabilirliğini güçlendirmiştir.",
    "Rapor dönemlerinde yapılan teknik iyileştirmeler yalnızca görünür özelliklerle sınırlı kalmamış; arka planda hata yönetimi ve performans süreleri üzerinde de optimizasyonlar uygulanmıştır. Böylece sistem daha stabil bir çalışma profiline ulaşmıştır.",
]

RESULT_PARAGRAPHS += [
    "Sınıf bazlı çıktıların değerlendirilmesi, özellikle riskli sınıflarda karar kalitesinin güçlendirilmesine katkı vermiştir. Bu analizler sayesinde, model davranışının sadece genel ortalamalarla değil hedef sınıf duyarlılığı ile de yorumlanması sağlanmıştır.",
    "Sistem performansı ile kullanıcı deneyimi çıktıları birlikte değerlendirildiğinde, projenin teknik başarıyı pratik faydaya dönüştürdüğü görülmektedir. Bu durum, başvuru formunda belirtilen yaygın etki beklentisi ile uyumludur.",
    "Uçtan uca akış testlerinde, eksik veri ve servis kesintisi gibi gerçek hayatta sık karşılaşılan durumlarda uygulamanın çalışmayı sürdürdüğü doğrulanmıştır. Bu bulgu, prototipin operasyonel olgunluğunu desteklemektedir.",
    "Proje kapsamında elde edilen performans seviyeleri, ileriki dönemde veri genişletme ve dış doğrulama çalışmaları ile daha da güçlendirilebilecek bir temel sunmaktadır.",
]

OUTPUT_PARAGRAPHS += [
    "Çalışma sonucunda oluşan kod tabanı, değerlendirme betikleri ve rapor dokümanları birlikte ele alındığında proje çıktısının yalnızca dönemsel bir teslim değil, sürdürülebilir bir araştırma altyapısı olduğu görülmektedir.",
    "Sunum ve raporlama materyallerinin standartlaştırılması, proje sonuçlarının farklı akademik kurul ve paydaşlara tutarlı biçimde aktarılabilmesini kolaylaştırmıştır.",
]


def qn(tag: str) -> str:
    return f"{{{W_NS}}}{tag}"


def set_text(paragraph: ET.Element, text: str) -> None:
    ppr = paragraph.find("w:pPr", NS)
    for child in list(paragraph):
        paragraph.remove(child)
    if ppr is not None:
        paragraph.append(deepcopy(ppr))
    run = ET.SubElement(paragraph, qn("r"))
    t = ET.SubElement(run, qn("t"))
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t.text = text


def make_paragraph(template: ET.Element, text: str) -> ET.Element:
    new_p = ET.Element(qn("p"))
    ppr = template.find("w:pPr", NS)
    if ppr is not None:
        new_p.append(deepcopy(ppr))
    run = ET.SubElement(new_p, qn("r"))
    t = ET.SubElement(run, qn("t"))
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t.text = text
    return new_p


def insert_after(body: ET.Element, anchor: ET.Element, lines: list[str]) -> None:
    idx = list(body).index(anchor)
    for offset, line in enumerate(lines, start=1):
        body.insert(idx + offset, make_paragraph(anchor, line))


def set_table_cell_text(cell: ET.Element, text: str) -> None:
    p = cell.find("w:p", NS)
    if p is None:
        p = ET.SubElement(cell, qn("p"))
    set_text(p, text)


def main() -> None:
    if not SOURCE_DOCX.exists():
        raise FileNotFoundError(f"Template not found: {SOURCE_DOCX}")

    with zipfile.ZipFile(SOURCE_DOCX, "r") as zin:
        root = ET.fromstring(zin.read("word/document.xml"))
        body = root.find("w:body", NS)
        if body is None:
            raise RuntimeError("word/document.xml body not found")

        children = list(body)

        # 1) Cover paragraph: keep same location/structure, update values.
        cover_text = (
            "2209/A ÜNİVERSİTE ÖĞRENCİLERİ ARAŞTIRMA PROJELERİ DESTEK PROGRAMI SONUÇ RAPORU "
            f"PROJE BAŞLIĞI: {PROJECT_TITLE} "
            f"PROJE YÜRÜTÜCÜSÜNÜN ADI: {STUDENT} "
            f"DANIŞMANININ ADI: {ADVISOR} "
            "GENEL BİLGİLER"
        )
        set_text(children[0], cover_text)

        # 2) First table (project information)
        info_tbl = children[2]
        info_rows = info_tbl.findall("w:tr", NS)
        set_table_cell_text(info_rows[0].findall("w:tc", NS)[1], PROJECT_TITLE)
        set_table_cell_text(info_rows[1].findall("w:tc", NS)[1], STUDENT)
        set_table_cell_text(info_rows[2].findall("w:tc", NS)[1], ADVISOR)
        set_table_cell_text(
            info_rows[3].findall("w:tc", NS)[1],
            "Başlangıç ve bitiş tarihleri başvuru formunda belirtilen takvime uygun olarak tamamlanmıştır.",
        )

        # 3) Main section placeholders in body
        current = list(body)
        intro_ph = current[8]
        work_ph = current[11]
        result_ph = current[13]
        output_ph = current[15]
        expense_ph = current[17]
        signature_tbl = current[23]
        date_p = current[27]

        set_text(intro_ph, INTRO_PARAGRAPHS[0])
        insert_after(body, intro_ph, INTRO_PARAGRAPHS[1:])

        set_text(work_ph, WORK_PARAGRAPHS[0])
        insert_after(body, work_ph, WORK_PARAGRAPHS[1:])

        set_text(result_ph, RESULT_PARAGRAPHS[0])
        insert_after(body, result_ph, RESULT_PARAGRAPHS[1:])

        set_text(output_ph, OUTPUT_PARAGRAPHS[0])
        insert_after(body, output_ph, OUTPUT_PARAGRAPHS[1:])

        set_text(expense_ph, EXPENSE_PARAGRAPHS[0])
        insert_after(body, expense_ph, EXPENSE_PARAGRAPHS[1:])

        # 4) Signature table
        sig_rows = signature_tbl.findall("w:tr", NS)
        sig_row_1 = sig_rows[1].findall("w:tc", NS)
        set_table_cell_text(sig_row_1[0], STUDENT)
        set_table_cell_text(sig_row_1[1], ADVISOR)

        # 5) Date line
        set_text(date_p, f"Tarih : {DATE_TEXT}")

        new_xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)

        with zipfile.ZipFile(TARGET_DOCX, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "word/document.xml":
                    data = new_xml
                zout.writestr(item, data)

    print(f"Generated: {TARGET_DOCX}")


if __name__ == "__main__":
    main()
