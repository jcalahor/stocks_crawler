from parser_util import Parser


buffer = "hola hola yo bien y tu, hola como estas tu en tu dia yo estoy bien carajo"

p = Parser(buffer)
p.move_to('estas')
word = p.extract_between('en', 'yo')
print (word)



