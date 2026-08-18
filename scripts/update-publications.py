"""Regenere Publications.bib depuis HAL.

Interroge l'API archives-ouvertes.fr pour l'identifiant HAL de l'auteur, puis
reecrit les entrees avec des cles mnemoniques stables (JOE24, ICML24, ...) et
un champ KEYWORDS portant la categorie, utilise pour filtrer les listes du
chapitre CV.

Toute nouvelle publication deposee sur HAL apparait ici comme cle non mappee :
ajouter une ligne dans MAP, puis relancer.

    python3 scripts/update-publications.py
"""

import re
import pathlib
import urllib.parse
import urllib.request

AUTHOR_ID = 'ammar-mian'
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT = ROOT / 'Publications.bib'

query = urllib.parse.urlencode({
    'q': f'authIdHal_s:{AUTHOR_ID}',
    'rows': 500,
    'sort': 'producedDateY_i desc',
    'wt': 'bibtex',
})
with urllib.request.urlopen(
        f'https://api.archives-ouvertes.fr/search/?{query}') as response:
    txt = response.read().decode('utf-8')
ents = re.findall(r'@(\w+)\{([^,]+),\n(.*?)\n\}\n', txt, re.S)
src = {}
for t, k, b in ents:
    fields = dict(re.findall(r'\n?  ([A-Z_]+) = \{(.*?)\},(?=\n  [A-Z_]+ = |\n$)', b + '\n', re.S))
    src[k] = (t, {a: re.sub(r'\s+', ' ', v).strip() for a, v in fields.items()})

# halkey -> (newkey, category)
MAP = [
    # --- journaux ---
    ('wang:hal-05321266',        'SP26',      'journal'),
    ('jafuno:hal-04902720',      'JSTARS25',  'journal'),
    ('mian:hal-04694905',        'SP24',      'journal'),
    ('lerda:hal-04651458',       'JOE24',     'journal'),
    ('gallet:hal-04075772',      'TGRS23',    'journal'),
    ('mian:hal-02345330',        'JSTARS20',  'journal'),
    ('bouchard:hal-02972691',    'SP20',      'journal'),
    ('mian:hal-01975924',        'TSP19',     'journal'),
    ('mian:hal-02057622',        'TGRS19',    'journal'),
    ('benabdallah:hal-02305115', 'GRSL19',    'journal'),
    # --- chapitres d'ouvrage ---
    ('mian:hal-04014783',        'CHAP22',    'chapitre'),
    ('mian:hal-03519630',        'CHAP21a',   'chapitre'),
    ('mian:hal-03519611',        'CHAP21b',   'chapitre'),
    # --- conferences d'apprentissage automatique ---
    ('bouchard:hal-04694884',    'ICML24',    'confml'),
    ('hippertferrer:hal-04249001','ECML23',   'confml'),
    # --- conferences internationales de traitement du signal ---
    ('verlynde:hal-05314112',    'IGARSS25',  'confint'),
    ('gallet:hal-04629670',      'ICASSP24',  'confint'),
    ('jafuno:hal-04770269',      'IGARSS24',  'confint'),
    ('hippertferrer:hal-03856816','EUSIPCO22', 'confint'),
    ('gallet:hal-03726277',      'IGARSS22',  'confint'),
    ('bouchard:hal-03521267',    'EUSIPCO21', 'confint'),
    ('mian:hal-02152199',        'ICASSP19',  'confint'),
    ('mian:hal-01840783',        'ICASSP18',  'confint'),
    ('mian:hal-01840793',        'EUSIPCO18', 'confint'),
    ('mian:hal-01617069',        'EUSIPCO17', 'confint'),
    # --- conferences nationales ---
    ('petellat:hal-05154984',    'RSV25',     'confnat'),
    ('lerda:hal-04234464',       'GRETSI23a', 'confnat'),
    ('jafuno:hal-04234436',      'GRETSI23b', 'confnat'),
    ('hippertferrer:hal-04228029','GRETSI23c','confnat'),
    ('gallet:hal-03726282',      'GRETSI22',  'confnat'),
    ('mian:hal-02388708',        'GRETSI19',  'confnat'),
    ('mian:hal-01617062',        'GRETSI17',  'confnat'),
    ('lerda:hal-05626565',       'JOE26',     'journal'),
    ('aristimunha:hal-05714371', 'PREP26',    'nonliste'),
    ('gallet:hal-05529546',      'EUSIPCO26a', 'confint'),
    # --- these ---
    ('mian:tel-02464840',        'THESE19',   'these'),
]

TITLE_OVERRIDE = {
    'IGARSS25': 'Effects of Class Distribution Shift in Multi-Label '
                'Classification Splits: a Study Case on BigEarthNet',
    'ICASSP24': 'Renyi Divergences Learning for Explainable Classification '
                'of SAR Image Pairs',
}

DROP = {'KEYWORDS', 'PDF', 'HAL_VERSION', 'HAL_ID', 'X_ID', 'ORGANIZATION'}
# PUBLISHER n'a de sens que pour les chapitres d'ouvrage.
KEEP_PUBLISHER = {'incollection'}
ORDER = ['AUTHOR', 'TITLE', 'JOURNAL', 'BOOKTITLE', 'SERIES', 'VOLUME',
         'NUMBER', 'PAGES', 'PUBLISHER', 'YEAR', 'MONTH', 'ADDRESS',
         'SCHOOL', 'DOI', 'URL', 'NOTE']

out = ['''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Publications.bib -- production scientifique personnelle
%%
%% Genere depuis HAL (authIdHal_s = ammar-mian), API archives-ouvertes.fr.
%% Les cles sont mnemoniques et stables : elles sont citables depuis
%% n'importe quel chapitre du memoire, p.ex. \\cite{JOE24}.
%%
%% Le champ KEYWORDS porte la categorie, utilisee pour filtrer les listes
%% dans le chapitre CV :
%%   ownpub    -- toute publication personnelle (marqueur commun)
%%   journal   -- revue internationale a comite de lecture
%%   chapitre  -- chapitre d'ouvrage
%%   confml    -- conference d'apprentissage automatique (rang A / A*)
%%   confint   -- conference internationale de traitement du signal
%%   confnat   -- conference nationale
%%   nonliste  -- citable, mais volontairement hors de la liste classee
%%   these     -- manuscrit de these
%%
%% Les entrees marquees TODO sont absentes de HAL : a completer a la main.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
''']

cats = [('journal', 'Revues internationales a comite de lecture'),
        ('chapitre', "Chapitres d'ouvrage"),
        ('confml', 'Conferences d\'apprentissage automatique'),
        ('confint', 'Conferences internationales de traitement du signal'),
        ('confnat', 'Conferences nationales'),
        ('nonliste', 'Hors liste de publications (cite ailleurs dans le CV)'),
        ('these', 'Manuscrit de these')]

by_cat = {}
for halk, newk, cat in MAP:
    by_cat.setdefault(cat, []).append((halk, newk))

for cat, label in cats:
    out.append('\n%% ' + '-' * 72)
    out.append('%% ' + label)
    out.append('%% ' + '-' * 72 + '\n')
    for halk, newk in by_cat.get(cat, []):
        t, f = src[halk]
        if t == 'unpublished':
            t = 'misc'
        lines = [f'@{t}{{{newk},']
        for name in ORDER:
            if name == 'PUBLISHER' and t not in KEEP_PUBLISHER:
                continue
            if name in f and name not in DROP:
                lines.append(f'  {name} = {{{f[name]}}},')
        if newk in TITLE_OVERRIDE:
            lines = [l for l in lines if not l.startswith('  TITLE =')]
            lines.insert(2, '  TITLE = {{%s}},' % TITLE_OVERRIDE[newk])
        if newk == 'CHAP22':
            # HAL ne renseigne pas l'editeur pour ce chapitre.
            lines.append('  PUBLISHER = {{Wiley}},')
        if newk == 'JOE26':
            lines[0] = '@article{JOE26,'
            lines = [l for l in lines if not l.startswith('  NOTE =')]
            lines.insert(3, '  JOURNAL = {{IEEE Journal of Oceanic Engineering}},')
            lines.append("  NOTE = {Accept{\\'e}, {\\`a} para{\\^i}tre},")
        if newk == 'EUSIPCO26a':
            lines[0] = '@inproceedings{EUSIPCO26a,'
            lines = [l for l in lines if not l.startswith('  NOTE =')]
            lines.insert(3, '  BOOKTITLE = {{European Signal Processing Conference (EUSIPCO)}},')
            lines.append("  NOTE = {Accept{\\'e}, {\\`a} para{\\^i}tre},")
        lines.append(f'  KEYWORDS = {{ownpub, {cat}}},')
        lines.append('}')
        out.append('\n'.join(lines) + '\n')

out.append('''
%% ----------------------------------------------------------------------------
%% Absent de HAL -- a completer (placeholders)
%% ----------------------------------------------------------------------------

%% TODO nom et lieu exacts de la conference ; deposer sur HAL puis regenerer.
@inproceedings{MEAS25,
  AUTHOR = {Benoit, Eric and Mian, Ammar},
  TITLE = {{Reproducibility related to machine learning assisted measurements}},
  BOOKTITLE = {{Measurement: Sensors}},
  VOLUME = {38},
  PAGES = {101791},
  YEAR = {2025},
  DOI = {TODO},
  URL = {TODO},
  KEYWORDS = {ownpub, confint},
}

%% TODO deposer sur HAL puis regenerer cette entree.
@inproceedings{EUSIPCO25,
  AUTHOR = {Verlynde, Matthieu and Mian, Ammar and Yan, Yajing},
  TITLE = {{Scoring Frugality for Remote Sensing Data Processing Algorithms}},
  BOOKTITLE = {{European Signal Processing Conference (EUSIPCO)}},
  PAGES = {1722--1726},
  YEAR = {2025},
  ADDRESS = {TODO},
  DOI = {TODO},
  URL = {TODO},
  KEYWORDS = {ownpub, confint},
}

%% TODO pagination et lieu ; deposer sur HAL puis regenerer cette entree.
@inproceedings{EUSIPCO26b,
  AUTHOR = {Pautrel, Thibault and Bouchard, Florent and Mian, Ammar and
            Ginolhac, Guillaume},
  TITLE = {{FedSPDnet: Geometry-Aware Federated Deep Learning with SPDnet}},
  BOOKTITLE = {{European Signal Processing Conference (EUSIPCO)}},
  YEAR = {2026},
  ADDRESS = {TODO},
  DOI = {TODO},
  URL = {TODO},
  KEYWORDS = {ownpub, confint},
}

''')

OUTPUT.write_text('\n'.join(out))
print(f'{OUTPUT.name} : {len(MAP)} entrees ecrites, {len(src)} notices HAL')
missing = set(src) - {h for h, _, _ in MAP}
if missing:
    print('Cles HAL non mappees (ajouter dans MAP) :')
    for key in sorted(missing):
        print('   ', key, '--', src[key][1].get('TITLE', '')[:70])
