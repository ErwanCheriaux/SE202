# SE202 Dépôt Git

Bienvenue sur le gitLab de Erwan CHERIAUX !

# Step 1

Nous réalisons un compilateur écrit en Python3.4 pour du code Tiger ayant pour cible une architecture ARM.
La première étape consiste à ajouter les opérateurs binaires et de comparaisons dans la liste des tokens.
On réalise également des tests pour vérifier leurs bonnes implémentations: règle des priorités conformes.

De plus, on implémente la construction if/then/else.
Pour tester if/then/else entrez la commande:

./tiger.py -e -E"if 0 then 2 else 3"

La structure if/then/else fonctionne. Cependant, la composition if/then n'est pas géré.

L'étape 1 est validé après plusieurs tentative car le code est soumis a de nombreux tests unitaires lors du push sur le dépot git distant.

# Step 2

Il s'agit ici d'implémenter les déclaration de variables et de fonction, gérer le type INT, les commentaires et le moins unaire. Enfin, il faut veiller à ce que la sémentique soit réspecté tel que l'utilisation de variable déclaré en amont.

Expression pour tester la sémantique:

./tiger.py -bdE""

Pour gérer les commentaires, il faut passer dans un état exclus permettant d'ignorer les règles du code tiger.

# Step 3

Nous allons devoir gérer les types qui ne sont pas fixer explicitement par le programmeur, les séquences d'expression (séparé par des ';'), des affectations, du if/then et des boucles while et for.
Il faudra également pouvoir sortir d'une boucle avec le mot clé 'break'.  

Expression pour tester le typer:

./tiger.py -tbdE""

Le test 21 de l'étape 3 a été particulierement difficile à debuggé, faute d'information.

# Step 4

Dans cette étape, nous allons transformer notre code en représentation intermédiaire (IR)

Divers tests sont écrit en tiger dans le répertoires test/
Concernant le test bissextile.tiger, le résultat attendu est '1' pour une année bissextile et '0' pour une année non bissextile

Malgré une très grande confusion avec tant d'information dès les diapositives de cours, je comprends que l'on commence par ajouter des noeuds JUMP à la fin de chaque bloc qui n'en possède pas déjà.
Puis on met chacun bloque dans un dictionnaire python pour plus facilement manipulez-les blocs et les réordonner.

Je ne comprends pas pourquoi est-ce que l'affichage de mon dico à lieu 2 fois lors de l'execution de cette commande :

./tiger.py -c tests/fact_rec.tiger
