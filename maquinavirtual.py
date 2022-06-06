

class maquinavirtual(object):
    
    def __init__(self,funDirT,constT,tempT,quadruplosT,paramT):
        self.pointer = 0
        self.historialPointer = []
        self.currentScope = 'principal'
        self.siguienteScope = ''
        self.currentScopeReturn = ''
        self.funDir = funDirT
        self.paramT = paramT
        self.const = constT
        self.temp = tempT
        self.quadruplos = quadruplosT
        self.isJumping = False

        self.memL = [[None]*2500,[None]*2500,[None]*2500,[None]*2500,[None]*2500]#int,float,char,string,dataframe
        self.memLsize = []#int,float,char,string,dataframe
        self.params = []
        #local
        self.intLpointer = 0
        self.floatLpointer = 0
        self.charLpointer = 0
        self.stringLpointer = 0
        self.dataframeLpointer = 0
    
    def correrPrograma(self):
        indexFinal = len(self.quadruplos)
        print('-----------------------------------------------')
        print('empieza la maquina virtual')
        print('index final',end=': ')
        print(indexFinal)
        while self.pointer < indexFinal:
            print('quadruplo: ',end='')
            print(self.pointer)
            print('operacion: ',end='')
            print(self.quadruplos[self.pointer])

            self.isJumping = False
            quad = self.quadruplos[self.pointer]
            
            if quad[0] == 'GOTO':#GOTO incondicional
                self.pointer = quad[3]
                self.isJumping = True
            elif quad[0] in ['+','-','*','/']:#operaciones aritmeticas
                leftO = self.regresaValor(quad[1])
                rightO = self.regresaValor(quad[2])
                print('leftO')
                print(leftO)
                print('rightO')
                print(rightO)
                op = quad[0]
                ans = eval(f'{leftO} {op} {rightO}')
                
                self.guardarValor(quad[3],ans)
            elif quad[0] == 'GotoF':
                if self.regresaValor(quad[1]) == False:
                    self.pointer = quad[3]
                    self.isJumping = True
            elif quad[0] in ['<','>','<=','>=','==']:
                leftO = self.regresaValor(quad[1])
                rightO = self.regresaValor(quad[2])
                op = quad[0]
                print(f'{leftO} {op} {rightO}')
                ans = eval(f'{leftO} {op} {rightO}')
                print('operacion booleana')
                print(ans)
                self.guardarValor(quad[3],ans)
            elif quad[0] == '=':
                self.guardarValor(quad[3],self.regresaValor(quad[1]))
            elif quad[0] == 'LEE':
                self.lectura(quad[3])
            elif quad[0] == 'ESCRIBE':
                print(self.regresaValor(quad[3]))#no quitar este
            elif quad[0] == 'ERA':
                self.siguienteScope = quad[3]
                self.params = []
                self.nuevoTamanoFunc(quad[3])
            elif quad[0] == 'PARAMETER':
                self.params.append(self.regresaValor(quad[1]))
                #self.guardaValorL(quad[1],self.regresaValor(quad[1]))
            elif quad[0] == 'GOSUB':
                self.currentScope = self.siguienteScope
                self.aplicarTamanoFunc()
                self.guardaParams()
                #print('llega')
                self.historialPointer.append(self.pointer)#se guarda aqui o en el gosub?
                self.pointer = quad[3]-1
                #self.isJumping = True
                print('')
            elif quad[0] == 'ENDFunc':
                self.pointer = self.historialPointer.pop()
                self.saleFuncion()
            if not self.isJumping:
                self.pointer += 1


    def regresaValor(self,dir):
        #print(self.temp)
        print('regresa valor')
        print(dir)
        if dir >= 0 and dir < 12500:#variable global
            print(self.funDir['global'][1][dir][1])
            return self.funDir['global'][1][dir][1]
        elif dir >= 12500 and dir < 25000:#local
            print(self.regresaValorL(dir))
            return self.regresaValorL(dir)
        elif dir >= 25000 and dir < 32500:#temp
            if dir >= 2500 and dir < 27500:#int
                print(self.temp[0][dir])
                return self.temp[0][dir]
            elif dir >= 27500 and dir < 30000:#float
                print(self.temp[1][dir])
                return self.temp[1][dir]
            else:#bool
                print(self.temp[2][dir])
                return self.temp[2][dir]
        elif dir >= 32500 and dir < 42500:#const
            if dir >= 32500 and dir < 35000:#int
                print(self.const[0][dir])
                return self.const[0][dir]
            elif dir >= 35000 and dir < 37500:#float
                print(self.const[1][dir])
                return self.const[1][dir]
            elif dir >= 37500 and dir < 40000:#char
                print(self.const[2][dir])
                return self.const[2][dir]
            else:
                print(self.const[3][dir])
                return self.const[3][dir]
        else: 
            return -1

    def lectura(self,dir):
        val = input(">")
        #print(dir)
        tipo = self.regresaTipo(dir)
        
        try:
            if tipo == 'int':
                val = int(val)
                self.guardarValor(dir,val)
            elif tipo == 'float':
                val = float(val)
                self.guardarValor(dir,val)
            elif tipo == 'char':
                val = chr(val)
            elif tipo == 'string':
                self.guardarValor(dir,val)
            else:
                print('error tipos incorrectos')
            
        except:
            print('error: tipo de input no congruente con tipo de variable')
    
    def regresaTipo(self,dir):
        if dir >= 0 and dir < 12500:#variable global
            return self.funDir['global'][1][dir][0]
        elif dir >= 12500 and dir < 25000:#local
            if dir >= 12500 and dir < 15000:#int
                return 'int'
            elif dir>=15000 and dir < 17500:#float
                return 'float'
            elif dir>=17500 and dir < 20000:#char
                return 'char'
            elif dir>=20000 and dir < 22500:#string
                return 'string'
            elif dir>=22500 and dir < 25000:#dataframe
                return 'dataframe'
        elif dir >= 25000 and dir < 32500:#temp
            if dir >= 2500 and dir < 27500:#int
                return 'int'
            elif dir >= 27500 and dir < 30000:#float
                return 'float'
            else:#bool
                return 'bool'
        elif dir >= 32500 and dir < 42500:#const
            if dir >= 32500 and dir < 35000:#int
                return 'int'
            elif dir >= 35000 and dir < 37500:#float
                return 'float'
            elif dir >= 37500 and dir < 40000:#char
                return 'char'
            else:
                return 'string'
        else: 
            print('no se encontro la variable')

    def nuevoTamanoFunc(self,scope):
        i = self.funDir[scope][0][2][0]
        f = self.funDir[scope][0][2][1]
        c = self.funDir[scope][0][2][2]
        s = self.funDir[scope][0][2][3]
        d = self.funDir[scope][0][2][4]
        self.memLsize.append([i,f,c,s,d])
        
        print(self.memLsize)

    def aplicarTamanoFunc(self):
        self.intLpointer += self.funDir[self.currentScope][0][2][0]
        self.floatLpointer += self.funDir[self.currentScope][0][2][1]
        self.charLpointer += self.funDir[self.currentScope][0][2][2]
        self.stringLpointer += self.funDir[self.currentScope][0][2][3]
        self.dataframeLpointer += self.funDir[self.currentScope][0][2][4]

    def saleFuncion(self):
        self.intLpointer -= self.memLsize[-1][0]
        self.floatLpointer -= self.memLsize[-1][1]
        self.charLpointer -= self.memLsize[-1][2]
        self.stringLpointer -= self.memLsize[-1][3]
        self.dataframeLpointer -= self.memLsize[-1][4]
        remove = self.memLsize.pop()

    def regresaValorL(self,dir):
        #print(self.memL)
        if dir >= 12500 and dir < 15000:#int
            dir -= 12500
            dir += self.intLpointer
            return self.memL[0][dir]
        elif dir>=15000 and dir < 17500:#float
            dir -= 15000
            dir += self.floatLpointer
            return self.memL[1][dir]
        elif dir>=17500 and dir < 20000:#char
            dir -= 17500
            dir += self.charLpointer
            return self.memL[2][dir]
        elif dir>=20000 and dir < 22500:#string
            dir -= 20000
            dir += self.stringLpointer
            return self.memL[3][dir]
        elif dir>=22500 and dir < 25000:#dataframe
            print('dataframe')

    def guardaValorL(self,dir,val):
        #print('guarda valor')
        #print(dir)
        if dir >= 12500 and dir < 15000:#int
            dir -= 12500
            dir += self.intLpointer
            #print(dir)
            self.memL[0][dir] = val
            print('guarda int')
            print(dir)
            print(val)
        elif dir>=15000 and dir < 17500:#float
            dir -= 15000
            dir += self.floatLpointer
            #print(dir)
            self.memL[1][dir] = val
        elif dir>=17500 and dir < 20000:#char
            dir -= 17500
            dir += self.charLpointer
            #print(dir)
            self.memL[2][dir] = val
        elif dir>=20000 and dir < 22500:#string
            dir -= 20000
            dir += self.stringLpointer
            #print(dir)
            self.memL[3][dir] = val
        elif dir>=22500 and dir < 25000:#dataframe
            print('dataframe')

    def guardaParams(self):
        x = 0
        
        for i in self.params:
            #print('llega')
            #print(self.paramT)
            if self.paramT[self.currentScope][x] == 'int':
                self.memL[0][self.intLpointer+x] = i
            elif self.paramT[self.currentScope][x] == 'float':
                self.memL[1][self.floatLpointer+x] = i
            elif self.paramT[self.currentScope][x] == 'char':
                self.memL[2][self.charLpointer+x] = i
            elif self.paramT[self.currentScope][x] == 'string':
                self.memL[3][self.stringLpointer+x] = i
            elif self.paramT[self.currentScope][x] == 'dataframe':
                self.memL[4][self.dataframeLpointer+x] = i
            x += 1

    def guardarValor(self,dir,valor):
        #print('guardar valor')
        #print(dir)
        #print(valor)
        if dir >= 0 and dir < 12500:#variable global
            self.funDir['global'][1][dir][1] = valor
        elif dir >= 12500 and dir < 25000:#local
            #self.funDir[self.currentScope][1][dir][1] = valor
            self.guardaValorL(dir,valor)
        elif dir >= 25000 and dir < 32500:#temp
            if dir >= 2500 and dir < 27500:#int
                self.temp[0][dir] = valor
            elif dir >= 27500 and dir < 30000:#float
                self.temp[1][dir] = valor
            else:#bool
                self.temp[2][dir] = valor
        elif dir >= 32500 and dir < 42500:#const
            if dir >= 32500 and dir < 35000:#int
                self.const[0][dir] = valor
            elif dir >= 35000 and dir < 37500:#float
                self.const[1][dir] = valor 
            elif dir >= 37500 and dir < 40000:#char
                self.const[2][dir] = valor
            else:
                self.const[3][dir] = valor
        else: 
            print('no se encontro la variable')