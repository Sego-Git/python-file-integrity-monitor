# Python File Integrity Monitor (FIM)

A Python-based cybersecurity project that monitors files for unauthorized changes using SHA-256 hashing. It supports trusted baselines, manual integrity scans, real-time filesystem event detection, and security logging.

This project was developed as a hands-on learning exercise to explore Python programming, file integrity monitoring, event-driven programming, and basic security monitoring concepts.

## Features

### Version 1 — Basic File Integrity Monitoring

* Calculate file hashes using SHA-256.
* Create a trusted baseline of file hashes.
* Detect added, modified, and deleted files.

### Version 2 — Modular CLI and Logging

* Command-line interface built with `argparse`.
* JSON-based baseline storage.
* Recursive folder scanning.
* Configurable logging through `config.json`.
* Modular architecture separating configuration, hashing, baseline management, integrity checks, and logging.
* Automated unit tests.

### Version 3 — Real-Time Monitoring

* Real-time filesystem event detection using Watchdog.
* Detection of file creation, modification, deletion, and move events.
* Debouncing to reduce repeated integrity scans.
* Real-time event logging in `security.log`.
* Safe shutdown handling for the observer and pending timer.
* Preservation of the original trusted baseline during monitoring.

## Technologies Used

* Python 3
* SHA-256 hashing (`hashlib`)
* JSON
* `argparse`
* `logging`
* `os`
* `threading`
* Watchdog
* `unittest`

## Project Structure

```text
Python File Integrity Monitor/
│
├── monitor.py
├── watcher.py
├── file_utils.py
├── baseline.py
├── integrity.py
├── config.py
├── logger.py
├── config.json
├── README.md
├── .gitignore
│
├── baselines/
│   └── *_baseline.json
│
├── documents/
│
└── tests/
    └── ...
```

*Note: The exact files inside `tests/` and the contents of your working folders may vary.*

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Sego-Git/python-file-integrity-monitor.git
cd python-file-integrity-monitor
```

### 2. Install the dependency

```bash
python -m pip install watchdog
```

### 3. Configure the application

Review `config.json`:

```json
{
    "log_file": "security.log",
    "log_level": "INFO",
    "baseline_directory": "baselines"
}
```

The configuration specifies the log file, logging level, and directory used to store baseline files.

## Usage

Run the commands from the project directory.

### Create a trusted baseline

```bash
python monitor.py create-baseline "documents"
```

This calculates the SHA-256 hash of each accessible file and saves the hashes to a JSON baseline.

### Perform a manual integrity scan

```bash
python monitor.py scan "documents"
```

This compares the current folder contents with the trusted baseline and reports detected additions, modifications, and deletions.

### Start real-time monitoring

```bash
python monitor.py watch "documents"
```

The watcher monitors the selected folder recursively. When relevant filesystem events occur, the program logs the events and schedules an integrity scan.

Press `Ctrl+C` to stop monitoring.

### Run automated tests

```bash
python -m unittest discover -s tests -v
```

## How It Works

1. **Baseline creation:** the program calculates SHA-256 hashes and stores them in JSON.
2. **Integrity checking:** current file hashes are compared with the stored hashes.
3. **Change detection:** the program identifies added, modified, and deleted files.
4. **Real-time monitoring:** Watchdog reports filesystem events, triggering a debounced integrity scan.
5. **Logging:** relevant events and integrity findings are recorded for later review.

The trusted baseline is not automatically updated during monitoring. A new baseline should be created deliberately when changes have been reviewed and approved.

## Security Considerations and Limitations

* A baseline is only trustworthy if its creation and storage are protected.
* SHA-256 helps detect content changes but does not establish who made a change or whether it was malicious.
* This project is a learning tool, not a replacement for a production endpoint detection or enterprise security monitoring platform.
* The current real-time implementation performs full-folder scans after event bursts. Large directory trees may require optimization.
* Filesystem notifications may be duplicated or missed under certain conditions; important integrity checks should not depend solely on real-time events.
* Baselines and logs should be protected from unauthorized modification.

## Learning Objectives

Through this project, I practised:

* Python functions, modules, exceptions, and file handling.
* Hashing and file integrity verification.
* JSON serialization and deserialization.
* Command-line interface development.
* Logging and security event recording.
* Event-driven programming and threading.
* Automated testing and incremental software development.

## Future Improvements

* Improve event handling and reduce unnecessary scans.
* Add more robust handling of file moves, inaccessible files, and monitoring errors.
* Expand automated test coverage for real-time monitoring.
* Improve baseline security and configuration validation.
* Add a user interface for viewing alerts and integrity reports.

## Author

**Sego-Git**

GitHub: https://github.com/Sego-Git
