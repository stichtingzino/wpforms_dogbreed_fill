
# WPForms dogbreed fill
A plugin to create  a selection field for users to select breeds from a provided .csv or .json file

## Description
This plugin is used to generate a list of selection fields in a wpforms form showing all dog breeds to choose from based on the selected groups. Another option is to show all recognised FCI groups divided by type (group description).

## Usage
The best way to use this is to add a selection choice to your form and use the word "breed" in the label (which you would hide) of the question. This is intended to be used with the Description of the question showing the user what is requested to fill in.

Another option is to put the word "allraces" in the label, this will generate a selection list based on the entire list of breeds but divided by the group description, e.g. "Terries","Pointing Dogs", "Retrieves - Flushing Dogs - Water Dogs", within each group the further selection will be opened.

## Input source
The following (dutch) prompt can be used to request updated data from gemini, put this directly in the AI search prompt from google and it should provide the resulting data as json and csv in 4 different languages.

```
Je bent een data-expert gespecialiseerd in kynologie. Genereer een uitgebreid overzicht van hondenrassen per officiële FCI-rasgroep (1 tot en met 10), gebaseerd op de rassen uit de database van het Nederlandse LICG. 

Ik heb deze data nodig in vier verschillende talen: Engels, Frans, Duits en Nederlands. Genereer voor ELKE taal een apart CSV- en JSON-codeblok, zodat ik deze eenvoudig kan opslaan als losse bestanden per taal. Vertaal zowel de namen van de FCI-groepen als de namen van de hondenrassen naar de officiële kynologische benamingen van de doeltaal.

Hanteer voor elk taalbestand de volgende strikte structuur:

### [TAALNAAM] DATASET

1. CSV-formaat:
- Bestandsnaamindicatie: fci_rassen_[taalcode].csv
- Kolommen: FCI_Group, Group_Name, Breeds
- Gebruik een komma (,) als kolomscheider.
- Gebruik een puntkomma (;) om de verschillende hondenrassen binnen de kolom 'Breeds' te scheiden.

2. JSON-formaat:
- Bestandsnaamindicatie: fci_rassen_[taalcode].json
- Structuur: Geldige JSON-array van objecten.
- Keys: "fci_group" (integer), "group_name" (string), "breeds" (array van strings).

Genereer achtereenvolgens de blokken voor:
1. Nederlands (NL)
2. Engels (EN)
3. Frans (FR)
4. Duits (DE)

Geef geen inleidende praatjes, start direct met het eerste taalblok.
```