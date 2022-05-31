from inspect import _void
from textwrap import indent
import json

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



    def print(self):
        print(json.dumps(self.funDir,indent=2))


class printTest:
    def __init__(self):
        print("test")

class quadrupleManager(object):
    
    def __init__(self):
        self.pilaO = []#operandos
        self.pilaT = []#tipo

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
            print("operacion valida, falta verificar tipos")
            if dupla in self.cubosemantico[op]:
                print("tipos validos")
                return True
        return False