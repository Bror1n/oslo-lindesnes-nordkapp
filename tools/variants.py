# Alternative routes. Each replaces a run of main stages (by exact main stage name, first..last).
# "start" = waypoint the variant leaves from (end of the stage before `first`).
VARIANTS=[
 {"id":"coast","notes":['The longest variant: 18 riding days instead of 14, about 360 km more, and 15 ferries. Ferry waits make the days longer than the distances suggest.', 'Passengers travel free on the public road ferries in Vestland, Møre og Romsdal and Trøndelag, and only vehicles pay. Check that a bicycle counts as free on each one. The Lauvvik–Oanes ferry is privately run and sells tickets on board.', 'The outer coast north of Stavanger cannot be ridden: the Byfjord and Mastrafjord tunnels are closed to bikes and the Skudeneshavn ferry stopped in 2013. The track goes through Ryfylke instead. The coast bus from Stavanger to Haugesund is the shortcut if you accept a bus.', 'Kristiansund is left out because both roads into it use subsea tunnels closed to bikes.', 'Many tunnels on Fv57, Rv5, Fv614 and Fv61 are open to bikes. Carry strong front and rear lights and a reflective vest.', 'Bergen – Rutledal is 121 km. It can be cut at the Leirvåg–Sløvåg ferry.', 'The west coast is the wettest part of Norway. Expect rain on more than half the days.'],"title":"The coast to Trondheim",
  "blurb":"Stays on the west coast all the way from Lindesnes to Trondheim instead of crossing the mountains: Jæren, Ryfylke, the Sunnhordland islands, Bergen, the mouths of Sognefjord and Nordfjord, Ålesund, the Atlantic Road and the Nordmøre coast.",
  "first":"Lindesnes fyr – Evje","last":"Berkåk – Trondheim","start":"Lindesnes fyr",
  "stages":[
   ("Lindesnes fyr – Flekkefjord", ["Vigeland, Lindesnes","Lyngdal","Feda","Flekkefjord"]),
   ("Flekkefjord – Egersund (Jøssingfjord)", ["Åna-Sira","Jøssingfjord","Hauge i Dalane","Egersund"]),
   ("Egersund – Lauvvik (Jæren coast)", ["Brusand","Varhaug","Bryne","Sandnes","Lauvvik ferjekai"]),
   ("Lauvvik – Hjelmeland (Ryfylke)", ["Oanes","Jørpeland","Tau, Strand","Årdal, Hjelmeland","Hjelmelandsvågen"]),
   ("Hjelmeland – Ølen", ["Nesvik","Vikedal","Ølensjøen"]),
   ("Ølen – Leirvik (Skånevik, Stord)", ["Etne","Skånevik","Utåker","Skjersholmane","Leirvik, Stord"]),
   ("Leirvik – Bergen (Tysnes)", ["Jektevik, Stord","Hodnanes","Våge, Tysnes","Halhjem","Osøyro","Bergen"]),
   ("Bergen – Rutledal", ["Knarvik","Sløvåg","Rutledal"]),
   ("Rutledal – Førde (Sognefjord mouth)", ["Rysjedalsvika","fast:Dale, Fjaler","Førde"]),
   ("Førde – Svelgen", ["Naustdal","Eikefjord","Svelgen"]),
   ("Svelgen – Åheim (Nordfjord)", ["Isane","Stårheim","Maurstad","Åheim"]),
   ("Åheim – Ålesund", ["Koparnes","Årvika ferjekai","Larsnes","Ulsteinvik","Hareid","Sulesund","Ålesund"]),
   ("Ålesund – Midsund", ["Brattvåg","Dryna ferjekai","Midsund"]),
   ("Midsund – Bud", ["Solholmen ferjekai","Mordalsvågen","Bud"]),
   ("Bud – Batnfjordsøra (Atlantic Road)", ["Vevang","Kårvåg","Vevang","Eide, Hustadvika","fast:Batnfjordsøra"]),
   ("Batnfjordsøra – Aure", ["Kanestraum","Halsa ferjekai","Aure"]),
   ("Aure – Krokstadøra", ["Kyrksæterøra","Krokstadøra"]),
   ("Krokstadøra – Trondheim", ["Orkanger","Trondheim"]),
  ]},
 {"id":"lysefjord","notes":['The Lauvvik–Lysebotn tourist ferry runs in summer only, about 2.5 hours, and should be booked. Sleep in Lysebotn.', 'The first day is the hardest on the south coast: 121 km and 1,600 m of climbing.', 'Lysevegen and Suleskarvegen are closed in winter and normally open in late May.', 'Kjerag and Preikestolen each need most of a day on foot, so allow rest days for them.'],"title":"Lysefjord and the North Sea Road",
  "blurb":"West from Lindesnes along the North Sea coast and Jæren, the tourist ferry up Lysefjord, then Lysevegen and Suleskarvegen over to Setesdal.",
  "first":"Lindesnes fyr – Evje","last":"Evje – Valle","start":"Lindesnes fyr",
  "stages":[
   ("Lindesnes fyr – Flekkefjord", ["Vigeland, Lindesnes","Lyngdal","Feda","Flekkefjord"]),
   ("Flekkefjord – Egersund (Jøssingfjord)", ["Åna-Sira","Jøssingfjord","Hauge i Dalane","Egersund"]),
   ("Egersund – Lauvvik (Jæren)", ["Brusand","Varhaug","Bryne","Sandnes","Lauvvik ferjekai"]),
   ("Lysebotn – Valle (Lysevegen, Suleskarvegen)", ["Lysebotn","Suleskard","Valle, Agder"]),
  ]},
 {"id":"nigardsbreen","notes":['This breaks the unbroken riding line: the bus from Lærdal to Sogndal goes through tunnels that are closed to bikes. Check that the bus takes bikes.', "You lose the Filefjell King's Road and Tindevegen."],"title":"Nigardsbreen and Jostedalen",
  "blurb":"Bus from Lærdal to Sogndal instead of Filefjell and Tindevegen, then up Jostedalen to the glacier and back to Sognefjellsvegen.",
  "first":"Lærdal – Tyinkrysset (Kongevegen over Filefjell)","last":"Tyinkrysset – Turtagrø (Tindevegen)","start":"Lærdalsøyri",
  "stages":[
   ("Sogndal – Nigardsbreen (bus from Lærdal)", ["Sogndal","Gaupne","Breheimsenteret"]),
   ("Nigardsbreen – Turtagrø", ["Gaupne","Skjolden, Luster","Turtagrø"]),
  ]},
 {"id":"geiranger","notes":['You lose Dovrefjell, the musk oxen and Rondane.', 'Between Pollfoss and Grotli the track uses the old gravel road beside Rv15. Not verified on the ground.', 'The direct road from Åndalsnes to Molde has a subsea tunnel closed to bikes, so the track goes along the south shore to the Vestnes–Molde ferry.', 'The Atlantic Road is ridden out to Kårvåg and back, because the tunnel onward to Kristiansund is closed to bikes.', 'Trollstigen and the Geiranger road are closed in winter and normally open in late May or June.'],"title":"Geiranger, Trollstigen and the Atlantic Road",
  "blurb":"West from Lom to Geirangerfjord, over Ørnevegen and Trollstigen to Åndalsnes, out to the Atlantic Road, then the Nordmøre fjords and Surnadal to Trondheim.",
  "first":"Lom – Dombås","last":"Berkåk – Trondheim","start":"Lom",
  "stages":[
   ("Lom – Geiranger", ["fast:Bismo","Pollfoss","Grotli","fast:Geiranger"]),
   ("Geiranger – Åndalsnes (Trollstigen)", ["Eidsdal","Linge ferjekai","Valldal","Trollstigen","Åndalsnes"]),
   ("Åndalsnes – Bud", ["Vestnes ferjekai","Molde ferjekai","Bud"]),
   ("Bud – Batnfjordsøra (Atlantic Road)", ["Vevang","Kårvåg","Vevang","Eide, Hustadvika","fast:Batnfjordsøra"]),
   ("Batnfjordsøra – Rindal", ["Kanestraum","Halsa ferjekai","fast:Surnadalsøra","Rindal"]),
   ("Rindal – Trondheim", ["Orkanger","Trondheim"]),
  ]},
 {"id":"havoysund","notes":['An out-and-back: the same 89 km road both ways, very exposed to wind.', 'Havøysund has a shop and rooms. There is almost nothing in between.'],"title":"Havøysund",
  "blurb":"Out and back from Olderfjord on the national tourist route to the fishing village of Havøysund.",
  "first":"Skaidi – Repvåg","last":"Skaidi – Repvåg","start":"Skaidi",
  "stages":[
   ("Skaidi – Havøysund", ["Olderfjord","Havøysund"]),
   ("Havøysund – Olderfjord", ["Olderfjord"]),
   ("Olderfjord – Repvåg", ["Repvåg"]),
  ]},
]
# Gravel mode is a switch, not a variant. Every leg of the main route and of each variant is re-routed on
# gravel where route.pick_gravel accepts it. In addition GRAVEL_BLOCK replaces main stages first..last with
# the Jotunheimen gravel roads, unless an active variant overlaps those stages.
GRAVEL_BLOCK={"first":"Tyinkrysset – Turtagrø (Tindevegen)","last":"Lom – Dombås","start":"Tyinkrysset",
  "stages":[
   ("Tyinkrysset – Beitostølen (Slettefjell)", ["Beitostølen"]),
   ("Beitostølen – Skåbu (Jotunheimvegen)", ["Bygdisheim","Skåbu"]),
   ("Skåbu – Vågåmo (Murudalen)", ["Randsverk","Vågåmo"]),
   ("Vågåmo – Dombås (Slådalsvegen)", ["Dombås"]),
  ]}
GRAVEL_NOTES=['Each leg is re-routed onto gravel only where that adds at least 3 km of gravel for at most 15 % more distance, without new hiking paths or boats. Elsewhere the track is unchanged.',
   'Between Tyin and Dombås the track leaves the main route for four days on mountain gravel roads: Slettefjellvegen, Jotunheimvegen, Murudalen and Slådalsvegen. You lose Tindevegen, Sognefjellet and Lom. With the Nigardsbreen or Geiranger variant switched on these four days are not used, because those variants need Sognefjellet or Lom.',
   'Gravel mode works together with the alternative routes. Each of them has its own gravel version.',
   'Jotunheimvegen, Slettefjellvegen and Slådalsvegen are summer toll roads and normally open in late June. Check before leaving.',
   'Gravel days are slower. Count on 15 to 25 % less distance per hour than on asphalt.',
   'Surfaces come from OpenStreetMap tags and are not checked on the ground. Forest roads can be rough or gated.']
V_FERRIES=[("Lauvvik ferjekai","Lysebotn"),("Eidsdal","Linge ferjekai"),("Vestnes ferjekai","Molde ferjekai"),("Kanestraum","Halsa ferjekai"),("Lærdalsøyri","Sogndal")]
