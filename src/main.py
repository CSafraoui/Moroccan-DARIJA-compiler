from o_lexer import OLexer
from o_parser import OParser
from o_interpreter import Process
import sys #module pour interagir avec la ligne de commande (lire les arguments...)


def interpreteur():
    lexer = OLexer()
    parser = OParser()
    env = {}
    program = Process((), env=env)
    while True:
        try:
            text = input('>> ')
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        if text:
            tokens = lexer.tokenize(text)
            try:
                tree = parser.parse(tokens)
                program.tree = tree
                program.run()
            except TypeError as e:
                if str(e).startswith("'NoneType' object is not iterable"):
                    print("khatae f syntax")
                else:
                    print("kayna erreur !!")


def compilateur():
    lexer = OLexer()
    parser = OParser()
    with open(sys.argv[1]) as opened_file:
        #sys.argv: fct qui renvoie liste d’arguments de ligne de commande transmis à un script Python.
        # Le nom du script est toujours l’élément à l’index 0,
        # et le reste des arguments sont stockés à des indices ultérieurs.
        tokens = lexer.tokenize(opened_file.read())
        tree = parser.parse(tokens)
        program = Process(tree)
        program.run()



if __name__ == "__main__":
    #utilisé pour exécuter un certain code uniquement
    # si le fichier a été exécuté directement, et non importé.
    if len(sys.argv) == 1:
        interpreteur()
    else:
        compilateur()
