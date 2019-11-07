
"""Import Libraries"""

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import json
import re
import numpy as np

"""Parse pinterest board for all saved recipes"""

print('First lets find out what recipes we need to find ingredients for, sit tight!')

print('----------------------------------------------------------------------')

# Insert your pinterest board URL here, the script will do the rest
url =''

page = requests.get(url)

soup = bs(page.text,'lxml')

"""Format pinterest board into list to index and find all the recipes used in the board"""

output = soup.find('script', type="application/json")

clean = re.compile('<.*?>')

output = re.sub(clean,"",str(output))

output = json.loads(output)

finder = output['resources']['data']['ReactBoardFeedResource']

finder = str(finder).split(':')[0]

finder = str(finder).replace("{","")

finder = str(finder).replace ("'","")

finder = str(finder)

top = output['resources']['data']['ReactBoardFeedResource'][finder]['data']['board_feed']

counter = 0

found_recipes = []

print(' ')

print(' ')

print('Looks like we found these recipes....')

print('--------------------------------------------')

for x in top:
  my_recipe = top[counter]['rich_metadata']['title']


  found_recipes.append(my_recipe)

  counter = counter + 1


for x in found_recipes:
  print(x)


print('----------------------------')

print(' ')

print(' ')

print('Getting ingredients!')

print('----------------------------')

print(' ')

print(' ')


"""Feed recipe names into API to get recipe ID's"""

url = 'https://api.spoonacular.com/recipes/search?'
key = '5b34fb8278da4f40bab3590f5b6d77bf'

ids = []

number_of_results_to_return = 1

# get id of each recipe to then get ingredients for
for recipe in found_recipes:

  isvalid = False

  while not isvalid:

    try:
      response = requests.get(url+
                   'query='+str(recipe)+
                   '&number='+str(number_of_results_to_return)+
                  '&apiKey=' + str(key))

      json_data = json.loads(response.text)

      found_id = json_data['results'][0]['id']

      ids.append(found_id)

      isvalid = True

    except:
      recipe = str(recipe.rsplit(" ", 1)[0])


"""Feed Recipe ID's into API to get ingredients list"""

url = 'https://api.spoonacular.com/recipes/'

ingredients = []

for x in ids:
  response = requests.get(url+str(x)+'/ingredientWidget.json?apiKey='+str(key))

  json_data = json.loads(response.text)

  counter = 0

  for x in json_data['ingredients']:
    name = json_data['ingredients'][counter]['name']
    unit = json_data['ingredients'][counter]['amount']['us']['unit']
    value = json_data['ingredients'][counter]['amount']['us']['value']

    counter = counter + 1

    final = str(value) + " " + str(unit) + " " + str(name)

    ingredients.append(final)

"""Combine ingredients"""

# Find unique ingredients

unique_ingredients = []
ingredients_array = []

final_consolidated_ingredients = []

for x in ingredients:
  name = str(x).split(" ",1)[1]
  ingredients_array.append(name)

  set(unique_ingredients)

  if name not in unique_ingredients:
    unique_ingredients.append(name)




# Now that we have the names of all the unique ingredients, we need to find all of the occurrences of each ingredient in the ingredients list
ingredients_array = np.array(ingredients_array)


for item in unique_ingredients:
  searchval = str(item)

  matches = np.where(ingredients_array == searchval)[0]



  # Set a list to refresh every time we reach a new unique ingredient
  consolidated = []

  # Set the counter to 0, as this will be the tracker for number of things to add (2 cloves of garlic)
  counter = 0

  number_of_matches_found = len(matches)

  a_number = 1

  # Now that we know where the matches are, we need to combine the numbers in front of each matched description to get a consolidated list

  for x in matches:
    # Grab all of the items in the list to count up the counter variable to sum all of the amounts of the item
    while a_number < number_of_matches_found:
      food = ingredients[x]

      number = float(str(food).split(" ",1)[0])

      counter = counter + number

      a_number = a_number + 1

  # Grab the final item in the list and get the final count
  food = ingredients[x]

  number = float(str(food).split(" ",1)[0])

  counter = counter + number

  # Format the final item to get the final ingredient to add to the final consolidated list

  description = str(food).split(" ",1)[1]

  final_item = str(counter) + " " + str(description)



  final_consolidated_ingredients.append(final_item)



"""Display final ingredients needed"""

print('Ingredients needed:')
print('---------------------------------------------------')

for item in final_consolidated_ingredients:
  print(item)


input()
