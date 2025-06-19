# web_ui.py

from flask import Flask, render_template_string, request
from engine import build_game

app = Flask(__name__)
game = None


@app.route("/", methods=["GET", "POST"])
def home():
    global game
    output = []

    if request.method == "POST":
        cmd = request.form.get("command", "").strip().lower()
        if cmd == "start":
            name = request.form.get("name", "Adventurer")
            game = build_game(name)
            output = game.look()
        elif game:
            if cmd in ["n", "e", "s", "w"]:
                output = game.move(cmd)
            elif cmd == "a":
                output = game.attack()
            elif cmd == "r":
                output = game.flee()
            elif cmd == "look":
                output = game.look()
            elif cmd == "quit":
                output = ["Thanks for playing!"]
                game = None
            else:
                output = ["Unknown command."]

    return render_template_string("""
    <h1>🧱 Dungeon Crawler</h1>
    <form method="post">
        {% if not game %}
            <input name="name" placeholder="Enter your name" required>
            <button name="command" value="start">Start</button>
        {% else %}
            <input name="command" placeholder="Enter command (n/e/s/w/a/r/look/quit)">
            <button type="submit">Go</button>
        {% endif %}
    </form>
    <pre>
{{ output | join('\n') }}
    </pre>
    """,
                                  output=output,
                                  game=game)
