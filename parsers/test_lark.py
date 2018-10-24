from lark import Lark, Transformer, Visitor

grammar = '''
    start: (_WS* tag _WS*)+
    tag: _WS* NAME "{" _content "}" _WS*
    _content: tag+ | TEXT
    TEXT: (WS|LETTER|DIGIT)+
    NAME: WORD
    _WS: WS

    %ignore " "

    %import common.WORD
    %import common.WS
    %import common.LETTER
    %import common.DIGIT
'''

document = '''
head{
  title{The Book}
}
body{
  chapter{
    title{Chap1}
    p{text of a book}
  }
}
'''

l = Lark(grammar)
tree = l.parse(document)
print(tree.pretty())

for node in tree.iter_subtrees():
    print(node)
