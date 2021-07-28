from waitress import serve
import app
serve(app.app, listen='*:8080')