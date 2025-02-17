# SKSKBachelor

# **Drone Detection Simulation**
Om du har spørsmål om programmet kan du kontakte Vetle Andre Jonhaugen på:
  Mail: vetjon@outlook.com  
  Telefon: 45 87 40 96

## **Beskrivelse**
Programmene simulerer en maritim overvåkingssituasjon der en båt, støttet av droner, forsøker å oppdage en ubåt. Det inkluderer simulering av bevegelser, deteksjon ved hjelp av sonar, og visualisering av resultater som varmekart, kakediagrammer og linjediagrammer.

## **Funksjoner**
- Simulering av bevegelser for båt, droner og ubåt.
- Deteksjon av ubåt basert på sonarrekkevidde.
- Sporing av spilldata for analyse.
- Visualisering av:
  - **Varmekart** over ubåtens posisjon.
  - **Kakediagram** over hvordan spillene endte.
  - **Linjediagram** over avstanden mellom båt og ubåt per spill.

## **Installasjon**
### **Krav**
- Python 3.13
- Følgende Python-biblioteker:
  - `pygame`
  - `matplotlib`
  - `numpy`
  - `random`

### **Trinn for installasjon**
1. Klon prosjektet:
   ```bash
   git clone https://github.com/vetjon/SKSKBachelor.git
   cd SKSKBachelor
2. Installer requirements:
   ```bash
   pip install -r requirements.txt

### Generelt
Simuleringen består av en ubåt, et fartøy, og droner som opererer ut fra fartøyet. Alle simuleringene avsluttes enten når ubåten blir detektert, eller om ubåten for fartøyet innenfor sin torpedorekkevidde. Oppførselen til de forskjellige enhetene er forskjellig i hvert program. Dette vil beskrive nærmere senere. Hvert program simuleres 1000 ganger før det produserer flere data/resultater:
  - Kakediagram over hvor mange av simuleringene som ender i deteksjon, eller at ubåten for fartøyet innenfor sin torpedorekkevidde
  - Et linjediagram over avstand mellom ubåten og fartøyet ved simuleringsslutt
  - Et heatmap over hvor ubåten var i forhold til fartøyet ved simuleringsslutt


#### Spinning.py
  Dette programmet brukes for å simulere et fartøy i ro med droner rundt hele fartyøet i en skjerm. Viktige parametere som ble justert i dette programmet er: 
  
  - NUM_DRONES
  - DETECTION_INTERVAL
  - angular_speed

  NUM_DRONES justerer antall droner i skjermen. DETECTION_INTERVAL justerer hvor lenge det går mellom hver gang dronene detekterer. angular_speed beveger dronene til en ny posisjon hver frame. Dette ble brukt for å plassere dronene slik at den nye posisjonen der det nye settet med droner posisjoneres i før neste deteksjon.

  Programmet ble også brukt til å simulere et enkelt helikopter i skjerm rundt et fartøy i ro. NUM_DRONES ble satt til 1 og fart og deteksjonsintervall ble satt ut fra hvor langt helikopteret skulle fly mellom hvert dypp.

#### Drone_in_front.py
Dette programmet ble brukt for å simulere en droneskjerm for et fartøy i bevegelse. Endringer som er gjort for dette programmet er at både fartøyet og ubåten er i bevegelse. Droneskjermen er tettere på fartøyet, siden de må gjøre opp for bevegelsen til fartøyet. De viktigste parameterne som ble justert til forskjellige tester er:

- NUM_DRONES
- angle_offset

Som tidligere blir NUM_DRONES brukt til å bestemme antall droner i skjermen. Disse blir fordelt med likt mellomrom utover skjermen, basert på hvor stor angle_offset som er valgt. angle_offset bestemmer hvor stor vinkel framfor fartøyet dronene plasseres. Om dette settes til (-90, 90) betyr det at dronene fordeles fra 90 grader styrbord til 90 grader babord.

#### Heli_sim.py
Dette programmet brukes til å simulere et helikopter i skjerm for et fartøy i bevegelse. Forskjellen mellom dette programmet og de andre er at helikopteret patruljerer fremfor fartøyet på en utvalgt radius og vinkel foran fartøyet.

- SCREEN_RADIUS
- start_angle
- end_angle

SCREEN_RADIUS ble brukt for å bestemme hvor langt fremfor fartøyet helikopteret patruljerer. start_angle og end_angle bestemmer hvor langt til hver side av fartøyet helikopteret patruljerer. Om start_angle og end_angle er henholdsvis -30 og 30 grader, vil helikopteret patruljere mellom 30 grader styrbord og babord.

