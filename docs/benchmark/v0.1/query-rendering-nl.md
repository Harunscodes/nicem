# NiceM Query Rendering — Nederlands v0.1

**Status:** 36 Nederlandse queryteksten voor de NiceM v0.1-benchmark
**Rol:** Een van drie gelijkwaardige queryrenderings (EN/NL/TR). Elke query is opgesteld vanuit de intentspecificatie en de verwachte factmapping — niet als vertaling van de Engelse rendering.
**Versie:** qr-nl-v0.1.0 (nog niet bevroren)
**Afhankelijk van:** `query-rendering-plan.md` (qr-plan-v0.1.0), `intent-set.md` (intent-v0.1.0), `expected-fact-mapping.md` (efm-v0.1.0)
**Feeds into:** Stage 1 tokenizer sanity gate (tokenize queries; compute NL token counts)
**Review status:** Draft — onafhankelijke review door native Dutch speaker vereist vóór publicatieclaims (LR6/QR8)

**Noot:** Engels is niet de canonieke querybron. Deze queries zijn zelfstandig opgesteld vanuit de intentspecificaties.

---

## Eenvoudige feitelijke intenties (INT-001–INT-012)

---

## INT-001

- **intent_id:** INT-001
- **language:** nl
- **query_text:** "Hoe lang is de garantie op NiceHome-apparaten?"
- **linked_fact_ids:** [F0201]
- **expected_fact_set_id:** INT-001
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Directe garantiezoekopdracht. Geen apparaattype opgegeven — test het bereik "alle apparaten". AC7: verkeerd antwoord is 30 dagen (retourperiode).

---

## INT-002

- **intent_id:** INT-002
- **language:** nl
- **query_text:** "Hoeveel dagen heb ik om een NiceHome-apparaat te retourneren?"
- **linked_fact_ids:** [F0301]
- **expected_fact_set_id:** INT-002
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Retourperiode lookup. AC7: verkeerd antwoord is 2 jaar (garantie). AC1: 30 dagen hier is de retourperiode, niet de cloudopslag.

---

## INT-003

- **intent_id:** INT-003
- **language:** nl
- **query_text:** "Wat meet de NiceHome Sensor?"
- **linked_fact_ids:** [F0102]
- **expected_fact_set_id:** INT-003
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Alle drie metingen vereist (temperatuur, luchtvochtigheid, beweging). Query vraagt wat de Sensor meet zonder antwoord te impliceren.

---

## INT-004

- **intent_id:** INT-004
- **language:** nl
- **query_text:** "Nadat ik mijn apparaat heb geretourneerd, waar wordt mijn terugbetaling naartoe gestuurd?"
- **linked_fact_ids:** [F0307]
- **expected_fact_set_id:** INT-004
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Alleen de bestemming van de terugbetaling. Niet de verwerkingstijd (INT-011 dekt dat).

---

## INT-005

- **intent_id:** INT-005
- **language:** nl
- **query_text:** "Ik heb het Camera Plus Plan. Hoe lang worden mijn cloudvideo-opnames bewaard?"
- **linked_fact_ids:** [F0402]
- **expected_fact_set_id:** INT-005
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Actieve abonnementscontext expliciet vermeld. AC1: 30 dagen hier is opslag, niet retourperiode. AC3: verkeerd antwoord is 14 dagen (proefperiode).

---

## INT-006

- **intent_id:** INT-006
- **language:** nl
- **query_text:** "Hoe lang duurt de gratis proefperiode van het Camera Plus Plan?"
- **linked_fact_ids:** [F0405]
- **expected_fact_set_id:** INT-006
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Alleen de duur van de proefperiode. AC3: verkeerd antwoord is 30 dagen (opslagperiode).

---

## INT-007

- **intent_id:** INT-007
- **language:** nl
- **query_text:** "Hoe lang duurt standaardverzending?"
- **linked_fact_ids:** [F0502]
- **expected_fact_set_id:** INT-007
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** "Standaard" expliciet vermeld. Verwacht antwoord: 5 tot 7 werkdagen. Verkeerd antwoord: expresverzending (2 werkdagen).

---

## INT-008

- **intent_id:** INT-008
- **language:** nl
- **query_text:** "Kan ik de NiceHome Camera buiten gebruiken?"
- **linked_fact_ids:** [F0104]
- **expected_fact_set_id:** INT-008
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Test de beperking "alleen voor binnenshuis". Ja/nee-vraag om de restrictiefeit te activeren.

---

## INT-009

- **intent_id:** INT-009
- **language:** nl
- **query_text:** "Hoe lang duurt het doorgaans om een NiceHome-apparaat te repareren?"
- **linked_fact_ids:** [F0707]
- **expected_fact_set_id:** INT-009
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** "Doorgaans" overeenkomstig de factformulering. Antwoord vereist "na ontvangst" als ankerpunt. Verkeerd antwoord: 14 werkdagen (terugbetalingsverwerkingstijd).

---

## INT-010

- **intent_id:** INT-010
- **language:** nl
- **query_text:** "Biedt NiceHome een cloudabonnement aan, en hoe heet dat?"
- **linked_fact_ids:** [F0401]
- **expected_fact_set_id:** INT-010
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Test de naam van het abonnement. "Camera Plus Plan" is de beheerde term; verzonnen namen = FAIL.

---

## INT-011

- **intent_id:** INT-011
- **language:** nl
- **query_text:** "Hoe lang duurt het voordat ik mijn terugbetaling ontvang nadat ik een apparaat heb geretourneerd?"
- **linked_fact_ids:** [F0308]
- **expected_fact_set_id:** INT-011
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Verwerkingstijd terugbetaling. "Werkdagen" en "na ontvangst" vereist. Verkeerd antwoord: 10 werkdagen (reparatiedoorlooptijd).

---

## INT-012

- **intent_id:** INT-012
- **language:** nl
- **query_text:** "Kan ik de NiceHome Plug op afstand in- en uitschakelen zonder een Hub?"
- **linked_fact_ids:** [F0107]
- **expected_fact_set_id:** INT-012
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Test de gedeeltelijke uitzondering. Beide onderdelen vereist: aan/uit werkt zonder Hub EN automatisering vereist Hub.

---

## Voorwaardelijke beleidsintensies (INT-013–INT-024)

---

## INT-013

- **intent_id:** INT-013
- **language:** nl
- **query_text:** "Ik heb een Hub van de eerste generatie. Kan ik daar een NiceHome Sensor van de tweede generatie op aansluiten?"
- **linked_fact_ids:** [F0108, F0109]
- **expected_fact_set_id:** INT-013
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** Beide voorwaarden vermeld: Hub gen 1, Sensor gen 2. AC1 compatibiliteitsasymmetrie. Verwacht: NIET compatibel; Hub gen 2 vereist.

---

## INT-014

- **intent_id:** INT-014
- **language:** nl
- **query_text:** "Ik heb mijn NiceHome Plug uitgepakt maar wil hem niet meer houden. Het apparaat is onbeschadigd en ik zit nog binnen de retourperiode. Kan ik hem terugsturen, en wie betaalt de retourverzendkosten?"
- **linked_fact_ids:** [F0302, F0303]
- **expected_fact_set_id:** INT-014
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** Drie voorwaarden vermeld: uitgepakt, onbeschadigd, binnen retourperiode. Driedelig antwoord vereist: retour geaccepteerd + volledige terugbetaling + klant betaalt verzending.

---

## INT-015

- **intent_id:** INT-015
- **language:** nl
- **query_text:** "Ik heb mijn NiceHome Camera laten vallen en nu werkt hij niet meer. Valt dit onder de garantie?"
- **linked_fact_ids:** [F0202, F0203]
- **expected_fact_set_id:** INT-015
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** "Laten vallen" maakt accidentele schade ondubbelzinnig. Verwacht: NIET gedekt. Algemene dekking toepassen zonder uitsluiting = FAIL.

---

## INT-016

- **intent_id:** INT-016
- **language:** nl
- **query_text:** "Ik heb de behuizing van mijn NiceHome Hub geopend en een aantal interne onderdelen vervangen. Nu werkt hij niet meer. Valt dit nog onder de garantie?"
- **linked_fact_ids:** [F0202, F0204]
- **expected_fact_set_id:** INT-016
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** Onbevoegde aanpassing expliciet vermeld. Verwacht: garantie vervalt voor schade door wijziging. Beide feiten vereist.

---

## INT-017

- **intent_id:** INT-017
- **language:** nl
- **query_text:** "Als ik mijn Camera Plus Plan opzeg midden in een factureringsperiode, heb ik dan nog toegang tot cloudopslag tot het einde van de periode? En krijg ik een gedeeltelijke terugbetaling?"
- **linked_fact_ids:** [F0407, F0408]
- **expected_fact_set_id:** INT-017
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** Beide deelvragen samen gesteld. Beide onderdelen vereist: toegang blijft tot einde periode + geen gedeeltelijke terugbetaling.

---

## INT-018

- **intent_id:** INT-018
- **language:** nl
- **query_text:** "Mijn NiceHome Hub is drie jaar oud en heeft een hardwarefout. Kan hij nog worden gerepareerd, en wat moet ik betalen?"
- **linked_fact_ids:** [F0702, F0706]
- **expected_fact_set_id:** INT-018
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** "Drie jaar oud" maakt de buiten-garantieconditie ondubbelzinnig. Beide onderdelen vereist: servicekosten + klant betaalt tweerichtingsverzending.

---

## INT-019

- **intent_id:** INT-019
- **language:** nl
- **query_text:** "Mijn apparaat wordt vervangen onder garantie en ik heb gehoord dat het vervangende apparaat een gereviseerd exemplaar is. Hoe lang is de garantie op dat vervangende apparaat?"
- **linked_fact_ids:** [F0704, F0705]
- **expected_fact_set_id:** INT-019
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** AC8-intentie. Drie FAIL-patronen vooraf geregistreerd: vast 90 dagen, volledig 2-jaarsreset, geen garantie. Vereist: "het langste van resterend garantie of 90 dagen".

---

## INT-020

- **intent_id:** INT-020
- **language:** nl
- **query_text:** "Ik heb vier uur geleden een bestelling geplaatst en wil die annuleren voordat hij wordt verstuurd. Kan dat nog?"
- **linked_fact_ids:** [F0505, F0506]
- **expected_fact_set_id:** INT-020
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** "Vier uur geleden" maakt de na-venster-conditie expliciet. Beide onderdelen vereist: annulering niet meer mogelijk + retour na levering als alternatief.

---

## INT-021

- **intent_id:** INT-021
- **language:** nl
- **query_text:** "Ik wil expresverzending voor een NiceHome Camera die momenteel niet op voorraad is. Is dat mogelijk?"
- **linked_fact_ids:** [F0503, F0504]
- **expected_fact_set_id:** INT-021
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** "Niet op voorraad" maakt de conditie ondubbelzinnig. Verwacht: expresverzending NIET beschikbaar voor bestelde-maar-niet-op-voorraad-artikelen.

---

## INT-022

- **intent_id:** INT-022
- **language:** nl
- **query_text:** "Ik heb het Camera Plus Plan betaald en wil via het retourproces een terugbetaling krijgen voor het abonnement. Is dat mogelijk?"
- **linked_fact_ids:** [F0306, F0408]
- **expected_fact_set_id:** INT-022
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** Abonnementsrestitutie via retourproces — cross-document uitsluiting. Verwacht: abonnementen vallen niet onder het retourproces; opzegging is een apart traject.

---

## INT-023

- **intent_id:** INT-023
- **language:** nl
- **query_text:** "Ik heb het scherm van mijn NiceHome Camera zelf gebarsten. Kan ik hem retourneren voor een terugbetaling?"
- **linked_fact_ids:** [F0304]
- **expected_fact_set_id:** INT-023
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** "Zelf" maakt klantgerelateerde schade ondubbelzinnig. Verwacht: niet in aanmerking voor retourrestitutie.

---

## INT-024

- **intent_id:** INT-024
- **language:** nl
- **query_text:** "Ik heb mijn Camera Plus Plan geüpgraded midden in een factureringsperiode. Wanneer gaat het nieuwe plan in?"
- **linked_fact_ids:** [F0409]
- **expected_fact_set_id:** INT-024
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** Upgrade vermeld (upgrade en downgrade volgen dezelfde regel per F0409). Verwacht: begin van de volgende factureringsperiode.

---

## Probleemoplossings- en procesintensies (INT-025–INT-036)

---

## INT-025

- **intent_id:** INT-025
- **language:** nl
- **query_text:** "Al mijn NiceHome-apparaten worden als offline weergegeven. Welke stappen kan ik nemen om het verbindingsprobleem te diagnosticeren en op te lossen?"
- **linked_fact_ids:** [F0601, F0602, F0603, F0604]
- **expected_fact_set_id:** INT-025
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Geen eerdere stappen vermeld. Volledige vierstapsdiagnostiek vereist. AC5: stap 3 is "herstarten", niet "fabrieksinstellingen herstellen".

---

## INT-026

- **intent_id:** INT-026
- **language:** nl
- **query_text:** "Hoe voeg ik een nieuwe NiceHome Sensor toe aan mijn systeem?"
- **linked_fact_ids:** [F0606, F0607, F0608]
- **expected_fact_set_id:** INT-026
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** AC2: "5 seconden" vereist, niet 10. Drie geordende stappen vereist. "Apparaat toevoegen" in de app is stap 1.

---

## INT-027

- **intent_id:** INT-027
- **language:** nl
- **query_text:** "Ik heb de koppelstappen gevolgd, maar het apparaat heeft niet gekoppeld. Wat moet ik nu proberen?"
- **linked_fact_ids:** [F0606, F0607, F0608, F0609]
- **expected_fact_set_id:** INT-027
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Koppelingsverloop vermeld. Verwacht: controleer of apparaat binnen bereik van de Hub is. Eerste stap mag niet fabrieksreset zijn.

---

## INT-028

- **intent_id:** INT-028
- **language:** nl
- **query_text:** "Mijn NiceHome Sensor heeft nog garantie en werkt niet meer. Hoe dien ik een garantieclaim in?"
- **linked_fact_ids:** [F0205, F0206, F0207, F0208]
- **expected_fact_set_id:** INT-028
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Binnen garantie vermeld. Vier geordende stappen vereist; vooruitbetaald verzendlabel vereist (klant betaalt geen verzending).

---

## INT-029

- **intent_id:** INT-029
- **language:** nl
- **query_text:** "Ik wil een ongeopende NiceHome Hub retourneren en ik zit nog binnen de retourperiode. Welke stappen moet ik volgen?"
- **linked_fact_ids:** [F0309, F0310, F0311]
- **expected_fact_set_id:** INT-029
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Ongeopend + binnen retourperiode vermeld. Drie geordende stappen vereist; retourautor isatiestap is cruciaal; verzenden zonder autorisatie = FAIL.

---

## INT-030

- **intent_id:** INT-030
- **language:** nl
- **query_text:** "Ik ben mijn wachtwoord vergeten en kan niet meer inloggen op mijn account. Hoe kan ik mijn wachtwoord opnieuw instellen?"
- **linked_fact_ids:** [F0801, F0802, F0803]
- **expected_fact_set_id:** INT-030
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Drie geordende stappen vereist. E-maillinkmechanisme vereist. Telefonische reset = FAIL.

---

## INT-031

- **intent_id:** INT-031
- **language:** nl
- **query_text:** "Hoe herstel ik mijn NiceHome Hub naar de fabrieksinstellingen, en wat moet ik daarna doen?"
- **linked_fact_ids:** [F0806, F0807]
- **expected_fact_set_id:** INT-031
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** AC2: "10 seconden" vereist (niet 5). AC9: vereiste om apparaat opnieuw te koppelen moet worden vermeld (F0807 uit D08-S4). Twee chunks betrokken (D08-S3 + D08-S4).

---

## INT-032

- **intent_id:** INT-032
- **language:** nl
- **query_text:** "Ik ga mijn NiceHome Camera terugzetten naar de fabrieksinstellingen en ik maak me zorgen over mijn cloudvideo-opnames. Worden die verwijderd door een fabrieksreset?"
- **linked_fact_ids:** [F0804, F0805, F0809]
- **expected_fact_set_id:** INT-032
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** AC9: cloudvideo wordt NIET verwijderd door fabrieksreset (F0809). Beide onderdelen vereist: instellingen/accountkoppeling gewist + cloudvideo niet verwijderd. AC5: fabrieksresetcontext is expliciet.

---

## INT-033

- **intent_id:** INT-033
- **language:** nl
- **query_text:** "Mijn NiceHome Plug reageert nergens op — hij gaat niet aan en reageert ook niet op de app. Wat kan ik doen?"
- **linked_fact_ids:** [F0610, F0611]
- **expected_fact_set_id:** INT-033
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Volledige niet-reactie vermeld. Twee geordende stappen: (1) aan/uit-schakelaar via app, (2) zachte reset. AC5: stap 2 is zachte reset, niet fabrieksreset.

---

## INT-034

- **intent_id:** INT-034
- **language:** nl
- **query_text:** "Het lampje van mijn NiceHome Hub knippert rood. Wat betekent dit en wat moet ik doen?"
- **linked_fact_ids:** [F0605, F0603, F0604]
- **expected_fact_set_id:** INT-034
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Indicatorsymptoom beschreven. Betekenis (netwerkverbinding verbroken) is vereist; volgende stap (netwerk/routercontrole) wordt verwacht. Misidentificatie als hardwarefout = FAIL.

---

## INT-035

- **intent_id:** INT-035
- **language:** nl
- **query_text:** "Mijn bestelling is ruim na de verwachte leverdatum, maar er is geen bevestiging dat de zending verloren is gegaan. Waar heb ik recht op — een volledige terugbetaling, een vervanging, of iets anders?"
- **linked_fact_ids:** [F0507, F0508]
- **expected_fact_set_id:** INT-035
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Vertraagde zending expliciet vermeld (na het venster, niet bevestigd verloren). AC6: teruggave van verzendkosten is de van toepassing zijnde oplossing, niet productvervanging.

---

## INT-036

- **intent_id:** INT-036
- **language:** nl
- **query_text:** "Mijn NiceHome Camera is verloren gegaan of gestolen. Kan ik hem op afstand uit mijn account verwijderen om ongeautoriseerd gebruik te voorkomen?"
- **linked_fact_ids:** [F0808]
- **expected_fact_set_id:** INT-036
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Verloren/gestolen vermeld. Verwacht: verwijdering op afstand via de app is mogelijk. Fysieke toegang vereist = FAIL.

---

## Kwaliteitscontrole

| Controle | Resultaat |
|---|---|
| Precies 36 items | PASS — INT-001 t/m INT-036 |
| Geen fact-ID's in query_text | PASS — geverifieerd |
| Geen document-/chunk-ID's in query_text | PASS — geverifieerd |
| Geen antwoordhints in query_text | PASS — queries stellen vragen, sturen niet |
| Alle voorwaarden behouden voor voorwaardelijke intenties | PASS — per item gecontroleerd |
| Probleemoplossingsintensies bewaren probleemstatus | PASS — per item gecontroleerd |
| Niet letterlijk vertaald vanuit het Engels | PASS — zelfstandig opgesteld vanuit intentspecificaties |
| Beheerde productnamen correct gebruikt | PASS — NiceHome Hub/Sensor/Plug/Camera; Camera Plus Plan |
| TODO_REVIEW-markeringen in query_text | GEEN |

**Review-afhankelijkheid:** Nederlandse rendering is opgesteld door een niet-native Dutch speaker. Onafhankelijke review door een native Dutch speaker is vereist vóór publicatieclaims (LR6/QR8). Voor interne Stage 1 (alleen tokenizer) is de rendering voldoende.

---

*Versie: qr-nl-v0.1.0. Nederlands is een gelijkwaardige rendering; het is geen vertaling van de Engelse queries.*
