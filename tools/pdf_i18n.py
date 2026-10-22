"""Chinese and Hungarian wording for all Rumah Márton PDFs (residence brochures, floor plans, project brochure).

English lives in build.py / brochure.py. Each language below overrides it. Chinese follows the client's own
Chinese brochure terminology (玛墩山邸, 花园宅邸, 顶层宅邸, 玛顿山, 布达城堡, 盖勒特山 …).
Run:  python3 build_lang.py hu   |   python3 build_lang.py zh
"""

ROOMS = {
 "hu": {"Private lobby": "Privát liftelőtér", "Entrance hall": "Bejárati előszoba", "Study": "Dolgozószoba", "Foyer": "Előtér",
        "Powder room": "Vendég-WC", "Kitchen and dining": "Konyha és étkező", "Living": "Nappali", "Corridor": "Folyosó",
        "Bedroom 01": "Hálószoba 01", "Bedroom 02": "Hálószoba 02", "Bathroom": "Fürdőszoba", "Entrance foyer": "Előszoba",
        "Master suite": "Fő hálószoba", "Master closet": "Gardrób", "Master bath": "Fő fürdőszoba", "Bedroom 03 / study": "Hálószoba 03 / dolgozószoba"},
 "zh": {"Private lobby": "私人电梯前厅", "Entrance hall": "入户门厅", "Study": "书房", "Foyer": "玄关",
        "Powder room": "客用盥洗室", "Kitchen and dining": "厨房与餐厅", "Living": "起居室", "Corridor": "走廊",
        "Bedroom 01": "卧室一", "Bedroom 02": "卧室二", "Bathroom": "卫浴", "Entrance foyer": "玄关",
        "Master suite": "主卧套房", "Master closet": "主卧更衣间", "Master bath": "主卧卫浴", "Bedroom 03 / study": "卧室三 / 书房"},
}
TOTALS = {
 "hu": {"Interior": "Belső alapterület", "Terrace": "Terasz", "Terraces": "Teraszok", "Weighted area": "Súlyozott alapterület",
        "Private garden": "Privát kert", "Balcony": "Erkély", "Balconies": "Erkélyek", "Rooftop terrace": "Tetőterasz",
        "terraces at 50%": "teraszok 50%-kal számítva", "outdoor areas at 50%": "kültéri területek 50%-kal számítva",
        "with kitchen provision · see roof plan": "kültéri konyha előkészítéssel · lásd a tetőszint alaprajzát",
        "private to the Penthouse, with provision for an outdoor kitchen": "a penthouse kizárólagos használatában, kültéri konyha előkészítéssel"},
 "zh": {"Interior": "室内面积", "Terrace": "露台", "Terraces": "露台合计", "Weighted area": "加权面积",
        "Private garden": "专属花园", "Balcony": "阳台", "Balconies": "阳台合计", "Rooftop terrace": "屋顶露台",
        "terraces at 50%": "露台按 50% 计", "outdoor areas at 50%": "户外面积按 50% 计",
        "with kitchen provision · see roof plan": "预留户外厨房 · 详见屋顶平面图",
        "private to the Penthouse, with provision for an outdoor kitchen": "顶层宅邸专属，预留户外厨房"},
}
PLAN_TITLES = {
 "hu": {"Ground floor plan": "Földszinti alaprajz", "Floor plan · 3 bedrooms": "Alaprajz · 3 hálószoba",
        "Floor plan · 2 bedrooms, grand master suite": "Alaprajz · 2 hálószoba, tágas fő hálószobával", "Rooftop terrace plan": "Tetőterasz alaprajza",
        "The balconies B1 and B2 are on the residence floor below.": "A B1 és B2 erkély az alatta lévő lakószinten található."},
 "zh": {"Ground floor plan": "首层平面图", "Floor plan · 3 bedrooms": "平面图 · 三房",
        "Floor plan · 2 bedrooms, grand master suite": "平面图 · 两房，奢阔主卧套房", "Rooftop terrace plan": "屋顶露台平面图",
        "The balconies B1 and B2 are on the residence floor below.": "阳台 B1 与 B2 位于下一层的宅邸楼层。"},
}
CAPTIONS = {
 "hu": {"Garden Residence": "Kertes rezidencia", "Penthouse Residence": "Penthouse", "Living": "Nappali", "Master suite": "Fő hálószoba",
        "Second bedroom": "Második hálószoba", "Study": "Dolgozószoba", "Rooftop terrace": "Tetőterasz",
        "Outdoor kitchen and dining": "Kültéri konyha és étkező", "Bathroom": "Fürdőszoba", "Concept": "koncepció",
        "The view from Mártonhegy": "Kilátás a Mártonhegyről", "Mártonhegy, Budapest XII": "Mártonhegy, Budapest XII. kerület"},
 "zh": {"Garden Residence": "花园宅邸", "Penthouse Residence": "顶层宅邸", "Living": "起居室", "Master suite": "主卧套房",
        "Second bedroom": "次卧", "Study": "书房 / 多功能室", "Rooftop terrace": "屋顶露台",
        "Outdoor kitchen and dining": "室内外无界衔接 · 户外厨房与餐区", "Bathroom": "浴室", "Concept": "概念图",
        "The view from Mártonhegy": "玛顿山远眺", "Mártonhegy, Budapest XII": "布达佩斯第十二区 · 玛顿山"},
}

UNITS = {
 "hu": {
  "garden": dict(name="Kertes rezidencia", file="Rumah-Marton-Kertes-Rezidencia-HU.pdf",
                 lede="Kétszobás otthon dolgozószobával, amely közvetlenül saját privát kertjére nyílik – tágas teraszokkal és a falba futó tolóajtókon túl kültéri konyha kiépítésének lehetőségével.",
                 facts=[("Szint", "Földszint"), ("Hálószobák", "2 hálószoba és egy dolgozószoba, amely harmadik hálószobaként is használható"),
                        ("Belső alapterület", "86 m²"), ("Teraszok", "61 m²"), ("Privát kert", "232 m²")]),
  "penthouse": dict(name="Penthouse", file="Rumah-Marton-Penthouse-HU.pdf",
                 lede="Budapestre néző, privát legfelső szinti otthon két erkéllyel és kizárólagos tetőterasszal, amelyet a szabadtéri életre és a vendéglátásra terveztünk, saját kültéri konyha kiépítésének lehetőségével.",
                 facts=[("Szint", "Legfelső szint, tetőterasszal"), ("Hálószobák", "3 hálószoba, vagy 2 egy tágasabb fő hálószobával"),
                        ("Belső alapterület", "100 m²"), ("Erkélyek", "21 m²"), ("Tetőterasz", "39 m²")])},
 "zh": {
  "garden": dict(name="花园宅邸", file="Rumah-Marton-Garden-Residence-ZH.pdf",
                 lede="两卧一书房的居所，直通专属私家花园；宽阔露台在全高隐藏式推拉门外徐徐展开，并预留独立户外厨房。",
                 facts=[("楼层", "首层"), ("卧室", "2 间卧室及 1 间书房，书房可作第三间卧室"),
                        ("室内面积", "86 m²"), ("露台", "61 m²"), ("专属花园", "232 m²")]),
  "penthouse": dict(name="顶层宅邸", file="Rumah-Marton-Penthouse-Residence-ZH.pdf",
                 lede="俯瞰布达佩斯的私属顶层宅邸，拥有两处阳台及一座专属屋顶露台，专为户外生活与宴客而设，并预留独立户外厨房。",
                 facts=[("楼层", "顶层，配屋顶露台"), ("卧室", "三房，或两房配更奢阔的主卧套房"),
                        ("室内面积", "100 m²"), ("阳台", "21 m²"), ("屋顶露台", "39 m²")])},
}

# ---------- residence-brochure + shared strings ----------
T = {
 "hu": dict(
  eyebrow="Rumah Márton<br>Mártonhegy, Budapest", areas_note="Alapterületek m²-ben, az engedélyezett tervek alapján.",
  be_in_touch="Lépjen kapcsolatba velünk", l_vr="A lakás felfedezése 360°-ban", l_site="A Rumah Márton weboldala",
  l_wy="A WY Design bemutatkozása", l_pei="Ismerje meg Pei Yongot — interjú",
  addr="Rumah Márton<br>Mártonvölgyi út, XII. kerület, Budapest", done="Tervezett átadás — 2028 III. negyedév",
  included="Minden otthon része", map_cap="A környék · tájékoztató menetidők", mins="perc", doc_prefix="Rumah Márton",
  tabs={"penthouse-plan-3-bedrooms": "3 hálószoba", "penthouse-plan-2-bedrooms": "2 hálószoba", "penthouse-roof-terrace-plan": "Tetőterasz", "garden-residence-plan": "Földszint"},
  map={"Normafa": "Normafa", "American International School (AISB)": "Amerikai Nemzetközi Iskola (AISB)",
       "The British International School (BISB)": "Brit Nemzetközi Iskola (BISB)", "Britannica International School": "Britannica Nemzetközi Iskola",
       "Hegyvidék Shopping Centre": "Hegyvidék Bevásárlóközpont", "MOM Park": "MOM Park", "Citadella": "Citadella", "Castle Hill": "Budai Vár",
       "Parliament": "Országház", "Margaret Island": "Margitsziget", "Andrássy út": "Andrássy út", "Villa Bagatelle": "Villa Bagatelle"},
  # project brochure
  cover_title="Rumah Márton", pts_head="Gondosan megkomponált életforma",
  pts_sub="Díjnyertes csapat alkotása – átgondolt tervezési szemlélettel és megalkuvás nélküli részletgazdagsággal.",
  spec_title="Műszaki tartalom", get_in_touch="Lépjen kapcsolatba velünk", recognition="Válogatott elismerések",
  online="Vagy írjon nekünk online", meta="Mártonvölgyi út, Budapest XII. · Átadás 2028 III. negyedév",
  doc_title="Rumah Márton · Mártonhegy, Budapest"),
 "zh": dict(
  eyebrow="玛墩山邸 Rumah Márton<br>布达佩斯 · 玛顿山", areas_note="面积单位为平方米，依据已获批图纸。",
  be_in_touch="联系我们", l_vr="360° 探索宅邸", l_site="访问玛墩山邸网站", l_wy="探索 WY Design", l_pei="开发者 Pei Yong — 人物专访",
  addr="玛墩山邸 Rumah Márton<br>布达佩斯第十二区 Mártonvölgyi út", done="计划竣工 — 2028年第三季度",
  included="每户标配", map_cap="周边环境 · 大致车程", mins="分钟", doc_prefix="玛墩山邸 Rumah Márton",
  tabs={"penthouse-plan-3-bedrooms": "三房", "penthouse-plan-2-bedrooms": "两房", "penthouse-roof-terrace-plan": "屋顶露台", "garden-residence-plan": "首层"},
  map={"Normafa": "诺尔马法森林公园", "American International School (AISB)": "美国国际学校 AISB",
       "The British International School (BISB)": "英国国际学校 BISB", "Britannica International School": "Britannica 国际学校",
       "Hegyvidék Shopping Centre": "Hegyvidék 购物中心", "MOM Park": "MOM Park 商业中心", "Citadella": "盖勒特山 Citadella", "Castle Hill": "布达城堡",
       "Parliament": "议会大厦", "Margaret Island": "玛格丽特岛", "Andrássy út": "安德拉什大街", "Villa Bagatelle": "Villa Bagatelle 咖啡馆",
       "Rumah Márton": "玛墩山邸"},
  cover_title="玛墩山邸", pts_head="臻选生活方式",
  pts_sub="由屡获殊荣的团队以深思的设计理念与对细节的极致追求倾心打造。",
  spec_title="建筑居住配置总览", get_in_touch="联系我们", recognition="媒体报道与奖项",
  online="或在线给我们留言", meta="布达佩斯第十二区 Mártonvölgyi út · 2028年第三季度竣工",
  doc_title="玛墩山邸 Rumah Márton · 布达佩斯玛顿山"),
}

RES = {
 "hu": dict(
  CLOSING_LEFT=["Szívesen megmutatjuk Önnek a helyszínt, és részletesen bemutatjuk a {name} terveit.",
                "Ha szeretné, díjnyertes építészcsapatunkkal azt is áttekinthetjük, hogyan igazíthatók a burkolatok, a műszaki tartalom és a terek az Ön igényeihez – a tervezési és kivitelezési lehetőségek függvényében.",
                "Részletes műszaki leírás, árak, fizetési ütemezés és feltételek, valamint a tervezett kivitelezési ütemterv kérésre rendelkezésre áll."],
  INCLUDED=[("Magánszféra és megközelítés", ["Szintenként egy lakás, közvetlen liftkapcsolattal a privát előtérbe",
                                             "Kulcs nélküli belépés, biztonságos pinceszinti tároló és elektromosautó-töltő előkészítés"]),
            ("Komfort és technológia", ["Geotermikus vagy levegő–víz hőszivattyús fűtés-hűtés, szűrt friss levegős szellőzéssel",
                                        "Okosotthon-előkészítés a későbbi bővítéshez"]),
            ("Anyagok és felületek", ["Háromrétegű üvegezésű ablakok, belül natúr tölgy kerettel",
                                      "Tölgy és mészkő burkolatok, finom ásványi vakolatú falak",
                                      "Gondosan kidolgozott részletek az előterekben és a fürdőszobákban"]),
            ("Szabadtéri élet", ["Privát kültéri lakóterek", "Saját kültéri konyha kiépítésének lehetősége"])],
  BESPOKE=("Egyedi belsőépítészet", "Szívesen megtervezzük Önnel együtt a teljesen berendezett, egyedi belső tereket. Keressen minket, és fedezzük fel együtt a lehetőségeket."),
  SMALL_PRINT="Az illusztrációk építészeti látványtervek. Az alapterületek, a műszaki tartalom, az alaprajzi változatok és az átadási határidők a végleges adásvételi dokumentációban kerülnek rögzítésre.",
  LOCATION_SHORT=dict(title="Mártonhegy, Budapest XII. kerület", body=[
      "A Rumah Márton a Hegyvidéken, a XII. kerületben található – Budapest egyik legrégebbi és legpatinásabb lakókörnyékén, amely villáiról, erdős dombjairól és időtlen eleganciájáról ismert.",
      "A ház a Mártonhegy lejtőjén, egy csendes egyirányú utcában áll, kilátással a Várra és a Citadellára. A Normafa és a Budai-hegység néhány percnyire van; a nemzetközi iskolák, a Villa Bagatelle, a MOM Park és a belváros is könnyen elérhető."])),
 "zh": dict(
  CLOSING_LEFT=["我们期待带您亲临现场，并为您详细介绍{name}的设计与规划。",
                "如您愿意，我们的获奖建筑团队也可与您共同探讨，如何根据您的需求定制饰面、配置与空间（以设计及施工可行性为前提）。",
                "详细技术规格、价格、付款阶段与条款，以及工程进度计划，均可应要求提供。"],
  INCLUDED=[("私密与通达", ["一层一户，电梯直达私人电梯前厅", "无钥匙门禁、安全的地下储藏间及电动汽车充电预留"]),
            ("舒适与科技", ["地源或空气源热泵供暖与制冷，配备过滤新风系统", "智能家居预备基础设施，便于日后升级"]),
            ("材料与饰面", ["三层玻璃窗，室内侧为天然橡木窗框", "橡木与石灰石地面，搭配精致矿物灰泥墙面", "大堂与浴室的考究细节与饰面"]),
            ("户外生活", ["私属户外生活空间", "预留独立户外厨房"])],
  BESPOKE=("专属室内定制", "我们乐于与您共同打造全套精装与家具配置的专属室内。欢迎与我们联系，探索更多可能。"),
  SMALL_PRINT="图片均为建筑效果图。面积、技术规格、户型方案及竣工日期以最终买卖文件确认为准。",
  LOCATION_SHORT=dict(title="布达佩斯第十二区<br>玛顿山", body=[
      "玛墩山邸位于布达佩斯第十二区 Hegyvidék——布达佩斯最古老、最尊贵的住宅区之一，以别墅、森林丘陵与恒久优雅著称。",
      "宅邸隐于玛顿山坡地上一条宁静的单行道，远眺布达城堡与盖勒特山。诺尔马法森林与布达山近在咫尺，国际学校、Villa Bagatelle、MOM Park 与市中心均交通便利。"])),
}

# ---------- project brochure ----------
BRO = {
 "hu": dict(
  EYEBROW="Rumah Márton<br>Mártonhegy, Budapest",
  COVER_lede="A csendes luxus átgondolt otthona a budapesti Mártonhegyen.",
  COVER_facts=[("Cím", "Mártonvölgyi út, Budapest XII."), ("A projekt állása", "Építési engedély megadva<br>Társasház-alapítás bejegyezve"), ("Átadás", "Tervezetten 2028 III. negyedév")],
  INTRO=dict(title="Átgondolt terek. Tapintható anyagok. Időtlen jelenlét.", body=[
   "A Mártonhegy csendes dombjai között, Budapest egyik legkeresettebb lakókörnyékén a Rumah Márton mindössze három exkluzív rezidenciából álló, ritka kollekció – mindegyiket magánvillaként gondoltuk el. Szintenként egy lakás, közvetlen liftkapcsolat, napfényes belső terek és tágas teraszok, amelyek privát kertre vagy tetőteraszra nyílnak, mindegyik kültéri konyha kiépítésének lehetőségével: minden otthon a lakásélet új formáját kínálja, ahol egy villa elvonultsága egy gondosan megkomponált menedék kifinomultságával találkozik.",
   "Ez nem egy szokványos fejlesztés, hanem díjnyertes csapat gondos és tudatos munkájával formált lakóélmény. Elegáns térszervezés és átgondolt arányok vezetik az építészetet; a ház minden fordulójában új kilátás tárul fel. A finom erezetű tölgy, a lágy tónusú mészkő és az ásványi mészvakolat palettáját egyedi, növényekkel beültetett erkélyek és keskeny keretű, háromrétegű üvegfalak egészítik ki – mind a csendes, maradandó luxus iránti elkötelezettséget tükrözik.",
   "A WY Rumah sorozat második darabjaként a Rumah Márton azt a szemléletet viszi tovább, amely átgondolt, tapintható és időtlen otthonokat teremt – őszinte gondossággal és mesterségbeli tudással tervezve és építve."]),
  LOCATION=dict(title="Emelkedett élet Budapest egyik legelőkelőbb, mégis rejtett zugában", body=[
   "A Rumah Márton a XII. kerület szívében található – Budapest egyik legrégebbi és legpatinásabb környékén, amely arisztokrata villáiról, erdős dombjairól és időtlen eleganciájáról híres. A Hegyvidékként ismert történelmi negyed a természeti szépség, a kulturális gazdagság és a modern kényelem ritka egységét kínálja.",
   "Egy csendes egyirányú utcában, egy 1100 m²-es telek enyhe lejtőjén diszkréten elhelyezkedő ház egyszerre nyújt magánszférát és visszafogott megjelenést. Emelt fekvéséből panoráma nyílik a Várra és a Citadellára. A körülölelő zöld nemcsak friss levegőt és nyugalmat hoz, hanem az elvonultság érzését is – mindössze néhány percre a városközponttól.",
   "A környéken kiváló nemzetközi és magyar iskolák, olyan kifinomult kávézók, mint a Villa Bagatelle, valamint igényes célpontok – a Hegyvidék Bevásárlóközpont, a MOM Park és a Mammut – találhatók. Kulturális nevezetességek és kikapcsolódási lehetőségek, a Normafától a Budai-hegységig, néhány percnyire várnak."]),
  POINTS=[("Szintenként egy lakás.", "Két lakás és egy villaszerű penthouse ritka hármasa."),
          ("Privát kertek, tetőteraszok és kültéri konyhák.", ""),
          ("Panorámás kilátás a Várra és a Citadellára.", ""),
          ("Mélygarázs. Saját tároló.", ""),
          ("Visszafogott elegancia. Csendes luxus.", ""),
          ("Gondos alkotás.", "A WY Design második limitált sorozata.")],
  TEAM=dict(title="A Rumah Márton mögött álló csapat", body=[
   "A Rumah Mártont díjnyertes csapat formálja – a WY Design, a Kettőpera Építészek és egy megbízható helyi kivitelező –, akiket a minőség, az átgondolt tervezés és a maradandó kivitelezés iránti közös elkötelezettség köt össze.",
   "A csapatot az vezérli, hogyan élünk a terekben, és hogyan készülnek, épülnek azok; így minden döntésben jelen van a gondosság, az építészeti szándéktól az anyagválasztáson át a kivitelezés pontosságáig. Minden elemet hosszú távra terveztünk: hogy méltósággal öregedjen, támogassa a mindennapi kényelmet, és a csendes állandóság érzését hordozza.",
   "Ezt az otthont nem a hivalkodás, hanem a tartalom határozza meg – olyan hely, ahol a minőség az elkészítésében és az idő múlásával is érezhető."]),
  SPEC=[
   [[("Épületgépészet", "Komfort, fűtés-hűtés és szellőzés", ["Mennyezetbe integrált fűtés és hűtés, padlófűtéssel kiegészítve, nagy hatásfokú geotermikus vagy levegő–víz hőszivattyúval – egész évben kellemes klíma", "Önálló központi légtechnika beépített pollen- és porszűrővel", "Okosotthon-infrastruktúra a későbbi Loxone- vagy azzal egyenértékű rendszer integrálásához; a teljes okosvezérlés opcionálisan kérhető", "A fürdőszobákban padlófűtés és elektromos törölközőszárító", "Fűtött kocsibehajtó a biztonságos téli közlekedésért"]),
     ("", "Szellőzés", ["Minden helyiség nyitható ablakokon keresztül természetes módon is szellőztethető", "Friss levegő energiatakarékos, hővisszanyerős rendszeren keresztül", "Gépi elszívás a fürdőszobákban"]),
     ("", "Megújuló energia", ["Teljesen elektromos rendszer, gázbekötés nélkül", "Energia fenntartható geotermikus rendszerből", "A későbbi napelemes rendszer előkészítése megtörténik; tetőre szerelt napelemek, inverterek és integrált akkumulátoros tároló opcionálisan kérhetők", "A közös rendszerek – világítás, fűtés és a behajtó fűtése – közös mérőórán keresztül üzemelnek"]),
     ("", "Okosotthon", ["A kulcs nélküli belépés és az alább ismertetett okosotthon-előkészítés az alapcsomag része; további vezérlőeszközök, szoftver, programozás, beüzemelés és rendszerintegráció opcionálisan kérhető", "Kulcs nélküli belépés kóddal vagy kulcstartós azonosítóval a garázskapukhoz, bejáratokhoz, kapukhoz és a lifthez", "Többhelyiséges audiokábelezés, mennyezeti hangszórók későbbi beépítéséhez előkészítve", "Előkészítés falba süllyesztett érintőpanelhez, amely a világítást, a klímát, az árnyékolást és a videó-kaputelefont egyesíti", "Előkészítés helyi vezérlőpanelekhez, zónánként személyre szabható beállítással", "Távoli hozzáférés és vezérlés mobilalkalmazással", "Automatizált okosárnyékolás a komfort és az energiahatékonyság érdekében"])],
    [("Lakói szolgáltatások", "Mélygarázs", ["Biztonságos, beléptetőrendszerrel védett mélygarázs, összesen 6 parkolóhellyel", "Saját, háromfázisú elektromosautó-töltő előkészítés a lakás egyedi mérőórájára kötve; a töltőegység külön rendelhető", "Kerékpártároló"]),
     ("", "Biztonság", ["Ellenőrzött lifthozzáférés, lakásonként egyedi kóddal vagy kulcstartós azonosítóval", "Magas biztonsági fokozatú zárak minden külső ajtón", "Diszkrét kamerarendszer a fő közlekedőkben és a bejáratoknál", "Saját kamerarendszer a lakásbejáratoknál és teraszokon, kizárólag az érintett lakók számára elérhető", "Videó-kaputelefon és lakásriasztó opcionálisan kérhető"]),
     ("", "Tárolók", ["Zárt, biztonságos pinceszinti tárolók 15–18 m² között"]),
     ("", "Kertek és kültéri terek", ["Kizárólagos kerthasználat a kijelölt lakásokhoz:", "Földszint: privát előkert (az alaprajzok szerint)", "Első emelet: kijelölt hátsó kertrészek (az alaprajzok szerint)", "Penthouse: a tetőterasz kizárólagos használata, mások csak megállapodás alapján férhetnek hozzá", "Minden lakásban előkészítés saját kültéri konyhához", "Programozható automata öntözőrendszer a gondtalan kertfenntartásért"])]],
   [[("Külső kialakítás", "Homlokzat", ["Tartós, vízlepergető ásványi vakolat és mészkő homlokzatburkolat"]),
     ("", "Ablakok", ["Háromrétegű üvegezésű ablakok, belül natúr kezelésű tölgy kerettel, Josko vagy azzal egyenértékű gyártótól", "Szőtt textil árnyékolók, egyben beépített szúnyoghálóként"]),
     ("", "Külső ajtók", ["Belmagasságú, falba futó tolóajtók a teraszokra és keskeny keretű tolóajtók az erkélyekre", "Natúr fa bejárati ajtó minden lakáshoz", "Tűzgátló pinceajtók"]),
     ("", "Erkélyek és teraszok", ["Szoborszerű fém korlátok, beépített növényzettel lágyítva", "Fagyálló, csúszásmentes mészkő burkolat"]),
     ("Bejárat és lift", "", ["Csendesen hívogató, mészkőburkolatú előcsarnok, lágyan megvilágított kazettás mennyezettel", "Közvetlen, privát lifthozzáférés minden lakáshoz; a felső szinti otthonokban natúr anyagú privát előtér, meleg fényű süllyesztett világítással"]),
     ("Üzemeltetés", "", ["A kert, a liftelőtér és a közös területek karbantartása és takarítása megállapodás szerinti közös költség keretében"])],
    [("Lakásbelsők", "Padló", ["Padlófűtés kiváló minőségű hang- és hőszigeteléssel", "Világos tónusú, természetes erezetű tölgy parketta kortárs rakásmintával valamennyi hálószobában, valamint a penthouse nappali- és étkezőterében", "Világos, csiszolt mészkő vagy azzal egyenértékű burkolat az alsó szinti lakások nappali- és konyhaterében", "Azonos kőburkolat a fürdőszobák padlóján és falain"]),
     ("", "Mennyezet", ["Tágas, 2700 mm-es belmagasság minden szinten", "Az alsó szinti lakásokban álmennyezet, diszkréten integrált gépészettel és süllyesztett hangulatvilágítással", "A penthouse-ban kezelt látszó födém, a világítás extrudált lineáris profilokba integrálva – letisztult, minimalista hatás"]),
     ("", "Belső falak és ajtók", ["Hangszigetelt belső falak finom vakolt felülettel", "Visszafogott tölgyfurnér vagy azzal egyenértékű beltéri ajtók, minimalista részletekkel"]),
     ("", "Fürdőszobák", ["Válogatott szaniterek Axor, Dornbracht, Duravit vagy azzal egyenértékű gyártótól; a végleges kiválasztást a lakásra vonatkozó műszaki leírás rögzíti", "Építészeti igényű csaptelepek harmonizált, elegáns felülettel", "Fűtött törölközőtartók a nagyobb kényelemért", "Nyitható ablak a fürdőszobákban a természetes szellőzésért"]),
     ("", "Konyhák", ["Egyedi tölgyfurnéros bútorzat, természetes mészkő munkalap és hátfal, a nagyobb lakásoknál kőlap konyhaszigettel – opcionális belsőépítészeti választásként"]),
     ("", "Háztartási gépek és elektromos szerelvények", ["Átgondoltan elhelyezett víz- és villanyszerelési csatlakozások a konyhai gépekhez és a mosógéphez", "Válogatott háztartásigép-csomagok Gaggenau, Miele vagy azzal egyenértékű gyártótól, opcionális választásként", "Elegáns Berker vagy azzal egyenértékű kapcsolók és aljzatok az alapcsomagban; Loxone-vezérlés az opcionális okosotthon-csomag részeként"]),
     ("", "Belső világítás", ["Átgondolt világítástervezés közvetlen és közvetett fényekkel, integrált LED-szalagokkal", "Előkészítés fejlett világításvezérléshez, jelenetek beállításával és fényerő-szabályozással", "Előkészítés asztali és állólámpák bekötéséhez az opcionális világításvezérlő rendszerbe"])]]],
  SPEC_NOTE="A végleges műszaki tartalom a megállapodott vételárhoz és a választott opcionális fejlesztésekhez igazodik, a lakásra vonatkozó műszaki leírásban rögzítve.",
  CLOSING=["Szívesen megmutatjuk Önnek a helyszínt, és részletesen bemutatjuk a Rumah Márton terveit.",
           "Ha szeretné, díjnyertes építészcsapatunkkal azt is áttekinthetjük, hogyan igazíthatók a burkolatok, a műszaki tartalom és a terek az Ön igényeihez – a tervezési és kivitelezési lehetőségek függvényében.",
           "Részletes műszaki leírás, árak, fizetési ütemezés és feltételek, valamint a tervezett kivitelezési ütemterv kérésre rendelkezésre áll."],
  LINK_LABELS=["A Kertes rezidencia 360°-ban", "A Penthouse 360°-ban", "A Rumah Márton weboldala", "A WY Design bemutatkozása", "Ismerje meg Pei Yongot — interjú"],
  PRESS_LABELS=["Designboom", "EDGE International Award", "BIG SEE Architecture Award", "BIG SEE Interior Award"]),
 "zh": dict(
  EYEBROW="玛墩山邸 Rumah Márton<br>布达佩斯 · 玛顿山",
  COVER_lede="一座匠造的静奢之居，<br>隐于布达佩斯玛顿山间。",
  COVER_facts=[("地址", "布达佩斯第十二区 Mártonvölgyi út"), ("项目进展", "已获建筑许可<br>公寓分户产权已登记"), ("竣工", "计划于 2028 年第三季度")],
  INTRO=dict(title="细腻空间。<br>触感材质。<br>永恒气韵。", body=[
   "玛墩山邸坐落于布达佩斯最令人向往的玛顿山宁静坡地，呈现三户稀有宅邸，每一户皆以独立私邸为构想。一层一户，电梯直达，阳光自然洒入；宽阔露台延伸至私家花园或屋顶景观，并预留户外厨房。别墅般的私密，与度假居所般的雅致氛围在此交织，开启公寓生活的全新方式。",
   "这超越寻常开发项目，是一场由获奖团队深思熟虑打造的匠心居住体验。优雅的空间布局与和谐比例引领建筑，让每一次转角皆化作风景。细纹橡木、柔和石灰石与天然矿物灰泥，搭配定制花槽阳台及极简边框三层玻璃幕墙，尽显对静谧恒久奢华的承诺。",
   "作为 WY Rumah 系列第二章，玛墩山邸传承“用心 · 触感 · 永恒”的理念，以真挚之心设计与建造。"]),
  LOCATION=dict(title="隐栖于布达佩斯的尊贵秘境", body=[
   "玛墩山邸静卧于布达佩斯第十二区的核心地带。这片被称为 Hegyvidék 的历史社区，是布达佩斯最古老、最尊贵的住宅区之一，以贵族别墅、森林丘陵与恒久优雅著称，自然之美、文化底蕴与现代便利在此交汇。",
   "宅邸隐于宁静的单行道，稳踞于约 1,100 平方米的缓坡之上，低调而私密。居高远望，布达城堡与盖勒特山（自由女神像）尽收眼底。环绕四周的绿意带来清新空气与宁静，更带来一份隐逸之感——而城市中心仅数分钟之遥。",
   "周边汇聚国际与本地知名学府、Villa Bagatelle 等雅致咖啡馆，以及 Hegyvidék 购物中心、MOM Park 与 Mammut 等购物地标。从诺尔马法森林到布达山，文化地标与自然休闲胜境近在咫尺。"]),
  POINTS=[("一层一户，独享私密。", "两套公寓与一套顶层别墅式宅邸，臻稀呈现。"),
          ("专属庭院 · 屋顶露台 · 户外厨房。", ""),
          ("无界视野，尽揽布达城堡与盖勒特山。", ""),
          ("地下私家车位 · 专属储藏间。", ""),
          ("低调洗练，静谧奢华。", ""),
          ("思衡雅致 · 精筑呈献。", "WY Design 限量系 · 第二作。")],
  TEAM=dict(title="屡获殊荣的团队", body=[
   "玛墩山邸由屡获殊荣的团队共同呈现——WY Design、Kettőpera 建筑事务所与值得信赖的本地建造团队，凝聚于对品质、深思设计与持久工艺的共同承诺。",
   "团队以对空间如何被居住、被制造与被建造的敏锐理解为指引，在每一个决策中注入关怀：从建筑意图到材料甄选，再到施工精度。每一处细节皆以长远视野考量——让建筑随岁月优雅沉淀，为日常生活带来舒适，并承载一份静谧的恒久。",
   "这是一处不以张扬定义、而以内涵立身的居所——品质既体现在建造之中，也延续于岁月流转之间。"]),
  SPEC=[
   [[("建筑配套与系统", "舒适环境与通风系统", ["全屋采用顶面供暖与制冷系统，结合地面采暖；由高效地源热泵或空气源热泵驱动，四季恒温舒适", "配备独立中央新风系统，并集成花粉与粉尘过滤装置", "全屋预设智能家居基础设施，可于日后接入 Loxone 或同等级智能家居系统；完整智能控制功能可作为选配升级", "浴室配有地暖与电热毛巾架", "车道设有电加热系统，确保冬季出入安全"]),
     ("", "通风系统", ["全屋房间均设可开启窗扇，实现自然通风", "新风由高效热回收系统引入", "浴室设有机械排风系统"]),
     ("", "可再生能源", ["全屋采用纯电力系统，无燃气接入", "能源来源于可持续地热系统", "已预留未来太阳能系统的安装条件；屋顶太阳能板、逆变器及一体化储能装置可作为选配升级", "公共系统（照明、供暖及车道加热）由公共电表统一供电"]),
     ("", "智能家居系统", ["已包含无钥匙门禁系统及下述智能家居预备基础设施；额外的控制设备、软件、程序设置、系统调试及整合服务均可作为选配升级", "车库门、入口、大门与电梯均支持密码或门禁钥匙扣通行", "预留多区域音频线路，可于日后加装吊顶扬声器", "预留墙嵌式触控面板安装条件，统一控制照明、室温、遮阳与可视对讲", "预留区域控制面板安装条件，实现个性化分区调节", "可通过手机应用实现远程访问与管理", "智能电动遮阳系统，提升居住舒适度与能源效率"])],
    [("住户设施", "地下车库", ["安全管控的地下车库，共设 6 个车位", "各户预设独立三相电动汽车充电电源接入条件，并连接至对应住户的独立电表；充电设备需另行配置", "自行车存放区"]),
     ("", "安防系统", ["电梯出入受控，每户配备专属密码或门禁钥匙扣授权", "全部外门采用高等级安全锁具", "主要通道及出入口设有低调隐蔽的监控系统", "各户入口及私属露台设有独立监控系统，仅对应住户可查看", "可视对讲及住户报警系统可作为选配升级"]),
     ("", "住户储藏空间", ["私密、安全的地下储藏间，面积约 15–18 平方米"]),
     ("", "花园及户外空间", ["指定户型享有专属花园使用权：", "首层：专属前庭花园（以平面图为准）", "二层：指定后花园（以平面图为准）", "顶层：屋顶露台专属使用，其他住户仅可在协议下使用", "每户均预留独立户外厨房的安装条件", "花园配备可编程定时的自动灌溉系统，便于轻松养护"])]],
   [[("外立面与外部工艺", "外墙", ["外墙采用耐久、憎水型矿物灰泥及石灰石饰面"]),
     ("", "窗户", ["采用 Josko 或同等级品牌的三层玻璃窗，室内侧为天然橡木饰面", "编织织物帘兼具防蚊功能，提升居住舒适度"]),
     ("", "外门", ["通往露台的全高隐藏式推拉门，以及通往阳台的极简框架推拉门", "每户配备天然木质入户门", "地下室配备防火等级门"]),
     ("", "阳台与露台", ["雕塑感金属栏杆，融合绿植元素", "防冻、防滑石灰石地面"]),
     ("入口空间与电梯", "", ["大堂采用石灰石饰面，辅以柔和的天花灯槽，营造静雅迎宾氛围", "电梯直达各户；楼上户型均设独立电梯前厅，采用自然质感饰面，辅以温润的嵌入式灯光"]),
     ("维护", "", ["花园、电梯大堂及公共区域的维护与清洁服务，以协商一致的管理费形式提供"])],
    [("室内精装与材料", "地面铺装", ["地暖系统配备高等级隔音与保温层", "所有卧室及顶层宅邸的起居与餐厅区域铺设浅色天然纹理橡木地板，以现代拼铺方式呈现", "下层户型的起居与厨房区域铺设浅色细磨石灰石，或同等级饰面材料", "浴室地面与墙面采用相同石材饰面"]),
     ("", "天花", ["全楼各层室内净高约 2700 毫米", "下层户型采用石膏板吊顶，巧妙整合建筑设备与嵌入式氛围照明", "顶层宅邸采用处理后的结构顶板，照明嵌入线性型材之中，呈现极简效果"]),
     ("", "内墙与室内门", ["内墙具备隔音层，并采用精细灰泥饰面", "室内门采用橡木饰面或同等级材料，搭配简约细节"]),
     ("", "浴室", ["精选 Axor、Dornbracht、Duravit 或同等级品牌的卫浴产品；最终选型以各户专属技术规格文件为准", "设计精致、饰面协调统一的建筑级卫浴五金", "电热毛巾架，提升日常舒适度", "浴室设可开启窗扇，实现自然通风"]),
     ("", "厨房", ["定制橡木饰面橱柜、天然石灰石操作台及防溅板，以及较大户型的整块石材厨房中岛，均可作为选配装修方案"]),
     ("", "厨电与电气", ["厨房及洗衣设备均预留合理布局的给排水与电气接口", "Gaggenau、Miele 或同等级品牌的精选电器套装，可作为选配方案", "标配 Berker 或同等级品牌的精致电气插座；Loxone 智能控制可通过选配智能家居套装实现"]),
     ("", "室内照明", ["结合直接与间接光源的照明设计，融入嵌入式 LED 灯带", "预留高级照明控制系统，可实现场景设置与亮度调节", "预留台灯与落地灯接入选配照明控制系统的条件"])]]],
  SPEC_NOTE="最终技术规格将根据双方协商一致的购买价格及所选升级配置进行调整，并以各户专属技术规格文件为准。",
  CLOSING=["我们期待带您亲临现场，并为您详细介绍玛墩山邸的设计与规划。",
           "如您愿意，我们的获奖建筑团队也可与您共同探讨，如何根据您的需求定制饰面、配置与空间（以设计及施工可行性为前提）。",
           "详细技术规格、价格、付款阶段与条款，以及工程进度计划，均可应要求提供。"],
  LINK_LABELS=["360° 探索花园宅邸", "360° 探索顶层宅邸", "访问玛墩山邸网站", "探索 WY Design", "开发者 Pei Yong — 人物专访"],
  PRESS_LABELS=["Designboom 媒体报道", "EDGE 国际奖", "BIG SEE 建筑奖", "BIG SEE 室内设计奖"]),
}
