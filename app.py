from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    try:
        videos = os.listdir(app.config['UPLOAD_FOLDER'])
    except FileNotFoundError:
        videos = []
    return render_template('index.html', videos=videos)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        video = request.files['video']
        if video:
            filename = secure_filename(video.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            video.save(filepath)
            return redirect(url_for('index'))
    return render_template('admin.html')

# Bind to 0.0.0.0 for Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
