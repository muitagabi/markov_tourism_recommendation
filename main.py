import pandas as pd
import numpy as np
from itertools import permutations
from itertools import combinations_with_replacement

def create_main_table():

    # Loading datasets
    locations = pd.read_csv("https://raw.githubusercontent.com/gabriellecastilho/datasets/master/indonesia_tourism.csv")
    ratings = pd.read_csv("https://raw.githubusercontent.com/gabriellecastilho/datasets/master/indonesia_tourism_rating.csv")
    users = pd.read_csv("https://raw.githubusercontent.com/gabriellecastilho/datasets/master/indonesia_tourism_user.csv")

    # Merging / Joining datasets
    main_table = pd.merge(ratings, users, on='User_Id', how='inner')
    main_table = pd.merge(main_table, locations, on="Place_Id", how="inner")

    # Dropping duplicates
    main_table = main_table.drop_duplicates()

    # Creating column "Age Range"
    main_table["Age_Range"] = pd.cut(main_table['Age'], bins=[0, 17, 25, 35, 50, 65, 100], labels=['0-17', '18-25', '26-35', '36-50', '51-65', '65+'])

    # Selecting only relevant attributes
    main_table = main_table[["User_Id", "Age", "Age_Range", "Place_Id", "Place_Name", "Category", "City", "Place_Ratings", "Rating", "Price"]]

    # Sorting values by user id and ratings
    main_table = main_table.sort_values(by=["User_Id", "Place_Ratings", "Rating"], ascending=[True, False, False])

    # Reordering table index
    main_table = main_table.reset_index(drop=True)

    # Translating categories to English
    def translate_category(item):
        if item == "Taman Hiburan": return "Amusement Park"
        elif item == "Tempat Ibadah": return "Place of Worship"
        elif item == "Budaya": return "Culture"
        elif item == "Cagar Alam": return "Natural Reserve"
        elif item == "Bahari": return "Nautical"
        elif item == "Pusat Perbelanjaan": return "Shopping Center"

    main_table["Category"] = main_table[["Category"]].applymap(translate_category)

    return main_table

def create_probability_table(user, main_table):

    # Case when a new user doesn't have a history
    if user not in main_table["User_Id"].unique():

        # Creating dataframe with equal probabilities
        prob_table = pd.DataFrame()
        prob_table["Category"] = main_table["Category"].unique()
        prob_table["Probability"] = 1 / prob_table.shape[0]

    else:

        # Filtering main table by target user
        user_table = main_table[main_table["User_Id"] == user]

        # Creating dataframe with user history category count and average rating
        prob_table = pd.DataFrame()
        prob_table["Count"] = user_table["Category"].value_counts()
        prob_table["Avg_Rating"] =  user_table.groupby("Category")["Place_Ratings"].mean()
        prob_table.reset_index(inplace=True)
        prob_table = prob_table.rename(columns = {'index':'Category'})

        # Adding categories not present in user history
        for category in main_table["Category"].unique():
            if category not in prob_table["Category"].unique():
                new_row = {'Category': category, 'Count': 1, 'Avg_Rating': 1}
                prob_table.loc[len(prob_table)] = new_row

        # Calculating weighted count sum of places visited by rating
        weighted_sum = (prob_table["Avg_Rating"] * prob_table["Count"]).sum()

        # Creating and calculating column "Probability" for each category
        prob_table["Probability"] = (prob_table["Count"] * prob_table["Avg_Rating"]) /  weighted_sum

    return prob_table

def create_transition_matrix(user, main_table):

    # Calling the function create_probability_table for the categories the user has visited
    prob = create_probability_table(user, main_table)

    # Creating the categories transitions for the transition matrix
    perm = list(permutations(prob["Category"].unique(), 2))
    comb = list(combinations_with_replacement(prob["Category"].unique(), 2))
    transition_matrix = pd.DataFrame(data = perm + comb, columns = ("Category_1", "Category_2"))
    transition_matrix = transition_matrix.drop_duplicates().reset_index(drop=True)

    # Getting the probability to visit a category
    def probability(row):
        return prob["Probability"][prob["Category"] == row[1]].iloc[0]

    transition_matrix["Probability"] = transition_matrix.apply(probability, axis=1)

    return transition_matrix

def recommend_category(user, category, transition_matrix):

    np.random.seed(1)
    # Selecting a new category based on the transition matrix probabilities
    new_category = np.random.choice(transition_matrix["Category_2"][transition_matrix["Category_1"] == category].values,
                                replace=True,
                                p=transition_matrix["Probability"][transition_matrix["Category_1"] == category].values)
    return new_category

def create_rating_by_age_table(city, main_table):

    # Filtering places by target city
    places_by_city = main_table[main_table["City"] == city]

    # Selecting the necessary columns and calculating the average rating by age range
    rating_by_age = places_by_city[["Age_Range", "Place_Id", "Place_Name", "Category", "Place_Ratings", "Rating"]].groupby(["Age_Range", "Category",  "Place_Id", "Place_Name"]).mean().dropna()

    # Calculating general rating weighted by age range ratings
    rating_by_age["Final_Rating"] = (rating_by_age["Place_Ratings"] + rating_by_age["Rating"])/2

    # Dropping columns that are not needed anymore
    rating_by_age = rating_by_age.drop(columns=["Place_Ratings", "Rating"])

    # Ranking best places by rating
    rating_by_age = rating_by_age.sort_values(["Age_Range", "Final_Rating"], ascending=[True, False])
    rating_by_age.reset_index(inplace=True)

    return rating_by_age

def create_user_history(user, main_table):

    # Case when the user doesn't have a history
    if user not in main_table["User_Id"].unique():
        return []

    else:
        # Listing the id of places visited by users
        def list_locations(row):
            return list(row['Place_Id'])

        user_history = main_table.groupby('User_Id').apply(list_locations)

        # Returning only the id of places visited by target user
        return user_history[user]
    
def recommend_place(user, new_category, city, main_table, rating_by_age, user_history):

    # Case when user doesn't have a history
    if user not in main_table["User_Id"].unique():

        # Sorting options for all ages by rating
        options = rating_by_age.sort_values("Final_Rating", ascending=False)

        # Selecting best places from the category recommended
        options = options[options["Category"] == new_category]
        options = list(options["Place_Id"])

        # Finding place name
        recommended_places = {}
        for place_id in options[:5]:
            place_name = main_table["Place_Name"][main_table["Place_Id"] == place_id].iloc[0]
            recommended_places[place_id] = place_name

    else:

        # Finding the user's age range
        age_range = main_table["Age_Range"][main_table["User_Id"] == user].iloc[0]

        # Selecting options from the same age range
        options = rating_by_age[rating_by_age["Age_Range"] == age_range]

        # Selecting best places from the category recommended
        options = options[options["Category"] == new_category]
        options = list(options["Place_Id"])

        # If filters generate an empty list, remove filters
        if len(options) == 0:
            options = rating_by_age.sort_values("Final_Rating", ascending=False)
            options = list(options["Place_Id"])

        # Calculate user average spending history for the category
        avg_spending = main_table["Price"][main_table["User_Id"] == user][main_table["Category"] == new_category][main_table["Price"] != 0].mean()

        # Checking if user already visited the place or if it's too expensive
        recommended_ids = []
        for place_id in options:
            place_price = main_table["Price"][main_table["Place_Id"] == place_id].iloc[0]
            if (place_id not in user_history) and (place_price < 2 * avg_spending):
                recommended_ids.append(place_id)

        # Finding names of places
        recommended_places = {}
        for place_id in recommended_ids[:5]:
            place_name = main_table["Place_Name"][main_table["Place_Id"] == place_id].iloc[0]
            recommended_places[place_id] = place_name

    # Returning id and name for recommended place
    return recommended_places

def run_program(user, main_table, category, city):

    # Creating transition matrix for target user
    transition_matrix = create_transition_matrix(user, main_table)

    # Recommending a category for target user
    new_category = recommend_category(user, category, transition_matrix)

    # Creating table with places ranking by age range
    rating_by_age = create_rating_by_age_table(city, main_table)

    # Creating list with places visited by target user
    user_history = create_user_history(user, main_table)

    # Recommending best ranked places from category, given that user hasn't visited it yet
    recommended_places = recommend_place(user, new_category, city, main_table, rating_by_age, user_history)

    return new_category, recommended_places

if __name__ == "__main__":

    # Creating main table
    main_table = create_main_table()

    # Defining target user, city, and category of the page originating the recommendation
    # Example: User 1 is visiting the page of a museum (culture) in Jakarta

    available_users = main_table["User_Id"].unique()
    user = int(input(f"""Add User ID ({available_users.min()} to {available_users.max()}): """))
    if user not in available_users:
        print(f"""User {user} is new. No history found.""")

    available_categories = main_table["Category"].unique()
    category = input(f"""Add Category ({", ".join(available_categories)}): """)
    while category not in available_categories:
        category = input(f"""Category not found.\nAdd Category ({", ".join(available_categories)}):""")

    available_cities = main_table["City"].unique()
    city = input(f"""Add City ({", ".join(available_cities)}): """)
    while city not in available_cities:
        city = input(f"""City not found.\nAdd City ({", ".join(available_cities)}):""")

    # Running program
    new_category, recommended_places = run_program(user, main_table, category, city)

    # Printing recomendation category and place name
    print(f"""\nCategory Recommended:\n{new_category}\n\nTop Recommendations:\n{recommended_places}""")
