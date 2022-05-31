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
        return p

    @_('ID "(" ")" ";"')
    def void(self,p):
        return p

    @_('ID "(" void2 ";"')
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

    @_('ID ")"')
    def lectura2(self,p):
        return p

    @_('ID "," lectura2')
    def lectura2(self,p):
        return p

    @_('ESCRIBE "(" escritura2')
    def escritura(self,p):
        return p

    @_('expresion ")" ";"')
    def escritura2(self,p):
        return p

    @_('expresion "," escritura2')
    def escritura2(self,p):
        return p

    @_('CTESTRING ")" ";"')
    def escritura2(self,p):
        return p

    @_('CTESTRING "," escritura2')
    def escritura2(self,p):
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
        return p

    @_('">" exp')
    def expresion2(self,p):
        return p

    @_('"<" ">" exp')
    def expresion2(self,p):
        return p

    @_('"=" "=" exp')
    def expresion2(self,p):
        return p

    @_('SI "(" expresion ")" ENTONCES bloque SINO bloque')
    def decision(self,p):
        return p

    @_('SI "(" expresion ")" ENTONCES bloque')
    def decision(self,p):
        return p

    @_('MIENTRAS "(" expresion ")" HAZ bloque')
    def condicional(self,p):
        return p

    @_('DESDE ID "=" exp HASTA exp HACER bloque')
    def nocondicional(self,p):
        return p

    @_('termino')
    def exp(self,p):
        return p

    @_('termino "+" exp')
    def exp(self,p):
        return p

    @_('termino "-" exp')
    def exp(self,p):
        return p

    @_('factor')
    def termino(self,p):
        return p

    @_('factor "*" termino')
    def termino(self,p):
        return p

    @_('factor "/" termino')
    def termino(self,p):
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
        return p

    @_('CTEINT')
    def varcte(self,p):
        return p

    @_('CTEFLOAT')
    def varcte(self,p):
        return p

    @_('CTESTRING')
    def varcte(self,p):
        return p

    @_('CTECHAR')
    def varcte(self,p):
        return p

    @_('')
    def fin(self,p):
        print("codigo valido")
        dir.print()
        #dir.test()

        #area de tests
        qm.verificarTiposOp("+",("int","float"))


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
