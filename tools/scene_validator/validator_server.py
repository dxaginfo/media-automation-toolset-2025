#!/usr/bin/env python3
"""
Web server for SceneValidator tool.

Provides a web interface for uploading and validating scene files.

Typical usage:
    python validator_server.py --port 8080
"""

import os
import argparse
import tempfile
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import json
from scene_validator import SceneValidator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ValidatorServer")

# Default configuration file
DEFAULT_CONFIG = "config.yaml"

# HTML template for the upload form
HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Scene Validator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
        h1 { color: #333; }
        form { margin: 20px 0; padding: 20px; background-color: #f5f5f5; border-radius: 5px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="file"] { padding: 5px; }
        input[type="submit"] { padding: 10px 15px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
        input[type="submit"]:hover { background-color: #45a049; }
        .info { margin: 20px 0; padding: 10px; background-color: #e7f3fe; border-left: 6px solid #2196F3; }
    </style>
</head>
<body>
    <h1>Scene Validator</h1>
    
    <div class="info">
        <p>Upload a scene file to validate it against production guidelines.</p>
        <p>Supported file formats: .ma, .mb, .blend, .c4d</p>
    </div>
    
    <form action="/upload" method="post" enctype="multipart/form-data">
        <div class="form-group">
            <label for="file">Scene File:</label>
            <input type="file" name="file" id="file" required>
        </div>
        
        <div class="form-group">
            <label for="format">Output Format:</label>
            <select name="format" id="format">
                <option value="html">HTML</option>
                <option value="json">JSON</option>
                <option value="text">Text</option>
            </select>
        </div>
        
        <input type="submit" value="Validate">
    </form>
</body>
</html>
"""

class ValidatorHandler(BaseHTTPRequestHandler):
    """HTTP request handler for validator server."""
    
    def __init__(self, *args, **kwargs):
        self.validator = SceneValidator(DEFAULT_CONFIG)
        super().__init__(*args, **kwargs)
        
    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_FORM.encode())
        else:
            self.send_error(404, "File not found")
            
    def do_POST(self):
        """Handle POST requests."""
        if self.path == "/upload":
            try:
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )
                
                # Get the uploaded file
                fileitem = form['file']
                
                if not fileitem.file:
                    self.send_error(400, "No file was uploaded")
                    return
                    
                # Get the output format
                output_format = form.getvalue("format", "html")
                
                # Save the file to a temporary location
                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    tmp.write(fileitem.file.read())
                    tmp_path = tmp.name
                    
                # Validate the file
                logger.info(f"Validating uploaded file: {fileitem.filename}")
                result = self.validator.validate(tmp_path)
                
                # Remove the temporary file
                os.unlink(tmp_path)
                
                # Generate response based on format
                if output_format == "json":
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(result.to_json().encode())
                elif output_format == "text":
                    self.send_response(200)
                    self.send_header("Content-type", "text/plain")
                    self.end_headers()
                    self.wfile.write(result.summary().encode())
                else:  # html
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(result.to_html().encode())
                    
            except Exception as e:
                logger.exception("Error processing upload")
                self.send_error(500, f"Internal server error: {str(e)}")
        else:
            self.send_error(404, "File not found")


def run_server(port=8080):
    """Run the validator web server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, ValidatorHandler)
    logger.info(f"Starting validator server on port {port}")
    print(f"Server running at http://localhost:{port}/")
    httpd.serve_forever()


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="Run a web server for scene validation.")
    parser.add_argument("--port", "-p", type=int, default=8080, help="Port to run the server on (default: 8080)")
    
    args = parser.parse_args()
    run_server(args.port)


if __name__ == "__main__":
    main()
