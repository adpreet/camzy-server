import subprocess
subprocess.run(["pip", "install", "--upgrade", "yt-dlp"], capture_output=True)

from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os
# rest of your code...

from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess, json, os

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        video_id = self.path.strip("/")
        
        # Try different clients
        clients = ["android", "tv_embedded", "ios", "web"]
        url = ""
        
        for client in clients:
            result = subprocess.run(
                [
                    "yt-dlp",
                    "-g",
                    "--format", "best[ext=mp4]/best",
                    "--extractor-args", f"youtube:player_client={client}",
                    "--no-check-certificate",
                    "https://www.youtube.com/watch?v=" + video_id
                ],
                capture_output=True, text=True, timeout=30
            )
            url = result.stdout.strip().split("\n")[0]
            if url:
                print(f"Success with client: {client}")
                break
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"url": url}).encode())
        print(f"Served: {video_id} -> {url[:80] if url else 'EMPTY'}")
    
    def log_message(self, format, *args):
        pass

port = int(os.environ.get("PORT", 8888))
print(f"Starting server on port {port}")
HTTPServer(("0.0.0.0", port), Handler).serve_forever()
