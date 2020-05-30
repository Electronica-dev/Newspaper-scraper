# This is a text comparing program. It will return the names of the words which are common in two texts. The reason it's named as tablet is for easy access from the command line.
import sys, re

# text-one and text-two should ALWAYS be enclosed in commas.
if len(sys.argv) < 3:
    print('Usage: py tablet.py [text-one] [text-two] - copy phrase text')
    sys.exit()


def remove(text):
    # pattern to remove commas and newlines
    pattern = re.compile('[a-zA-Z ]+')

    # pattern to remove 'and' and the space after commas. (pun intended)
    remove_and = re.compile(' and |, ')

    # an inline expression to findall after removing whitespaces at the beginning and end and then passing that to remove_and to replace the 'and' with a comma.
    return pattern.findall(remove_and.sub(',', text.strip()))


list_one = remove(sys.argv[1])
list_two = remove(sys.argv[2])

#converting list to set
set_one = set(list_one)
set_two = set(list_two)
num=0

if len(set_one.intersection(set_two)) > 0:
    set=set_one.intersection(set_two)
    print('\nThe common ingredients are: ')
    for ele in set:
        num = num + 1
        print('\n'+str(num)+'.'+ele)
elif len(set_one.intersection(set_two)) == len(set_one):
    print('Medicines are exactly same.')
else:
    print('No common elements.')
