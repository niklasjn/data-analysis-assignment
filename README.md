# Caseoppgave dataanalyse

## Om prosjektet
Prosjektet er en praktisk besvarelse på en oppgave som en del av en ansettelsesprosess.
Prosjektet omfatter analyse av surveydata og klargjøring av rådata til analyse.

## Prosjektstruktur
TODO

## Avhengigheter
Prosjektet krever Python 3.11 eller nyere. Installer avhengigheter med:
```
pip install -r requirements.txt
```

## Kjøring av oppgaveløsninger

### 2.1.1 Studentbarometeret *Eget læringsutbytte*
TODO

### 2.1.2 Studentbarometeret *Indeks faglig og sosial læringsmiljø*
TODO

### 2.2 Klargjøring av respondentliste

#### Naviger til task-mappen
```
cd src/tasks/task_2_2
```
#### Kjør pipeline for datarens
```
python cleaning_pipeline.py
```
#### Alternativ: Kjør fra prosjektrot
```
python -m src.tasks.task_2_2.cleaning_pipeline
```
#### Utdata
Etter kjøring vil følgende filer genereres:

| Fil | Beskrivelse |
|-----|-------------|
| cleaned_data.xlsx |Renset datasett klar for analyse |
| needs_manual_inspection.xlsx | Rader som krever manuell gjennomgang |
| removed_rows.xlsx | Rader fjernet pga. valideringsfeil |
| processing.log | Kjøretidslogg |

#### Pipeline-trinn
Pipelinen følger en sekvensiell struktur for å sikre dataintegritet:

| Trinn | Beskrivelse |
|-------|-------------|
| 1. Normalisering | Standardiserer datoformater, endrer tekst til små bokstaver, fjerner overfladiske mellomrom |
| 2. Validering | Sjekk av gyldige verdier; datoer, tekster, tall |
| 3. Deduplisering | Identifisering og flytting av duplikater for manuell revidering |
| 4. Transformasjon | Fornavn og etternavn slås sammen, datoer formateres |
| 5. Dateberikning | Legger til fylkesnummer og inntektsnivå |
| 6. Standardisering | Klargjøring til utdata-fil. snake_case og definert rekkefølge på kolonner |

#### Utvalgte beslutninger og begrunnelser i datahåndteringen
- Ingen data slettes. Data som ikke blir med i utdata-fil lagres i egne filer for slettet data og data som krever manuell revidering
- Uklart hvorvidt duplikate e-postadresser bør håndteres ved at begge fjernes, eller kun én bevares. Løste ved fjerne alle forekomster, og flytte disse til inspeksjonsfil for manuell revidering av et menneske
- Valgte å flagge kombinasjon av samme fornavn, etternavn og fødselsdato som duplikater. 
  - Siden det i teorien kan finnes personer som har nøyaktig samme navn og fødselsdato, flyttes disse til manuell revidering av et menneske som kan ta endelig avgjørelse
- Kommunenummer/fylkesnummer: programmet laster per nå inn en Excel-fil "kommune_fylke_kartverket.xlsx"  med kommune- og fylkesnumre kopiert inn i Excel fra https://www.kartverket.no/til-lands/fakta-om-norge/norske-fylke-og-kommunar.
  - I valideringsfasen fjernes rader hvor kommunenummer ikke finnes i Excel-filen.
  - I databerikningsfasen matches kommunenummer fra råfil (som ikke er fjernet) opp mot kommunenummer og fylkesnummer fra Excel-filen slik at fylkesnummer kan legges til.
  - Det er uklart om Excel-filen er god, og bør undersøkes. Kan være bedre å bytte til f.eks. SSBs KLASS-API, men funksjonaliteten illustreres helt fint.
  - Det er mulig å droppe kommunenummersjekk og fylkesnummerberikning ved å ikke inkludere "kommune_fylke_kartverket.xlsx", uten at det medfører andre problemer enn at fylkesnummer ikke legges til. Kan være aktuelt for å se hvordan f.eks. filen med rader som krever manuell revidering utvikles (kommunummersjekk fjerner veldig mange rader fra rådataen)
- Inntektsnivå beregnes basert på tre kvantiler, slik at fordelingen alltid gir tre grupper uavhengig av faktisk inntektsfordeling i datasett. 
  - Tar ikke høyde for ekstremverdier utover å fjerne rader med inntekt 0 eller mindre i valideringsfasen. 
  - Fordelingen kan være misvisende, men er tatt med hensyn på tiltentk uvitenhet om mulige verdier i et stort datasett. 
  - Spesielle tilfeller som at alle i datasettet har samme inntekt medfører at inntektsnivå ikke genereres.

#### Fremtidig forbedring/neste trinn
- Produsere enhetstester for hver modul. Det finnes ingen tester per nå utover vanlig kjøring av program med datasett
- Generalisere hjelpefunksjonalitet der det er mulig, for fremtidig gjenbruk 