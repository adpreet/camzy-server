from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess, json, os

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        video_id = self.path.strip("/")
        result = subprocess.run(
            ["yt-dlp", "-g", "--format", "best", "https://www.youtube.com/watch?v=" + video_id],
            capture_output=True, text=True
        )
        url = result.stdout.strip()
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"url": url}).encode())
        print("Served: " + video_id + " -> " + url[:80])

port = int(os.environ.get("PORT", 8888))
print(f"Starting server on port {port}")
HTTPServer(("0.0.0.0", port), Handler).serve_forever()
