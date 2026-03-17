# Caseoppgave dataanalyse

## Om prosjektet
Prosjektet er en praktisk besvarelse på en oppgave som en del av en ansettelsesprosess.
Prosjektet omfatter analyse av surveydata og klargjøring av rådata til analyse.

## Prosjektstruktur
data-analysis-assignment/
├── README.md
├── requirements.txt
├── .editorconfig
├── data/
│   ├── raw/
│   │   ├── fiktiv_kontaktinformasjon.xlsx
│   │   ├── Kodebok_SB2025_portal.xlsx
│   │   ├── programfil_SB2025_portal.xlsx
│   │   └── kommune_fylke_kartverket.xlsx
│   ├── processed/
│   │   └── cleaned_data.xlsx
│   └── logs/
│       ├── processing.log
│       ├── removed_rows.xlsx
│       └── needs_manual_inspection.xlsx
└── src/
    ├── tasks/
    │   ├── task_2_1_1/
    │   │   ├── learning_outcome_visuals.py
    │   │   ├── helpers.py
    │   │   ├── config.py
    │   │   ├── __init__.py
    │   │   └── figures/
    │   │       └── laerutb_mean_scores.png
    │   ├── task_2_1_2/
    │   │   ├── psymiljo_analysis.py
    │   │   ├── config.py
    │   │   ├── __init__.py
    │   │   └── figures/
    │   │       └── psymiljo.png
    │   └── task_2_2/
    │       ├── cleaning_pipeline.py
    │       ├── normalization.py
    │       ├── validation.py
    │       ├── deduplication.py
    │       ├── transformation.py
    │       ├── enrichment.py
    │       ├── config.py
    │       └── __init__.py
    └── common/
        └── __init__.py

## Avhengigheter
Prosjektet krever Python 3.11 eller nyere. Installer avhengigheter med:
```
pip install -r requirements.txt
```

## Valgfritt og ikke formelt sett løsning på caseoppgave: Jupyter Notebook
Jeg har brukt Jupyter Notebook for enkel, grunnleggende visuell utforskning av datasettet.
Dette er ikke en del av besvarelsen min, men jeg har latt filene (med filending .ipynb) bli
igjen i oppgavemappene dersom det er av interesse å se på dem.

Altså ikke en streng avghengighet, og trenger verken installeres eller kjøres for fungerende test av prosjektet.

**Valgfritt**: Installere Jupyter Notebook
```
pip install jupyter
```
eller
```
pip install notebook
```
**Valgfritt**: Starte Jupyter Notebook
Via foretrukken kodeeditor med utvidelser som støtter Jupyter Notebook, eller
```
cd src/tasks/task_2_1_1
jupyter notebook
```
eller tilsvarende for oppgave 2.1.2.

## Oppgaveløsninger og kjøring av kode

### 2.1.1 Studentbarometeret *Eget læringsutbytte*

#### Naviger til riktig task-mappe
```
cd src/tasks/task_2_1_1
```
#### Kjør script for generering av søylediagram
```
python learning_outcome_visuals.py
```
#### Alternativ: Kjør fra prosjektrot
```
python -m src.tasks.task_2_1_1.learning_outcome_visuals
```
#### Utdata
- "/src/tasks/task_2_1_1/figures/laerutb_mean_scores.png". Figur med søylediagram over studenters tilfredshet med ulike variabler for læringsutbytte
- Enkel kontrollutskrift i terminal med gjennomsnitt, minimum, maksimum og standardavvik for hver variabel

#### Programflyt
- Laster inn variabeldefinisjoner fra kodebok for å mappe variabelkoder til spørsmålstekster
- Filtrerer ut manglende verdier (kodet som 9999) og verdier utenfor forventet verdi i intervall 1 - 5
- Beregner gjennomsnitt, minimum, maksimum og standardavvik for hver variabel
- Lager et horisontalt søylediagram hvor hver søyle representerer gjennomsnittsverdi per variabel

### 2.1.2 Studentbarometeret *Indeks faglig og sosial læringsmiljø*
#### Naviger til riktig task-mappe
```
cd src/tasks/task_2_1_2
```
#### Kjør script
```
python psymiljo_analysis.py
```
#### Alternativ: Kjør fra prosjektrot
```
python -m src.tasks.task_2_1_2.psymiljo_analysis
```
#### Utdata
- "/src/tasks/task_2_1_2/figures/psymiljo.png". Figur med topp antall studiesteder på snittscore for indeks psymiljo_15, og topp antall   fagfelt for hvert av studiestedene. Standard antall er topp 8 studiesteder med høyest snittscore totalt, og topp 4 fagfelt med høyest snittscore per studiested.
- Enkel kontrollutskrift i terminal med studiestedene som nevnt over, snittscore og deres topp fagfelt med snittscore.

#### Løsning og arkitekturell tilnærming
I kontrast til oppgave 2.1.1 og 2.2, valgte jeg en mindre modulbasert struktur her, og en enklere scriptbasert konsentrert arkitektur. Begrunnelsen for dette er at jeg ikke fant noe nytt eller spesielt å vise hva gjelder prosjektstruktur og organisering sammenlignet med de to andre oppgavene. Et alternativ ville være å flytte felleskonstanter eller hjelpefunksjoner på et høyere nivå, men det var vanskelig å rettferdiggjøre for en relativt liten oppgave og scope.
Dette gjør derimot filen mer lesbar med tydeligere analysefokus og mer effektiv uten abstraksjon og fil-overhead.

### 2.2 Klargjøring av respondentliste

#### Naviger til riktig task-mappe
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