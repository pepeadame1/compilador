from sly import Lexer

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

    @_(r'\"([^""]+)\"')
    def CTESTRING(self,t):
        return t

    @_(r'\d+\.\d+')
    def CTEFLOAT(self,t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def CTEINT(self,t):
        t.value = t.value
        return t

    @_(r'\'.*\'')
    def CTECHAR(self,t):
        t.value = t.value
        return t

    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self,t):
        return t