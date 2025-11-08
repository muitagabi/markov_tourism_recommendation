import numpy as np
import pandas as pd
from itertools import permutations
from itertools import combinations_with_replacement
from sklearn.model_selection import train_test_split
from top5_markov_holiday_recommendation import *
import warnings

def test_2_run_program(): 

  # Creating main table and splitting train test dataset
  main_table = create_main_table()

  # Set the random seed based on current time
  np.random.seed(int(time.time()))
  
  # Select a random existing user's information
  random_user = main_table.sample(n=1).iloc[0]

  # Fetch User_Id, Age_Range, Category, City of Random User
  random_user_id,random_user_age,random_user_category,random_user_city = random_user['User_Id'],random_user['Age_Range'],random_user['Category'],random_user['City']

  new_category, recommended_places = run_program(random_user_id, main_table, random_user_category, random_user_city)

  # Filter test users based on criteria
  test_users = main_table['User_Id'][(main_table['User_Id'] != random_user_id) &
                                    (main_table["Category"] == new_category) &
                                    (main_table["City"] == random_user_city) &
                                    (main_table["Age_Range"] == random_user_age)].unique()

  # Initialize a counter
  counter = 0

  # Iterate through test_users
  for user in test_users:
      # Get the unique places for the current user
      user_places = main_table[main_table["User_Id"] == user]["Place_Name"].unique()

      # Check if any recommended place exists in the user's unique places
      for place_id, place_name in recommended_places.items():
          if place_name in user_places:
              counter += 1
              break  # Break the inner loop as we've found a match
  # Calculate the ratio
  if len(test_users) > 0:
    ratio = counter / len(test_users)
  else:
    ratio = 0

  # Return the values
  return counter, len(test_users),round((ratio*100),2)


if __name__ == "__main__":
  
  n_users = int(input("Add number of users for testing: "))

  users_visited = 0
  users_total = 0
  ratio = []
  for i in range(n_users):
    visited_user,total_user,ratio_user = test_2_run_program()
    users_visited += visited_user
    users_total += total_user
    ratio.append(ratio_user)

  if n_users > 0:
    average_ratio = sum(ratio) / n_users
  else:
    average_ratio = 0

  print(f"""Success: {users_visited}\nTotal: {users_total}\nPercentage: {average_ratio :.2f}%""")
  
  



      
