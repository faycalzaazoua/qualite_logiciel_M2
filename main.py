import requests
from config import GITHUB_TOKEN, OWNER, REPO, PR_NUMBER

# Fonction pour récupérer les informations de la PR depuis l'API GitHub
def get_pull_request(owner, repo, pr_number, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    return response.json()

# Récupérer les données de la PR
try:
    pr_data = get_pull_request(OWNER, REPO, PR_NUMBER, GITHUB_TOKEN)
    
    # Vérifier si la clé 'files' existe dans la réponse de l'API
    if 'files' in pr_data:
        files_changed = pr_data['files']
        
        # Afficher les fichiers modifiés
        print("Fichiers modifiés dans la Pull Request :")
        for file in files_changed:
            print(file['filename'])
    
    else:
        print("Aucun fichier modifié trouvé dans la Pull Request.")
        
except KeyError as e:
    print(f"Erreur : la clé 'files' n'existe pas dans la réponse de l'API : {e}")
except Exception as e:
    print(f"Une erreur s'est produite lors de la récupération de la PR : {e}")
