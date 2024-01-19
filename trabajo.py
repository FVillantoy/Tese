from os import popen
from graphviz import Digraph

class Automata:

    language_input = input("Ingrese el alfabeto del lenguaje (separado por comas): ")
    
    def __init__(self, lenguaje = set(language_input.split(','))):
        self.estados = set()
        self.estadoinicial = None
        self.estadosfinales = []
        self.transiciones = dict()
        self.lenguaje = lenguaje

    @staticmethod
    def epsilon():
        return ":e:"

    def estado_inicial(self, estado):
        self.estadoinicial = estado
        self.estados.add(estado)

    def estados_finales(self, estado):
        if isinstance(estado, int):
            estado = [estado]
        for s in estado:
            if s not in self.estadosfinales:
                self.estadosfinales.append(s)

    def crear_transiciones(self, estado_origen, estado_destino, inp):
        if isinstance(inp, str):
            inp = set([inp])
        self.estados.add(estado_origen)
        self.estados.add(estado_destino)
        if estado_origen in self.transiciones:
            if estado_destino in self.transiciones[estado_origen]:
                self.transiciones[estado_origen][estado_destino] = self.transiciones[estado_origen][estado_destino].union(inp)
            else:
                self.transiciones[estado_origen][estado_destino] = inp
        else:
            self.transiciones[estado_origen] = {estado_destino : inp}

    def diccionario_transiciones(self, transiciones):
        for estado_origen, estados_destino in transiciones.items():
            for estado in estados_destino:
                self.crear_transiciones(estado_origen, estado, estados_destino[estado])

    def obtener_transiciones(self, estado, key):
        if isinstance(estado, int):
            estado = [estado]
        estados_tr = set()
        for st in estado:
            if st in self.transiciones:
                for tns in self.transiciones[st]:
                    if key in self.transiciones[st][tns]:
                        estados_tr.add(tns)
        return estados_tr

    def estadosconepsilon(self, findstate):
        estados_comp = set()
        estados = set([findstate])
        while len(estados)!= 0:
            estado = estados.pop()
            estados_comp.add(estado)
            if estado in self.transiciones:
                for tns in self.transiciones[estado]:
                    if Automata.epsilon() in self.transiciones[estado][tns] and tns not in estados_comp:
                        estados.add(tns)
        return estados_comp

    def mostrar(self):
        print("estados:", self.estados)
        print("estado inicial: ", self.estadoinicial)
        print("estados finales:", self.estadosfinales)
        print("transiciones:")
        for estado_origen, estados_destino in self.transiciones.items():
            for estado in estados_destino:
                for char in estados_destino[estado]:
                    print("  ", estado_origen, "->", estado, "en '" + char + "'", end=' ')
            print()

    def nuevoautomata(self, numero_inic):
        estados_originales = {}
        for i in list(self.estados):
            estados_originales[i] = numero_inic
            numero_inic += 1
        nuevoauto = Automata(self.lenguaje)
        nuevoauto.estado_inicial(estados_originales[self.estadoinicial])
        nuevoauto.estados_finales(estados_originales[self.estadosfinales[0]])
        for estado_origen, estados_destino in self.transiciones.items():
            for estado in estados_destino:
                nuevoauto.crear_transiciones(estados_originales[estado_origen], estados_originales[estado], estados_destino[estado])
        return [nuevoauto, numero_inic]

    def to_dot(self):
        dot = Digraph(format='png')
        dot.attr(rankdir='LR')  
        dot.attr('node', shape='circle')  

        for estado_origen, estados_destino in self.transiciones.items():
            for estado_destino, chars in estados_destino.items():
                label = ', '.join(chars)
                dot.edge(str(estado_origen), str(estado_destino), label=label)

        dot.node('start', style='invis')
        dot.edge('start', str(self.estadoinicial), style='invis')

        for estado_final in self.estadosfinales:
            dot.node(str(estado_final), shape='doublecircle')

        return dot

class crearAutomata:
    
    @staticmethod
    def estructura_basica(inp):
        estado1 = 1
        estado2 = 2
        base = Automata()
        base.estado_inicial(estado1)
        base.estados_finales(estado2)
        base.crear_transiciones(1, 2, inp)
        return base

    @staticmethod
    def caso_mas(a, b):
        [a, m1] = a.nuevoautomata(2)
        [b, m2] = b.nuevoautomata(m1)
        estado1 = 1
        estado2 = m2
        mas = Automata()
        mas.estado_inicial(estado1)
        mas.estados_finales(estado2)
        mas.crear_transiciones(mas.estadoinicial, a.estadoinicial, Automata.epsilon())
        mas.crear_transiciones(mas.estadoinicial, b.estadoinicial, Automata.epsilon())
        mas.crear_transiciones(a.estadosfinales[0], mas.estadosfinales[0], Automata.epsilon())
        mas.crear_transiciones(b.estadosfinales[0], mas.estadosfinales[0], Automata.epsilon())
        mas.diccionario_transiciones(a.transiciones)
        mas.diccionario_transiciones(b.transiciones)
        return mas

    @staticmethod
    def caso_punto(a, b):
        [a, m1] = a.nuevoautomata(1)
        [b, m2] = b.nuevoautomata(m1)
        estado1 = 1
        estado2 = m2-1
        punto = Automata()
        punto.estado_inicial(estado1)
        punto.estados_finales(estado2)
        punto.crear_transiciones(a.estadosfinales[0], b.estadoinicial, Automata.epsilon())
        punto.diccionario_transiciones(a.transiciones)
        punto.diccionario_transiciones(b.transiciones)
        return punto

    @staticmethod
    def caso_estrella(a):
        [a, m1] = a.nuevoautomata(2)
        estado1 = 1
        estado2 = m1
        estrella = Automata()
        estrella.estado_inicial(estado1)
        estrella.estados_finales(estado2)
        estrella.crear_transiciones(estrella.estadoinicial, a.estadoinicial, Automata.epsilon())
        estrella.crear_transiciones(estrella.estadoinicial, estrella.estadosfinales[0], Automata.epsilon())
        estrella.crear_transiciones(a.estadosfinales[0], estrella.estadosfinales[0], Automata.epsilon())
        estrella.crear_transiciones(a.estadosfinales[0], a.estadoinicial, Automata.epsilon())
        estrella.diccionario_transiciones(a.transiciones)
        return estrella


class NFAaDFA:
    
    def __init__(self, nfa):
        self.construirDFA(nfa)


    def crearDFA(self):
        return self.dfa

    def mostrarDFA(self):
        self.dfa.mostrar()

    def construirDFA(self, nfa):
        estados_comp = dict()
        estados_eps = dict()
        contador = 1
        estado1 = nfa.estadosconepsilon(nfa.estadoinicial)
        estados_eps[nfa.estadoinicial] = estado1
        dfa = Automata(nfa.lenguaje)
        dfa.estado_inicial(contador)
        estados = [[estado1, contador]]
        estados_comp[contador] = estado1
        contador +=  1
        while len(estados) != 0:
            [estado, desde_i] = estados.pop()
            for char in dfa.lenguaje:
                estados_tr = nfa.obtener_transiciones(estado, char)
                for s in list(estados_tr)[:]:
                    if s not in estados_eps:
                        estados_eps[s] = nfa.estadosconepsilon(s)
                    estados_tr = estados_tr.union(estados_eps[s])
                if len(estados_tr) != 0:
                    if estados_tr not in estados_comp.values():
                        estados.append([estados_tr, contador])
                        estados_comp[contador] = estados_tr
                        hasta_i = contador
                        contador +=  1
                    else:
                        hasta_i = [k for k, v in estados_comp.items() if v  ==  estados_tr][0]
                    dfa.crear_transiciones(desde_i, hasta_i, char)
        for valor, estado in estados_comp.items():
            if nfa.estadosfinales[0] in estado:
                dfa.estados_finales(valor)
        self.dfa = dfa

class ExpresionRegularANFA:
    
    def __init__(self, expresion_regular):
        self.estrella = '*'
        self.mas = '+'
        self.punto = '.'
        self.parentesisInicial = '('
        self.parentesisFinal = ')'
        self.operadores = [self.mas, self.punto]
        self.expresion_regular = expresion_regular
        self.alfabeto = [chr(i) for i in range(65,91)]
        self.alfabeto.extend([chr(i) for i in range(97,123)])
        self.alfabeto.extend([chr(i) for i in range(48,58)])
        self.construirNFA()

    def crearNFA(self):
        return self.nfa

    def mostrarNFA(self):
        self.nfa.mostrar()

    def construirNFA(self):
        lenguaje = set()
        self.pila = []
        self.automata = []
        previo = "::e::"
        for char in self.expresion_regular:
            if char in self.alfabeto:
                lenguaje.add(char)
                if previo != self.punto and (previo in self.alfabeto or previo in [self.parentesisFinal,self.estrella]):
                    self.agregar_operador_en_pila(self.punto)
                self.automata.append(crearAutomata.estructura_basica(char))
            elif char  ==  self.parentesisInicial:
                if previo != self.punto and (previo in self.alfabeto or previo in [self.parentesisFinal,self.estrella]):
                    self.agregar_operador_en_pila(self.punto)
                self.pila.append(char)
            elif char  ==  self.parentesisFinal:
                if previo in self.operadores:
                    raise BaseException("Error procesando '%s' despues de '%s'" % (char, previo))
                while(1):
                    if len(self.pila) == 0:
                        raise BaseException("Error procesando '%s'. La pila esta vacia" % char)
                    o = self.pila.pop()
                    if o == self.parentesisInicial:
                        break
                    elif o in self.operadores:
                        self.procesar_operador(o)
            elif char == self.estrella:
                if previo in self.operadores or previo  == self.parentesisInicial or previo == self.estrella:
                    raise BaseException("Error procesando '%s' despues de '%s'" % (char, previo))
                self.procesar_operador(char)
            elif char in self.operadores:
                if previo in self.operadores or previo  == self.parentesisInicial:
                    raise BaseException("Error procesando '%s' despues de '%s'" % (char, previo))
                else:
                    self.agregar_operador_en_pila(char)
            else:
                raise BaseException("El simbolo '%s' no esta permitido" % char)
            previo = char
        while len(self.pila) != 0:
            op = self.pila.pop()
            self.procesar_operador(op)
        if len(self.automata) > 1:
            print (self.automata)
            raise BaseException("No se puede analizar la expresion regular")
        self.nfa = self.automata.pop()
        self.nfa.lenguaje = lenguaje

    def agregar_operador_en_pila(self, char):
        while(1):
            if len(self.pila) == 0:
                break
            top = self.pila[len(self.pila)-1]
            if top == self.parentesisInicial:
                break
            if top == char or top == self.punto:
                op = self.pila.pop()
                self.procesar_operador(op)
            else:
                break
        self.pila.append(char)

    def procesar_operador(self, operador):
        if len(self.automata) == 0:
            raise BaseException("Error procesando operador '%s'. La pila esta vacia" % operador)
        if operador == self.estrella:
            a = self.automata.pop()
            self.automata.append(crearAutomata.caso_estrella(a))
        elif operador in self.operadores:
            if len(self.automata) < 2:
                raise BaseException("Error procesando operador '%s'. Operador incorrecto" % operador)
            a = self.automata.pop()
            b = self.automata.pop()
            if operador == self.mas:
                self.automata.append(crearAutomata.caso_mas(b,a))
            elif operador == self.punto:
                self.automata.append(crearAutomata.caso_punto(b,a))
    

def main():
    inp = input("Ingrese la expresion regular: ")
    print ("Expresion Regular: ", inp)
    nfaObj = ExpresionRegularANFA(inp)
    nfa = nfaObj.crearNFA()
    dfaObj = NFAaDFA(nfa)
    dfa = dfaObj.crearDFA()
    print ("\nNFA: ")
    nfaObj.mostrarNFA()
    print ("\nDFA: ")
    dfaObj.mostrarDFA()

    nfa_dot = nfa.to_dot()
    dfa_dot = dfa.to_dot()

    nfa_dot.render('nfa', format='png', cleanup=True)
    dfa_dot.render('dfa', format='png', cleanup=True)



if __name__  ==  '__main__':
    main()

