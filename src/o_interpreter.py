from random import randint
from math import sin, cos, tan, asin, acos, atan, sqrt
from o_lexer import OLexer
from o_parser import OParser




















def standard_library():
    """ Fonction qui génère un dictionnaire contenant toutes les fonctions de base """
    env = Env()
    env.update({
        'kteb': lambda val: print(val),
        '_9ra': lambda prompt: input(prompt),
        '_3chwa2i': lambda max: randint(0, max),
        'wach_3achari': lambda val: isinstance(val, float),
        'wach_sa7i7': lambda val: isinstance(val, int),
        'wach_klma': lambda val: isinstance(val, str),
        'wach_mnti9i': lambda val: isinstance(val, bool),
        '_7wl_l_3achari': lambda val: float(val),
        '_7wl_l_sa7i7': lambda val: int(val),
        '_7wl_l_klma': lambda val: str(val),
        '_7wl_l_manti9i': lambda val: bool(val),
        'tol': lambda obj: len(obj),
        'sin': lambda val: sin(val),
        'cos': lambda val: cos(val),
        'tan': lambda val: tan(val),
        'asin': lambda val: asin(val),
        'acos': lambda val: acos(val),
        'atan': lambda val: atan(val),
        'jadr': lambda val: sqrt(val),
        '_2os': lambda base, exponent: pow(base, exponent),
        'khrj': lambda val: exit(val),
    })
    return env


class Process:
    """ Le processus principal qui exécute l'arbre de syntaxe abstraite """
    def __init__(self, tree, filename="?", env={}):  # tree is the outpout of the parser
        self.tree = tree
        self.file_path = filename
        if not isinstance(env, Env):
            _env = env
            env = Env(outer=standard_library())
            env.update(_env)
        self.env = Env(outer=env)
        self.should_return = False
        self.depth = 0  # profondeur dyal l'arbre syntaxique
        self.types = {'sa7i7': int, '_3achari': float, 'klma': str, 'mnte9i': bool, 's7i7': True}
        self.rtypes = {int: 'sa7i7', float: '_3achari', str: 'klma', bool: 'mnte9i', 'ghalet': False}

    # evalue et execute chaque ligne de l'arbre syntaxique et gere les erreurs
    def run(self, tree=None, env={}):
        current_env = self.env
        result = None # au debut d'execution il y a rien à retourne
        if env != {}:
            self.env = env
        if tree is None:
            # print(tree) -> il y a pas encore d'UL ds mon arbre -> None ->debut d'execution ou fin
            for line in self.tree:
                try:
                    result = self.evaluate(line)
                except ValueError as e:
                    print(e)
                    break
                except UnboundLocalError as e:
                    print(e)
                    break
                except NameError as e:
                    print(e)
                    break
                except IndexError as e:
                    print(e)
                    break
                except TypeError as e:
                    print(e)
                    break
                if self.depth == 0:
                    # nothing to return, in case if the line evaluted does not contain a instruction
                    # like if line, or for line before go inside the block
                    self.should_return = False
                if self.should_return:
                    return result
        else:
            # print(tree) -> l'arbre syntaxique est plein, il existe une instruction dedans
            for line in tree:
                try:
                    result = self.evaluate(line)
                except ValueError as e:
                    print(e)
                    break
                except UnboundLocalError as e:
                    print(e)
                    break
                except NameError as e:
                    print(e)
                    break
                except IndexError as e:
                    print(e)
                    break
                except TypeError as e:
                    print(e)
                    break
                if self.depth == 0:
                    self.should_return = False
                if self.should_return:
                    return result
        self.env = current_env
        return result

    def evaluate(self, parsed):
        """ Évaluation d'un arbre / d'un tuple / d'une expression analysé """
        if type(parsed) != tuple:
            return parsed
        else:
            action = parsed[0]
            if action == 'dalla':  # ('dalla' (parsed[0]), p.ID(parsed[1]), ('params', p.params(parsed[2])), ('block', p.block(parsed[3])))
                params = parsed[2]  # p.params
                body = parsed[3]  # p.block
                self.env.update({parsed[1]: Function(
                    self, params[1], body, self.env)})
                return None
            elif action == 'call':  # ('call', p.ID, ('args', p.args))
                func = self.env.find(parsed[1])
                #print(type(func)) type of function is function not Function d'apres l'initialisation
                args = [self.evaluate(arg) for arg in parsed[2][1]]
                res = func(*args)
                return res

            elif action == 'rj3':  # ('rj3', p.expr)
                result = self.evaluate(parsed[1])
                self.should_return = True
                return result

            elif action == 'var_define':  # ('var_define', p.var, p.expr)
                name = parsed[1]
                if name in self.env:
                    raise NameError('man9drch n3awd n3rf had lvariable \'%s\'' % name)
                result = self.evaluate(parsed[2])
                self.env.update({name: Value(result, type(result))})
                return None


            elif action == 'var_define_no_expr':  # ('var_define_no_expr', p.var, p.var_type)
                name = parsed[1]
                if name in self.env:
                    raise NameError('man9drch n3awd n3rf had lvariable \'%s\'' % name)
                self.env.update({name: Value(None, self.types[parsed[2]])})
                return None

            elif action == 'var_assign':  # ('var_assign', p.var, p.expr)
                # ('var_assign', p.var, ('*', ('var', p.var), p.expr))
                # ('*', ('var', p.var), p.expr)==p.expr==parsed[2]
                if type(parsed[1]) is not tuple:
                    if parsed[1] not in self.env:
                        raise UnboundLocalError(
                            'mat9derch initialiser had l variable \'%s\' 7it mamkaynach' % parsed[1])
                    result = self.evaluate(parsed[2])
                    var = self.env.find(parsed[1])
                    if type(result) != var.type:
                        raise ValueError(
                            "had lvariable '{}' khas tkon '{}' blast '{}'".format(parsed[1],
                                                                                  self.rtypes[type(result)], self.rtypes[var.type]))

                    var.value = result
                    return None


            elif action == 'ila':  # ('ila', ('condition', p.expr), ('block', p.block), None)
                # ('ila', ('condition', p.expr), ('block', p.block0), ('block', p.block1))

                cond = self.evaluate(parsed[1])  # ('condition', p.expr)
                if cond:
                    return self.evaluate(parsed[2])
                if parsed[3] is not None:
                    return self.evaluate(parsed[3])
            elif action == 'ma7d':  # ('ma7d', ('condition', p.expr), ('block', p.block))
                # (p.var_assign0, ('ma7d', ('condition', p.expr), ('block', p.block + (p.var_assign1,))))
                cond = self.evaluate(parsed[1])
                while cond:
                    self.evaluate(parsed[2])
                    cond = self.evaluate(parsed[1])
            elif action == 'condition':  # ('condition', p.expr)
                return self.evaluate(parsed[1])
            elif action == 'block':  # ('block', p.block)
                return self.run(parsed[1])  # parsed[1] contient un block d'instructions 3liha derna run.
            elif action == 'var':  # ('var', p.var)
                var = self.env.find(parsed[1])
                if not isinstance(var, Value):  # not instance mli katkun parametre dyal cho fonction
                    return var
                return var.value

            elif action == '+':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if ((type(result) == int or type(result) == float) and (type(result2) == int or type(result2) == float)) or (type(result) == str or type(result) == str):
                    return result + result2
                else:
                    raise ValueError("t9dr tzid ghi l a3dad !")


            elif action == '-':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if (type(result) == int or type(result) == float) and (type(result2) == int or type(result2) == float):
                    return result - result2
                else:
                    raise ValueError("t9dr tn9s ghi l a3dad !")
            elif action == '*':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if (type(result) == int or type(result) == float) and (type(result2) == int or type(result2) == float):
                    return result * result2
                else:
                    raise ValueError("t9dr tdreb ghi l a3dad !")
            elif action == '/':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if (type(result) == int or type(result) == float) and (type(result2) == int or type(result2) == float):
                    return result / result2
                else:
                    raise ValueError("t9dr t9sm ghi l a3dad !")
            elif action == '%':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if (type(result) == int or type(result) == float) and (type(result2) == int or type(result2) == float):
                    return result % result2
                else:
                    raise ValueError("t9dr t7ssb lmodulo ghi l a3dad !")
            elif action == '==':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result == result2
            elif action == '!=':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result != result2
            elif action == '<':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if (type(result) == int or type(result) == float) and (type(result2) == int or type(result2) == float):
                    return result < result2
                else:
                    raise ValueError("t9dr t9arn ghi bin l a3dad !")
            elif action == '>':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if (type(result) == int or type(result) == float) and (type(result2) == int or type(result2) == int):
                    return result > result2
                else:
                    raise ValueError("t9dr t9arn ghi bin l a3dad !")
            elif action == '<=':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if (type(result) == int or type(result) == float) and (type(result2) == int or type(result2) == int):
                    return result <= result2
                else:
                    raise ValueError("t9dr t9arn ghi bin l a3dad !")
            elif action == '>=':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if (type(result) == int or type(result) == float) and (type(result2) == int or type(result2) == int):
                    return result >= result2
                else:
                    raise ValueError("t9dr t9arn ghi bin l a3dad !")
            elif action == 'w':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result and result2
            elif action == 'wla':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result or result2
            elif action == '!':  # ('!', p.expr)
                result = self.evaluate(parsed[1])
                if result:
                    return False
                return True
            elif action == '?:':  # ('?:', p.expr0, p.expr1, p.expr2)
                # v = 2<5 ? "ah" : "la";
                cond = self.evaluate(parsed[1])
                if cond:
                    return self.evaluate(parsed[2])
                return self.evaluate(parsed[3])
            else:  # exemple:for statment, incr decr
                if len(parsed) > 0 and type(parsed[0]) == tuple:
                    return self.run(parsed)
                return None


class Env(dict):
    """ Classe d'environnement """
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))  # zip:renvoie un itérateur à partir de plusieurs itérateurs.
        # params=[1,2,3] et args =[a,b,c] => after zip: x=[(1, a), (2,b), (3,c)]
        self.outer = outer

    def find(self, name):  # name= tokens
        if name in self:
            return self[name]
        elif self.outer is not None:
            return self.outer.find(name)
        raise UnboundLocalError("{} mam3rfch".format(name))


# analyse semantique et execution d'une fonction
class Function(object):
    """
    Object fonction
    """
    def __init__(self, process, params, body, env):
        self.process = process
        self.params = params
        self.body = body
        self.env = env
        self.type = 'function'

    def __call__(self, *args):  # *args est utilisé pour passer une liste d’arguments
        # de longueur variable.
        params = []
        for i in range(len(self.params)):
            # on s'assure du type de l'argument il faut qu'il soit du meme type que parametre
            # self.params=[('nom_param', 'type_param'), ('nom_param', 'type_param'),.....]
            if type(args[i]) != self.process.types[self.params[i][1]]:  # params[i][1]=type_param
                raise TypeError("had lparametr '{}' khas ykun {} blast {}."
                                .format(self.params[i][0], self.params[i][1], self.process.rtypes[type(args[i])]))
            params.append(self.params[i][0])  # params[i][0]=nom_param
        return self.process.run(self.body, Env(params, args, self.env))

#tout objet de notre fichier est considère comme objet de type Value
class Value(object):
    """ Class container pour les valeurs dans le langage Darija """
    # constractor
    def __init__(self, value, val_type):
        self.value = value
        self.type = val_type

    def __len__(self):
        return len(self.value)

    def __str__(self):
        return "{}: {}".format(self.value, self.type)

    # getter de la valeur
    def get(self):
        return self.value


if __name__=="__main__":
    lexer = OLexer()
    parser = OParser()
    with open("src/variables.darija") as opened_file:
        #sys.argv: fct qui renvoie liste d’arguments de ligne de commande transmis à un script Python.
        # Le nom du script est toujours l’élément à l’index 0,
        # et le reste des arguments sont stockés à des indices ultérieurs.
        tokens = lexer.tokenize(opened_file.read())
        tree = parser.parse(tokens)
        program = Process(tree)
        program.run()