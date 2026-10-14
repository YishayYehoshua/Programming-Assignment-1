# Multi-Threaded HTTP/1.0 Web Server

A lightweight, concurrent HTTP/1.0 web server built from scratch using Python's standard low-level socket API.

## Dependencies
This project requires strictly no external frameworks or libraries. It uses only Python's built-in modules:
- `socket` (for low-level TCP networking)
- `threading` (for concurrency)
- `os` and `mimetypes` (for file handling)

קישור לצפייה בסרטון : https://drive.google.com/file/d/1qObOFV7L3sC_M5ifzxX-_Un64qdvQ4Nl/view?usp=sharing

## Directory Structure
.
├── server.py
├── README.md
└── static/
    ├── public/
    │   ├── index.html
    │   ├── style.css
    │   └── about.html
    ├── docs/
    │   └── readme.txt
    └── secret/
        └── confidential.txt

## How to Run
Run the server using Python 3:
```bash
python3 server.py# Programming-Assignment-1
