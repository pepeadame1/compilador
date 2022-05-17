from inspect import _void


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
        print(self.funDir)

    def test():
        print("test")

class printTest:
    def __init__(self):
        print("test")