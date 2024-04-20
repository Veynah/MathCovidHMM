# MathCovidHMM
<h2>Projet de groupe dans le cadre du cours de mathématique appliqué à l'informatique.</h2>

<h3>
Nos consignes:<br>
<h4>sur base du modèle d'optimisation des chaines de markov à variables cachées, <br>
utilisez l'algorithme EM pour génerer des matrices de transition pour un graphe à<br>
19 sommets (communes de bxl),  en utilisant les données du fichier Json.
</h4>
</h3>

<h3>Qu'est ce que le hidden markov model ?</h3>
<img src='./img/1-hmm.png' width=70%> <br>
Un processus de Markov est un processus stochastique dans lequel la distribution de probabilité conditionnelle d'un état futur dépend uniquement de l'état actuel et, étant donné l'état actuel, il est conditionnellement indépendant du passé. Un modèle de Markov caché (HMM) est une extension dans laquelle la séquence d'états est latente et est révélée indirectement via un mécanisme probabiliste. En d'autres termes, un HMM est un processus stochastique doublement imbriqué avec une dynamique stochastique sous-jacente (par exemple, l'état de sévérité de la pandémie de COVID-19 dans une région géographique ou un état) qui, bien qu'inobservable (caché), peut être inféré par l'observation d'un autre ensemble de processus stochastiques liés (par exemple, les taux d'infection, les décès). Les HMM fournissent l'appareillage théorique nécessaire pour apprendre un modèle probabiliste à partir des données ; et en permettant à un HMM d'analyser les observations du COVID-19 dans une région, il est possible d'estimer quel état de sévérité caractérise actuellement celle-ci, et également de prédire l'évolution la plus probable de l'état de sévérité au fil du temps.

<br>

Nous avons commencé par un fichier excel relatant tous les cas d'infection en Belgique
sur une période du `01-03-2020` au `03-04-2021`.
Le fichier était pollué de données inutiles sachant que nous devions nous concentrer
sur les 19 communes de Bruxelles.<br>
Voici à quoi ressemblait le fichier excel initial:<br>
<img src='./img/2-fichierInitial.png' width=70%> <br>

<br>

<h3>Etape 1: Traitement des données</h3>

Nous avons nettoyé les données pour n'avoir que ce dont
nous avions besoin. <br>
<img src='./img/3-donneesV1.png' width=70%> <br>

<br>
Puis nous avons remplacé tous les <5 par des 2. En dessous de 5
voulait dire un nombre de cas proche de 0 donc pour ne pas trop
off set les données, nous avons choisi en dessous de la médiane.
Et avons obtenu ceci: <br>
<img src='./img/4-donnesV2.png' width=70%> <br>

Ce dernier fichier excel a ensuite été transformé en fichier Json intitulé `Covid19CleanChanged3.json`.
Celui-ci n'était pas encore complet et utilisable.
Il nous manquait encore les données des jours où il y avait 0 cas
par commune. Celles-ci n'étant pas présentent, nous avons écrit un script
pour remplir les trous. A chaque jour où une commune n'apparaîssait pas, celle-ci se voyait
ajoutée au fichier Json et attribué un nombre de cas covid de 0.
<br>

Le script utilisé est le `updateJson.py`
Ceci nous donne notre `Updated_Covid19_Data.json`:


<img src="./img/5-donneesV3.png" width="70%">

<br>

En nous basant sur plusieurs articles que nous avons lus, l'approche générale est de
standardiser les données. Nous avons donc multiplié le nombre de cas de chaque commune par 10 000
et divisé chacun de ces nombres par la population respective de celles-ci.
Voici les différentes populations: <br>
"Anderlecht": 121723

"Auderghem": 34543

"Berchem-Sainte-Agathe": 24113

"Bruxelles": 186784

"Etterbeek": 48672

"Evere": 42693

"Forest (Bruxelles-Capitale)": 56866

"Ganshoren": 25206

"Ixelles": 87517

"Jette": 52952

"Koekelberg": 22168

"Molenbeek-Saint-Jean": 97637

"Saint-Gilles": 49662

"Saint-Josse-ten-Noode": 27050

"Schaerbeek": 131892

"Uccle": 84188

"Watermael-Boitsfort": 25202

"Woluwe-Saint-Lambert": 58040

"Woluwe-Saint-Pierre": 42038

Ces chiffres ont été obtenues via : https://ibsa.brussels/chiffres/chiffres-cles-de-la-region

<br>

Grâce au script `standart.py`, nous obtenons donc un fichier Json presque utilisable intitulé:
`Standardized_Covid19_data10K.json` <br>
Nous avions aussi fait le test en prenant le nombre de cas par 100 000 mais nous obtenions des nombres 
de cas par jour trop farfelus. <br>
Nous obtenons donc des graphiques avec `GraphStandardised3.py` comme ceci : <br>
<img src="./Projet/CodeVERSION1/GraphStandard10KParCommune/COVID19_Anderlecht.png" width="25%">
<img src="./Projet/CodeVERSION1/GraphStandard10KParCommune/COVID19_Auderghem.png" width="25%">
<img src="./Projet/CodeVERSION1/GraphStandard10KParCommune/COVID19_Berchem-Sainte-Agathe.png" width="25%">
<img src="./Projet/CodeVERSION1/GraphStandard10KParCommune/COVID19_Bruxelles.png" width="25%">
<br>
<img src="./Projet/CodeVERSION1/GraphStandard10KParCommune/COVID19_Etterbeek.png" width="25%">
<img src="./Projet/CodeVERSION1/GraphStandard10KParCommune/COVID19_Evere.png" width="25%">
<img src="./Projet/CodeVERSION1/GraphStandard10KParCommune/COVID19_Forest_(Bruxelles-Capitale).png" width="25%">
<img src="./Projet/CodeVERSION1/GraphStandard10KParCommune/COVID19_Ganshoren.png" width="25%">
<br>
<img src="./Projet/CodeVERSION1/GraphStandard10KParCommune/COVID19_Ixelles.png" width="25%">
<img src="./Projet/CodeVERSION1/GraphStandard10KParCommune/COVID19_Jette.png" width="25%">
<img src="./Projet/CodeVERSION1/GraphStandard10KParCommune/COVID19_Koekelberg.png" width="25%">
<img src="./Projet/CodeVERSION1/GraphStandard10KParCommune/COVID19_Molenbeek-Saint-Jean.png" width="25%">
<br>
<img src="./Projet/CodeVERSION1/GraphStandard10KParCommune/COVID19_Saint-Gilles.png" width="25%">
<img src="./Projet/CodeVERSION1/GraphStandard10KParCommune/COVID19_Saint-Josse-ten-Noode.png" width="25%">
<img src="./Projet/CodeVERSION1/GraphStandard10KParCommune/COVID19_Schaerbeek.png" width="25%">
<img src="./Projet/CodeVERSION1/GraphStandard10KParCommune/COVID19_Uccle.png" width="25%">
<br>
<img src="./Projet/CodeVERSION1/GraphStandard10KParCommune/COVID19_Watermael-Boitsfort.png" width="25%">
<img src="./Projet/CodeVERSION1/GraphStandard10KParCommune/COVID19_Woluwe-Saint-Lambert.png" width="25%">
<img src="./Projet/CodeVERSION1/GraphStandard10KParCommune/COVID19_Woluwe-Saint-Pierre.png" width="25%">

<br>

Une fois les données standardisée, nous devons encore les traiter un peu pour pouvoir les utiliser.
L'algorithme de Hampel, souvent utilisé dans le cadre du filtrage Hampel pour la suppression des valeurs aberrantes (ou "outliers"), est une technique robuste pour identifier et traiter les points anormaux dans des séries de données. Voici une explication simple et détaillée de cet algorithme :

### Fonctionnement de base
1. **Fenêtre glissante** : L'algorithme parcourt les données à l'aide d'une fenêtre glissante de taille configurable. Cela signifie qu'à chaque étape, il considère un sous-ensemble des données autour d'un point central. La taille de cette fenêtre détermine combien de points de données sont pris en compte à chaque étape.

2. **Calcul de la médiane et de l'écart-type robuste** : À l'intérieur de chaque fenêtre, l'algorithme calcule la médiane des données. La médiane est moins sensible aux valeurs extrêmes que la moyenne, ce qui la rend plus robuste. Ensuite, il calcule également une version robustifiée de l'écart-type, qui est une mesure de la dispersion des données autour de la médiane.

3. **Détection des outliers** : Pour chaque point de données dans la fenêtre, l'algorithme vérifie si ce point s'écarte de manière significative de la médiane par rapport à l'écart-type robustifié. Un point est généralement considéré comme aberrant si sa valeur dépasse la médiane de plus d'un certain multiple de l'écart-type robustifié (souvent autour de 2,5 à 3 fois).

4. **Remplacement des outliers** : Si un point est identifié comme un outlier, il est remplacé par la médiane de la fenêtre. Cette méthode de remplacement assure que les données restent lisses et moins affectées par des erreurs sporadiques ou des anomalies.

### Pourquoi utiliser le filtrage Hampel ?
- **Robustesse** : Le filtrage Hampel est particulièrement robuste contre les valeurs aberrantes car il n'utilise pas la moyenne, qui peut être fortement influencée par des valeurs extrêmes.
- **Adaptabilité** : La taille de la fenêtre et le multiple de l'écart-type peuvent être ajustés en fonction de la spécificité des données et du degré de sensibilité aux outliers souhaité.

### Applications typiques
- **Traitement de données temporelles** : Très utilisé pour lisser les séries temporelles où les valeurs aberrantes peuvent fausser les tendances et les analyses, comme les données de trafic, les relevés météorologiques, ou ici, les données liées au COVID-19.
- **Suppression du bruit dans les capteurs ou les mesures** : Idéal pour corriger les erreurs de mesure dans les données capturées par des capteurs.

En résumé, l'algorithme de Hampel est une méthode puissante et flexible pour nettoyer les ensembles de données, en assurant que les résultats des analyses soient fiables et non biaisés par des données anormales. Cela le rend extrêmement utile dans une multitude de contextes où la précision des données est cruciale.

Nous avons fait des tests en changeant de fenêtre, de 7 jours à 28 et au début nous étions partis sur les données prodiguées par la 
fenêtre de 7 jours, mais celle-ci laissait trop de bruits. <br>
`hampel2.py` permet de comparer les différentes fenêtres, les graphiques sont disponibles ici: <br>
<a href="https://github.com/Veynah/MathCovidHMM/tree/main/Projet/CodeVERSION1/GraphHampel2TestWindowSigma3" target="_blank">Graphiques de comparaison de fenêtres</a>

