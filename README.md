# TransLocator

## Project Structure
    The project structure is as follows:
    - `data`: Contains the dataset in json format.
    - `src`: Contains the source code for the project.
    - `requirements.txt`: Contains the required python packages for the project.
    - `README.md`: Contains the project documentation.

## Dataset
   The dataset used for this project is provided in the `data` directory in json format. The dataset contains information about the location of the bus stops in the city of Bengaluru. The dataset contains the following fields:
   - `bug_id`: Unique identifier for the bug.
   - `bug_title`: Title of the bug.
   - `bug_description`: Description of the bug.
   - `project`: Project to which the bug belongs.
   - `sub_project`: Subject to which the bug belongs.
   - `version`: Version of the project.
   - `fixed_version`: Version in which the bug was fixed.
   - `fixed_files`: Files in which the bug was fixed as a json array.


## Installing Required Packages


### Python 3.10:

#### Windows:

1. **Download Python 3.10:**  
   - Visit [python.org/downloads](https://www.python.org/downloads/)
   - Download the Windows installer (`Windows Installer (64-bit)` recommended).
   - Run the installer.
   - Check the box to add Python to PATH during installation.

2. **Verify Installation:**  
   - Open Command Prompt.
   - Type `python --version`.
   - You should see `Python 3.10.x`.

#### Linux (Ubuntu/Debian):

1. **Install Python 3.10:**  
   - Open Terminal.
   - Run the following commands:
     ```
     sudo apt update
     sudo apt install python3.10
     ```

2. **Verify Installation:**  
   - Type `python3.10 --version`.
   - You should see `Python 3.10.x`.

### Elasticsearch:

#### Windows:

1. **Download Elasticsearch:**
   - Visit [elastic.co/downloads/elasticsearch](https://www.elastic.co/downloads/elasticsearch).
   - Download the ZIP package for Windows.

2. **Extract and Start Elasticsearch:**  
   - Extract the downloaded ZIP file.
   - Navigate to the extracted directory.
   - Run `bin\elasticsearch.bat` in Command Prompt.

3. **Verify Installation:**  
   - Open a web browser.
   - Go to [http://localhost:9200](http://localhost:9200).
   - Check for a JSON response indicating Elasticsearch is running.

#### Linux (Ubuntu/Debian):

1. **Download and Install Elasticsearch:**  
   - Open Terminal.
   - Run the following commands:
     ```
     wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-<version>-amd64.deb
     sudo dpkg -i elasticsearch-<version>-amd64.deb
     ```

2. **Start Elasticsearch Service:**  
   - Run:
     ```
     sudo systemctl start elasticsearch
     sudo systemctl enable elasticsearch
     ```

3. **Verify Installation:**  
   - Open a web browser.
   - Go to [http://localhost:9200](http://localhost:9200).
   - Ensure Elasticsearch is running by checking for a JSON response.


### Install Required Python Packages:

1. **Navigate to Project Directory:**
   - Open terminal/command prompt.
   - Use `cd` to move to the directory containing `requirements.txt`.

2. **Install Packages:**
   - Run `pip install -r requirements.txt`.
