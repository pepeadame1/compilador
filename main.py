from sly import Lexer
from sly import Parser
from parseFunctions import *

dir = fundir()
qm = quadrupleManager()

class BasicLexer(Lexer):

    tokens = {SI, SINO, PROGRAMA, ESCRIBE, VAR, INT, FLOAT, STRING, CHAR, DATAFRAME, ID, CTESTRING, CTEINT, CTEFLOAT, CTECHAR, FUNCION, REGRESA, LEE, CARGAARCHIVO, RUTA, ENTONCES, MIENTRAS, HAZ, DESDE, HASTA, HACER, PRINCIPAL,VOID}
    ignore = '\t'

    literals = {';',',',':','{','}','=','(',')','+','-','*','/','<','>','[',']'}

    #definiciones
    SINO = r'sino'
    SI = r'si'
    PROGRAMA = r'programa'
    PRINCIPAL = r'principal'
    ESCRIBE = r'escribe'
    VAR = r'var'
    INT = r'int'
    FLOAT = r'float'
    CHAR = r'char'
    STRING = r'string'
    DATAFRAME = r'dataframe'
    HACER = r'hacer'
    HASTA = r'hasta'
    DESDE = r'desde'
    HAZ = r'haz'
    MIENTRAS = r'mientras'
    ENTONCES = r'entonces'
    RUTA = r'ruta'
    CARGAARCHIVO = r'cargaArchivo'
    LEE = r'lee'
    REGRESA = r'regresa'
    FUNCION = r'funcion'
    VOID = r'void'



    @_(r'\n')
    def newline(self,t):
        pass

    @_(r' ')
    def space(self,t):
        pass

    @_(r'"[^"]*"')
    def CTESTRING(self,t):
        return t

    @_(r'\d+\.\d+')
    def CTEFLOAT(self,t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def CTEINT(self,t):
        t.value = float(t.value)
        return t

    @_(r'\'.*\'')
    def CTECHAR(self,t):
        t.value = float(t.value)
        return t

    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self,t):
        return t

class BasicParser(Parser):
    tokens = BasicLexer.tokens

    precedence = (
        ('left','+','-'),
        ('left','*','/'),
    )

    @_('catcherprograma ";" programa')
    def preprograma(self,p):
        return p

    @_("PROGRAMA ID")
    def catcherprograma(self,p):
        dir.addProgram(p[1])
        #dir.print()
        return p

    @_(' programa2 PRINCIPAL "(" ")" bloque fin')
    def programa(self,p):
        return p

    @_(' PRINCIPAL "(" ")" bloque fin')
    def programa(self,p):
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
        #dir.checarTablaScope()
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

    @_('ID "[" CTEINT "]"')#aqui notar que es un arreglo
    def var3(self,p):
        return p

    @_('ID "[" CTEINT "]" "," var3')#aqui notar que es un arreglo
    def var3(self,p):
        return p

    @_('varhelp var3')
    def var3(self,p):
        return p

    @_('varhelp')
    def var3(self,p):
        return p

    @_('ID ","')
    def varhelp(self,p):
        dir.agregarVariable(p[0])
        #dir.print()

    @_('ID')
    def varhelp(self,p):
        dir.agregarVariable(p[0])
        #dir.print()
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

    @_('tipo ID')
    def paramhelp(self,p):
        dir.agregarVariable(p[1])
        return p

    @_('funcshelper funcs2')
    def funcs(self,p):
        #dir.agregarFunc(p[2])
        #dir.print
        return p

    @_('FUNCION tipo ID')
    def funcshelper(self,p):
        dir.setscope(p[2])
        dir.setreturn(dir.currentType)
        dir.agregarFunc(p[2])
        return p

    '''
    @_('FUNCION ID funcs2')##no recuerdo para que pusimos esto
    def funcs(self,p):
        dir.agregarFunc(p[1])
        dir.print
        return p
    '''

    @_('"(" param ")" funcs3')
    def funcs2(self,p):
        return p

    @_('"(" ")" funcs3')
    def funcs2(self,p):
        return p

    @_('vars bloque')
    def funcs3(self,p):
        return p

    @_('bloque')
    def funcs3(self,p):
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
        print("lo que vamos a asignar")
        print(leftO)
        print("tipo:")
        print(leftT)
        tipoId = dir.getVariableType(p[0])
        if qm.verificarTiposOp('=',(leftT,tipoId)):
            qm.pushQuadruple('=',leftO,"",p[0])
        else:
            print("type mismatch")
        return p

    @_('ID "(" ")" ";"')#creo que aqui
    def void(self,p):
        return p

    @_('ID "(" void2 ";"')#creo que aqui
    def void(self,p):
        return p

    @_('expresion ")"')
    def void2(self,p):
        return p

    @_('expresion "," void2')
    def void2(self,p):
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
        if dir.vairableExists(p[0]):#verificar que exista el id
            qm.pushQuadruple('LEE',"","",p[0])
        return p

    @_('ESCRIBE "(" escritura2')
    def escritura(self,p):
        return p

    @_('escritura3 ")" ";"')
    def escritura2(self,p):
        return p

    @_('escritura3 "," escritura2')
    def escritura2(self,p):
        return p

    @_('escritura4 ")" ";"')
    def escritura2(self,p):
        return p

    @_('escritura4 "," escritura2')
    def escritura2(self,p):
        return p

    @_('expresion')
    def escritura3(self,p):#se crea el cuadruplo para escribir una expresion
        
        exp = qm.popPilaO()
        tipo = qm.popPilaT()

        print(qm.popPilaT())
        qm.pushQuadruple("ESCRIBE","","",exp)
        return p

    @_('CTESTRING')
    def escritura4(self,p):#se crea el cuadruplo para escribir un string
        qm.pushQuadruple("ESCRIBE","","",p[0])

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
        return p

    @_('">" exp')
    def expresion2(self,p):
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
            qm.pushAvail(qm.resultCounter())
            qm.pushQuadruple('==',leftO,rightO,qm.resultCounter())
            qm.pushPilaO(qm.resultCounter())
            qm.pushPilaT(resultT)
            qm.resultAdd()
        else:
            print("type mismatch")
        return p

    @_('decision1 ENTONCES bloque decision2 SINO bloque')
    def decision(self,p):
        end =qm.popPSaltos()
        cont = qm.quadCount()
        print(end)
        print(cont)
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
        print("ifffffff")
        tipo = qm.popPilaT()
        #print(qm.popPilaO())
        #print(qm.popPilaO())
        #print(qm.popAvail())
        if tipo != "bool":
            print("type mismatch")
        else:
            exp = qm.popPilaO()
            qm.pushQuadruple("GotoF",exp,"","")
            cont = qm.quadCount()
            qm.pushPSaltos(cont-1)
        print("end iffffff")
        return p
    
    @_('')
    def decision2(self,p):
        qm.pushQuadruple("GOTO","","","_")
        
        false = qm.popPSaltos()
        cont = qm.quadCount()
        qm.pushPSaltos(cont - 1)
        print('falseEeeeeeee')
        print(false)
        print(cont)
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
        if expT == bool:
            result = qm.popPilaO()
            qm.pushQuadruple("GotoF",result,"","")
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


    @_('DESDE ID "=" exp HASTA exp HACER bloque')
    def nocondicional(self,p):
        return p

    @_('termino validatipos1')
    def exp(self,p):
        return p

    @_('')
    def validatipos1(self,p):
        #print("validatipos")
        print(qm.topPOper())
        if qm.topPOper() == '+' or qm.topPOper() == '-':
            rightO = qm.popPilaO()
            rightType = qm.popPilaT()
            leftO = qm.popPilaO()
            leftType = qm.popPilaT()
            operator = qm.popPOper()
            if qm.verificarTiposOp(operator,(rightType,leftType)):
                resultT = qm.regresaTipoCuboSemantico(operator,(rightType,leftType))
                qm.pushAvail(qm.resultCounter())
                qm.pushQuadruple(operator,leftO,rightO,qm.resultCounter())#falta entender result
                qm.pushPilaO(qm.resultCounter())#falta entender result
                qm.pushPilaT(resultT)
                qm.resultAdd()
            else:
                print("type mismatch")
        return p

    @_('')
    def validatipos2(self,p):
        
        #print("validatipos")
        print(qm.topPOper())
        if qm.topPOper() == '*' or qm.topPOper() == '/':
            rightO = qm.popPilaO()
            rightType = qm.popPilaT()
            leftO = qm.popPilaO()
            leftType = qm.popPilaT()
            operator = qm.popPOper()
            print("rightO")
            print(rightO)
            print("rightType")
            print(rightType)
            print("leftO")
            print(leftO)
            print("leftType")
            print(leftType)
            print("operator")
            print(operator)
            if qm.verificarTiposOp(operator,(rightType,leftType)):
                resultT = qm.regresaTipoCuboSemantico(operator,(rightType,leftType))
                qm.pushAvail(qm.resultCounter())
                qm.pushQuadruple(operator,leftO,rightO,qm.resultCounter())#falta entender result
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
        return p

    @_('CTEFLOAT')
    def varcte(self,p):
        qm.pushPilaO(p[0])
        qm.pushPilaT('float')
        return p

    @_('CTESTRING')
    def varcte(self,p):
        qm.pushPilaO(p[0])
        qm.pushPilaT('string')
        return p

    @_('CTECHAR')
    def varcte(self,p):
        qm.pushPilaO(p[0])
        qm.pushPilaT('char')
        return p

    @_('')
    def fin(self,p):
        print("codigo valido")
        dir.print()
        #dir.test()
        qm.print()
        #area de tests
        #qm.verificarTiposOp("+",("int","float"))


        dir.borrar()
        return p


if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser()
    env = {}

    f = open('patito.txt','r')
    text = str(f.read())

    '''for tok in lexer.tokenize(text):
        print('type=%r, value=%r' % (tok.type, tok.value))
'''
    #print(text)
    try:
        tree = parser.parse(lexer.tokenize(text))
        #print(tree)
        
    except:
        print("fail")
