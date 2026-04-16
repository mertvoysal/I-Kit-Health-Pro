from __future__ import annotations

from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile


SOURCE_DOCX = Path(r"C:\Users\mertv\Downloads\2209-a_sonuc_raporu(BETA1) (2).docx")
TARGET_DOCX = Path(r"C:\Users\mertv\Downloads\2209-a_sonuc_raporu_REVIZE_FINAL.docx")

NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NSMAP = {"w": NS_W}


REVISED_REPORT = """
2209/A UNIVERSITE OGRENCILERI ARASTIRMA PROJELERI DESTEK PROGRAMI
SONUC RAPORU

PROJE BASLIGI:
I-KIT: TIROID HASTALIKLARI ICIN YAPAY ZEKA DESTEKLI ERKEN TAHMIN VE RANDEVU ONERI SISTEMI

PROJE YURUTUCUSU:
Mert Voysal

DANISMAN:
Prof. Dr. Gozde Ulutagay

1) GIRIS
Bu sonuc raporu, proje onerisi asamasinda tanimlanan bilimsel hedefler ile uygulama surecinde elde edilen teknik ve urun tabanli cikarimlari birlikte sunmak amaciyla hazirlanmistir.
Projenin temel problemi, tiroid hastaliklarinda erken risk siniflandirmasinin hem laboratuvar parametrelerinin cok boyutlu yapisi hem de saha kosullarindaki eksik/veri heterojenligi nedeniyle zorlasmasidir.
Bu kapsamda I-Kit, sadece bir siniflandirma modeli degil, klinik karar destek mantigina yakin calisan tumlesik bir dijital yardimci olarak tasarlanmistir.

Basvuru formunda beyan edilen ana hedefler su sekildeydi:
- Tiroid durumunun yapay zeka destekli erken tahmini,
- Hekim/randevu yonlendirme katmani ile uygulamaya donuk fayda uretilmesi,
- Dogruluk ve sinif-bazli basari olcutlerinin raporlanmasi,
- Dusuk maliyetli ve erisilebilir bir dijital saglik prototipinin ortaya konmasi.

Proje surecinde bu hedefler korunmus; ayrica model guvenligi, tekrar uretilebilirlik (reproducibility), canli ortam uyumlulugu ve kullanici deneyimi katmanlariyla calisma kapsamli sekilde derinlestirilmistir.

2) RAPOR DONEMLERINDE YAPILAN CALISMALAR
2.1 Veri Hazirlama ve On Isleme
Calismada kullanilan veri setinde eksik degerler, olcum bayraklari ve kategorik degiskenler sistematik olarak ele alinmistir.
Numerik alanlarda medyan tabanli tamamlama; kategorik alanlarda ise tutarli kodlama adimlari uygulanmistir.
Ayrica sistemin sahadaki gercek kullanimina uygun olarak, kullanicinin tum panel degerlerini girmedigi senaryolarda tahminin durmamasini saglayan guvenli varsayim mekanizmasi gelistirilmistir.

2.2 Algoritma Secimi ve Modelleme
Farkli algoritma alternatifleri degerlendirilmis; tabular ve kategorik odakli saglik verilerinde dengeli performans vermesi nedeniyle CatBoost tabanli yapi ana model olarak secilmistir.
Model; egitim/test ayrimi, capraz dogrulama ve sinif-bazli metriklerle denetlenmistir.
Bu surec, basvuru formunda tanimlanan "olculebilir performans" hedefiyle uyumlu olacak sekilde yurutulmustur.

2.3 Guvenlik ve Klinik Mantik Katmani
Sisteme yalnizca istatistiksel degil, biyolojik olarak da makul sinir kontrolleri eklenmistir.
Asiri veya anlamsiz girislere karsi laboratuvar aralik kontrolleri tanimlanmis; boylece modelin dis veri girdi risklerine karsi dayanikliligi artirilmistir.
Ek olarak, kritik hormon paternlerinde deterministik destek kurallari ile model ciktilarinin klinik aciklanabilirligi guclendirilmistir.

2.4 Randevu ve Uzman Yonlendirme Modulu
Projenin ayirt edici katkilarindan biri, tahmin sonucunun eyleme donusmesini saglayan uzman yonlendirme katmanidir.
Bu katmanda:
- Brans uygunlugu,
- Hekim unvan/tecrube katkisi,
- Hasta memnuniyeti,
- Mesafe/rota bilgisi
birlikte degerlendirilerek kullaniciya sirali uzman listesi sunulmustur.
Canli konum verisinin alinamadigi kosullarda sistemin ilce tabanli geri donus mekanizmasi otomatik olarak devreye alinmistir.

2.5 Uygulama ve Arayuz Gelistirme
Modelleme calismasi kullaniciya dogrudan temas eden web tabanli bir arayuze donusturulmustur.
Arayuzde:
- giris dogrulama,
- yuklenme geri bildirimi,
- acik etik uyari metinleri,
- sonuc gorunsellestirme ve hekim tablosu
gibi unsurlar uygulanmistir.
Bu sayede proje, yalnizca akademik metrik sunan bir model degil; sahada test edilebilir bir prototip niteligine ulasmistir.

3) DEGERLENDIRME VE BULGULAR
3.1 Performans Metrikleri
Guncel degerlendirme ciktilarina gore model:
- Accuracy: 0.9858
- Precision (macro): 0.9341
- Recall (macro): 0.8823
- F1-score (macro): 0.9055
degerlerine ulasmistir.

5-katmanli stratified cross-validation sonuclarinda da performansin kararliligini destekleyen ortalama degerler elde edilmistir.
Bu bulgular, basvuru asamasinda hedeflenen basari esitiginin asildigini ve modelin farkli bolmelerde tutarli performans gosterdigini ortaya koymaktadir.

3.2 Teknik Yorum
Makro metriklerin raporlanmasi sayesinde sinif dengesizliklerinin olasi etkisi tek bir dogruluk degerine indirgenmemis; siniflar arasi davranis da takip edilmistir.
Bu yaklasim, 2209-A kapsaminda beklenen arastirma disiplini ve metodolojik seffaflik acisindan olumlu bir ciktidir.

3.3 Uygulama Yorum
Sistem, "saglikli" sonucunda gereksiz yonlendirmeyi azaltirken; riskli paternlerde uygun uzmana yonlendirme saglamaktadir.
Bu yapi, zaman yonetimi, hasta farkindaligi ve birinci basamakta dijital destek acisindan pratik fayda uretmektedir.

4) KISITLAR, RISKLER VE B PLANI
Calismanin baslica kisitlari:
- Veri setinin tarihsel olcum bilesenleri nedeniyle bazi modern panel esdegerliklerinin dolayli yorum gerektirmesi,
- Canli rota servislerinin dis bagimlilik icermesi,
- Farkli hastane/bolge dagilimlarinda performansin tekrar test edilme ihtiyaci.

Uygulanan B plani yaklasimlari:
- Rota servisi kesintisinde ilce/mesafe geri donusu,
- Eksik veri senaryosunda guvenli varsayim mekanizmasi,
- Donemsel yeniden degerlendirme scripti ile metrik guncelleme.

Bu yaklasimlar sayesinde sistem tek noktadan hata veren bir yapi olmaktan cikarilip operasyonel olarak daha dayanikli hale getirilmistir.

5) ETIK, GUVENLIK VE KLINIK SORUMLULUK
Proje boyunca "tani koyan sistem" iddiasi yerine "karar destek" ilkesi benimsenmistir.
Arayuz ve API ciktilarinda bu sinir acikca belirtilmistir.
Nihai klinik karar sorumlulugu hekimde kalacak sekilde metinler ve kullanim akisi duzenlenmistir.
Bu tutum, hem etik uyum hem de kamu sagligi acisindan gerekli bir emniyet katmani olusturmaktadir.

6) CIKTILAR (YAYIN, SUNUM, DIJITAL URUN)
Projenin somut ciktisi, canli ortamda calisabilir bir web prototipidir.
Ek olarak:
- tekrar uretilebilir degerlendirme scriptleri,
- model metadata dosyalari,
- teknik rapor ve profil dokumanlari
hazirlanmistir.
Calismanin gelisime acik dogasi sayesinde ulusal kongre bildirisi/teknik makale formatina donusturulebilecek bir metodolojik omurga ortaya cikmistir.

7) BASVURU FORMU ILE ORTUSME DEGERLENDIRMESI
Bu sonuc raporu, basvuru formunda tanimlanan:
- problem tanimi,
- yontem,
- olculebilir basari,
- yaygin etki,
- surdurulebilirlik
basliklariyla dogrudan uyumludur.
Proje, vaat edilen cekirdek hedefleri gerceklestirmekle kalmamis; urunlestirme, guvenlik, etik ve canli kullanim katmanlariyla kapsamini genisletmistir.

8) SONUC
I-Kit projesi, 2209-A baglaminda ogrenci arastirma projesinden uygulamaya donuk bir dijital saglik prototipine donusen, olculebilir, tekrar uretilebilir ve gelistirilebilir bir calisma olarak tamamlanmistir.
Elde edilen bulgular, erken risk siniflandirmasi ve uzman yonlendirme konusunda yuksek potansiyel gostermektedir.
Bir sonraki asamada veri cesitliliginin artirilmasi, sahaya ozel kalibrasyonlar ve klinik isbirligi pilotlari ile sistemin etkisinin genisletilmesi hedeflenmektedir.
""".strip()


def extract_sect_pr_xml(document_xml: bytes) -> str:
    root = ET.fromstring(document_xml)
    body = root.find("w:body", NSMAP)
    if body is None:
        return ""
    sect = body.find("w:sectPr", NSMAP)
    if sect is None:
        return ""
    return ET.tostring(sect, encoding="unicode")


def paragraph_xml(text: str) -> str:
    if not text.strip():
        return "<w:p/>"
    safe_text = escape(text)
    return (
        "<w:p>"
        "<w:r><w:rPr><w:sz w:val=\"22\"/></w:rPr>"
        f"<w:t xml:space=\"preserve\">{safe_text}</w:t></w:r>"
        "</w:p>"
    )


def build_document_xml(report_text: str, sect_pr_xml: str) -> str:
    paragraphs = [paragraph_xml(line) for line in report_text.splitlines()]
    sect = sect_pr_xml if sect_pr_xml else "<w:sectPr/>"
    body_xml = "".join(paragraphs) + sect
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        f"<w:document xmlns:w=\"{NS_W}\">"
        f"<w:body>{body_xml}</w:body>"
        "</w:document>"
    )


def main() -> None:
    if not SOURCE_DOCX.exists():
        raise FileNotFoundError(f"Source docx not found: {SOURCE_DOCX}")

    with zipfile.ZipFile(SOURCE_DOCX, "r") as zin:
        original_document_xml = zin.read("word/document.xml")
        sect_pr_xml = extract_sect_pr_xml(original_document_xml)
        new_document_xml = build_document_xml(REVISED_REPORT, sect_pr_xml).encode("utf-8")

        with zipfile.ZipFile(TARGET_DOCX, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "word/document.xml":
                    data = new_document_xml
                zout.writestr(item, data)

    print(f"Revised report created: {TARGET_DOCX}")


if __name__ == "__main__":
    main()
