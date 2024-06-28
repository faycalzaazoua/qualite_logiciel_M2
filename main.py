import requests
import subprocess
import openai
from config import GITHUB_TOKEN, OPENAI_API_KEY, OWNER, REPO, PR_NUMBER

# Initialisation du client OpenAI
openai.api_key = OPENAI_API_KEY

# Fonction pour extraire les informations de la PR
def get_pull_request(owner, repo, pr_number, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    return response.json()

# Fonction pour exécuter Pylint et Flake8
def run_linter(file_path):
    pylint_result = subprocess.run(['pylint', file_path], capture_output=True, text=True)
    flake8_result = subprocess.run(['flake8', file_path], capture_output=True, text=True)
    return pylint_result.stdout, flake8_result.stdout

# Fonction pour obtenir des suggestions d'IA
def get_code_review_suggestions(code):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Please review the following code and provide suggestions for improvements and comments:\n\n{code}\n\nSuggestions:",
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Extraire les données de la PR
pr_data = get_pull_request(OWNER, REPO, PR_NUMBER, GITHUB_TOKEN)
files_changed = pr_data['files']

# Analyse de chaque fichier modifié
for file in files_changed:
    file_path = file['filename']
    # Assurez-vous que le fichier local existe et est à jour
    with open(file_path, 'w') as f:
        f.write(requests.get(file['raw_url']).text)
    
    with open(file_path, 'r') as f:
        code = f.read()
    
    # Exécution des linters
    pylint_output, flake8_output = run_linter(file_path)
    print(f"Pylint Output for {file_path}:\n{pylint_output}")
    print(f"Flake8 Output for {file_path}:\n{flake8_output}")
    
    # Obtenir des suggestions d'IA
    suggestions = get_code_review_suggestions(code)
    print(f"AI Suggestions for {file_path}:\n{suggestions}")
