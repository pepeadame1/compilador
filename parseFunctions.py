from inspect import _void
from itertools import count
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
        self.funDir["global"] = [["void",0],dict()]
        self.paraTable = dict()
        self.currentScope = "global"

    def settype(self,type):
        self.currentType = type

    def setscope(self,scope):
        
        self.currentScope = scope

    def setreturn(self, regresa):
        self.currentScopeReturn = regresa

    def borrar(self):#aqui se borra todo
        self.funDir = dict()

    def borrarScope(self):
        self.funDir[self.currentScope][1] = dict()

    def checarTablaScope(self):
        if self.currentScope in self.funDir:#si hay tabla de el scope actual
            print("ya existe esta tabla")
        else:#si no hay tabla para el scope actual
            self.funDir[self.currentScope] = [[self.currentScopeReturn],dict()]
            self.paraTable[self.currentScope] = []

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
            self.funDir[id] = [[self.currentScopeReturn], dict()]
            self.paraTable[self.currentScope] = []

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

    def addParamT(self,paramT):
        self.paraTable[self.currentScope].append(paramT)


    def print(self):
        #print(json.dumps(self.funDir,indent=2))
        for key, value in self.funDir.items():
            print("------------------------")
            print(key)
            print('return: ',end='')
            print(value[0])
            for i in value[1]:
                print(i,end=': ')
                print(self.funDir[key][1][i])

    def printParams(self):
        print(self.paraTable)

    def countParams(self):
        lenght = len(self.paraTable[self.currentScope])
        if len(self.funDir[self.currentScope][0])>1:
            self.funDir[self.currentScope][0][1] = lenght
        else:
            self.funDir[self.currentScope][0].append(lenght)

    def setAvail(self,avail):
        count = len(avail)
        if len(self.funDir[self.currentScope][0])>4:
            self.funDir[self.currentScope][0][4] = count
        else:
            self.funDir[self.currentScope][0].append(count)
    
    def countLocalVar(self):
        varCount = len(self.funDir[self.currentScope][1])
        if self.currentScope != "global":
            lenght = len(self.paraTable[self.currentScope])
            if len(self.funDir[self.currentScope][0])>2:
                self.funDir[self.currentScope][0][2] = varCount-lenght
            else:
                self.funDir[self.currentScope][0].append(varCount-lenght)
        elif self.currentScope == "global":
            varCount = len(self.funDir[self.currentScope][1])
            if len(self.funDir[self.currentScope][0])>2:
                self.funDir[self.currentScope][0][2] = varCount
            else:
                self.funDir[self.currentScope][0].append(varCount)

    def setQuadCounter(self,count):
        if len(self.funDir[self.currentScope][0])>3:
            self.funDir[self.currentScope][0][2] = count
        else:
            self.funDir[self.currentScope][0].append(count)

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
        '<=':{('int','int'): 'bool',('float','float'):'bool',('int','float'):'bool',('float','int'):'bool'},
        '>=':{('int','int'): 'bool',('float','float'):'bool',('int','float'):'bool',('float','int'):'bool'},
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
            print("out of values")

    def pushPilaT(self,x):
        self.pilaT.append(x)

    def popPilaT(self):
        if self.pilaT:
            return self.pilaT.pop()
        else:
            print("out of values")

    def pushPOper(self,x):
        self.POper.append(x)

    def popPOper(self):
        if self.POper:
            return self.POper.pop()
        else:
            print("out of values")

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
        if self.pSaltos:
            return self.pSaltos.pop()
        else:
            print("out of values")
    def resultCounter(self):
        return self.resultI

    def resultAdd(self):
        self.resultI = self.resultI+1

    def quadCount(self):
        return len(self.quadruplos)
    
    def fill(self,end,cont):
        self.quadruplos[end][3] = cont

    def popAvail(self):
        return self.avail.pop()

    def getAvail(self):
        return self.avail

    def print(self):
        x = 0
        for i in self.quadruplos:
            print("------------------------")
            print(x,end='| ')
            print(i[0],end=' |')
            print(i[1],end=' |')
            print(i[2],end=' |')
            print(i[3])
            x = x+1
        print("------------------------")

        #print(json.dumps(self.quadruplos,indent=2))