import requests

base_url = "https://api.mangadex.org"

title = "Kanojyo to Himitsu to Koimoyou"
r = requests.get(
    f"{base_url}/manga",
    params={"title": title}
)
print([manga["id"] for manga in r.json()["data"]])