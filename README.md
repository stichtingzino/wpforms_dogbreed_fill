
# WPForms Dog Breed Fill Plugin and Breed Data Generation Tool

This repository contains a WordPress plugin (`wpforms_dogbreed_fill`) and a Python tool (`get-dogbreeds`) to generate and manage a list of official FCI dog breeds in multiple languages.

## Table of Contents

1. [Installation](#installation)
   - [WordPress Plugin](#wordpress-plugin)
   - [Python Tool](#python-tool)
2. [Usage](#usage)
   - [WordPress Plugin](#wordpress-plugin-usage)
   - [Python Tool](#python-tool-usage)
3. [References](#references)

## Installation

### WordPress Plugin

1. **Download the Plugin:**
   - Go to the [GitHub Releases](https://github.com/stichtingzino/wpforms_dogbreed_fill/releases) page.
   - Download the latest `wpforms_dogbreed_fill.zip` file.

2. **Install the Plugin:**
   - Log in to your WordPress admin dashboard.
   - Navigate to **Plugins > Add New**.
   - Click on **Upload Plugin**.
   - Upload the `wpforms_dogbreed_fill.zip` file you downloaded.
   - Click **Install Now** and then **Activate**.

### Python Tool

1. **Install the Tool:**
   - Ensure you have `pipx` installed. If not, install it using:
     ```sh
     pip install pipx
     ```
   - Install the `get-dogbreeds` tool using `pipx`:
     ```sh
     pipx install .
     ```

## Usage

### WordPress Plugin Usage

1. **Admin Page:**
   - After activating the plugin, navigate to **WPForms > Dog Breeds** in the WordPress admin dashboard.
   - Here, you can manage the dog breeds data and configure the plugin settings.

2. **WPForms Selection List:**
   - To activate the plugin in a WPForms selection list, add the word "breeds" to the field label or description.
   - For example, label a selection list field as "Dog Breeds" or "Select a Breed".

### Python Tool Usage

1. **Generate Dog Breed Data:**
   - Run the `get-dogbreeds` command in your terminal:
     ```sh
     get-dogbreeds
     ```
   - This command will generate JSON and CSV files containing the list of official FCI dog breeds in multiple languages.

2. **Requirements:**
   - **Google Gemini API Key:** You need a valid API key to access the Google Gemini API.
   - **Environment Variable:** Set the `GOOGLE_GEMINI_API_KEY` environment variable with your API key:
     ```sh
     export GOOGLE_GEMINI_API_KEY="your_api_key_here"
     ```
   - Alternatively, you can use a 1Password URL:
     ```sh
     export GOOGLE_GEMINI_API_KEY="op://vault/entry_name/password"
     ```

## References

- [Documentation for generating API keys for Google Gemini](https://developers.gemini.google.com/docs/guides/getting-started#api-key)
- [1Password CLI Documentation](https://developer.1password.com/docs/cli/)

# Google Gemini prompt
Initially this project was setup with a manual process using Google gemini to extract the dogbreeds from the official sites. Below is the original prompt that was used. In this version, the prompt is part of the python code and a relatively simple prompt is being used for the four different supported languages.

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