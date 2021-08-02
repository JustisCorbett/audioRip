from waitress import serve
import audiorip
serve(audiorip.app, listen='*:8080')