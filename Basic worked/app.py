from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

def get_video_info(video_url):
    with YoutubeDL() as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        formats = info_dict.get('formats', [])
        video_options = []

        for fmt in formats:
            if 'video' in fmt['format_note']:
                video_options.append({
                    'quality': fmt['format_note'],
                    'file_size': fmt.get('filesize'),
                    'url': fmt['url']
                })

        audio_options = [{
            'quality': 'Audio (MP3)',
            'file_size': None,
            'url': info_dict['url']
        }]

        return video_options, audio_options

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        video_url = request.form['url']
        video_options, audio_options = get_video_info(video_url)

        return render_template('download.html', video_options=video_options, audio_options=audio_options)
    except Exception as e:
        print(f"Error: {e}")
        return render_template('index.html', error="Failed to fetch video information. Please try again.")

@app.route('/download/video/<path:video_url>')
def download_video(video_url):
    return redirect(video_url)

@app.route('/download/audio/<path:audio_url>')
def download_audio(audio_url):
    return redirect(audio_url)

def get_video_info(video_url):
    with YoutubeDL() as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        formats = info_dict.get('formats', [])
        video_options = []

        for fmt in formats:
            if 'video' in fmt.get('format_note', ''):
                video_options.append({
                    'quality': fmt.get('format_note', 'Unknown quality'),
                    'file_size': fmt.get('filesize', 'Not available'),
                    'url': fmt['url']
                })

        audio_options = [{
            'quality': 'Audio (MP3)',
            'file_size': None,
            'url': info_dict['url']
        }]

        return video_options, audio_options

if __name__ == '__main__':
    app.run(debug=True)
