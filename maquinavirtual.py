

class maquinavirtual(object):
    
    def __init__(self,funDirT,constT,tempT,quadruplosT):
        self.pointer = 0
        self.currentScope = 'principal'
        self.currentScopeReturn = ''
        self.funDir = funDirT
        self.const = constT
        self.temp = tempT
        self.quadruplos = quadruplosT
        self.isJumping = False


    
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
                self.guardarValor(quad[3],self.regresaValor(ans))
            elif quad[0] == '=':
                self.guardarValor(quad[3],self.regresaValor(quad[1]))
            elif quad[0] == 'LEE':
                self.lectura(quad[3])
            elif quad[0] == 'ESCRIBE':
                print(self.regresaValor(quad[3]))#no quitar este
            
            if not self.isJumping:
                self.pointer += 1


    def regresaValor(self,dir):

        #print(self.temp)
        if dir >= 0 and dir < 12500:#variable global
            return self.funDir['global'][1][dir][1]
        elif dir >= 12500 and dir < 25000:#local
            return self.funDir[self.currentScope][1][dir][1]
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
            return -1

    def lectura(self,dir):
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
    
    def regresaTipo(self,dir):
        if dir >= 0 and dir < 12500:#variable global
            return self.funDir['global'][1][dir][0]
        elif dir >= 12500 and dir < 25000:#local
            return self.funDir[self.currentScope][1][dir][0]
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

    def guardarValor(self,dir,valor):
        print('guardar valor')
        print(dir)
        print(valor)
        if dir >= 0 and dir < 12500:#variable global
            self.funDir['global'][1][dir][1] = valor
        elif dir >= 12500 and dir < 25000:#local
            self.funDir[self.currentScope][1][dir][1] = valor
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