import os

files = [
    r"d:\Portal\Project\static\css\style.css",
    r"d:\Portal\Project\templates\layout.html",
    r"d:\Portal\Project\templates\home.html",
    r"d:\Portal\Project\templates\profile.html",
    r"d:\Portal\Project\templates\complaint_summary.html",
    r"d:\Portal\Project\templates\complain_create.html",
    r"d:\Portal\Project\templates\details.html",
    r"d:\Portal\Project\templates\registration\login.html",
    r"d:\Portal\Project\templates\forgot_password.html",
    r"d:\Portal\Project\templates\changepassword.html",
    r"d:\Portal\Project\templates\password_reset_done.html",
    r"d:\Portal\Project\templates\password_reset_confirm.html",
    r"d:\Portal\Project\templates\password_reset_complete.html",
    r"d:\Portal\Project\templates\Privacy.html"
]

for file_path in files:
    if os.path.exists(file_path):
        try:
            # First try reading as utf-8, maybe it's already utf-8
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Read using Windows default encoding (cp1252)
            with open(file_path, 'r', encoding='cp1252') as f:
                content = f.read()
            
            # Write back as utf-8
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed encoding for {file_path}")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            
print("Encoding check complete.")
