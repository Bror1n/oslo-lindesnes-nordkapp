# Stage definitions: (stage name, [via-point queries for geocoding]).
# First point of a stage = last point of previous stage (not repeated).
# Via-points force the intended road where the router could pick a tunnel/E-road.
STAGES = [
 # ---- Part A: Oslo -> Lindesnes (coast, Nasjonal sykkelrute 1 / EuroVelo 12) ----
 ("Oslo – Tønsberg",          ["Oslo rådhus, Oslo", "Drammen", "Holmestrand", "Tønsberg"]),
 ("Tønsberg – Kragerø",       ["Larvik", "Stavern", "Helgeroa", "Brevik, Porsgrunn", "Kragerø"]),
 ("Kragerø – Arendal",        ["Risør", "Tvedestrand", "Arendal"]),
 ("Arendal – Mandal",         ["Grimstad", "Lillesand", "Kristiansand", "Mandal"]),
 ("Mandal – Lindesnes fyr",   ["Spangereid", "Lindesnes fyr"]),
 # ---- Part B: Lindesnes -> Trondheim, inland over the mountains ----
 ("Lindesnes fyr – Evje",     ["Vigeland, Lindesnes", "Marnardal", "Bjelland, Lindesnes", "Evje"]),
 ("Evje – Valle",             ["Byglandsfjord", "Bygland", "Valle, Agder"]),
 ("Valle – Haukeligrend",     ["Bykle", "Hovden, Bykle", "Haukeligrend"]),
 ("Haukeligrend – Røldal",    ["Haukeliseter fjellstue", "Dyrskar", "Røldal"]),
 ("Røldal – Eidfjord",        ["Seljestad, Ullensvang", "Odda", "Kinsarvik", "fast:Eidfjord"]),
 ("Eidfjord – Haugastøl",     ["Vøringsfossen", "fast:Dyranut", "fast:Fagerheim fjellstugu", "fast:Haugastøl"]),
 ("Haugastøl – Flåm (Rallarvegen)", ["Finse", "Hallingskeid", "Myrdal, Aurland", "Flåm"]),
 ("Flåm – Lærdal (Aurlandsfjellet)", ["Aurlandsvangen", "Stegastein", "Flotane, Aurland", "Lærdalsøyri"]),
 ("Lærdal – Tyinkrysset (Kongevegen over Filefjell)", ["Borgund stavkyrkje", "Maristova", "Tyinkrysset"]),
 ("Tyinkrysset – Turtagrø (Tindevegen)", ["fast:Øvre Årdal", "Turtagrø"]),
 ("Turtagrø – Lom (Sognefjellet)", ["Sognefjellshytta", "Lom"]),
 ("Lom – Dombås",             ["Vågåmo", "Otta, Sel", "Dombås"]),
 ("Dombås – Berkåk (Dovrefjell)", ["Hjerkinn", "Kongsvoll", "Oppdal", "Berkåk"]),
 ("Berkåk – Trondheim",       ["Støren, Midtre Gauldal", "Melhus", "Trondheim"]),
 # ---- Part C: Trondheim -> Nordkapp via Kystriksveien, Lofoten, Senja, Lyngen ----
 ("Trondheim – Steinkjer",    ["Stjørdal", "Levanger", "Verdalsøra", "Steinkjer"]),
 ("Steinkjer – Namsos",       ["Malm, Steinkjer", "Namsos"]),
 ("Namsos – Foldereid",       ["Lund ferjekai", "Hofles", "Foldereid"]),
 ("Foldereid – Brønnøysund",  ["Holm, Bindal", "Vennesund", "Brønnøysund"]),
 ("Brønnøysund – Sandnessjøen", ["Horn, Brønnøy", "Andalsvåg", "Forvik", "Tjøtta", "Sandnessjøen"]),
 ("Sandnessjøen – Jektvik",   ["Levang, Leirfjord", "Nesna", "Stokkvågen", "Kilboghamn ferjekai", "Jektvik"]),
 ("Jektvik – Ørnes",          ["Ågskardet", "Forøy, Meløy", "Halsa, Meløy", "Ørnes"]),
 ("Ørnes – Bodø",             ["Saltstraumen", "Bodø"]),
 ("Moskenes – Leknes (Lofoten)", ["Moskenes", "Å i Lofoten", "Reine", "Ramberg, Flakstad", "Leknes"]),
 ("Leknes – Svolvær",         ["Henningsvær", "Kabelvåg", "Svolvær"]),
 ("Svolvær – Sortland",       ["Fiskebøl", "Melbu", "Stokmarknes", "Sortland"]),
 ("Sortland – Andenes",       ["Risøyhamn", "Bleik", "Andenes"]),
 ("Gryllefjord – Botnhamn (Senja)", ["Gryllefjord", "Bergsbotn", "Ersfjord, Senja", "Botnhamn ferjekai"]),
 ("Brensholmen – Tromsø",     ["Brensholmen", "Kvaløysletta", "Tromsø"]),
 ("Tromsø – Olderdalen (Lyngen)", ["Breivikeidet", "Svensby", "Lyngseidet", "Olderdalen"]),
 ("Olderdalen – Burfjord",    ["Storslett", "Burfjord"]),
 ("Burfjord – Alta",          ["Talvik", "Alta"]),
 ("Alta – Skaidi",            ["Skaidi"]),
 ("Skaidi – Repvåg",          ["Olderfjord", "Repvåg"]),
 ("Repvåg – Nordkapp",        ["Honningsvåg", "Nordkapp"]),
]
# Ferries where the router must be allowed to jump: (from query, to query)
FERRIES = [
 ("Fodnes ferjekai", "Mannheller"), ("Lund ferjekai", "Hofles"), ("Holm, Bindal", "Vennesund"),
 ("Horn, Brønnøy", "Andalsvåg"), ("Forvik", "Tjøtta"), ("Levang, Leirfjord", "Nesna"),
 ("Kilboghamn ferjekai", "Jektvik"), ("Ågskardet", "Forøy, Meløy"), ("Bodø", "Moskenes"),
 ("Fiskebøl", "Melbu"), ("Andenes", "Gryllefjord"), ("Botnhamn ferjekai", "Brensholmen"),
 ("Breivikeidet", "Svensby"), ("Lyngseidet", "Olderdalen"),
]
