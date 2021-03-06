from inspect import _void
from itertools import count
from re import M
from textwrap import indent
import json
from unittest import result

#todas las funciones tienen que tener self como parametro

class fundir(object):


    def __init__(self):
        self.funDir = dict()
        self.constTable = [dict(),dict(),dict(),dict()]#en orden [int,float,char,string]
        self.tempTable = [dict(),dict(),dict()]#en orden son [int,float,bool]
        self.programName = ""
        self.currentScope = ""
        self.currentScopeReturn = ""
        self.newScope = ""
        self.currentType = ""
        self.paramC = 0
        self.auxArrId = ""

    def addProgram(self,id):#funcion para inicializar valores
        self.programName = id
        self.funDir["global"] = [["void",0],dict()]
        self.funDir["principal"] = [["void",0],dict()]
        #self.funDir["temp"] = [["void",0],dict()]
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

    def borrarScope(self):#borra las variables de una funcion local
        self.funDir[self.currentScope][1] = dict()

    def checarTablaScope(self):#verifica si existe una tabla para es contexto
        if not self.currentScope in self.funDir:
            self.funDir[self.currentScope] = [[self.currentScopeReturn],dict()]
            self.paraTable[self.currentScope] = []

    def agregarVariable(self, id,adr):#agrega una variable al contexto actual
        if id in self.funDir[self.currentScope][1]:#ya esta el id en la tabla
            print("error: el id ya esta en uso")
        else:
            self.funDir[self.currentScope][1][id] = [self.currentType,"valor",adr, []]

    def setArreglo(self,id):#inicializa la informacion de un arreglo
        self.funDir[self.currentScope][1][id][3] = [0, 1, []] # dim, r, [lim inf, lim sup, m/k]
    
    def addLimite(self, id, limite):#agrega los limites de un arreglo
        if(int(limite) < 1):
            print("error: limite debe ser mayor a 0")
        
        else:
            self.funDir[self.currentScope][1][id][3][2].append([0, int(limite), 0])
            self.funDir[self.currentScope][1][id][3][1] = (int(limite) + 1) * self.funDir[self.currentScope][1][id][3][1]
            self.funDir[self.currentScope][1][id][3][0] = self.funDir[self.currentScope][1][id][3][0] + 1

    def arrCalc(self, id):#calcula la informacion necesaria de un arreglo
        count = self.funDir[self.currentScope][1][id][3][0]
        self.funDir[self.currentScope][1][id][3][0] = 1
        r = self.funDir[self.currentScope][1][id][3][1]
        k = 0
        size = r
        i = 0
        while i < count:
            m = r / (self.funDir[self.currentScope][1][id][3][2][i][1] + 1)
            self.funDir[self.currentScope][1][id][3][2][i][2] = m
            r = m
            k = k + self.funDir[self.currentScope][1][id][3][2][i][0] * m
        
            self.funDir[self.currentScope][1][id][3][0] = self.funDir[self.currentScope][1][id][3][0] + 1
            i = i + 1
        self.funDir[self.currentScope][1][id][3][2][i - 1][2] = k

        self.auxArrId = ""
        self.funDir[self.currentScope][1][id][2] = self.funDir[self.currentScope][1][id][2] + self.funDir[self.currentScope][1][id][3][1]

    def agregarFunc(self, id):#agrega una funcion a dirFun
        if id in self.funDir: #ya esta la func en la tabla
            print("error: la funcion ya fue declarada previamente")
        else:
            self.funDir[id] = [[self.currentScopeReturn], dict()]
            self.paraTable[self.currentScope] = []

    def getVariableType(self,name):#regresa el tipo de una variable
        if name in self.funDir[self.currentScope][1]:
            return self.funDir[self.currentScope][1][name][0]
        elif name in self.funDir["global"][1]:
            return self.funDir["global"][1][name][0]
    
    def variableExists(self,id):#valida la existencia de una variable
        if id in self.funDir[self.currentScope][1]:
            return True
        elif id in self.funDir["global"][1]:
            return True
        else:
            return False

    def addConst(self,tipo,val,adr):#agrega un valor constante
        if tipo == 'int':
            self.constTable[0][val] = adr
        elif tipo=='float':
            self.constTable[1][val] = adr
        elif tipo=='char':
            self.constTable[2][val] = adr
        elif tipo=='string':
            self.constTable[3][val] = adr

    def isConst(self,id,tipo):#valida si una constante existe
        if tipo == 'int':
            if id in self.constTable[0]:
                return True
        elif tipo=='float':
            if id in self.constTable[1]:
                return True
        elif tipo=='char':
            if id in self.constTable[2]:
                return True
        elif tipo=='string':
            if id in self.constTable[3]:
                return True
        return False

    def isTemp(self,id,tipo):#valida si una variable es temporal
        if tipo == 'int':
            if id in self.tempTable[0]:
                return True
        elif tipo=='float':
            if id in self.tempTable[1]:
                return True
        elif tipo=='bool':
            if id in self.tempTable[2]:
                return True
        return False

    def addTemp(self,tipo,val,adr):#agrega una variable temporal
        if tipo == 'int':
            self.tempTable[0][val] = adr
        elif tipo=='float':
            self.tempTable[1][val] = adr
        elif tipo=='bool':
            self.tempTable[2][val] = adr
        else:
            print("error: se trato de guardar un temp que no es int,float o bool")

    def borrarTemp(self):#borra la tabla de variables temporales
        self.tempTable = [dict(),dict(),dict()]
    
    def returnConst(self,id,tipo):#regresa un valor constante
        if tipo == 'int':
            return self.constTable[0][id]
        elif tipo=='float':
            return self.constTable[1][id]
        elif tipo=='char':
            return self.constTable[2][id]
        elif tipo=='string':
            return self.constTable[3][id]
        else:
            return -1

    def returnTemp(self,id,tipo):#regresa un valor temporal
        if tipo == 'int':
            return self.tempTable[0][id]
        elif tipo=='float':
            return self.tempTable[1][id]
        elif tipo=='bool':
            return self.tempTable[2][id]
        else:
            return -1

    def returnAdr(self,id):#regresa la direccion de memoria de una variable
        if self.variableExists(id):
            if id in self.funDir[self.currentScope][1]:
                return self.funDir[self.currentScope][1][id][2]
            elif id in self.funDir["global"][1]:
                return self.funDir['global'][1][id][2]
            else:
                print("error: no se encontro la direccion")

    def returnAdrFull(self,id,tipo):#esta funcion regresa la direccion de memoria sin importar si es global,local,temporal o constante
        if self.variableExists(id):
            print('est normal')
            return self.returnAdr(id)
        elif self.isTemp(id,tipo):
            print('es temp')
            return self.returnTemp(id,tipo)
        elif self.isConst(id,tipo):
            return self.returnConst(id,tipo)
        else:
            return -1


    def validaConst(self,tipo,val):#valida si una constante existe
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
        else:
            return False

    def addParamT(self,paramT):#va agregando los tipos de parametros de una funcion
        self.paraTable[self.currentScope].append(paramT)

    def returnParamT(self):#regresa la tabla de parametros
        return self.paraTable
    #################################################
    def funcExists(self,id):#verifica si una funcion existe
        if id in self.funDir:
            return True
        else:
            print("error: la funcion no ha sido declarada")
            return False

    def startParamC(self):#reinicia el contador de parametros
        self.paramC = 0
        

    def sumaParamC(self):#incrementa el contador de parametros
        self.paramC = self.paramC + 1
        
    
    def validaParam(self, argumentType):#valida si una variable es del mismo tipo que la variable parametrica de una funcion
        if argumentType == self.paraTable[self.newScope][self.paramC]: 
            return True
        else:
            print("error: el tipo de parametros esta mal")
            return False

    def getParamC(self):#regresa el contador de parametros
        return self.paramC

    def validaSize(self):#valida la cantidad de variables parametricas
        if self.paramC == len(self.paraTable[self.newScope])-1:
            return True
        else:
            print("El numero de parametros no es correcto")
            return False
    
    def print(self):#imprime funDir
        
        for key, value in self.funDir.items():
            print("------------------------")
            print(key)
            print('return: ',end='')
            print(value[0])
            for i in value[1]:
                print(i,end=': ')
                print(self.funDir[key][1][i])

    def printParams(self):#imprime la tabla de parametros
        print(self.paraTable)

    def printConst(self):#imprime la tabla de constantes
        print("CONST: ")
        print("----------")
        print('int: ')
        for i in self.constTable[0]:
            print(i,end=', ')
            print(self.constTable[0][i])
        print('float: ')
        for i in self.constTable[1]:
            print(i,end=': ')
            print(self.constTable[1][i])
        print('char: ')
        for i in self.constTable[2]:
            print(i,end=': ')
            print(self.constTable[2][i])
        print('string: ')
        for i in self.constTable[3]:
            print(i,end=': ')
            print(self.constTable[3][i])
        print("----------")

    def printTemp(self):#imprime la tabla de variables temporales
        print("TEMP")
        print("----------")
        print('int:')
        for i in self.tempTable[0]:
            print(i,end=', ')
            print(self.tempTable[0][i])
        print('float:')
        for i in self.tempTable[1]:
            print(i,end=': ')
            print(self.tempTable[1][i])
        print('bool:')
        for i in self.tempTable[2]:
            print(i,end=': ')
            print(self.tempTable[2][i])
        print(print("----------"))

    def countParams(self):#cuenta la cantidad de parametros de una funcion
        lenght = len(self.paraTable[self.currentScope])
        if len(self.funDir[self.currentScope][0])>1:
            self.funDir[self.currentScope][0][1] = lenght
        else:
            self.funDir[self.currentScope][0].append(lenght)

    def setAvail(self,avail):#guarda el valor de avail(temporal previo)
        count = len(avail)
        if len(self.funDir[self.currentScope][0])>4:
            self.funDir[self.currentScope][0][4] = count
        else:
            self.funDir[self.currentScope][0].append(count)
    
   
    def countLocalVar(self):#cuenta las variables/parametros de una funcion local
        int = 0
        float = 0
        char = 0
        string = 0
        dataframe = 0
        for i in self.funDir[self.currentScope][1]:
            if self.funDir[self.currentScope][1][i][0] == 'int':
                int += 1
            elif self.funDir[self.currentScope][1][i][0] == 'float':
                float += 1
            elif self.funDir[self.currentScope][1][i][0] == 'char':
                char += 1
            elif self.funDir[self.currentScope][1][i][0] == 'string':
                string += 1
            elif self.funDir[self.currentScope][1][i][0] == 'dataframe':
                dataframe += 1

        if len(self.funDir[self.currentScope][0])>2:
            print('error: el indice del arreglo esta mal')
        else:
            self.funDir[self.currentScope][0].append([int,float,char,string,dataframe])


    def setQuadCounter(self,count):#guarda el quadruplo donde inicia una funcion
        if len(self.funDir[self.currentScope][0])>3:
            self.funDir[self.currentScope][0][3] = count
        else:
            self.funDir[self.currentScope][0].append(count)

    def getQuadCounter(self):#regresa el apuntador a el quadruplo donde inicia la funcion
        return self.funDir[self.newScope][0][3]

    def getScope(self):#regresa el contexto actual
        if self.currentScope == 'global':
            return 'global'
        else:
            return 'local'

    def exportFundir(self):#exporta funDir y cambia los valores a direcciones
        exitT = dict()
        for x in self.funDir:

            exitT[x] = [self.funDir[x][0],dict()]
            for i in self.funDir[x][1]:
                exitT[x][1][self.returnAdr(i)] = self.funDir[x][1][i]
        return exitT

    def exportConst(self):#exporta la tabla de constantes
        exit = [dict(),dict(),dict(),dict()]
        for i in self.constTable[0]:#int
            exit[0][self.constTable[0][i]] = i
        for i in self.constTable[1]:#int
            exit[1][self.constTable[1][i]] = i
        for i in self.constTable[2]:#int
            exit[2][self.constTable[2][i]] = i
        for i in self.constTable[3]:#int
            exit[3][self.constTable[3][i]] = i
        return exit

    def exportTemp(self):#exporta la tabla de temporales
        exit = [dict(),dict(),dict()]
        for i in self.tempTable[0]:#int
            exit[0][self.tempTable[0][i]] = 0
        for i in self.tempTable[1]:#float
            exit[1][self.tempTable[1][i]] = 0.0
        for i in self.tempTable[2]:#bool
            exit[2][self.tempTable[2][i]] = True
        return exit

class quadrupleManager(object):
    
    def __init__(self):
        self.pilaO = []#operandos
        self.pilaT = []#tipo
        self.POper = []#pila de operadores
        self.avail = []#pila para los resultados temporales
        self.quadruplos = []#pila de quadruplos
        self.resultI = 0 #para tener el index de t1,t2
        self.pSaltos = []#pila de saltos
        self.pilaControl = []#pila para guardar adr de vControl

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

    def regresaTipoCuboSemantico(self,op,dupla):#regresa la respuesta a la interaccion entre 2 tipos
        return self.cubosemantico[op][dupla]

    def pushPilaO(self,x):#push a la pila de operandos
        self.pilaO.append(x)
    
    def popPilaO(self):#pop a la pila de operandos
        if self.pilaO:
            return self.pilaO.pop()
        else:
            print("no hay valores en la pilaO")

    def pushPilaT(self,x):#push a la pila de tipos
        self.pilaT.append(x)

    def popPilaT(self):#pop a la pila de tipos
        if self.pilaT:
            return self.pilaT.pop()
        else:
            print("no hay valores en la pilaT")

    def pushPOper(self,x):#pop a la pila de operadores
        self.POper.append(x)

    def popPOper(self):
        if self.POper:
            return self.POper.pop()
        else:
            print("no hay valores en la pila POper")

    def topPOper(self):#regresa el ultimo valor de la pila de operadores sin hacer pop
        if self.POper:
            return self.POper[-1]

    def pushPcontrol(self,x):#push a la pila de control
        self.pilaControl.append(x)

    def popPcontrol(self):#pop a la pila de control
        if self.pilaControl:
            return self.pilaControl.pop()

    def pushAvail(self,x):#push a avail(previamente el contador de temporales)
        self.avail.append(x)

    def pushQuadruple(self,op,left,right,result):#push a la lista de quadruplos
        self.quadruplos.append([op,left,right,result])

    def pushPSaltos(self,x):#push a la pila de saltos
        self.pSaltos.append(x)
    
    def popPSaltos(self):#pop a la pila de saltos
        if self.pSaltos:
            return self.pSaltos.pop()
        else:
            print("no hay valores en la pila de saltos")
    def resultCounter(self):
        return "t"+str(self.resultI)

    def resultAdd(self):#suma 1 a el iterador de resultados(temporales)
        self.resultI = self.resultI+1

    def quadCount(self):#regresa el numero de quadruplos hasta el momento
        return len(self.quadruplos)
    
    def fill(self,end,cont):#llena informacion de los saltos en los cuadruplos
        self.quadruplos[end][3] = cont

    def popAvail(self):#pop a la pila de avail(temporales)
        return self.avail.pop()

    def getAvail(self):#regresa avail (temporales)
        return self.avail

    def setQuadValuePrincipal(self):#encuentra el quadruplo donde empieza principal() y actualiza el goto inicial
        self.quadruplos[0][3] = self.quadCount()

    def returnQuadruplos(self):#regresa la lista de quadruplos
        return self.quadruplos

    def print(self):#imprime los cuadruplos
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

class MemoriaVirtual(object):

    def __init__(self):
        #rangos
        #global
        self.intG = 0
        self.floatG = 2500
        self.charG = 5000
        self.stringG = 7500
        self.dataframeG = 10000
        #local
        self.intL = 12500
        self.floatL = 15000
        self.charL = 17500
        self.stringL = 20000
        self.dataframeL = 22500
        #temp
        self.intT = 25000
        self.floatT = 27500
        self.boolT = 30000
        #const
        self.intC = 32500
        self.floatC = 35000
        self.charC = 37500
        self.stringC = 40000

        #rangos de tipos


    
    def addVar(self,tipo,scope):#calcula la nueva direccion para una variable
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
                print('WHAT THE FUCKS')
                print(self.intL)
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


    def limpiaLocal(self):#limpia los indices de las variables locales
        self.intL = 12500
        self.floatL = 15000
        self.charL = 17500
        self.stringL = 20000
        self.dataframeL = 22500

