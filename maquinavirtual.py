

class maquinavirtual(object):
    
    def __init__(self,funDirT,constT,tempT,quadruplosT,paramT):
        self.pointer = 0
        self.historialPointer = []
        self.eraCounter = 0
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
        self.memLsize = [[0,0,0,0,0]]#int,float,char,string,dataframe
        self.params = []
        #local
        self.intLpointer = 0
        self.floatLpointer = 0
        self.charLpointer = 0
        self.stringLpointer = 0
        self.dataframeLpointer = 0
        
        self.valorRegreso = None
    
    def correrPrograma(self):#corre las instrucciones dadas por los cuadruplos
        indexFinal = len(self.quadruplos)
        while self.pointer < indexFinal:
            self.isJumping = False
            quad = self.quadruplos[self.pointer]
            #print('quad: ')
            #print(quad)
            if quad[0] == 'GOTO':#GOTO incondicional
                self.pointer = quad[3]
                self.isJumping = True
            elif quad[0] in ['+','-','*','/']:#operaciones aritmeticas
                leftO = self.regresaValor(quad[1])
                rightO = self.regresaValor(quad[2])
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
                ans = eval(f'{leftO} {op} {rightO}')
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
            elif quad[0] == 'GOSUB':
                self.currentScope = self.siguienteScope
                self.aplicarTamanoFunc()
                
                self.guardaParams()
                self.addEra()
                
                self.historialPointer.append(self.pointer)#se guarda aqui o en el gosub?
                self.pointer = quad[3]-1
            elif quad[0] == 'ENDFunc':
                self.pointer = self.historialPointer.pop()
                self.saleFuncion()
                self.subEra()
            elif quad[0] == '=RET':
                self.guardarValor(quad[3], self.valorRegreso)
            elif quad[0] == 'REGV':
                #print(self.regresaValor(quad[1]))
                self.valorRegreso = self.regresaValor(quad[1])
            if not self.isJumping:
                self.pointer += 1

    def regresaValor(self,dir):#regresa el valor de una direccion de memoria
        if dir >= 0 and dir < 12500:#variable global
            return self.funDir['global'][1][dir][1]
        elif dir >= 12500 and dir < 25000:#local
            #print('viene aqui')
            return self.regresaValorL(dir)
        elif dir >= 25000 and dir < 32500:#temp
            if dir >= 2500 and dir < 27500:#int
                return self.temp[0][dir]
            elif dir >= 27500 and dir < 30000:#float
                return self.temp[1][dir]
            else:#bool
                return self.temp[2][dir]
        elif dir >= 32500 and dir < 42500:#const
            if dir >= 32500 and dir < 35000:#int
                return self.const[0][dir]
            elif dir >= 35000 and dir < 37500:#float
                return self.const[1][dir]
            elif dir >= 37500 and dir < 40000:#char
                return self.const[2][dir]
            else:
                return self.const[3][dir]
        else: 
            print('no existe este valor')
            return -1
            

    def lectura(self,dir):#lee input del usuario
        val = input(">")
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
    
    def regresaTipo(self,dir):#regresa el tipo de una variable
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

    def nuevoTamanoFunc(self,scope):#agrega el nuevo tamano de una funcion
        i = self.funDir[scope][0][2][0]
        f = self.funDir[scope][0][2][1]
        c = self.funDir[scope][0][2][2]
        s = self.funDir[scope][0][2][3]
        d = self.funDir[scope][0][2][4]
        self.memLsize.append([i,f,c,s,d])

    def aplicarTamanoFunc(self):#suma el nuevo tamano de una funcion a los apuntadores de memoria
        self.intLpointer += self.memLsize[self.eraCounter][0]
        self.floatLpointer += self.memLsize[self.eraCounter][1]
        self.charLpointer += self.memLsize[self.eraCounter][1]
        self.stringLpointer += self.memLsize[self.eraCounter][3]
        self.dataframeLpointer += self.memLsize[self.eraCounter][4]

    def addEra(self):
        self.eraCounter += 1

    def subEra(self):
        self.eraCounter -= 1

    def saleFuncion(self):#resta el el tamano de memoria de los apuntadores una vez que se acaba una funcion
        self.intLpointer -= self.memLsize[-1][0]
        self.floatLpointer -= self.memLsize[-1][1]
        self.charLpointer -= self.memLsize[-1][2]
        self.stringLpointer -= self.memLsize[-1][3]
        self.dataframeLpointer -= self.memLsize[-1][4]
        remove = self.memLsize.pop()

    def regresaValorL(self,dir):#regresa el valor de una variable local
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

    def guardaValorL(self,dir,val):#guarda el valor de una variable local
        if dir >= 12500 and dir < 15000:#int
            dir -= 12500
            dir += self.intLpointer
            self.memL[0][dir] = val
        elif dir>=15000 and dir < 17500:#float
            dir -= 15000
            dir += self.floatLpointer
            self.memL[1][dir] = val
        elif dir>=17500 and dir < 20000:#char
            dir -= 17500
            dir += self.charLpointer
            self.memL[2][dir] = val
        elif dir>=20000 and dir < 22500:#string
            dir -= 20000
            dir += self.stringLpointer
            self.memL[3][dir] = val
        elif dir>=22500 and dir < 25000:#dataframe
            print('dataframe')

    def guardaParams(self):#guarda los parametros de una funcion a su memoria local
        x = 0

        for i in self.params:
            if self.paramT[self.currentScope][x] == 'int':
                self.memL[0][self.intLpointer+x] = i
                #print(self.memL[0][self.intLpointer+x])
            elif self.paramT[self.currentScope][x] == 'float':
                self.memL[1][self.floatLpointer+x] = i
            elif self.paramT[self.currentScope][x] == 'char':
                self.memL[2][self.charLpointer+x] = i
            elif self.paramT[self.currentScope][x] == 'string':
                self.memL[3][self.stringLpointer+x] = i
            elif self.paramT[self.currentScope][x] == 'dataframe':
                self.memL[4][self.dataframeLpointer+x] = i
            x += 1

    def guardarValor(self,dir,valor):#guarda el valor de una variable
        if dir >= 0 and dir < 12500:#variable global
            self.funDir['global'][1][dir][1] = valor
        elif dir >= 12500 and dir < 25000:#local
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