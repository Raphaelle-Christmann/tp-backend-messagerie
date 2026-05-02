## Question 1 : En quoi HTTP convient-il bien à cette application ?

**Réponse :** Toutes les actions que l'on réalise dans la messagerie (créer un utilisateur, envoyer/supprimer un message, etc) sont des actions simples, avec un aspect binaire : l'action peut-être réalisée, ou non. Ceci fonctionne bien avec le modèle requête/réponse de HTTP. De plus, les codes de statut HTTP (404, 400, 201, etc) correspondent bien aux erreurs que l'on peut rencontrer dans notre messagerie. Enfin, autre point intéressant dans le cadre de la messagerie : les actions réalisées sont indépendantes, elles ne doivent pas être réalisées dans un certain ordre (d'un point de vue logique, il est certes mieux de crééer l'utilisateur avant qu'il envoie un message... mais cela ne bloque pas l'application et son fonctionnement si on fait l'inverse), ce qui là aussi marche bien avec le fonctionnement de HTTP, qui est sans état (chaque requête contient toutes les informations nécessaires, pas besoin de garder en mémoire celles d'avant).

## Question 2 : Quelles limites apparaissent si 'lon veut une vraie messagerie "vivante" ?

**Réponse :** Dans le fonctionnement actuel des choses, c'est toujours le client qui initie la communication. Donc le fonctionnement est assez limité, car c'est par exemple lui-même qui doit signalé qu'il a lu un message, et en face, l'autre utilisateur doit vérifier par lui même que son message est lu. Même si on modifie le code pour que le message soit noté comme lu à son ouverture automatiquement, ce n'est pas possible que ce soit fait en temps réel, car il doit le redemander au serveur. Donc il n'y a pas d'actualisation en direct possible, le fonctionnement est lent et alourdi pour les utilisateurs car ils doivent tout faire. Si on veut aussi savoir automatiquement qu'un nouveau message est arrivé, il est alors nécessaire de faire deux requêtes en parallèle en gardant en mémoire les informations de la requête sur le message. Ceci est possible via le polling, mais c'est lourd dès qu'un grand nombre de personnes utilisent la messagerie. La limite principale reste le fait que le serveur attend d'être contacté par l'utilisateur, il ne peut pas prendre d'intiative, et ceci freine donc beaucoup l'usage de la messagerie.

## Question 3 : Pourquoi WebSocket serait une évolution naturelle ?

**Réponse :** HTTP a le mode de fonctionnement suivant : demande du client, réponse du serveur, fermeture de la connexion ; et le serveur ne "prend pas d'initiatives". Avec WebSocket, la connexion est ouverte en permanence, et le servuer peut envoyer des données au client n'importe quand. Donc dans notre cas, si un utilisateur envoie un message, le receveur peut être notifié instantanément, et quand il lit le message, l'expéditeur est notifié lui aussi instantanément. Ceci permet de résoudre ce problème d'instantanéité, et permet à l'utilisateur d'être passif. L'évolution est donc logique. Il n'y a pas besoin de modifier fondamentalement la structure de la messagerie, il suffirait de modifier le mode de communication entre utilisateurs et serveur.

## Note d'explication du projet/des choix faits :

**I. Choix de modélisation :**

Structure de la base de données : J'ai mis en place une seule base SQLite, mais avec deux tables (utilisateurs et messages) car ce sont deux entités distinctes avec des rôles différents.
Les deux clés étrangères dans message (sender_id et receiver_id) permettent de représenter la relation entre les utilisateurs et les messages sans dupliquer les données.

Séparation modèles / schémas : Les modèles définissent la structure de la base de données, alors que les schémas définissent ce que l'API expose. Ce qu'on stocke en base n'est pas forcément ce qu'on veut montrer à l'extérieur (par exemple UserCreate n'a pas d'id car c'est la base qui le génère, et MessageCreate n'a pas de sent_at ni is_read car ils sont automatiques).

Organisation du code : Deux routers séparés sont mis en place pour que chaque fichier aie un rôle clair et limité, ce qui rend le code plus facile à lire et à comprendre.
Les routes /inbox et /sent sont dans users.py car elles parlent de l'utilisateur, pas du message en lui-même.

Validation des données : EmailStr et min_length=1 garantissent que les données entrantes sont cohérentes dès l'entrée dans l'appli, ce qui évite des erreurs en base.

**II. Routes disponibles**

Utilisateurs :
- POST   /users                     : Créer un utilisateur
- GET    /users                        : Lister tous les utilisateurs
- GET    /users/{user_id}              : Récupérer un utilisateur par son id
- GET    /users/by_username/{username} : Récupérer un utilisateur par son nom
- GET    /users/{user_id}/inbox        : Boîte de réception (optionnel: ?unread_only=true)
- GET    /users/{user_id}/sent         : Messages envoyés

Messages :
- POST   /messages                     : Envoyer un message
- GET    /messages/{message_id}        : Consulter un message
- PATCH  /messages/{message_id}/read   : Marquer un message comme lu
- DELETE /messages/{message_id}        : Supprimer un message

**III. Limites de la solution HTTP**

Ceci rejoins ce qui est globalement évoqué dans la question 2 plus haut : on a surtout un problème pour rendre l'usage de la messagerie instantané. Il n'est pas possible de notifier directement les utilisateurs de nouveaux messages, etc. L'utilisateur doit toujours initier la communication avec le serveur, la connexion n'est pas permanente, et elle est coupée dès que la requête a reçu une réponse du serveur.
