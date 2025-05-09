Voici un fichier `README.md` complet pour votre projet Job Finder :

```markdown
# 🛡️ Cyber Job Finder

Un outil de recherche d'offres d'emploi en cybersécurité, spécialement conçu pour le marché camerounais avec focus sur Douala et le télétravail.

## 🚀 Fonctionnalités

- Recherche automatique sur multiples plateformes (LinkedIn, Indeed, sites locaux)
- Ciblage des entreprises locales (MTN, Orange, banques, etc.)
- Filtrage par mots-clés et localisation
- Notification des nouveaux résultats
- Stockage des résultats au format JSON
- Architecture modulaire et conteneurisée

## 🛠 Prérequis

- Docker 20.10+
- Docker Compose 2.0+
- Clé API SERPAPI (optionnel)

## 🏗 Installation

1. Clonez le dépôt :
```bash
git clone [URL_DU_DEPOT]
cd job_finder
```

2. Configurez les variables d'environnement :
```bash
cp .env.example .env
# Editez le fichier .env avec vos paramètres
```

3. Construisez et lancez les conteneurs :
```bash
docker-compose up --build -d
```

## ⚙ Configuration

### Fichiers de configuration

- `config/keywords.json` : Mots-clés de recherche et localisations
- `config/sites.json` : Sites d'emploi et entreprises cibles

### Variables d'environnement (.env)

| Variable | Description | Valeur par défaut |
|----------|-------------|-------------------|
| `SERPAPI_KEY` | Clé API pour SerpAPI | (requis) |
| `NOTIFICATION_ENABLED` | Activer les notifications | `true` |
| `RESULTS_DIR` | Dossier de stockage des résultats | `/data/job_results` |

## 🐋 Utilisation avec Docker

**Lancer le service :**
```bash
docker-compose up -d
```

**Voir les logs :**
```bash
docker-compose logs -f
```

**Arrêter le service :**
```bash
docker-compose down
```

## 📁 Structure des fichiers

```
job_finder/
├── docker-compose.yml
├── Dockerfile
├── README.md
├── .env
├── requirements.txt
├── main.py
├── config/
│   ├── keywords.json
│   └── sites.json
├── modules/
│   ├── __init__.py
│   ├── notification.py
│   ├── search.py
│   └── storage.py
└── job_results/
    └── jobs_YYYY-MM-DD.json
```

## 🔍 Personnalisation

1. **Modifier les mots-clés** :
Editez `config/keywords.json` pour ajouter/supprimer des termes de recherche.

2. **Ajouter des sites** :
Modifiez `config/sites.json` pour inclure de nouvelles plateformes.

3. **Planification** :
Pour exécuter quotidiennement, ajoutez à crontab :
```bash
0 9 * * * cd /chemin/vers/job_finder && docker-compose run --rm job-finder
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Étapes :
1. Forkez le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some amazing feature'`)
4. Pushez (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 Licence

Distribué sous licence MIT. Voir `LICENSE` pour plus d'informations.

## ✉ Contact

Votre Nom - [@votre_twitter](https://twitter.com/votre_twitter) - votre@email.com

Lien du projet : [https://github.com/votre/repo](https://github.com/votre/repo)
```

## 🔧 Fichiers supplémentaires recommandés

1. Créez un `.env.example` :
```env
SERPAPI_KEY=votre_cle_api_ici
NOTIFICATION_ENABLED=true
RESULTS_DIR=/data/job_results
```