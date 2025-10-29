# jadn-cli

The JADN (JSON Abstract Data Notation) CLI (Command Line Interface) provides the ability to validate, convert, translate and transform JADN compliant schemas.  In addition, the CLI provides the ability to validate JSON, CBOR or XML data against JADN schemas.

## Getting Started with jadn-cli

Follow these steps to set up and run the JADN CLI from scratch:

1. **Clone or Fork the Repository**

   ```sh
   git clone https://github.com/ScreamBun/jadn-cli.git
   cd jadn-cli
   ```

2. **(Optional) Create and Activate a Virtual Environment**

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **(Optional) Install Additional Tools**
   If you use `poetry` or `pytest`, install them as needed:

   ```sh
   pip install poetry pytest
   ```

5. **Prepare Your Schemas and Data**
   - Place your JADN schema files in the `schemas` directory.
   - Place your data files the `data` directory.
   - Note: files generated will be dropped in the `output` directory

6. **Run the CLI**

   ```sh
   python jadn_cli.py
   ```

7. **Run a Command**
   You can run a command from within the CLI script.  
   This method provides help context and leads you through a series of prompts.  

   Also, if you don't have a schema or data yet, we have preloaded the music-database.jadn schema and a music_library.json file for you to try out.  Here's an example:

   ```sh
   schema_v my_schema.jadn
   ```

   Or run a command directly from the terminal:

   ```sh
   python jadn_cli.py schema_v my_schema.jadn
   ```

   Don't want to type in the entire file name? Enter a command with no args to get a numbering option:

   ```sh
   (jadn) schema_v
   Files in './schemas' directory:
   1 - music-database.jadn
   Enter a schema by name or number (type 'exit' to cancel): 1
   ```

   Already know what number to use? Enter it in as an argument:

   ```sh
   (jadn) schema_v 1
   ```

   Run help or man to see a list of commands and examples.

**Note:**

- Replace `my_schema.jadn` with the actual filename of your schema in the `schemas` directory.
- To disable helper prompts and run the cli inline only, go to the config.toml file and change use_prompts to false.

## Update an Existing CLI

If you already have the CLI cloned and you just want to pull down the latest and greatest, here is how.

Follow these steps to set up and run the JADN CLI from scratch:

1. **Using Git Pull the Latest**

From the terminal, locate your jadn-cli directory and enter the directory.  
Then at root, run this git command:

   ```sh
   cd jadn-cli
   ```

   ```sh
   git pull https://github.com/ScreamBun/jadn-cli.git
   ```

<!-- markdownlint-disable-next-line MD029 -->
2. **Run the CLI**
Now just fire it up:

   ```sh
   python jadn_cli.py
   ```
