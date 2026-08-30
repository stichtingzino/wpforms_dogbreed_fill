
# WPForms dogbreed fill
A plugin to create  a selection field for users to select breeds from a provided .csv or .json file

## Description
This plugin is used to generate a list of selection fields in a wpforms form showing all dog breeds to choose from based on the selected groups. Another option is to show all recognised FCI groups divided by type (group description).

## Usage
The best way to use this is to add a selection choice to your form and use the word "breed" in the label (which you would hide) of the question. This is intended to be used with the Description of the question showing the user what is requested to fill in.

Another option is to put the word "allraces" in the label, this will generate a selection list based on the entire list of breeds but divided by the group description, e.g. "Terries","Pointing Dogs", "Retrieves - Flushing Dogs - Water Dogs", within each group the further selection will be opened.

## Input source
The following prompt can be used to request updated data from Gemini. Put this directly in the AI search prompt from Google and it should provide the resulting data as JSON and CSV in 4 different languages.

```
You are a data expert specializing in cynology. Generate a comprehensive overview of dog breeds per official FCI breed group (1 through 10), based on the breeds from the Dutch LICG database. 

I need this data in four different languages: English, French, German, and Dutch. Generate for EACH language a separate CSV and JSON code block, so I can easily save them as separate files per language. Translate both the names of the FCI groups and the names of the dog breeds to the official cynological designations of the target language.

Follow this strict structure for each language file:

### [LANGUAGE NAME] DATASET

1. CSV format:
- Filename indication: fci_rassen_[language_code].csv
- Columns: FCI_Group, Group_Name, Breeds
- Use a comma (,) as column separator.
- Use a semicolon (;) to separate the different dog breeds within the 'Breeds' column.

2. JSON format:
- Filename indication: fci_rassen_[language_code].json
- Structure: Valid JSON array of objects.
- Keys: "fci_group" (integer), "group_name" (string), "breeds" (array of strings).

Generate the blocks sequentially for:
1. Dutch (NL)
2. English (EN)
3. French (FR)
4. German (DE)

Do not give introductory comments, start directly with the first language block.
```