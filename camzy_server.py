from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess, json, os

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        video_id = self.path.strip("/")
        
        # Try multiple format options
        formats = [
            "best[ext=mp4]",
            "best",
            "bestvideo[ext=mp4]+bestaudio/best",
            "worstvideo+worstaudio/worst",
        ]
        
        url = ""
        for fmt in formats:
            result = subprocess.run(
                ["yt-dlp", "-g", "--format", fmt, 
                 "--no-check-certificate",
                 "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                 "https://www.youtube.com/watch?v=" + video_id],
                capture_output=True, text=True, timeout=30
            )
            url = result.stdout.strip().split("\n")[0]
            if url:
                break
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"url": url}).encode())
        print("Served: " + video_id + " -> " + url[:80])

port = int(os.environ.get("PORT", 8888))
print(f"Starting server on port {port}")
HTTPServer(("0.0.0.0", port), Handler).serve_forever()
