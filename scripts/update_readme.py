import os
import requests

USERNAME = "AlexCaitete"
TOKEN = os.environ.get("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

repos_url = f"https://api.github.com/users/{USERNAME}/repos?sort=updated&direction=desc&per_page=6"
repos = requests.get(repos_url, headers=headers).json()

cards = []
for repo in repos:
    if repo["fork"] or repo["name"] == USERNAME:
        continue
    name = repo["name"]
    card = f'<a href="https://github.com/{USERNAME}/{name}">\n  <img src="https://github-readme-stats.vercel.app/api/pin/?username={USERNAME}&repo={name}&theme=dracula&hide_border=false" />\n</a>'
    cards.append(card)

# Monta o HTML em grid de 2 colunas
rows = ""
for i in range(0, len(cards), 2):
    left = cards[i]
    right = cards[i+1] if i+1 < len(cards) else ""
    rows += f"""<tr>
<td>{left}</td>
<td>{right}</td>
</tr>\n"""

section = f"""<table>
{rows}</table>"""

with open("README.md", "r") as f:
    content = f.read()

start_tag = "<!--START_SECTION:projects-->"
end_tag = "<!--END_SECTION:projects-->"

new_section = f"{start_tag}\n{section}\n{end_tag}"
start_idx = content.index(start_tag)
end_idx = content.index(end_tag) + len(end_tag)

new_content = content[:start_idx] + new_section + content[end_idx:]

with open("README.md", "w") as f:
    f.write(new_content)

print("README atualizado com sucesso!")
