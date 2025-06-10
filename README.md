# jadn-cli

The JADN (JSON Abstract Data Notation) CLI (Command Line Interface) provides the ability to validate, convert, translate and transform JADN compliant schemas.  In addition, the cli provides the ability to validate JSON, CBOR or XML data against JADN schemas.

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
   You can run a command from the within CLI script.  
   This method provides help context and leads you through a series of prompts.  

   Also, if you don't have a schema or data yet, we have preloaded the music-database.jadn scheam and a music_library.json file for you to try out.  Here's an example:

   ```sh
   jadn) schema_v my_schema.jadn
   ```

   Or run a command directly from the terminal:

   ```sh
   python jadn_cli.py schema_v my_schema.jadn
   ```

   Run help or man to see a list of commands and examples.

**Note:**  
Replace `my_schema.jadn` with the actual filename of your schema in the `schemas` directory.
