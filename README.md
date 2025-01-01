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
  Dette programmet ble brukt for å simulere et fartøy med droner rundt hele fartyøet i en skjerm. Viktige parametere som ble justert i dette programmet er: 
  
  - NUM_DRONES
  - DETECTION_INTERVAL
  - angular_speed

  NUM_DRONES justerer antall droner i skjermen. DETECTION_INTERVAL justerer hvor lenge det går mellom hver gang dronene detekterer. angular_speed beveger dronene til en ny posisjon hver frame. Dette ble brukt for å plassere dronene slik at den nye posisjonen
  
