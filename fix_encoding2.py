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
        content = None
        # Try various encodings to read
        for enc in ['utf-8', 'cp1252', 'utf-16']:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                pass
        
        if content is not None:
            # Write back strictly as utf-8
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Ensured utf-8 for {file_path}")
