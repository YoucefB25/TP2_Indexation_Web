1) Structure globale du code : 

Le code s'organise de la manière suivante : 

Le dossier "data" contient le fichier jsonl donné en entrée (products.jsonl), ainsi que les quatre index produits en sortie : title_index, description_index, feature_index et review_index.

Le fichier utils.py contient les fonctions génériques utilisées pour extraire les données du jsonl et pour produire les json de sortie. 

Le fichier indexer.py contient nos trois principales classes d'index (ProductIndexer, FeatureIndexer et ReviewIndexer) et leurs fonctions encapsulées. 

Enfin le fichier main.py constitue le point d'entrée pour exécuter le code et obtenir les sorties, qui s'enregistrent automatiquement dans le dossier "data".

Pour exécuter le code, il suffit d'entrer dans un terminal "python3 main.py", après s'être positionné dans le dossier "Indexation_Web_TP2_YoucefBoulfrad". 

2) Description des classes et de leurs fonctionalités 

2.a) Index pour le filtrage des documents (classe ProductIndexer) : 

Pour filtrer les documents et pouvoir (plus tard) effectuer une recherche sur eux, deux index inversés sont créés, un index sur les titres et un index sur la description. 

Ceci permettra une priorisation dans la recherche : un résultat où le token apparait dans le titre aura probablement plus de poids qu'un résultat où ce token n'apparait que dans la description.

Les deux sont des index inversés : le token constitue la clé, et les documents où il est dans le titre (pour le premier index) et ceux où il est dans la description (pour le deuxième index) constituent la valeur. Il s'agit donc de deux dictionnaires clé-valeur. 

Vous pouvez les ouvrir et les consulter (title_index.json et description_index.json).

Pour les deux fichiers json, pour chaque token, il y a les ID des documents où il apparait (dans le titre ou dans la description) ainsi que la position où il apparait dans le titre ou la description du document. 

Par exemple, dans "description_index.json", le token "indulge" apparait dans le document ayant l'ID "1" à la position 0 (premier token du champ "description").

2.b) Index des reviews (classe ReviewIndexer) : 

Cette classe construit un index des reviews pour chaque document (et non-pas pour chaque variant, puisque les reviews sont identiques entre variants), à partir des informations contenues dans le jsonl dans les champs contenus dans "product_reviews", c'est à dire "id", "date", "rating" et "text". 

Le résultat (contenu dans le fichier "review_index.json") contient simplement pour chaque ID (identifiant un document), sa note moyenne, le nombnre de reviews, et la dernière note obtenue. 

Les informations textuelles (commentaires) sont ignorées. 

2.c) Index des features (classe FeatureIndexer) : 

Cette classe constuit un index des caractéristiques des documents. C'est un index inversé. 

C'est à dire que pour chaque fammille de caractértiques (par exemple "material", "purpose", "sugar content", etc ) et chaque caractéristique précise (contenue dans une famille de caractéristiques, par exemple "purpose"->"gifting") donne la liste des documents qui l'ont. 

Dans l'exemple utilisé, les documents dont l'objectif (purpose) est d'offrir un cadeau (gifting) sont les documents dont les IDs sont 25, 13 et 1. 

L'output de cette classe est bien évidemment le fichier "feature_index.json". 
