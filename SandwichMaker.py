import pyinputplus as pyip

totalCost = 0

# Storing cost of items in a dictionary as values.
costBread = {'Wheat':10, 'White':8, 'Sourdough':12}
costProtein = {'Chicken':30, 'Turkey':50, 'Ham':40, 'Tofu':20}
costCheese = {'Cheddar':10, 'Swiss':15, 'Mozzarella':10}

# List of choices.
breadType = ['Wheat', 'White', 'Sourdough']
proteinType = ['Chicken', 'Turkey', 'Ham', 'Tofu']
cheeseType = ['Cheddar', 'Swiss', 'Mozzarella']
flavourList = ['Mayo', 'Mustard', 'Lettuce', 'Tomato']

# Menus to choose from the choices and to also update the cost variable.
chooseBread = pyip.inputMenu(choices=breadType, numbered=True)
print('Chosen Bread:', chooseBread,'\n')
for k,v in costBread.items():
    if k == chooseBread:
        totalCost += v

chooseProtein = pyip.inputMenu(choices=proteinType, numbered=True)
print('Chosen Protein:', chooseProtein,'\n')
for k,v in costProtein.items():
    if k == chooseProtein:
        totalCost += v

# Yes or No prompt for cheese.
choiceCheese = pyip.inputYesNo(prompt='Do you want cheese?\n')
if choiceCheese == 'yes':
    chooseCheese = pyip.inputMenu(choices=cheeseType, numbered=True)
    print('Chosen Cheese:', chooseCheese,'\n')
for k,v in costCheese.items():
    if k == chooseCheese:
        totalCost += v

# Add ons
for flavour in flavourList:
    choiceFlavour = pyip.inputYesNo(f'Do you want {flavour}?\n')
    if choiceFlavour == 'yes':
        print(f'{flavour} added.')
        continue

noOfSandwiches = pyip.inputInt(prompt='How many sandwiches do you want?\n')
print('Total cost: ', totalCost*noOfSandwiches)
