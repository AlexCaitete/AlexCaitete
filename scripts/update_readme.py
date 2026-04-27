import os
import requests

USERNAME = "AlexCaitete"
TOKEN = os.environ.get("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Busca todos os repos públicos ordenados pelo mais recente
repos_url = f"https://api.github.com/users/{USERNAME}/repos?sort=updated&direction=desc&per_page=6"
repos = requests.get(repos_url, headers=headers).json()

lines = ["\n"]

for repo in repos:
    if repo["fork"]:  # ignora forks
        continue

    name = repo["name"]
    description = repo["description"] or "Sem descrição"
    url = repo["html_url"]
    stars = repo["stargazers_count"]

    # Busca linguagens do repo
    langs_url = f"https://api.github.com/repos/{USERNAME}/{name}/languages"
    langs = requests.get(langs_url, headers=headers).json()
    lang_list = ", ".join(langs.keys()) if langs else "—"

    lines.append(f"| [{name}]({url}) | {description} | {lang_list} | ⭐ {stars} |\n")

table = "| Projeto | Descrição | Linguagens/Ferramentas | Stars |\n"
table += "|--------|-----------|----------------------|-------|\n"
table += "".join(lines)

# Atualiza o README
with open("README.md", "r") as f:
    content = f.read()

start_tag = "<!--START_SECTION:projects-->"
end_tag = "<!--END_SECTION:projects-->"

new_section = f"{start_tag}\n{table}\n{end_tag}"
start_idx = content.index(start_tag)
end_idx = content.index(end_tag) + len(end_tag)

new_content = content[:start_idx] + new_section + content[end_idx:]

with open("README.md", "w") as f:
    f.write(new_content)

print("README atualizado com sucesso!")
