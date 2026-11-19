# Alternative routes. Each replaces a run of main stages (by exact main stage name, first..last).
# "start" = waypoint the variant leaves from (end of the stage before `first`).
VARIANTS=[
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
V_FERRIES=[("Lauvvik ferjekai","Lysebotn"),("Eidsdal","Linge ferjekai"),("Vestnes ferjekai","Molde ferjekai"),("Kanestraum","Halsa ferjekai"),("Lærdalsøyri","Sogndal")]
