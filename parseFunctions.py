from inspect import _void
from textwrap import indent
import json
from unittest import result

#todas las funciones tienen que tener self como parametro

class fundir(object):


    def __init__(self):
        self.funDir = dict()
        self.programName = ""
        self.currentScope = ""
        self.currentScopeReturn = ""
        self.currentType = ""

    def addProgram(self,id):
        self.programName = id
        print(self.programName)
        self.funDir["global"] = ["void",dict()]
        self.currentScope = "global"
        self.print()

    def settype(self,type):
        self.currentType = type

    def setscope(self,scope):
        
        self.currentScope = scope

    def setreturn(self, regresa):
        self.currentScopeReturn = regresa

    def borrar(self):#aqui se borra todo
        self.funDir = dict()

    def checarTablaScope(self):
        if self.currentScope in self.funDir:#si hay tabla de el scope actual
            print("ya existe esta tabla")
        else:#si no hay tabla para el scope actual
            self.funDir[self.currentScope] = [self.currentScopeReturn,dict()]

    def agregarVariable(self, id):
        if id in self.funDir[self.currentScope][1]:#ya esta el id en la tabla
            print("error the id is already being used")
        else:
            self.funDir[self.currentScope][1][id] = [self.currentType,"valor"]

   
    def agregarFunc(self, id):
        #self.currentScope = ""
        #self.currentScopeReturn = ""
        #self.currentType = "void"
        if id in self.funDir: #ya esta la func en la tabla
            print("error the function has already been decalred")
        else:
            self.funDir[id] = [self.currentScopeReturn, dict()]
            self.print()

    def getVariableType(self,name):#primero ver en local y luego en global por presedencia
        if name in self.funDir[self.currentScope][1]:
            return self.funDir[self.currentScope][1][name][0]
        elif name in self.funDir["global"][1]:
            return self.funDir["global"][1][name][0]
    
    def vairableExists(self,id):
        if id in self.funDir[self.currentScope][1]:
            return True
        elif id in self.funDir["global"][1]:
            return True
        else:
            return False

    def print(self):
        print(json.dumps(self.funDir,indent=2))


class printTest:
    def __init__(self):
        print("test")

class quadrupleManager(object):
    
    def __init__(self):
        self.pilaO = []#operandos
        self.pilaT = []#tipo
        self.POper = []#pila de operadores
        self.avail = []#pila para los resultados temporales
        self.quadruplos = []#pila de quadruplos
        self.resultI = 0 #para tener el index de t1,t2
        self.pSaltos = []#pila de saltos

        self.cubosemantico = {'=':{('int','int'): 'int',('float','float'): 'float', ('char','char'):'char'},
        '-':{('int','int'): 'int', ('float','float'):'float',('int','float'): 'float', ('float','int'):'float'},
        '+':{('int','int'): 'int', ('float','float'): 'float', ('int','float'):'float', ('float','int'):'float'},
        '/':{('int','int'): 'float', ('float','float'): 'float', ('int','float'):'float',('float','int'):'float'},
        '*':{('int','int'): 'int', ('float','float'): 'float', ('int','float'): 'float', ('float','int'):'float'},
        '<':{('int','int'): 'bool',('float','float'):'bool',('int','float'):'bool',('float','int'):'bool'},
        '>':{('int','int'): 'bool',('float','float'):'bool',('int','float'):'bool',('float','int'):'bool'},
        '!=':{('int','int'):'bool',('float','float'):'bool',('int','float'):'bool',('float','int'):'bool',('char','char'):'bool',('string','string'):'bool'},
        '==':{('int','int'):'bool',('float','float'):'bool',('int','float'):'bool',('float','int'):'bool',('char','char'):'bool',('string','string'):'bool'},
        '&&':{('bool','bool'): 'bool'},
        '||':{('bool','bool'): 'bool'},
        '!':{('bool'):'bool'}
        }

    def verificarTiposOp(self,op,dupla):#verifica si una operacion se encuentra en el cubo semantico
        if op in self.cubosemantico:
            if dupla in self.cubosemantico[op]:
                return True
        return False

    def regresaTipoCuboSemantico(self,op,dupla):
        return self.cubosemantico[op][dupla]

    def pushPilaO(self,x):
        self.pilaO.append(x)
    
    def popPilaO(self):
        if self.pilaO:
            return self.pilaO.pop()
        else:
            print("out of shit")

    def pushPilaT(self,x):
        self.pilaT.append(x)

    def popPilaT(self):
        return self.pilaT.pop()

    def pushPOper(self,x):
        self.POper.append(x)

    def popPOper(self):
        return self.POper.pop()

    def topPOper(self):
        if self.POper:
            return self.POper[-1]

    def pushAvail(self,x):
        self.avail.append(x)

    def pushQuadruple(self,op,left,right,result):
        self.quadruplos.append([op,left,right,result])

    def pushPSaltos(self,x):
        self.pSaltos.append(x)
    
    def popPSaltos(self):
            return self.pSaltos.pop()

    def resultCounter(self):
        return self.resultI

    def resultAdd(self):
        self.resultI = self.resultI+1

    def quadCount(self):
        return self.quadruplos.__sizeof__ -1
    
    def fill(self,end,cont):
        self.quadruplos[end][3] = cont

    def print(self):
        print(json.dumps(self.quadruplos,indent=2))