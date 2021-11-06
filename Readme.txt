Dans ce projet, on a realisé un mini langage de programmation en Darija marocaine, à l'aide du module SLY de python.
SLY est une implémentation 100% Python des outils lex et yacc couramment utilisés pour écrire des analyseurs et des compilateurs.

Le projet est composé de 4 fichier Python.
	
lexer.py: Definit l’analyseur lexicale du langage : l’alphabet, les mots reservés, les 	expressions regulières ainsi que les erreurs relatifs à l’alphabet.

parser.py: Definit l’analyseur syntaxique du langage : il definit la grammaire du langage et constitue l’arbre syntaxique abstraite.

interpreter.py: Interprete l’arbre syntaxique abstraite , effectue l’analyse semantique et gère les erreurs.

main.py: execute le code écrit en darija en mode interpreteur et compilateur. 


