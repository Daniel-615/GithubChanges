from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    if not data:
        return "No JSON recibido", 400

    if 'head_commit' in data:
        repo_name = data['repository']['name']
        pusher = data['pusher']['name']
        commit_msg = data['head_commit']['message']
        commit_url = data['head_commit']['url']

        print(f"Push detectado en el repo '{repo_name}' por '{pusher}'")
        print(f"Mensaje del commit: {commit_msg}")

        # 🎨 Embed para mostrarlo como tarjeta
        embed = {
            "title": f"Nuevo Push en {repo_name}",
            "description": f"**Mensaje del Commit:** {commit_msg}",
            "url": commit_url,
            "color": 0x7289DA,  # azul tipo Discord
            "fields": [
                {
                    "name": "👤 Autor",
                    "value": pusher,
                    "inline": True
                },
                {
                    "name": "🔗 Enlace al Commit",
                    "value": f"[Ver Commit]({commit_url})",
                    "inline": False
                }
            ],
            "footer": {
                "text": "GitHub Notifier",
                "icon_url": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
            }
        }

        requests.post(DISCORD_WEBHOOK_URL, json={"embeds": [embed]})

    else:
        print("Otro evento recibido, no es un push.")

    return jsonify({"status": "OK"}), 200
