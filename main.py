import requests
from config import GITHUB_TOKEN, OPENAI_API_KEY

def get_ai_comments(file_paths):
    # Appel à l'API d'IA pour obtenir des commentaires sur les fichiers spécifiés
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'file_paths': file_paths  # Liste des chemins des fichiers à analyser
    }
    response = requests.post('https://api.openai.com/v1/ai-comments', headers=headers, json=data)
    return response.json()

def get_modified_files():
    # Récupérer la liste des fichiers modifiés pour le commit en cours
    # Par exemple, en utilisant `git diff --cached --name-only --diff-filter=ACM`
