import os
from flask import Flask, render_template, request, url_for, jsonify
import sys

sys.path.append(os.path.abspath('../'))
from Maze_solver import main

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['SOLVED_FOLDER'] = 'static/solved/'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def home():
    uploaded_file_url = None
    solved_file_url = None

    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            file_ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"maze.{file_ext}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(file_path)

            uploaded_file_url = url_for('static', filename=f"uploads/{filename}")

    return render_template('index.html', uploaded_file_url=uploaded_file_url, solved_file_url=solved_file_url)

@app.route('/solve_maze', methods=['POST'])
def solve_maze():
    uploaded_file_url = request.form.get('file_url')

    if not uploaded_file_url:
        return {'success': False, 'error': 'No uploaded file URL provided'}, 400

    uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(uploaded_file_url))
    solved_image_path = os.path.join(app.config['SOLVED_FOLDER'], "solved_maze.jpg") 
    try:
        os.makedirs(app.config['SOLVED_FOLDER'], exist_ok=True)

        main(uploaded_file_path, solved_image_path)

        if os.path.exists(solved_image_path):
            solved_file_url = url_for('static', filename="solved/solved_maze.jpg")
            return {'success': True, 'solved_file_url': solved_file_url}
        else:
            return {'success': False, 'error': 'Solved maze not found'}, 500
    except Exception as e:
        return {'success': False, 'error': str(e)}, 500

@app.route('/delete_maze', methods=['POST'])
def delete_maze():
    try:
        uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], "maze.jpg")
        solved_image_path = os.path.join(app.config['SOLVED_FOLDER'], "solved_maze.jpg")

        if os.path.exists(uploaded_file_path):
            os.remove(uploaded_file_path)
        if os.path.exists(solved_image_path):
            os.remove(solved_image_path)

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
