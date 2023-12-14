from flask import Flask, render_template, request, send_file
from pytube import YouTube
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    format = request.form.get('format')

    if not url or not format:
        return render_template('error.html', message='Please fill in all fields!')

    try:
        yt = YouTube(url)
        
        if format == 'mp4':
            video = yt.streams.get_highest_resolution()
            file_stream = io.BytesIO()
            video.stream_to_buffer(file_stream)
            file_stream.seek(0)
        elif format == 'mp3':
            mp3_stream = yt.streams.get_audio_only()
            file_stream = io.BytesIO()
            mp3_stream.stream_to_buffer(file_stream)
            file_stream.seek(0)

        return send_file(file_stream, as_attachment=True, download_name=f'{yt.title}.{format}')
    
    except Exception as e:
        return render_template('error.html', message=f'Error: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True)
