from inspect import _void
from itertools import count
from textwrap import indent
import json
from unittest import result

#todas las funciones tienen que tener self como parametro

class fundir(object):


    def __init__(self):
        self.funDir = dict()
        self.constTable = [dict(),dict(),dict(),dict(),dict()]#en orden [int,float,char,string,datafrome]
        self.programName = ""
        self.currentScope = ""
        self.currentScopeReturn = ""
        self.newScope = ""
        self.currentType = ""
        self.paramC = 0

    def addProgram(self,id):
        self.programName = id
        self.funDir["global"] = [["void",0],dict()]
        self.funDir["principal"] = [["void",0],dict()]
        self.funDir["const"] = [["void",0],dict()]
        self.funDir["temp"] = [["void",0],dict()]
        self.paraTable = dict()
        self.currentScope = "global"

    def settype(self,type):
        self.currentType = type

    def setscope(self,scope):
        self.currentScope = scope

    def setNewScope(self,scope):
        self.newScope = scope

    def setreturn(self, regresa):
        self.currentScopeReturn = regresa

    def getCurrentType(self):
        return self.currentType

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

    def agregarVariable(self, id,adr):
        if id in self.funDir[self.currentScope][1]:#ya esta el id en la tabla
            print("error the id is already being used")
        else:
            self.funDir[self.currentScope][1][id] = [self.currentType,"valor",adr]
            
   
    def agregarFunc(self, id):
        #self.currentScope = ""
        #self.currentScopeReturn = ""
        #self.currentType = "void"
        if id in self.funDir: #ya esta la func en la tabla
            print("error: la funcion ya fue declarada previamente")
        else:
            self.funDir[id] = [[self.currentScopeReturn], dict()]
            self.paraTable[self.currentScope] = []

    def getVariableType(self,name):#primero ver en local y luego en global por presedencia
        if name in self.funDir[self.currentScope][1]:
            return self.funDir[self.currentScope][1][name][0]
        elif name in self.funDir["global"][1]:
            return self.funDir["global"][1][name][0]
    
    def variableExists(self,id):
        if id in self.funDir[self.currentScope][1]:
            return True
        elif id in self.funDir["global"][1]:
            return True
        else:
            return False

    def addConst(self,tipo,val):
        if tipo == 'int':
            self.constTable[0][val] = "adress"
        elif tipo=='float':
            self.constTable[1][val] = "adress"
        elif tipo=='char':
            self.constTable[2][val] = "adress"
        elif tipo=='string':
            self.constTable[3][val] = "adress"
        elif tipo=='dataframe':
            self.constTable[4][val] = "adress"

    def returnAdr(self,id):
        if self.variableExists(id):
            if id in self.funDir[self.currentScope][1]:
                #print("esto es lo que creo que se quiere sacar:")
                #print(self.funDir[self.currentScope][1][id][2])
                return self.funDir[self.currentScope][1][id][2]
            elif id in self.funDir["global"][1]:
                return self.funDir['global'][1][id][2]
            else:
                print("error")

    def validaConst(self,tipo,val):
        if tipo == 'int':
            if val in self.constTable[0]:
                return True
        elif tipo=='float':
            if val in self.constTable[1]:
                return True
        elif tipo=='char':
            if val in self.constTable[2]:
                return True
        elif tipo=='string':
            if val in self.constTable[3]:
                return True
        elif tipo=='dataframe':
            if val in self.constTable[4]:
                return True
        else:
            return False

    def addParamT(self,paramT):
        self.paraTable[self.currentScope].append(paramT)

    #################################################
    def funcExists(self,id):
        if id in self.funDir:
            return True
        else:
            print("error: la funcion no ha sido declarada")
            return False

    def startParamC(self):
        self.paramC = 0
        #self.paraPointer = id(self.paraTable[id][0]) ##segun yo el id regresa el espacio de memoria

    def sumaParamC(self):
        self.paramC = self.paramC + 1
        #self.paraPointer = id(self.paraTable[self.currentScope][self.paramC])
    
    def validaParam(self, argumentType):
        if argumentType == self.paraTable[self.newScope][self.paramC]: ###no estoy seguro de cual es el currentScope
            return True
        else:
            print("error: el tipo de parametros esta mal")
            return False

    def getParamC(self):
        return self.paramC

    def validaSize(self):
        if self.paramC == len(self.paraTable[self.newScope])-1:
            return True
        else:
            print("El numero de parametros no es correcto")
            return False

    ########################################################

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

    def printConst(self):
        print(self.constTable)
        print("----------")
        print('int: ',end='')
        for i in self.constTable[0]:
            print(i,end=', ')
        print('')
        print('float: ',end='')
        for i in self.constTable[1]:
            print(i,end=', ')
        print('')
        print('char: ',end='')
        for i in self.constTable[2]:
            print(i,end=', ')
        print('')
        print('string: ',end='')
        for i in self.constTable[3]:
            print(i,end=', ')
        print('')
        print('dataframe: ',end='')
        for i in self.constTable[4]:
            print(i,end=', ')
        print('')
        print("----------")


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
            self.funDir[self.currentScope][0][3] = count
        else:
            self.funDir[self.currentScope][0].append(count)

    def getQuadCounter(self):
        return self.funDir[self.newScope][0][3]

    def getScope(self):
        if self.currentScope == 'global':
            return 'global'
        else:
            return 'local'

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
            print("no hay valores en la pilaO")

    def pushPilaT(self,x):
        self.pilaT.append(x)

    def popPilaT(self):
        if self.pilaT:
            return self.pilaT.pop()
        else:
            print("no hay valores en la pilaT")

    def pushPOper(self,x):
        self.POper.append(x)

    def popPOper(self):
        if self.POper:
            return self.POper.pop()
        else:
            print("no hay valores en la pila POper")

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
            print("no hay valores en la pila de saltos")
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

class MemoriaVirtual(object):



    def __init__(self):
        #rangos
        #global
        self.intG = 2500
        self.floatG = 5000
        self.charG = 7500
        self.stringG = 10000
        self.dataframeG = 12500
        #local
        self.intL = 15000
        self.floatL = 17500
        self.charL = 20000
        self.stringL = 22500
        self.dataframeL = 25000
        #temp
        self.intT = 27500
        self.floatT = 30000
        self.boolT = 32500
        #const
        self.intC = 35000
        self.floatC = 37500
        self.charC = 40000
        self.stringC = 42500

        #rangos de tipos
        #orden = [global, local, temp, const]
        self.intRango = [2500,15000,27500,3500]
        self.floatRango = [5000,17500,30000,37500]
        self.charRango = [7500,20000,-1,40000]
        self.string = [10000,22500,-1,42500]
        self.bool = [-1,-1,32500,-1]

    
    def addVar(self,tipo,scope):
        if scope == 'global':
            if tipo == 'int':
                self.intG += 1
                return self.intG-1
            elif tipo == 'float':
                self.floatG += 1
                return self.floatG - 1
            elif tipo == 'char':
                self.charG += 1
                return self.charG - 1
            elif tipo == 'string':
                self.stringG += 1
                return self.stringG - 1
        elif scope == 'local':
            if tipo == 'int':
                self.intL += 1
                return self.intL-1
            elif tipo == 'float':
                self.floatL += 1
                return self.floatL - 1
            elif tipo == 'char':
                self.charL += 1
                return self.charL - 1
            elif tipo == 'string':
                self.stringL += 1
                return self.stringL - 1
        elif scope == 'temp':
            if tipo == 'int':
                self.intT += 1
                return self.intT-1
            elif tipo == 'float':
                self.floatT += 1
                return self.floatT - 1
            elif tipo == 'bool':
                self.boolT += 1
                return self.boolT - 1
        elif scope == 'const':
            if tipo == 'int':
                self.intC += 1
                return self.intC-1
            elif tipo == 'float':
                self.floatC += 1
                return self.floatC - 1
            elif tipo == 'char':
                self.charC += 1
                return self.charC - 1
            elif tipo == 'string':
                self.stringC += 1
                return self.stringC - 1
        else:
            return -1


    def limpiaLocal(self):
        self.intL = 15000
        self.floatL = 17500
        self.charL = 20000
        self.stringL = 22500
        self.dataframeL = 25000

