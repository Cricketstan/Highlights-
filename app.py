from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max

# Home page - shows videos
@app.route('/')
def index():
    videos = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', videos=videos)

# Admin panel to upload videos
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        video = request.files['video']
        if video:
            filename = secure_filename(video.filename)
            video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)
