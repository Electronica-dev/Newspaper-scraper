# This is a text comparing program. It will return the names of the words which are common in two texts. The reason it's
# named as tablet is for easy access from the command line.

import sys

# text-one and text-two should ALWAYS be enclosed in commas.
if len(sys.argv) < 3:
    print('Usage: py tablet.py [text-one] [text-two]')
    sys.exit()


# function to remove comma and 'and'
def remove(rawText):
    splitText = rawText.replace('and', ',').split(',')
    List = [ele.strip() for ele in splitText]
    return List


list_one = remove(sys.argv[1])
list_two = remove(sys.argv[2])

set_one = set(list_one)
set_two = set(list_two)
num = 0

while len(set_one.intersection(set_two)) > 0:
    Set = set_one.intersection(set_two)
    if len(Set) == 1:
        print('\nThe common ingredient is: ' + '\n1. ' + str(*Set))
        break
    elif len(Set) > 1:
        print('\nThe common ingredients are: ')
        for ele in Set:
            num = num + 1
            print('\n'+str(num)+'.'+ele)
        break
    elif len(set_one.intersection(set_two)) == len(set_one):
        print('Medicines are exactly same.')
        break
if len(set_one.intersection(set_two)) == 0:
    print('No common elements.')
