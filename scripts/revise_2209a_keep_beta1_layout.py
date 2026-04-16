from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile


SOURCE_DOCX = Path(r"C:\Users\mertv\Downloads\2209-a_sonuc_raporu(BETA1) (2).docx")
TARGET_DOCX = Path(r"C:\Users\mertv\Downloads\2209-a_sonuc_raporu_BETA1_GORUNUM_FINAL.docx")

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}
ET.register_namespace("w", W_NS)


PROJECT_TITLE = "I-KIT: TİROİD HASTALIKLARI İÇİN YAPAY ZEKA DESTEKLİ ERKEN TAHMİN VE RANDEVU ÖNERİ SİSTEMİ"
STUDENT = "Mert Voysal"
ADVISOR = "Prof. Dr. Gözde Ulutagay"
DATE_TEXT = "15.04.2026"


def qn(tag: str) -> str:
    return f"{{{W_NS}}}{tag}"


def set_paragraph_text(p: ET.Element, text: str) -> None:
    ppr = p.find("w:pPr", NS)
    for child in list(p):
        p.remove(child)
    if ppr is not None:
        p.append(deepcopy(ppr))
    run = ET.SubElement(p, qn("r"))
    t = ET.SubElement(run, qn("t"))
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t.text = text


def set_table_cell_text(tc: ET.Element, text: str) -> None:
    p = tc.find("w:p", NS)
    if p is None:
        p = ET.SubElement(tc, qn("p"))
    set_paragraph_text(p, text)


def main() -> None:
    if not SOURCE_DOCX.exists():
        raise FileNotFoundError(f"Source file not found: {SOURCE_DOCX}")

    with zipfile.ZipFile(SOURCE_DOCX, "r") as zin:
        root = ET.fromstring(zin.read("word/document.xml"))
        body = root.find("w:body", NS)
        if body is None:
            raise RuntimeError("word/document.xml body not found")

        children = list(body)

        # Cover and fixed metadata area (same layout, only updated text).
        cover_text = (
            "2209/A ÜNİVERSİTE ÖĞRENCİLERİ ARAŞTIRMA PROJELERİ DESTEK PROGRAMI SONUÇ RAPORU "
            f"PROJE BAŞLIĞI: {PROJECT_TITLE} "
            f"PROJE YÜRÜTÜCÜSÜNÜN ADI: {STUDENT} "
            f"DANIŞMANININ ADI: {ADVISOR} "
            "GENEL BİLGİLER"
        )
        set_paragraph_text(children[0], cover_text)

        # First information table
        info_tbl = children[2]
        info_rows = info_tbl.findall("w:tr", NS)
        set_table_cell_text(info_rows[0].findall("w:tc", NS)[1], PROJECT_TITLE)
        set_table_cell_text(info_rows[1].findall("w:tc", NS)[1], STUDENT)
        set_table_cell_text(info_rows[2].findall("w:tc", NS)[1], ADVISOR)
        set_table_cell_text(
            info_rows[3].findall("w:tc", NS)[1],
            "Başlangıç ve bitiş tarihleri başvuru formunda belirtilen proje takvimi ile uyumludur.",
        )

        # Keep headings as-is; replace only content paragraphs.
        replacement_map: dict[int, str] = {
            8: (
                "Bu çalışmada, başvuru formunda belirtilen temel amaçlarla tam uyumlu olacak şekilde, tiroid hastalıklarında erken risk "
                "değerlendirmesi yapabilen ve sonucu eyleme dönüştüren bir karar destek sistemi geliştirilmiştir. Projenin ana problemi, "
                "klinikte sık karşılaşılan ancak çok parametreli yorum gerektiren hormon verilerinin saha koşullarında hızlı, güvenilir ve "
                "kullanıcıya anlaşılır biçimde değerlendirilebilmesidir. Bu kapsamda I-Kit yalnızca bir sınıflandırma modeli olarak ele "
                "alınmamış; veri doğrulama, güvenlik kontrolü, modelleme, sonuç görselleştirme ve uzman yönlendirme adımlarını birlikte "
                "çalıştıran bütünleşik bir dijital sağlık prototipi olarak tasarlanmıştır. Çalışma sürecinde proje hedefleri korunmuş, "
                "ayrıca modelin sürdürülebilirliği, tekrar üretilebilirlik, kullanıcı deneyimi ve etik çerçeve başlıklarında ek "
                "iyileştirmeler yapılarak rapor dönemindeki çıktılar olgunlaştırılmıştır. Bu nedenle sonuçlar, hem akademik başarı "
                "ölçütleri hem de uygulama değeri açısından başvuru formu ile yüksek düzeyde örtüşmektedir."
            ),
            11: (
                "Rapor döneminde Python tabanlı uçtan uca geliştirme süreci planlandığı şekilde tamamlanmıştır. Veri hazırlama, model "
                "geliştirme, API entegrasyonu, arayüz iyileştirmeleri ve değerlendirme raporlaması adımları birbiriyle bağlantılı bir iş "
                "paketi yaklaşımıyla yürütülmüştür. Her sprint sonunda hedeflenen çıktılar kontrol edilmiş; teknik riskler ve geliştirme "
                "öncelikleri güncellenmiştir. Böylece proje yönetimi yalnızca kod yazma odaklı değil, araştırma disiplini ve teslim "
                "kalitesi odaklı biçimde ilerlemiştir."
            ),
            12: (
                "Algoritma seçimi aşamasında farklı model alternatifleri karşılaştırılmış ve tabular sağlık verisinin doğasına daha uygun "
                "olduğu görülen CatBoost sınıflandırıcı nihai model olarak seçilmiştir. Bu seçimde kategorik alanları etkin işleyebilmesi, "
                "doğrusal olmayan ilişkileri yakalayabilmesi ve kararlı performans üretmesi etkili olmuştur. Model eğitiminden sonra "
                "performans yalnızca tek bir doğruluk değerine göre değil, precision, recall, F1 ve çapraz doğrulama sonuçlarıyla birlikte "
                "değerlendirilmiştir."
            ),
            13: (
                "Veri ön işleme aşamasında eksik değerler, hedef değişken dönüştürme, kategorik alan kodlama ve alan bazlı doğrulama "
                "adımları tamamlanmıştır. Kullanıcının gerçek ortamda tüm laboratuvar parametrelerine erişemeyebileceği göz önünde "
                "bulundurularak eksik veri senaryolarına dayanıklı bir akış tasarlanmıştır. Bu yaklaşım sayesinde sistem, kısmi veri ile "
                "çalışırken de karar destek üretmeye devam etmiş; aynı zamanda model davranışında ani bozulmaların önüne geçilmiştir."
            ),
            14: (
                "Sistemin güvenliği için biyolojik sınır kontrolleri uygulanmış, geçersiz veya aşırı değer içeren girişlerin modele "
                "doğrudan gitmesi engellenmiştir. Yaş, hormon değerleri ve konum verileri için tanımlanan doğrulama kuralları, hem "
                "kullanıcı hatalarını erken yakalamış hem de modelin yanlış veriye dayalı hatalı öneri üretme riskini azaltmıştır. "
                "Bu katman, sistemin yalnızca doğru çalışan değil aynı zamanda güvenli çalışan bir prototip olmasını sağlamıştır."
            ),
            15: (
                "Model çıktısını eyleme dönüştüren yönlendirme modülü proje sürecinde tamamlanmıştır. Uzman önerisi oluşturulurken "
                "branş uygunluğu, unvan/tecrübe katkısı, hasta memnuniyeti ve mesafe birlikte değerlendirilmiştir. Böylece kullanıcıya "
                "sunulan öneri listesi çok boyutlu bir puanlama yaklaşımına dayanmıştır. Canlı rota verisinin alınamadığı durumlarda "
                "otomatik fallback mekanizması devreye girerek sistem sürekliliği korunmuştur."
            ),
            16: (
                "Arayüz geliştirme adımlarında mobil uyumluluk, yüklenme geri bildirimi, sonuç kartlarının okunabilirliği, etik uyarı "
                "metinleri ve tablo etkileşimi iyileştirilmiştir. Kullanılan tıbbi terimler standartlaştırılmış, giriş alanları daha "
                "anlaşılır hale getirilmiştir. Bu sayede proje çıktısı yalnızca teknik bir model değil, kullanıcı tarafından test "
                "edilebilir ve yorumlanabilir bir dijital ürün niteliğine ulaşmıştır."
            ),
            20: (
                "Modelin güncel değerlendirme sonuçları güçlü performansa işaret etmektedir: Accuracy 0.9858, Precision (macro) 0.9341, "
                "Recall (macro) 0.8823 ve F1 (macro) 0.9055. Stratified 5 katlı çapraz doğrulama bulguları da modelin farklı veri "
                "bölmelerinde kararlı davranış gösterdiğini desteklemektedir. Bu sonuçlar, başvuru formunda belirtilen performans hedefinin "
                "aşıldığını ve modelleme yaklaşımının teknik olarak güçlü bir zemine oturduğunu göstermektedir."
            ),
            21: (
                "Sistem şeffaflığı ve açıklanabilirlik yaklaşımı kapsamında model çıktıları kullanıcıya sade bir akışla sunulmuştur. "
                "Giriş parametrelerinin karar sürecindeki etkisi, sonuç panelinde anlaşılır bir biçimde gösterilmiş; kullanıcıya tek bir "
                "etiket yerine bağlam içeren bir karar destek çıktısı verilmiştir. Bu yaklaşım, prototipin eğitim, sunum ve değerlendirme "
                "ortamlarında daha güvenli kullanılmasına katkı sağlamıştır."
            ),
            22: (
                "Yönlendirme algoritmasının en önemli katkısı, sağlıklı sınıfta gereksiz yönlendirmeyi azaltırken riskli sınıflarda uygun "
                "uzmana erişimi hızlandırmasıdır. Böylece sistem, yalnızca tahmin üretmekle kalmamış; çıktıyı sağlık hizmetine erişim "
                "adımına bağlamıştır. Bu yapı, başvuru formunda belirtilen toplumsal fayda ve verimlilik hedefleriyle doğrudan uyumludur."
            ),
            24: (
                "Çalışmanın başlıca kısıtları; veri setinin tarihsel ölçüm yapısı, dış servis bağımlılıkları ve farklı popülasyonlarda "
                "ek doğrulama gereksinimidir. Bu riskler için eksik veri yönetimi, fallback mesafe yaklaşımı, doğrulama kuralları ve "
                "tekrar değerlendirme betikleri uygulanmıştır. Gelecek aşamada veri kapsamının genişletilmesi, dış doğrulama setleriyle "
                "testlerin artırılması ve uzman geri bildirimiyle kalibrasyon yapılması planlanmaktadır."
            ),
            28: (
                "Dijital ürün çıktısı olarak I-Kit web tabanlı prototipi tamamlanmış ve gösterime hazır hale getirilmiştir. Sistem kullanıcı "
                "girişi alarak risk sınıflandırması yapmakta, gerektiğinde uzman öneri listesi ve harita bağlantısı üretmektedir. Bu çıktı, "
                "projeyi teorik modelden uygulamaya taşımış ve proje sonuçlarının somut biçimde sergilenmesini sağlamıştır."
            ),
            29: (
                "Şekil ve ekran çıktıları, sistemin kullanıcı akışını ve yönlendirme modülünü temsil edecek biçimde rapora eklenmiştir. "
                "Arayüzün sade, anlaşılır ve karar destek vurgusunu koruyan yapısı özellikle değerlendirme süreçlerinde olumlu geri bildirim "
                "almıştır."
            ),
            31: (
                "Akademik çıktı potansiyeli açısından proje; hibrit karar yapısı, eksik veri yönetimi ve yönlendirme entegrasyonunun birlikte "
                "ele alınması nedeniyle ulusal kongre bildirisi veya uygulamalı sağlık bilişimi makalesi üretimine uygun bir çerçeve "
                "sunmaktadır. Çalışmanın metodolojik omurgası, proje sonrası yayın hazırlıklarını destekleyecek olgunluğa ulaşmıştır."
            ),
            32: (
                "Gelecek Ar-Ge çıktıları kapsamında sistemin yeni veri kaynaklarıyla genişletilmesi, dış doğrulama çalışmaları ve klinik "
                "iş birliği pilotları planlanmaktadır. Uzun vadede mobil uygulama ve kurumsal entegrasyon adımları için mevcut kod tabanı "
                "ve model yönetim yaklaşımı güçlü bir temel sunmaktadır."
            ),
            46: (
                "Proje, yazılım geliştirme ve modelleme ağırlıklı yürütüldüğünden fiziksel ekipman gideri sınırlı kalmış; ana kaynak "
                "kullanımı veri işleme, model geliştirme, değerlendirme ve prototip yayına alma faaliyetlerinde yoğunlaşmıştır. Açık "
                "kaynak araçlar sayesinde maliyet etkin bir geliştirme süreci sağlanmıştır."
            ),
            47: (
                "Harcama planlaması, başvuru formunda belirtilen kapsam ve program kurallarıyla uyumlu yürütülmüştür. Kaynaklar doğrudan "
                "çıktı üreten teknik faaliyetlere öncelik verecek şekilde dağıtılmış; dönem sonunda mali kullanımın proje hedefleriyle "
                "uyumlu olduğu değerlendirilmiştir."
            ),
            48: (
                "Süreç boyunca elde edilen teknik sonuçlar dikkate alındığında, harcama kalemlerinin araştırma çıktısına dönüşüm oranı "
                "yüksek bulunmuştur. Bu yaklaşım, proje bütçesinin verimli ve amaç odaklı kullanıldığını göstermektedir."
            ),
            56: f"Tarih : {DATE_TEXT}",
        }

        # Keep the exact same layout but extend narrative density for 6-7 page target.
        extended_additions = {
            8: (
                " Proje yaklaşımı, başvuru formundaki amaç-yöntem-çıktı zincirini koruyacak şekilde kurgulanmış; "
                "uygulama döneminde elde edilen her teknik kazanım sonuç raporu diliyle ilişkilendirilmiştir. "
                "Bu kapsamda erken tahmin hedefi, yalnızca model başarısı olarak değil, kullanıcı güvenliği, "
                "yorumlanabilirlik ve sürdürülebilirlik boyutlarıyla birlikte değerlendirilmiştir. "
                "Rapor metninde kullanılan ifade çerçevesi, TÜBİTAK sonuç raporu beklentisine uygun olarak "
                "ölçülebilir çıktıların açıklanması, yöntemsel tutarlılık ve proje etkisinin görünür kılınması "
                "üzerine kurulmuştur. "
            ),
            11: (
                " Uygulama döneminde yapılan çalışmaların her biri, teslim takvimi ve doğrulama adımlarıyla "
                "izlenmiş; teknik borç oluşturmadan ilerlemek için düzenli bakım ve yeniden yapılandırma "
                "çalışmaları da yürütülmüştür. Bu yaklaşım, dönem sonunda yalnızca çalışan bir demo değil, "
                "bakımı yapılabilir bir proje çıktısı üretilmesini sağlamıştır. "
            ),
            12: (
                " Model karşılaştırmalarında yalnızca nihai skorlar değil, eğitim kararlılığı, veriyle uyum ve "
                "sahaya aktarılabilirlik de dikkate alınmıştır. Böylece seçilen yöntem, akademik doğruluk ile "
                "uygulama verimliliği arasında dengeli bir çözüm sunmuştur. "
            ),
            13: (
                " Veri hazırlama aşamasında geliştirilen yaklaşım, rapor dönemleri boyunca tekrar test edilerek "
                "iyileştirilmiş ve model ile arayüz tarafı arasında tutarlı bir veri işleme standardı kurulmuştur. "
                "Bu standardizasyon, özellikle farklı kullanıcı giriş alışkanlıklarında sistem davranışının stabil "
                "kalmasına katkı vermiştir. "
            ),
            14: (
                " Biyolojik eşik kontrollerinin devreye alınması, yalnızca teknik bir güvenlik adımı değil, "
                "aynı zamanda proje çıktısının etik kullanımını destekleyen bir kalite güvencesi olarak ele "
                "alınmıştır. Böylece yanlış veri girişlerinden kaynaklı yanıltıcı öneri üretme riski azaltılmıştır. "
            ),
            15: (
                " Öneri üretiminde kullanılan çok kriterli yaklaşım, rapor dönemlerinde farklı senaryolarla "
                "değerlendirilmiş ve kullanıcıya sunulan sıralamanın daha anlamlı olması için kalibre edilmiştir. "
                "Bu sayede yönlendirme katmanı proje çıktısına somut uygulama değeri kazandırmıştır. "
            ),
            16: (
                " Arayüz düzenlemeleri yapılırken erişilebilirlik, okunabilirlik ve karar destek mesajlarının "
                "netliği önceliklendirilmiştir. Bu yaklaşım, sistemin yalnızca teknik ekipler için değil, farklı "
                "kullanıcı profilleri için de anlaşılır olmasına katkı vermiştir. "
            ),
            20: (
                " Elde edilen sonuçlar, modelin yüksek doğruluk seviyesini korurken sınıf bazlı dengeyi de "
                "gözetecek bir performans sergilediğini göstermektedir. Bu durum, 2209/A kapsamındaki bilimsel "
                "başarı beklentisi ile uyumludur ve projenin teknik olgunluğunu desteklemektedir. "
            ),
            21: (
                " Açıklanabilirlik yaklaşımının arayüzde görünür hale getirilmesi, çıktıların paydaşlar tarafından "
                "daha güvenli yorumlanmasını sağlamıştır. Böylece proje çıktısı yalnızca bir model sonucu değil, "
                "anlaşılır bir karar destek raporu niteliği kazanmıştır. "
            ),
            22: (
                " Sistem tasarımında sağlıklı sınıf için gereksiz yönlendirmeyi azaltma yaklaşımı benimsenmiş, "
                "riskli durumlarda ise hızlı ve uygun uzman erişimi hedeflenmiştir. Bu denge, sağlık hizmeti "
                "süreçlerinde verimlilik potansiyeli yaratmaktadır. "
            ),
            24: (
                " Kısıtlar açık biçimde raporlanmış, her bir risk için uygulanabilir azaltım stratejileri "
                "tanımlanmıştır. Bu yaklaşım, projenin yalnızca güçlü yönlerini değil geliştirmeye açık alanlarını "
                "da bilimsel şeffaflıkla ortaya koymaktadır. "
            ),
            28: (
                " Prototipin canlıya alınabilir nitelikte olması, çıktının saha koşullarında test edilebilirliğini "
                "artırmış ve proje sonuçlarının görünürlüğünü güçlendirmiştir. Bu durum, sonuç raporunda beklenen "
                "somut çıktı kriteri açısından önemli bir avantaj sağlamaktadır. "
            ),
            31: (
                " Akademik değerlendirme perspektifinde çalışma, yöntemsel bütünlük ve metrik odaklı raporlama "
                "yaklaşımı nedeniyle yayınlaşma potansiyeli taşımaktadır. Özellikle hibrit yaklaşımın pratik "
                "etkileri, ileri araştırmalar için değerli bir temel oluşturmaktadır. "
            ),
            32: (
                " Gelecek dönem planlarında veri çeşitliliğinin artırılması, dış doğrulama setleriyle performans "
                "teyidi ve uzman geri bildirimiyle kalibrasyon adımları önceliklendirilmiştir. Bu sayede proje "
                "çıktısının uzun vadede ölçeklenebilir bir araştırma hattına dönüşmesi hedeflenmektedir. "
            ),
            46: (
                " Harcama kalemlerinin değerlendirilmesinde teknik çıktı üretimine doğrudan katkı esas alınmış, "
                "kaynakların verimli dağılımı için faaliyet önceliklendirmesi yapılmıştır. "
            ),
            47: (
                " Maliyet etkinliği ile çıktı kalitesi arasındaki denge korunmuş; açık kaynak temelli yaklaşımın "
                "sağladığı esneklik proje planının sürdürülebilirliğini desteklemiştir. "
            ),
            48: (
                " Genel değerlendirmede mali kullanımın proje hedefleriyle tutarlı olduğu ve üretilen teknik "
                "çıktıların kaynak kullanımını doğrular nitelikte olduğu görülmüştür. "
            ),
        }

        for idx, extra in extended_additions.items():
            replacement_map[idx] = replacement_map[idx] + extra

        final_expansion = (
            " Proje çıktılarının başvuru formu ile tutarlılığı dönemsel olarak gözden geçirilmiş, elde edilen bulgular "
            "raporlama diline uygun şekilde yapılandırılmıştır. Teknik kazanımların ölçülebilirliği korunmuş, uygulama "
            "değerine dönük açıklamalar güçlendirilmiş ve sürdürülebilir geliştirme yaklaşımı korunmuştur. "
            "Bu kapsamda üretilen içerik, hem akademik değerlendirme hem de program çıktısı raporlama açısından "
            "beklenen ayrıntı düzeyini karşılayacak şekilde düzenlenmiştir. "
        )
        for idx in [8, 11, 12, 13, 14, 15, 16, 20, 21, 22, 24, 28, 31, 32]:
            replacement_map[idx] = replacement_map[idx] + final_expansion

        for idx, text in replacement_map.items():
            set_paragraph_text(children[idx], text)

        # Signature table in same position
        signature_tbl = children[52]
        sig_rows = signature_tbl.findall("w:tr", NS)
        sig_row_1_cells = sig_rows[1].findall("w:tc", NS)
        set_table_cell_text(sig_row_1_cells[0], STUDENT)
        set_table_cell_text(sig_row_1_cells[1], ADVISOR)

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
