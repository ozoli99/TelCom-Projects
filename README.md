# TelCom-Projects
Telekommunikációs hálózatok egyetemi tárgy beadandói - Python

## CircuitSimulation
### Feladat
Adott a cs1.json, ami tartalmazza egy irányítatlan gráf leírását. A gráf végpont (end-points) és switch (switches) csomópontokat
tartalmaz. Az élek (links) kapacitással rendelkeznek (valós szám). Tegyük fel, hogy egy áramkörkapcsolt hálózatban vagyunk és
valamilyen RRP-szerű erőforrás foglaló protokollt használunk. Feltesszük, hogy csak a linkek megosztandó és szűk erőforrások. A
json tartalmazza a kialakítható lehetséges útvonalakat (possible-cicuits), továbbá a rendszerbe beérkező, két végpontot összekötő
áramkörigényeket kezdő és vég időponttal. A szimuláció a t=1 időpillanatban kezdődik és t=duration időpillanatban ér véget.
Készíts programot, ami leszimulálja az erőforrások lefoglalását és felszabadítását a JSON fájlban megadott topológia, kapacitások
és igények alapján!

Script paraméterezése: python3 client.py cs1.json

A program kimenete:
<esemény sorszám. <esemény név>: <node1><-><node2> st:<szimuálciós idő> [- <sikeres/sikertelen>]
Pl.:
1. igény foglalás: A<->C st:1 – sikeres
2. igény foglalás: B<->C st:2 – sikeres
3. igény felszabadítás: A<->C st:5
4. igény foglalás: D<->C st:6 – sikeres
5. igény foglalás: A<->C st:7 – sikertelen
…

## Protocoll
### Feladat1
A paraméterben kapott bináris fájlokat olvassuk be és irassuk ki az első record tartalmát a standard outputra! (az unpack visszatérési értékét)
- Parameter1 formátuma: bool, karakter, 9 hosszú string
- Parameter2 formátuma: 9 hosszú string, integer, float
- Parameter3 formátuma: float, karakter, bool
- Parameter4 formátuma: 9 hosszú string, bool, integer
### Feladat2
Írd ki a stdout-ra (print) a következő értéket bináris formátumban (a pack visszatérési értéke)! A string hosszát a szöveg mögött lévő szám jelzi!
Használandó struct paraméterek: f, i, c, ?, Xs (ahol a X a string hossza, pl: 3s)
- "elso"(15), 73, True
- 76.5, False, 'X'
- 64, "masodik"(13), 83.9
- 'Z', 95, "harmadik"(16)

Script paraméterezése:
python3 client.py < file1 > < file2 > < file3 > < file4 >
pl: python3 client.py db1.bin db2.bin db3.bin db4.bin

## GuessingGame
### Feladat
Készítsünk egy barkóba alkalmazást. A szerver legyen képes kiszolgálni több klienst. A szerver válasszon egy egész számot 1..100 között véletlenszerűen. A kliensek próbálják kitalálni a számot.
- A kliens logaritmikus keresés segítségével találja ki a gondolt számot. AZAZ a kliens NE a standard inputról dolgozzon.
- Ha egy kliens kitalálta a számot, akkor a szerver minden újabb kliens üzenetre a „Vége” (V) üzenetet küldi, amire a kliensek kilépnek.
- Nyertél (Y), Kiestél (K) és Vége (V) üzenet fogadása esetén a kliens bontja a kapcsolatot és terminál. Igen (I) / Nem (N) esetén folytatja a kérdezgetést.
- A kommunikációhoz TCP-t használjunk!
- A server a SELECT fv-t használja több kliens kiszolgálásához!

Üzenet formátum:
- Klienstől: bináris formában egy db karakter, 32 bites egész szám. (struct) Ne használjuk a byte sorrend módosító operátort a struct-ban! ('!')
  - A karakter lehet: <: kisebb-e, >: nagyobb-e, =: egyenlő-e
  - pl: ('>',10)
- Szervertől: ugyanaz a bináris formátum , de a számnak nincs szerepe, bármi lehet (struct)
  - A karakter lehet: I: Igen, N: Nem, K: Kiestél, Y: Nyertél, V: Vége
  - pl: ('V',0)

Script paraméterezése:
- python3 client.py < hostname > < port szám >
  - pl: python3 client.py localhost 10000
- python3 server.py < hostname > < port szám >
  - pl: python3 server.py localhost 10000
