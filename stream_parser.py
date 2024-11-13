#!/usr/bin/env python3
import os
import sys
from urllib.parse import urlparse
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.static_folder = 'static'

class StreamParser:
    def __init__(self):
        self.streams = []
        
    def add_stream(self, name, url, duration=-1):
        """Add a stream to the playlist
        Args:
            name (str): Stream name/title
            url (str): Stream URL
            duration (int): Duration in seconds, -1 for live streams
        """
        if not self._validate_url(url):
            raise ValueError(f"Invalid URL: {url}")
            
        self.streams.append({
            'name': name,
            'url': url,
            'duration': duration
        })
    
    def _validate_url(self, url):
        """Validate if the URL is properly formatted"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def generate_m3u(self, output_file='playlist.m3u'):
        """Generate M3U playlist file
        Args:
            output_file (str): Output file name
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write M3U header
            f.write('#EXTM3U\n')
            
            # Write stream entries
            for stream in self.streams:
                f.write(f'#EXTINF:{stream["duration"]},{stream["name"]}\n')
                f.write(f'{stream["url"]}\n')

# Create a global instance of StreamParser
stream_parser = StreamParser()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/add-stream', methods=['POST'])
def add_stream():
    try:
        data = request.json
        name = data.get('name')
        url = data.get('url')
        duration = data.get('duration', -1)
        
        stream_parser.add_stream(name, url, duration)
        return jsonify({'status': 'success', 'message': 'Stream added successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/generate', methods=['GET'])
def generate_playlist():
    try:
        stream_parser.generate_m3u()
        return send_file('playlist.m3u', as_attachment=True)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

def main():
    # Get port from environment variable (Replit sets this)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    main() 