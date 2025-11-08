import numpy as np
import pandas as pd
from itertools import permutations
from itertools import combinations_with_replacement
from sklearn.model_selection import train_test_split
from top5_markov_holiday_recommendation import *
import warnings

def test_1_run_program(user, category, city, main_table, train, test):

    # Creating transition matrix, recommending category, and checking user history based on train dataset
    transition_matrix = create_transition_matrix(user, train)
    new_category = recommend_category(user, category, transition_matrix)
    user_history = create_user_history(user, train) 

    # Creating table with places ranking by age range and recommending place based on test dataset
    rating_by_age = create_rating_by_age_table(city, test)
    recommended_places  = recommend_place(user, new_category, city, test, rating_by_age, user_history)

    return new_category, recommended_places

def test_1_success_count(user):
    warnings.filterwarnings("ignore")

    # Creating main table and splitting train test dataset
    main_table = create_main_table()
    train, test = train_test_split(main_table, random_state=1, test_size=0.5, stratify=main_table[["User_Id"]])

    # Creating list of visited places in test user history
    user_history_test = create_user_history(user, test)

    success_count = 0
    total_count = 0
    
    # Running test and checking if the category was visited by the user in the test dataset
    for category in main_table["Category"].unique():
        for city in main_table["City"].unique():
            new_category, recommended_places = test_1_run_program(user, category, city, main_table, train, test)
            categories_visited_test = test["Category"][test["User_Id"] == user][test["City"] == city].unique()

            # If category and place suggested were visited, count as success
            if new_category in categories_visited_test:
                total_count += 1
                for place_id in recommended_places.keys():
                    if place_id in user_history_test:
                        success_count += 1
                        pass

    return success_count, total_count

def test_1_sampling(n_users):
    success_total = 0
    total_total = 0
    np.random.seed(1)

    # Running the test for n_users number of users
    for user in np.random.randint(1, 301, n_users):
        success_count, total_count = test_1_success_count(user)
        success_total += success_count
        total_total += total_count

    return success_total, total_total, round(success_total/total_total, 4)

if __name__ == "__main__":

    n_users = int(input("Add number of users for testing: "))
    success_total, total_total, percentage = test_1_sampling(n_users)
    print(f"""Success: {success_total}\nTotal:{total_total}\nPercentage: {percentage * 100}""")
