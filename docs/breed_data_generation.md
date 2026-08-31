# Breed Data Generation

This document describes how to use the Python script in the `src` directory to generate a list of official FCI dog breeds and save them in JSON and CSV formats for multiple languages. It also includes information about the required and optional environment variables and how to store an API key in a 1Password vault.

## Installation

The script can be installed using `pipx` for easy management. First, ensure you have `pipx` installed:

```sh
pip install pipx
```

Then, install the script using `pipx`:

```sh
pipx install .
```

## Execution of the Python Script

The script `gen_breed_file.py` can be executed by running the following command in the terminal:

```sh
python src/fci_dogbreeds/gen_breed_file.py
```

## Environment Variables

Here is an overview of the environment variables you can set:

| Variable Name            | Description                                                                 | Required |
|--------------------------|------------------------------------------------------------------------------|----------|
| `GOOGLE_GEMINI_API_KEY`  | The API key for accessing the Google Gemini API.                             | Yes      |
| `OUTPUT_DIRECTORY`       | The path to the directory where the generated files will be saved.           | No       |
| `PROMPT_LANGUAGES`       | A dictionary with the available languages and their corresponding prompt display names. | No       |
| `TARGET_FILENAME_PREFIX` | The prefix used for the names of the generated files.                        | No       |

### Example of Environment Variables

Here is an example of how to set the environment variables in a Unix-like operating system (Linux, macOS):

```sh
export GOOGLE_GEMINI_API_KEY="your_api_key_here"
export OUTPUT_DIRECTORY="data"
export PROMPT_LANGUAGES='{"en": "English", "nl": "Nederlands"}'
export TARGET_FILENAME_PREFIX="fci_breeds_"
```

## Storing API Key in 1Password Vault

You can securely store the API key in a 1Password vault and use it in your environment variables. Here is an example of how to do this:

1. **Store API Key in 1Password**:
   - Create a new item in your 1Password vault.
   - Add the API key as a password or note.
   - Note the URL of the item, for example, `op://vault/entry_name/password`.

2. **Use the 1Password URL in the Environment Variable**:
   - Install the 1Password CLI (`op`) on your system.
   - Ensure you are logged in to your 1Password account.
   - Use the 1Password URL in the environment variable `GOOGLE_GEMINI_API_KEY`.

Here is an example of how to use the 1Password URL:

```sh
export GOOGLE_GEMINI_API_KEY="op://vault/entry_name/password"
```

The script will use the 1Password CLI to retrieve the API key when it is executed.

## References

- [Documentation for generating API keys for Google Gemini](https://developers.gemini.google.com/docs/guides/getting-started#api-key)
- [1Password CLI Documentation](https://developer.1password.com/docs/cli/)
