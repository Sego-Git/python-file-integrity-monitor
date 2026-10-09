# Python File Integrity Monitor (FIM)

A Python-based File Integrity Monitoring (FIM) tool that detects changes to files by comparing their SHA-256 hashes against a trusted baseline.

This project is part of my hands-on cybersecurity learning journey. It combines Python programming with fundamental defensive security concepts, including cryptographic hashing, file integrity checking, security event logging, exception handling, and automated testing.

## Project Overview

A File Integrity Monitor answers an important security question:

**Has any file been modified, added, or deleted since the trusted baseline was created?**

The monitor creates a baseline containing the SHA-256 hash of each file in a monitored directory. During subsequent scans, it calculates the hashes again and compares the current state with the stored baseline.

The tool identifies:

* Modified files
* Newly added files
* Deleted files
* Unchanged files

Security events are recorded in a configurable log file with timestamps and severity levels.

## How It Works

1. Select a directory to monitor.
2. Create a trusted baseline of its files and SHA-256 hashes.
3. Scan the directory again when needed.
4. Compare the current files and hashes against the baseline.
5. Report and log detected changes.

The monitor hashes file contents rather than storing the contents themselves.

SHA-256 produces a fixed-length hash. When file contents change, their hash will normally change too, allowing the monitor to detect modifications.

## Features

### File Integrity Monitoring

* SHA-256 file hashing
* Trusted baseline creation and loading
* Recursive directory scanning
* Modified-file detection
* Added-file detection
* Deleted-file detection
* Unchanged-file identification
* Separate baselines for monitored directories

### Command-Line Interface

* Command-line argument parsing using Python's `argparse`
* Separate commands for baseline creation and integrity scanning
* Built-in command help

### Logging and Configuration

* Configurable log file and severity level
* Timestamped security event logs
* External configuration through `config.json`
* Structured logging using Python's `logging` module

### Reliability and Testing

* Input and directory validation
* Exception handling for missing files, permission errors, and file-reading failures
* Handling of invalid JSON configuration and baseline files
* Modular code organization
* Automated tests using Python's built-in `unittest` framework

## Technologies Used

* Python
* SHA-256
* JSON
* `argparse`
* `logging`
* `unittest`
* Git and GitHub

## Project Structure

```text
Python File Integrity Monitor/
├── monitor.py
├── config.py
├── config.json
├── file_utils.py
├── baseline.py
├── integrity.py
├── logger.py
├── README.md
├── Notes.txt
├── .gitignore
├── baselines/
├── documents/
├── test folder/
└── tests/
    ├── test_baseline.py
    ├── test_file_utils.py
    └── test_integrity.py
```

Generated baseline JSON files and log files are excluded from version control by the project's `.gitignore` rules.

## Getting Started

### Requirements

* Python 3.10 or later
* Git (optional, for cloning and version control)

The project uses Python's standard library and does not currently require third-party packages.

### Setup

Clone the repository:

```bash
git clone https://github.com/Sego-Git/python-file-integrity-monitor
cd python-file-integrity-monitor
```

Replace `<YOUR_GITHUB_REPOSITORY_URL>` with the URL of your repository.

Make sure `config.json` exists and contains the required settings:

```json
{
    "log_file": "security.log",
    "log_level": "INFO",
    "baseline_directory": "baselines"
}
```

The configuration controls the log file, logging severity level, and directory used to store baselines.

### Usage

Display the available commands:

```bash
python monitor.py --help
```

Create a baseline for a directory:

```bash
python monitor.py create-baseline "documents"
```

Scan the directory against its baseline:

```bash
python monitor.py scan "documents"
```

For a directory whose name contains spaces, keep the quotation marks around the path.

Create a baseline before running the first scan. The monitor uses the stored baseline as its reference for later comparisons.

### Run the Automated Tests

From the project root, run:

```bash
python -m unittest discover -s tests -v
```

The test suite covers file hashing, baseline management, directory scanning, error handling, and file integrity changes.

At the current development checkpoint, **15 automated tests passed**.

## Cybersecurity Concepts Practiced

This project provides practical experience with:

* File Integrity Monitoring (FIM)
* Cryptographic hashing and SHA-256
* Trusted baselines
* File change detection
* Security event logging
* Defensive programming
* Exception handling
* Input validation
* Command-line tools
* Automated software testing
* Modular Python development
* Git-based version control

## Project Status

**Current version: Version 2 — Professionalized CLI File Integrity Monitor**

Version 2 builds on the original CLI implementation with improved command handling, configurable logging, external configuration, better exception handling, modular architecture, input validation, and automated tests.

### Roadmap

Potential future improvements include:

* Version 3: Real-time file monitoring
* Version 4: Database storage
* Version 5: Flask backend and API
* Version 6: Web-based monitoring dashboard
* Further security hardening and more detailed event analysis
* Possible SOC/SIEM integration

These are planned improvements, not features currently implemented.

## Learning Approach

The project is developed incrementally. Each stage introduces a new concept and builds on the previous one, with the goal of understanding both the Python implementation and the cybersecurity principles behind the tool.

## Limitations

This is an educational project and is not yet a production-grade security monitoring solution.

The baseline is stored locally. An attacker who can modify both the monitored files and the baseline may be able to undermine integrity checks. Production use would require stronger baseline protection, access controls, and additional security measures.

The tool performs scans when invoked; continuous real-time monitoring is planned for a future version.

## Disclaimer

This project is intended for educational and defensive cybersecurity purposes. Monitor only files and systems that you own or are authorized to inspect.
