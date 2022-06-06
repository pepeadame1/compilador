
from parser import *

if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser()
    env = {}

    #f = open('patito.txt','r')
    f = open('patitobackup.txt','r')
    text = str(f.read())

    try:
        tree = parser.parse(lexer.tokenize(text))
        
        
    except:
        print("fail")
