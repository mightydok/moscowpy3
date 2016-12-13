# encoding: utf-8

gorod = 'москва'

letter = -1
next_gorod_letter = gorod[letter]
print('1 ' + next_gorod_letter)

while next_gorod_letter in 'ъь':
    letter -= 1
    next_gorod_letter = gorod[letter]
    print('2 ' + next_gorod_letter)

print('3 ' + next_gorod_letter)
