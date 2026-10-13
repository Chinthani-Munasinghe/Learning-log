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
        "https://models.inference.ai.azure.com/chat/completions",
        data=json.dumps({
            "model": "gpt-4o-mini",
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
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read().decode()
    print("RESPONSE:", body[:500])
    text = json.loads(body)["choices"][0]["message"]["content"]
except urllib.error.HTTPError as e:
    detail = e.read().decode()[:300]
    print("HTTP ERROR:", e.code, detail)
    text = f"Study topic for today: {topic}.\n\n(AI generation skipped: HTTP {e.code})"
except Exception as e:
    text = f"Study topic for today: {topic}.\n\n(AI generation skipped: {e})"

os.makedirs("notes", exist_ok=True)
with open(f"notes/{date}.md", "w", encoding="utf-8") as f:
    f.write(f"# {topic} ({date})\n\n{text}\n")
