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

<h3>Etape 1: Nettoyer le fichier de base</h3>

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
Nous obtenons donc des graphiques comme ceci : <br>
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
