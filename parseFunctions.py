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

    def borrar(self):#aqui se borra todo
        self.funDir = dict()

    def checarTablaScope(self):
        if self.currentScope in self.funDir:#si hay tabla de el scope actual
            print("ya existe esta tabla")
        else:#si no hay tabla para el scope actual
            self.funDir[self.currentScope] = [self.currentScopeReturn,dict()]

    def agregarVariable(self, id):
        if id in self.funDir[self.currentScope][2]:#ya esta el id en la tabla
            print("error the id is already being used")
        else:
            print("test")
            self.funDir[self.currentScope][1][id] = [self.currentType,"valor"]

   
    def agregarFunc(self, id):
        self.currentScope = ""
        self.currentScopeReturn = ""
        self.currentType = "void"
        if id in self.funDir: #ya esta la func en la tabla
            print("error the function has already been decalred")
        else:
            self.programName = id
            print(self.programName)
            self.funDir[id] = ["void", dict()]
            self.currentScope = id
            self.print



    def print(self):
        print(self.funDir)

    def test():
        print("test")

class printTest:
    def __init__(self):
        print("test")