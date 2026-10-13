import datetime, json, os, random, urllib.request

topics = [
    "Sinhala NLP concepts",
    "speech recognition basics",
    "Python tips",
    "physical chemistry concepts",
    "analytical chemistry techniques",
    "JavaScript for web apps",
    "applied physics concepts",
]
topic = random.choice(topics)
date = datetime.date.today().isoformat()

try:
    req = urllib.request.Request(
        "https://models.github.ai/inference/chat/completions",
        data=json.dumps({
            "model": "openai/gpt-4.1-mini",
            "messages": [{
                "role": "user",
                "content": f"Write a short original study note (150 words) on: {topic}. Markdown, with one example.",
            }],
        }).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        },
    )
    text = json.load(urllib.request.urlopen(req, timeout=60))["choices"][0]["message"]["content"]
except Exception as e:
    text = f"Study topic for today: {topic}.\n\n(AI generation skipped: {e})"

os.makedirs("notes", exist_ok=True)
with open(f"notes/{date}.md", "w", encoding="utf-8") as f:
    f.write(f"# {topic} ({date})\n\n{text}\n")
