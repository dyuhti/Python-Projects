import os
import sqlite3
from cryptography.fernet import Fernet
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
from datetime import datetime

# Database setup
DB_NAME = "secure_file_system.db"
if not os.path.exists(DB_NAME):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password_hash TEXT,
        encryption_key TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE logs (
        id INTEGER PRIMARY KEY,
        username TEXT,
        action TEXT,
        file_path TEXT,
        timestamp TEXT
    )
    """)
    conn.commit()
    conn.close()

# Helper functions
def hash_password(password: str) -> str:
    return Fernet.generate_key().decode()

def get_encryption_key(username: str) -> bytes:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT encryption_key FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0].encode() if result else None

def log_action(username: str, action: str, file_path: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO logs (username, action, file_path, timestamp) VALUES (?, ?, ?, ?)",
                   (username, action, file_path, timestamp))
    conn.commit()
    conn.close()

def encrypt_file(file_path: str, key: bytes):
    with open(file_path, 'rb') as file:
        data = file.read()
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data)
    encrypted_file = file_path + ".enc"
    with open(encrypted_file, 'wb') as file:
        file.write(encrypted_data)
    os.remove(file_path)
    return encrypted_file

def decrypt_file(file_path: str, key: bytes):
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data)
    original_file = file_path.replace(".enc", "")
    with open(original_file, 'wb') as file:
        file.write(decrypted_data)
    os.remove(file_path)
    return original_file

# GUI Setup
class FileSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password-Protected File System")

        self.username_label = Label(root, text="Username:")
        self.username_label.grid(row=0, column=0)
        self.username_entry = Entry(root)
        self.username_entry.grid(row=0, column=1)

        self.password_label = Label(root, text="Password:")
        self.password_label.grid(row=1, column=0)
        self.password_entry = Entry(root, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = Button(root, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0)

        self.register_button = Button(root, text="Register", command=self.register)
        self.register_button.grid(row=2, column=1)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        encryption_key = get_encryption_key(username)
        if encryption_key:
            self.root.destroy()
            main_app = Tk()
            MainApp(main_app, username, encryption_key)
            main_app.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        encryption_key = Fernet.generate_key().decode()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password_hash, encryption_key) VALUES (?, ?, ?)",
                           (username, hash_password(password), encryption_key))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        finally:
            conn.close()

class MainApp:
    def __init__(self, root, username, key):
        self.root = root
        self.root.title(f"Welcome, {username}")
        self.username = username
        self.key = key

        self.encrypt_button = Button(root, text="Encrypt File", command=self.encrypt_file)
        self.encrypt_button.grid(row=0, column=0, padx=10, pady=10)

        self.decrypt_button = Button(root, text="Decrypt File", command=self.decrypt_file)
        self.decrypt_button.grid(row=0, column=1, padx=10, pady=10)

        self.logs_button = Button(root, text="View Logs", command=self.view_logs)
        self.logs_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def encrypt_file(self):
        file_path = filedialog.askopenfilename(title="Select a File to Encrypt")
        if file_path:
            encrypted_file = encrypt_file(file_path, self.key)
            log_action(self.username, "Encrypt", encrypted_file)
            messagebox.showinfo("Success", f"File encrypted successfully: {encrypted_file}")

    def decrypt_file(self):
        file_path = filedialog.askopenfilename(title="Select an Encrypted File")
        if file_path and file_path.endswith(".enc"):
            decrypted_file = decrypt_file(file_path, self.key)
            log_action(self.username, "Decrypt", decrypted_file)
            messagebox.showinfo("Success", f"File decrypted successfully: {decrypted_file}")
        else:
            messagebox.showwarning("Warning", "Please select a valid encrypted file")

    def view_logs(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT action, file_path, timestamp FROM logs WHERE username = ?", (self.username,))
        logs = cursor.fetchall()
        conn.close()
        log_window = Tk()
        log_window.title("Access Logs")
        Label(log_window, text="Action\t\tFile\t\tTimestamp").pack()
        for log in logs:
            Label(log_window, text=f"{log[0]}\t{log[1]}\t{log[2]}").pack()

# Main program
if __name__ == "__main__":
    root = Tk()
    FileSystemApp(root)
    root.mainloop()
