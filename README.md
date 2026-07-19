# afamind.com — site vitrine Flask

Application Flask servie par Gunicorn, déployée sur afamind.com.

## Lancement local

```bash
pip install -r requirements.txt
cp .env.example .env   # puis remplissez les valeurs
python app.py
```

## Variables d'environnement

Copiez `.env.example` en `.env` et renseignez chaque variable.

| Variable      | Obligatoire | Description |
|---------------|-------------|-------------|
| `SECRET_KEY`  | Oui         | Clé secrète Flask (sessions, flash messages) |
| `webhook`     | Oui         | URL du webhook Power Automate (formulaire de contact) |
| `BOOKINGS_URL`| Non         | URL Microsoft Bookings (page rendez-vous) |
| `FLASK_DEBUG` | Non         | `true` pour activer le mode debug (dev uniquement) |

### Générer une SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copiez la valeur générée dans votre `.env` :

```
SECRET_KEY=<valeur générée>
```

> Ne réutilisez jamais la même clé entre dev et prod, et ne la committez jamais.
