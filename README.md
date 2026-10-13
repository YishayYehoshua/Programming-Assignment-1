# Multi-Threaded HTTP/1.0 Web Server

A lightweight, concurrent HTTP/1.0 web server built from scratch using Python's standard low-level socket API.

## Demo Video
[Link to Demo Video] <--- **הדבק כאן את הקישור ליוטיוב/גוגל דרייב לאחר ההקלטה**

## Dependencies
This project requires strictly no external frameworks or libraries. It uses only Python's built-in modules:
- `socket` (for low-level TCP networking)
- `threading` (for concurrency)
- `os` and `mimetypes` (for file handling)

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
python3 server.py