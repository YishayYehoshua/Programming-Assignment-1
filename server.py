import socket
import threading
import os
import mimetypes

# הגדרת תצורת הרשת
HOST = '127.0.0.1'
PORT = 8080
BUFFER_SIZE = 1024

# נתיב תיקיית השורש של הקבצים הסטטיים
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

# רשימת תת-התיקיות המורשות לגישה (הגישה ל-secret חסומה)
ALLOWED_DIRECTORIES = ['public', 'docs']

def parse_http_request(raw_request):
    """
    מפענחת את שורת הבקשה (Request Line) מתוך טקסט הבקשה הגולמי.
    מחלצת את ה-Method, הנתיב המבוקש (Path) וגרסת הפרוטוקול.
    """
    lines = raw_request.split("\r\n")
    if not lines or len(lines[0].split()) != 3:
        return None, None, None
        
    request_line = lines[0]
    method, path, version = request_line.split()
    return method, path, version

def build_response(status_code, reason_phrase, content_type="text/plain", body=b""):
    """
    בונה תגובת HTTP/1.0 תקינה:
    Status Line, Headers (Content-Type, Content-Length), שורה ריקה (\r\n), ו-Body.
    """
    headers = [
        f"HTTP/1.0 {status_code} {reason_phrase}",
        f"Content-Type: {content_type}",
        f"Content-Length: {len(body)}",
        "Connection: close"
    ]
    # הרכבת הכותרות והפרדה על ידי שורה ריקה
    header_bytes = ("\r\n".join(headers) + "\r\n\r\n").encode('utf-8')
    return header_bytes + body

def handle_client(client_socket, client_address):
    """
    מטפלת בחיבור של לקוח בודד בתוך תהליכון:
    קריאת הזרם עד \r\n\r\n, פענוח הבקשה, אכיפת אבטחה, והחזרת הקובץ הסטטי המבוקש.
    """
    request_data = b""
    
    try:
        # אגירת בתים עד לאיתור רצף סיום כותרות הבקשה
        while True:
            chunk = client_socket.recv(BUFFER_SIZE)
            if not chunk:
                break
            request_data += chunk
            if b"\r\n\r\n" in request_data:
                break

        if not request_data:
            return

        request_text = request_data.decode('utf-8', errors='replace')
        method, path, version = parse_http_request(request_text)

        # בדיקת תקינות תחביר הבקשה (400 Bad Request)
        if not method or not path or not version:
            body = b"<h1>400 Bad Request</h1>"
            client_socket.sendall(build_response(400, "Bad Request", "text/html", body))
            return

        # בדיקת תמיכה בשיטת GET בלבד (405 Method Not Allowed)
        if method != 'GET':
            body = b"<h1>405 Method Not Allowed</h1>"
            client_socket.sendall(build_response(405, "Method Not Allowed", "text/html", body))
            return

        # מניעת התקפת Directory Traversal (חסימת שימוש ב-'..')
        if ".." in path:
            body = b"<h1>403 Forbidden: Directory Traversal Detected</h1>"
            client_socket.sendall(build_response(403, "Forbidden", "text/html", body))
            return

        # נירמול הנתיב והפניית ברירת מחדל
        clean_path = path.lstrip('/')
        if clean_path == "" or clean_path == "/":
            clean_path = "public/index.html"

        path_parts = clean_path.split('/')
        target_dir = path_parts[0] if path_parts else ""

        # חסימת גישה לתת-תיקיות שאינן מורשות (403 Forbidden)
        if target_dir not in ALLOWED_DIRECTORIES:
            body = b"<h1>403 Forbidden: Access to this directory is denied</h1>"
            client_socket.sendall(build_response(403, "Forbidden", "text/html", body))
            return

        # נתיב הקובץ המלא במערכת הקבצים
        file_path = os.path.join(BASE_DIR, clean_path)

        # בדיקה האם הקובץ קיים והאם הוא אכן קובץ ולא תיקייה (404 Not Found)
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            body = b"<h1>404 Not Found</h1>"
            client_socket.sendall(build_response(404, "Not Found", "text/html", body))
            return

        # זיהוי MIME Type של הקובץ
        content_type, _ = mimetypes.guess_type(file_path)
        if not content_type:
            content_type = "application/octet-stream"

        # קריאת תוכן הקובץ בפורמט בינארי
        with open(file_path, "rb") as file_handle:
            file_content = file_handle.read()

        # שליחת תגובה מוצלחת (200 OK)
        response = build_response(200, "OK", content_type, file_content)
        client_socket.sendall(response)

    except Exception as error:
        print(f"Error handling client {client_address}: {error}")
    finally:
        client_socket.close()

def start_server():
    """
    מאתחלת את שרת ה-TCP ומאזינה לחיבורים נכנסים במקביל.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server is listening on http://{HOST}:{PORT}...")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address)
        )
        client_thread.start()

if __name__ == "__main__":
    start_server()