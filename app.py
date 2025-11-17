from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__)
FILES_DIR = "files"

def file_size(file_path):
    size = os.path.getsize(os.path.join(FILES_DIR, file_path))
    for unit in ['B','KB','MB','GB']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"

@app.route("/")
def index():
    files = os.listdir(FILES_DIR)
    file_items = ''
    for f in files:
        file_items += f'''
        <div class="file-card">
            <div class="file-name">{f}</div>
            <div class="file-size">{file_size(f)}</div>
            <a class="download-btn" href="/files/{f}" download>Download</a>
        </div>
        '''
    return render_template_string(f'''
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>ファイル配布</title>
<style>
body {{
    font-family: Arial, sans-serif;
    background: #f0f2f5;
    margin: 0; padding: 20px;
}}
h1 {{ text-align: center; }}
.file-card {{
    background: #fff;
    border-radius: 8px;
    padding: 15px;
    margin: 10px auto;
    max-width: 400px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}}
.file-name {{ font-weight: bold; }}
.download-btn {{
    background: #007bff;
    color: #fff;
    text-decoration: none;
    padding: 5px 10px;
    border-radius: 5px;
}}
.download-btn:hover {{
    background: #0056b3;
}}
</style>
</head>
<body>
<h1>ファイル一覧</h1>
{file_items}
</body>
</html>
    ''')

@app.route("/files/<path:filename>")
def download(filename):
    return send_from_directory(FILES_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
