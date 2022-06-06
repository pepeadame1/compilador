from sly import Parser
from lexer import *
from parseFunctions import *
from maquinavirtual import *

dir = fundir()
qm = quadrupleManager()
mv = MemoriaVirtual()


class BasicParser(Parser):
    tokens = BasicLexer.tokens

    precedence = (
        ('left','+','-'),
        ('left','*','/'),
    )

    @_('catcherprograma ";" programa')
    def preprograma(self,p):
        print("fin de parser")
        maqVirt = maquinavirtual(dir.exportFundir(),dir.exportConst(),dir.exportTemp(),qm.returnQuadruplos(),dir.returnParamT())
        maqVirt.correrPrograma()
        return p

    @_("PROGRAMA ID")
    def catcherprograma(self,p):
        dir.addProgram(p[1])
        qm.pushQuadruple("GOTO","","","principal")
        dir.addConst('int',1,mv.addVar('int','const'))
        return p


    @_(' programa2 PRINCIPAL contextoprograma "(" ")" bloque fin')
    def programa(self,p):
        return p

    @_(' PRINCIPAL contextoprograma "(" ")" bloque fin')
    def programa(self,p):
        return p

    @_('')
    def contextoprograma(self,p):
        dir.setscope('principal')
        qm.setQuadValuePrincipal()
        return p

    @_('vars programa3')
    def programa2(self,p):
        return p

    @_('programa3')
    def programa2(self,p):
        return p

    @_('funcs programa3')
    def programa3(self,p):
        return p

    @_('funcs')
    def programa3(self,p):
        return p

    @_('varshelper var2')
    def vars(self,p):
        return p

    @_('VAR')
    def varshelper(self,p):
        dir.checarTablaScope()
        return p

    @_('tipo var3 ";" var2')
    def var2(self,p):
        return p

    @_('tipo var3 ";"')
    def var2(self,p):
        return p

    @_('varhelp2 "["  var4 arrCalc')#aqui notar que es un arreglo
    def var3(self,p):
        return p

    @_('varhelp2 "[" var4 arrCalc "," var3')#aqui notar que es un arreglo
    def var3(self,p):
        return p

    @_('varhelp var3')
    def var3(self,p):
        return p

    @_('varhelp')
    def var3(self,p):
        return p

    @_('CTEINT "]" "[" CTEINT "]"')
    def var4(self,p):
        dir.addLimite(dir.auxArrId, p[0])
        dir.addLimite(dir.auxArrId, p[3])
        return p

    @_('CTEINT "]"')
    def var4(self,p):
        dir.addLimite(dir.auxArrId, p[0])
        return p

    @_('ID ","')
    def varhelp(self,p):
        #print(dir.getScope())
        #print(mv.addVar(dir.getCurrentType(),dir.getScope()))
        #dir.agregarVariable(mv.addVar(dir.getCurrentType(),dir.getScope()))
        dir.agregarVariable(p[0],mv.addVar(dir.getCurrentType(),dir.getScope()))
        return p

    @_('ID')
    def varhelp(self,p):
        #print(mv.addVar(dir.getCurrentType(),dir.getScope()))
        #dir.agregarVariable(mv.addVar(dir.getCurrentType(),dir.getScope()))
        dir.agregarVariable(p[0],mv.addVar(dir.getCurrentType(),dir.getScope()))
        return p

    @_('ID')
    def varhelp2(self,p):
        dir.agregarVariable(p[0],mv.addVar(dir.getCurrentType(),dir.getScope()))
        dir.auxArrId = p[0]
        dir.setArreglo(dir.auxArrId)
        return p
        
    @_('')
    def arrCalc(self,p):
        dir.arrCalc(dir.auxArrId)
        return p

    @_('INT')
    def tipo(self,p):
        dir.settype("int")
        return p

    @_('FLOAT')
    def tipo(self,p):
        dir.settype("float")
        return p

    @_('STRING')
    def tipo(self,p):
        dir.settype("string")
        return p

    @_('CHAR')
    def tipo(self,p):
        dir.settype("char")
        return p

    @_('DATAFRAME')
    def tipo(self,p):
        dir.settype("dataframe")
        return p

    @_('VOID')#########################################################
    def tipo(self,p):
        dir.currentType = "void"
        return p

    @_('paramhelp "," param')
    def param(self,p):
        return p

    @_('paramhelp')
    def param(self,p):
        return p

    @_('tipo ID')#nodo 2 definicion de funcion
    def paramhelp(self,p):
        dir.agregarVariable(p[1],mv.addVar(dir.getCurrentType(),dir.getScope()))
        #dir.addParamT(p[0][1])
        dir.addParamT(dir.getCurrentType())
        return p

    @_('funcshelper funcs2')
    def funcs(self,p):
        return p

    @_('FUNCION tipo ID')#nodo 1 definicion de funcion
    def funcshelper(self,p):
        dir.setscope(p[2])
        dir.setreturn(dir.getCurrentType())
        dir.agregarFunc(p[2])
        return p

    '''
    @_('FUNCION ID funcs2')##no recuerdo para que pusimos esto
    def funcs(self,p):
        dir.agregarFunc(p[1])
        dir.print
        return p
    '''

    @_('"(" param ")" countparam funcs3')
    def funcs2(self,p):
        
        return p

    @_('"(" ")" countparam funcs3')
    def funcs2(self,p):
        return p

    @_('')
    def countparam(self,p):#nodo 4 definicion de funcion
        dir.countParams()
        
        return p

    @_('vars varcount bloque funcs4')
    def funcs3(self,p):
        return p

    @_('varcount bloque funcs4')
    def funcs3(self,p):
        return p

    @_('')#nodo 5 y 6 definicion de funcion
    def varcount(self,p):
        dir.countLocalVar()
        dir.setQuadCounter(qm.quadCount()) 
        return p

    @_('')
    def funcs4(self,p):#nodo 7 definicion de funcion
        #dir.borrarScope()###############################################################
        #dir.borrarTemp()################################################################
        qm.pushQuadruple("ENDFunc","","","")

        mv.limpiaLocal()
        return p

    @_('"{" "}"')
    def bloque(self,p):
        return p

    @_('"{" bloque2')
    def bloque(self,p):
        
        return p

    @_('estatuto "}"')
    def bloque2(self,p):
        return p

    @_('estatuto bloque2')
    def bloque2(self,p):
        return p

    @_('asignacion')
    def estatuto(self,p):
        return p

    @_('decision')
    def estatuto(self,p):
        return p

    @_('escritura')
    def estatuto(self,p):
        return p

    @_('void')
    def estatuto(self,p):
        return p

    @_('retorno')
    def estatuto(self,p):
        return p

    @_('lectura')
    def estatuto(self,p):
        return p

    @_('cargadatos')
    def estatuto(self,p):
        return p
    
    @_('condicional')#while 
    def estatuto(self,p):
        return p

    @_('nocondicional')
    def estatuto(self,p):
        return p

    @_('ID "=" expresion ";"')
    def asignacion(self,p):
        leftO = qm.popPilaO()
        leftT = qm.popPilaT()
        tipoId = dir.getVariableType(p[0])
        if qm.verificarTiposOp('=',(leftT,tipoId)):
            qm.pushQuadruple('=',dir.returnAdrFull(leftO,leftT),"",dir.returnAdr(p[0]))
        else:
            print("type mismatch")
        return p

    @_('verifyid "(" ")" ";"')
    def void(self,p):
        return p

    @_('verifyid "(" void2 ";"')
    def void(self,p):
        return p

    @_('ID')
    def verifyid(self,p):#nodo 1 y 2 de function call
        
        if dir.funcExists(p[0]):
            dir.startParamC()
            dir.setNewScope(p[0])
            qm.pushQuadruple("ERA","","",p[0])
            
        else:
            print("no se encontro la funcion")
            exit()
        return p

    @_('expresion void4 ")" void6')
    def void2(self,p):
        return p

    @_('expresion void4 "," void5 void2')
    def void2(self,p):
        return p

    @_('')
    def void4(self,p):#nodo 3 de function call
        arg = qm.popPilaO()
        argT = qm.popPilaT()
        if dir.validaParam(argT):
            #print("llega")
            qm.pushQuadruple("PARAMETER",dir.returnAdrFull(arg,argT),"","param"+str(dir.getParamC()))
            print("termina")
        else:
            exit()
        return p

    @_('')
    def void5(self,p):#nodo 4 de function call
        dir.sumaParamC()
        return p

    @_('')
    def void6(self,p):#nodo 5 y 6 de function call
        if dir.validaSize():
            qm.pushQuadruple("GOSUB",dir.currentScope,"",dir.getQuadCounter())#este es current scope o newscope?
        else:
            exit()
        return p

    @_('REGRESA "(" exp ")" ";"')
    def retorno(self,p):
        return p

    @_('LEE "(" lectura2 ";"')
    def lectura(self,p):
        return p

    @_('lectura3 ")"')
    def lectura2(self,p):
        return p

    @_('lectura3 "," lectura2')
    def lectura2(self,p):
        return p

    @_('ID')
    def lectura3(self,p):#aqui se agrega el quadruplo de lectura
        if dir.variableExists(p[0]):#verificar que exista el id
            qm.pushQuadruple('LEE',"","",dir.returnAdr(p[0]))
        return p
        

    @_('ESCRIBE "(" escritura2')
    def escritura(self,p):
        return p
    
    @_('escritura4 ")" ";"')
    def escritura2(self,p):
        return p

    @_('escritura4 "," escritura2')
    def escritura2(self,p):
        return p

    @_('escritura3 ")" ";"')
    def escritura2(self,p):
        return p

    @_('escritura3 "," escritura2')
    def escritura2(self,p):
        return p

    @_('CTESTRING')
    def escritura4(self,p):#se crea el cuadruplo para escribir un string
        #print("si encontro el string")
        if not dir.validaConst('string',p[0]):
            adr = mv.addVar('string','const')
            dir.addConst('string',p[0],adr)
        else:
            adr = dir.returnConst(p[0],'string')
        qm.pushQuadruple("ESCRIBE","","",adr)

    @_('expresion')
    def escritura3(self,p):#se crea el cuadruplo para escribir una expresion
        
        exp = qm.popPilaO()
        tipo = qm.popPilaT()

        qm.pushQuadruple("ESCRIBE","","",dir.returnAdrFull(exp,tipo))
        return p

    

    @_('CARGAARCHIVO "(" ID "," RUTA "," INT "," INT ")" ";"')
    def cargadatos(self,p):
        return p

    @_('exp expresion2')
    def expresion(self,p):
        return p

    @_('exp')
    def expresion(self,p):
        return p

    @_('"<" exp')
    def expresion2(self,p):
        rightO = qm.popPilaO()
        rightT = qm.popPilaT()
        leftO = qm.popPilaO()
        leftT = qm.popPilaT()
        if qm.verificarTiposOp('<',(rightT,leftT)):#si es valido
            resultT = qm.regresaTipoCuboSemantico('<',(rightT,leftT))
            #qm.pushAvail(qm.resultCounter())
            adr = mv.addVar(resultT,'temp')
            dir.addTemp(resultT,qm.resultCounter(),adr)
            qm.pushQuadruple('<',dir.returnAdrFull(leftO,leftT),dir.returnAdrFull(rightO,rightT),qm.resultCounter())
            qm.pushPilaO(qm.resultCounter())
            qm.pushPilaT(resultT)
            qm.resultAdd()
        else:
            print("tipos de datos no iguales")
        return p

    @_('">" "=" exp')
    def expresion2(self,p):
        rightO = qm.popPilaO()
        rightT = qm.popPilaT()
        leftO = qm.popPilaO()
        leftT = qm.popPilaT()
        if qm.verificarTiposOp('>=',(rightT,leftT)):#si es valido
            resultT = qm.regresaTipoCuboSemantico('>=',(rightT,leftT))
            #qm.pushAvail(qm.resultCounter())
            adr = mv.addVar(resultT,'temp')
            dir.addTemp(resultT,qm.resultCounter(),adr)
            qm.pushQuadruple('>=',dir.returnAdrFull(leftO,leftT),dir.returnAdrFull(rightO,rightT),qm.resultCounter())
            qm.pushPilaO(qm.resultCounter())
            qm.pushPilaT(resultT)
            qm.resultAdd()
        else:
            print("tipos de datos no iguales")
        return p

    @_('"<" "=" exp')
    def expresion2(self,p):
        rightO = qm.popPilaO()
        rightT = qm.popPilaT()
        leftO = qm.popPilaO()
        leftT = qm.popPilaT()
        if qm.verificarTiposOp('<=',(rightT,leftT)):#si es valido
            resultT = qm.regresaTipoCuboSemantico('<=',(rightT,leftT))
            #qm.pushAvail(qm.resultCounter())
            adr = mv.addVar(resultT,'temp')
            dir.addTemp(resultT,qm.resultCounter(),adr)
            qm.pushQuadruple('<=',dir.returnAdrFull(leftO,leftT),dir.returnAdrFull(rightO,rightT),qm.resultCounter())
            qm.pushPilaO(qm.resultCounter())
            qm.pushPilaT(resultT)
            qm.resultAdd()
        else:
            print("tipos de datos no iguales")
        return p

    @_('">" exp')
    def expresion2(self,p):
        rightO = qm.popPilaO()
        rightT = qm.popPilaT()
        leftO = qm.popPilaO()
        leftT = qm.popPilaT()
        if qm.verificarTiposOp('>',(rightT,leftT)):#si es valido
            resultT = qm.regresaTipoCuboSemantico('>',(rightT,leftT))
            #qm.pushAvail(qm.resultCounter())
            adr = mv.addVar(resultT,'temp')
            dir.addTemp(resultT,qm.resultCounter(),adr)
            qm.pushQuadruple('>',dir.returnAdrFull(leftO,leftT),dir.returnAdrFull(rightO,rightT),adr)
            qm.pushPilaO(qm.resultCounter())
            qm.pushPilaT(resultT)
            qm.resultAdd()
        else:
            print("tipos de datos no iguales")
        return p

    @_('"<" ">" exp')
    def expresion2(self,p):
        return p

    @_('"=" "=" exp')
    def expresion2(self,p):
        rightO = qm.popPilaO()
        rightT = qm.popPilaT()
        leftO = qm.popPilaO()
        leftT = qm.popPilaT()
        if qm.verificarTiposOp('==',(rightT,leftT)):#si es valido
            resultT = qm.regresaTipoCuboSemantico('==',(rightT,leftT))
            #qm.pushAvail(qm.resultCounter())
            adr = mv.addVar(resultT,'temp')
            dir.addTemp(resultT,qm.resultCounter(),adr)
            qm.pushQuadruple('==',dir.returnAdrFull(leftO,leftT),dir.returnAdrFull(rightO,rightT),adr)
            qm.pushPilaO(qm.resultCounter())
            qm.pushPilaT(resultT)
            qm.resultAdd()
        else:
            print("tipos de datos no iguales")
        return p

    @_('decision1 ENTONCES bloque decision2 SINO bloque')
    def decision(self,p):
        end =qm.popPSaltos()
        cont = qm.quadCount()
        qm.fill(end,cont)
        return p

    @_('decision1 ENTONCES bloque')
    def decision(self,p):
        end = qm.popPSaltos()
        cont = qm.quadCount()
        
        qm.fill(end,cont)
        return p

    @_('SI "(" expresion ")"')
    def decision1(self,p):

        tipo = qm.popPilaT()
        if tipo != "bool":
            print("tipos de datos no iguales")
        else:
            exp = qm.popPilaO()
            print("decision1--------------------")
            print(exp)
            qm.pushQuadruple("GotoF",dir.returnAdrFull(exp,tipo),"","")
            cont = qm.quadCount()
            qm.pushPSaltos(cont-1)
        return p
    
    @_('')
    def decision2(self,p):
        qm.pushQuadruple("GOTO","","","_")
        
        false = qm.popPSaltos()
        cont = qm.quadCount()
        qm.pushPSaltos(cont - 1)
        qm.fill(false,cont)
        return p


    @_('MIENTRAS condicional1 "(" expresion ")" condicional2 HAZ bloque condicional3')
    def condicional(self,p):
        return p

    @_('')
    def condicional1(self,p):
        qm.pushPSaltos(qm.quadCount())
        return p

    @_('')
    def condicional2(self,p):
        expT = qm.popPilaT()
        if expT == "bool":
            result = qm.popPilaO()
            qm.pushQuadruple("GotoF",dir.returnAdrFull(result,expT),"","")
            qm.pushPSaltos(qm.quadCount()-1)
        else:
            print("error")
        return p

    @_('')
    def condicional3(self,p):
        end = qm.popPSaltos()
        ret = qm.popPSaltos()
        qm.pushQuadruple("GOTO",'','',ret)
        qm.fill(end,qm.quadCount())


    @_('DESDE nocondicional1 "=" exp nocondicional2 HASTA exp nocondicional3 HACER bloque nocondicional4')
    def nocondicional(self,p):
        return p

    @_('ID')
    def nocondicional1(self,p):#punto 1
        tipo = dir.getVariableType(p[0])
        if tipo == 'int' or tipo == 'float':
            qm.pushPilaO(p[0])
            qm.pushPilaT(tipo)
        else:
            print("error: tipos de datos no iguales")
        return p

    @_('')
    def nocondicional2(self,p):#punto 2
        print('punto 2')
        expT = qm.popPilaT()
        if expT == 'int' or expT == 'float':
            exp = qm.popPilaO()
            vControl = qm.pilaO[-1]
            adr = mv.addVar(qm.pilaT[-1],'temp')
            #hacer vControl su propia variable
            dir.addTemp(qm.pilaT[-1],qm.resultCounter(),adr)
            qm.resultAdd()
            qm.pushPcontrol(adr)
            if qm.verificarTiposOp('=',(expT,qm.pilaT[-1])):
                qm.pushQuadruple('=',dir.returnAdrFull(exp,expT),'',dir.returnAdrFull(vControl,'int'))
                qm.pushQuadruple('=',dir.returnAdrFull(exp,expT),'',adr)
            else:
                print("error: los tipos de variable no son iguales")

    @_('')
    def nocondicional3(self,p):#punto 3
        expT = qm.popPilaT()
        if expT == 'int' or expT == 'float':
            exp = qm.popPilaO()
            adr = mv.addVar(expT,'temp')
            dir.addTemp(expT,qm.resultCounter(),adr)
            qm.resultAdd()
            vControl = qm.popPcontrol()
            qm.pushQuadruple('=',dir.returnAdrFull(exp,expT),'',adr)
            adrBool = mv.addVar('bool','temp')
            dir.addTemp('bool',qm.resultCounter(),adrBool)
            qm.resultAdd()
            qm.pushQuadruple('<',vControl,adr,adrBool)#este ex debe de ser un booleano temporal
            qm.pushPSaltos(qm.quadCount()-1)
            qm.pushQuadruple('GotoF',adrBool,'','')
            qm.pushPSaltos(qm.quadCount()-1)
            qm.pushPcontrol(vControl)
            
        else:
            print("error: los tipos de variable no son iguales")

    @_('')
    def nocondicional4(self,p):#punto 4
        vControl = qm.popPcontrol()
        adrBool = mv.addVar('int','temp')
        dir.addTemp('int',qm.resultCounter(),adrBool)
        qm.resultAdd()
        qm.pushQuadruple('+',vControl,dir.returnAdrFull(1,'int'),adrBool)#se tiene que agregar un 1 como const por default?
        qm.pushQuadruple('=',adrBool,'',vControl)
        qm.pushQuadruple('=',adrBool,'',dir.returnAdrFull(qm.pilaO[-1],qm.pilaT[-1]))
        fin = qm.popPSaltos()
        ret = qm.popPSaltos()
        qm.pushQuadruple('GOTO','','',ret)
        qm.fill(fin,qm.quadCount())
        elimina = qm.popPilaO()
        eliminaT = qm.popPilaT()

    @_('termino validatipos1')
    def exp(self,p):
        return p

    @_('')
    def validatipos1(self,p):
        if qm.topPOper() == '+' or qm.topPOper() == '-':
            rightO = qm.popPilaO()
            rightType = qm.popPilaT()
            leftO = qm.popPilaO()
            leftType = qm.popPilaT()
            operator = qm.popPOper()
            if qm.verificarTiposOp(operator,(rightType,leftType)):
                resultT = qm.regresaTipoCuboSemantico(operator,(rightType,leftType))
                qm.pushAvail(qm.resultCounter())
                adr = mv.addVar(resultT,'temp')
                dir.addTemp(resultT,qm.resultCounter(),adr)
                qm.pushQuadruple(operator,dir.returnAdrFull(leftO,leftType),dir.returnAdrFull(rightO,rightType),adr)#falta entender result
                qm.pushPilaO(qm.resultCounter())#falta entender result
                qm.pushPilaT(resultT)
                qm.resultAdd()
            else:
                print("type mismatch")
        return p

    @_('')
    def validatipos2(self,p):
        if qm.topPOper() == '*' or qm.topPOper() == '/':
            rightO = qm.popPilaO()
            rightType = qm.popPilaT()
            leftO = qm.popPilaO()
            leftType = qm.popPilaT()
            operator = qm.popPOper()
            if qm.verificarTiposOp(operator,(rightType,leftType)):
                resultT = qm.regresaTipoCuboSemantico(operator,(rightType,leftType))
                #qm.pushAvail(qm.resultCounter())
                adr = mv.addVar(resultT,'temp')
                dir.addTemp(resultT,qm.resultCounter(),adr)
                qm.pushQuadruple(operator,dir.returnAdrFull(leftO,leftType),dir.returnAdrFull(rightO,rightType),adr)#falta entender result
                qm.pushPilaO(qm.resultCounter())#falta entender result
                qm.pushPilaT(resultT)
                qm.resultAdd()
            else:
                print("type mismatch")
        return p


    @_('pushomas exp')
    def exp(self,p):
        return p

    @_('termino validatipos1 "+"')
    def pushomas(self,p):
        qm.pushPOper(p[2])
        return p

    @_('pushomin exp')
    def exp(self,p):
        return p

    @_('termino validatipos1 "-"')
    def pushomin(self,p):
        qm.pushPOper(p[2])
        return p

    @_('factor validatipos2')
    def termino(self,p):
        return p

    @_('pushomult termino')
    def termino(self,p):
        return p

    @_('factor validatipos2 "*"')
    def pushomult(self,p):
        qm.pushPOper(p[2])
        return p

    @_('pushodiv termino')
    def termino(self,p):
        return p

    @_('factor validatipos2 "/"')
    def pushodiv(self,p):
        qm.pushPOper(p[2])
        return p

    @_('"(" expresion ")"')
    def factor(self,p):
        return p

    @_('"+" varcte')
    def factor(self,p):
        return p

    @_('"-" varcte')
    def factor(self,p):
        return p

    @_('varcte')
    def factor(self,p):
        return p

    @_('ID')
    def varcte(self,p):
        qm.pushPilaO(p[0])
        qm.pushPilaT(dir.getVariableType(p[0]))
        return p

    @_('CTEINT')
    def varcte(self,p):
        qm.pushPilaO(p[0])
        qm.pushPilaT('int')
        if not dir.validaConst('int',p[0]):
            dir.addConst('int',p[0],mv.addVar('int','const'))
        return p

    @_('CTEFLOAT')
    def varcte(self,p):
        qm.pushPilaO(p[0])
        qm.pushPilaT('float')
        if not dir.validaConst('float',p[0]):
            dir.addConst('float',p[0],mv.addVar('float','const'))
        return p

    @_('CTESTRING')
    def varcte(self,p):
        qm.pushPilaO(p[0])
        qm.pushPilaT('string')
        if not dir.validaConst('string',p[0]):
            dir.addConst('string',p[0],mv.addVar('string','const'))
        return p

    @_('CTECHAR')
    def varcte(self,p):
        qm.pushPilaO(p[0])
        qm.pushPilaT('char')
        if not dir.validaConst('char',p[0]):
            dir.addConst('char',p[0],mv.addVar('char','const'))
        return p



    @_('')
    def fin(self,p):
        print("codigo valido")
        dir.print()
        #dir.test()
        qm.print()
        dir.printParams()
        dir.printTemp()
        #area de tests
        #qm.verificarTiposOp("+",("int","float"))
        dir.printConst()
        dir.exportConst()
        dir.exportTemp()
        dir.exportFundir()
        #dir.borrar()
        return p