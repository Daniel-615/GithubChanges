from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    if not data:
        return "No JSON recibido", 400

    if 'commits' in data and data['commits']:
        repo_name = data['repository']['name']
        avatar_url = data['sender']['avatar_url']
        commits = data['commits']

        embeds = []

        for commit in commits:
            pusher = commit['author']['name']
            commit_msg = commit['message']
            commit_url = commit['url']

            embed = {
                "title": f"Nuevo Commit en {repo_name}",
                "description": f"**Mensaje del Commit:** {commit_msg}",
                "url": commit_url,
                "color": 0x7289DA,
                "fields": [
                    {
                        "name": "Enlace al Commit",
                        "value": f"[Ver Commit]({commit_url})",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": f"{pusher} en GitHub",
                    "icon_url": avatar_url
                }
            }

            embeds.append(embed)

        # Discord solo permite hasta 10 embeds por mensaje
        for i in range(0, len(embeds), 10):
            requests.post(DISCORD_WEBHOOK_URL, json={"embeds": embeds[i:i+10]})

    else:
        print("Evento recibido, pero no hay commits.")
        return jsonify({"message": "No commits found"}), 200

    return jsonify({"status": "OK"}), 200
