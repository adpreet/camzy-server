import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os, time

# Cache: {video_id: (url, timestamp)}
cache = {}
CACHE_DURATION = 3600  # 1 hour

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        video_id = self.path.strip("/")
        
        # Return cached URL if still valid
        if video_id in cache:
            url, timestamp = cache[video_id]
            if time.time() - timestamp < CACHE_DURATION:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"url": url}).encode())
                print(f"Cache hit: {video_id}")
                return

        clients = ["tv_embedded", "android"]
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
                capture_output=True, text=True, timeout=15
            )
            print(f"stderr: {result.stderr}")
            url = result.stdout.strip().split("\n")[0]
            if url:
                print(f"Success with client: {client}")
                cache[video_id] = (url, time.time())
                break
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"url": url}).encode())
        print(f"Served: {video_id} -> {url[:80] if url else 'EMPTY'}")
    
    def log_message(self, format, *args):
        print(format % args)

port = int(os.environ.get("PORT", 8888))
print(f"Starting server on port {port}")
HTTPServer(("0.0.0.0", port), Handler).serve_forever()