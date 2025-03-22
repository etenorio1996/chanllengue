# Promgram Libraries
from flask import request, Flask
from datetime import datetime
import os

app = Flask("api")
os.makedirs("uploads", exist_ok=True)
app.route("upload", methods=["POST"])


def load_process():
    csv = request.files["file"]
    ruta_destino = os.path.join("uploads", csv.name)
    csv.save(ruta_destino)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)