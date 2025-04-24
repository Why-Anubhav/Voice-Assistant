from flask import Flask, render_template, request, jsonify
import datetime
import wikipedia
import webbrowser
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

app = Flask(__name__)


genai.configure(api_key="AIzaSyBClFvE7tLXzzm6ItZ0qLXeaMqdvjl2vmI")  # Replace with your API key
model = genai.GenerativeModel("gemini-1.5-flash")


sites = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
    "linkedin": "https://www.linkedin.com",
    "wikipedia": "https://www.wikipedia.org",
    "spotify": "https://www.spotify.com",
    "netflix": "https://www.netflix.com",
    "whatsapp": "https://web.whatsapp.com"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process_command():
    data = request.json
    action = data["action"]
    query = data["query"].lower()
    response_text = ""

    try:
        if action == "gemini":
            response = model.generate_content(query + " in 3 lines")
            response_text = response.text.strip()

        elif action == "wikipedia":
            response_text = wikipedia.summary(query, sentences=1)

        elif action == "play":
            search_query = '+'.join(query.split())
            yt_url = f"https://www.youtube.com/results?search_query={search_query}"
            res = requests.get(yt_url)
            soup = BeautifulSoup(res.text, "html.parser")
            video = soup.find("a", {"id": "video-title"})
            if video:
                video_url = f"https://www.youtube.com{video['href']}"
                webbrowser.open(video_url)
                response_text = f"Playing: {video_url}"
            else:
                response_text = "No video found."

        elif action == "time":
            now = datetime.datetime.now().strftime("%H hour %M minutes %S seconds")
            response_text = f"The current time is {now}"

        elif action == "site":
            matched = False
            for name, url in sites.items():
                if name in query:
                    webbrowser.open(url)
                    response_text = f"Opening {name}"
                    matched = True
                    break
            if not matched:
                response_text = "Site not found."

        else:
            response_text = "Unknown action."

    except Exception as e:
        response_text = f"Error occurred: {str(e)}"

    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)
