"""Run: python app.py ; open http://localhost:8001"""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import json
from urllib.parse import urlparse, parse_qs
from simulation import simulate, confirm_correction

ROOT = Path(__file__).resolve().parent
class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ('/api/simulate', '/api/correct'):
            example = parse_qs(parsed.query).get('example', ['climate'])[0]
            try:
                payload = simulate(example) if parsed.path.endswith('simulate') else confirm_correction(example)
                status = 200
            except ValueError as error:
                payload, status = {'error': str(error)}, 400
            body = json.dumps(payload, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()
if __name__ == '__main__':
    print('Simulation at http://localhost:8001')
    ThreadingHTTPServer(('localhost', 8001), Handler).serve_forever()
