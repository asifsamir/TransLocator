# TransLocator

## Install Required Packages

[//]: # (### Python 3.10:)

[//]: # (1. **Download Python 3.10:**  )

[//]: # (   - Visit [python.org/downloads]&#40;https://www.python.org/downloads/&#41;)

[//]: # (   - Download and run the installer for your operating system.)

[//]: # (   - Ensure to add Python to your system PATH during installation.)

[//]: # ()
[//]: # (2. **Verify Installation:**  )

[//]: # (   - Open a terminal/command prompt.)

[//]: # (   - Type `python --version` or `python3 --version`.)

[//]: # (   - You should see `Python 3.10.x` indicating a successful installation.)

[//]: # ()
[//]: # (### Elasticsearch:)

[//]: # ()
[//]: # (1. **Download Elasticsearch:**  )

[//]: # (   - Visit [elastic.co/downloads/elasticsearch]&#40;https://www.elastic.co/downloads/elasticsearch&#41;.)

[//]: # (   - Download the appropriate version for your OS.)

[//]: # ()
[//]: # (2. **Extract and Start Elasticsearch:**  )

[//]: # (   - Extract the downloaded package.)

[//]: # (   - Navigate to the )


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
