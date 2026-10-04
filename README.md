Python File Integrity Monitor

A beginner-friendly Python-based File Integrity Monitoring(FIM) tool that detects unauthorized or unexpected changes to files by comparing their SHA-256 hashes against a trusted baseline. 

This project was built as part of my hands-on cybersecurity learning journey, with the goal of understanding how basic file integrity monitoring works while developing practical Python and security skills.

************* Project Overview ***************

A File Integrity Monitor answers a simple but important security question: Has any file been modified, added, or deleted since the last time I checked?

The monitor created a trustes baseline containing the SHA-256 hash of each file in a monitored directory. During subsequent scans, it calculates the hashes again and compares them with the baseline. 

The tool can currently detect:
- Modified files
- Newly added files
- Deleted files
- Unchanged files

Detected security events are also recorded in a log file.

********* How It Works **********

The basic workflow is: 

Files on computer 
        │ 

        ▼ 
Calculate SHA-256 hash of each file 
        │ 
        ▼ 
Create trusted baseline 
        │ 
        ▼ 
        Later... 
        │ 
        ▼ 
Calculate hashes again 
        │ 
        ▼ 
Compare with baseline
    /      |        \
    /      |          \ 
Modified   Added      Deleted

The project uses cryptographic hashing rather than storing the contents of files.

If the contents of a file change, its SHA-256 hash will normally change as well, allowing the monitor to identify the modification.


*********** Current Features ***************
- SHA-356 file hashing
- Trusted baseline creation
- Recursive directory scanning
- Modified-file detection
- Added-file detection
- Detection of unchanged files
- Security event logging
- Timestamped log entries
- Separate baselines for different monitored foldes
- Command-line interface
- Basic input validation and error handling

********** Technologies ************

- Python
- SHA-256
- JSON
- File system operations
- Git/ GitHub

************ Cybersecurity Concepts Practiced ********

This project provides hands-on practice with several fundamental cybersecurity concepts:

- File Integrity Monitoring (FIM)
- Cryptographic hashing
- SHA-256
- Trusted baselines
- Change detection
- Security event logging
- File and directory monitoring
- Baseic security monitoring
- Defensive programming
- Command-line tools

************  Project Status **************

Current version: Initial CLI-based FIM

The current version focuses on understanding the core mechanics of File Integrity Monitoring before adding more advanced functionality.

The project will be developed progressively, with future versions potentially introducing:

- Improved configuration management
- Real-time file monitoring
- Database storage
- Flask Backend/API
- Web-based dashboard
- User authentication and authorization
- Security hardening
- SOC/SIEM integration
- More detailed security event analysis

********** Learning Approach ***********

Rather than starting directly with a large cybersecurity framework or web application, this project is being developed incrementally. 

Each stage introduces a new concept and builds on the previous one. This makes it possible to understand both implementation and the cybersecurity reasoning behing the tool. 

*********** Disclaimer **********

This project is intended for educational and defensive cybersecurity purposes. It should be tested only on systems and files that you are authorized to monitor. 

