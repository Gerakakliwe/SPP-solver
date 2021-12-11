import random
import pandas as pd
import matplotlib.pyplot as plt

###########
# PARSING #
###########

with open("sppnw32.txt", "r") as initial_data_file:  # Opening file
    print("---------------------------------")
    rows_n_cols = initial_data_file.readline().split()  # Reading first line with general information
    rows, cols = int(rows_n_cols[0]), int(rows_n_cols[1])  # Dividing first line into rows and cols
    print(f"There are {rows} rows and {cols} columns in file.")
    print("---------------------------------")

    lines = initial_data_file.readlines()
    initial_data_file.close()

with open("result.txt", "r+") as result_file:
    result_file.truncate(0)  # cleaning result file before writing in it
    result_file.close()


def do_hill_climbing(parsed_data):
    random.shuffle(parsed_data)
    # Preparing all other data to work with
    parsed = []
    for line in parsed_data:  # take each line in file
        split_line = line.split()  # splitting for convenience
        price = int(split_line[0])  # getting price
        n = int(split_line[1])  # getting quantity
        covered_rows = []  # list of items that each line covers
        for i in range(2, n + 2):
            covered_rows.append(split_line[i])

        parsed.append([price, n, covered_rows])  # In parsed we basically have all the data

    # We now have indices for each line of data
    parsed_w_indices = [(idx, item) for idx, item in enumerate(parsed, start=1)]

    ####################
    # INITIAL SOLUTION #
    ####################

    initial_solution_idx = []  # List of rows for initial solution
    initial_solution_price = 0  # Price of initial solution

    to_complete = []  # list for adding items from rows
    completed = [x for x in range(1, rows + 1)]  # Ideal list with which we are going to compare list to_complete

    for row in parsed_w_indices:
        # If all items in row are not in list - add those items
        if all(int(position) not in to_complete for position in row[1][2]):
            print(f"added row with id {row[0]}, pice {row[1][0]} and items: {row[1][2]}")
            for item in row[1][2]:
                to_complete.append(int(item))  # add every item in row

            initial_solution_idx.append(row[0])  # add index of added row
            initial_solution_price += row[1][0]  # add price of added row

        # sort after every appending to compare with ideal solution
        to_complete.sort()

        # If all rows are included - stop
        if to_complete == completed:
            break
    print("---------------------------------")
    print(f"initial solution indices are: {initial_solution_idx}")
    print(f"initial solution price is: {initial_solution_price}")

    #################
    # HILL CLIMBING #
    #################

    deleted = []  # list for items that we deleted and trying to find
    working_idx = initial_solution_idx.copy()  # result indices
    temp_idx = initial_solution_idx.copy()
    working_price = initial_solution_price  # price that we are trying to make lower
    temp_price = initial_solution_price  # temp price for comparing with starting price

    for index in initial_solution_idx:  # for every row that we used in initial solution
        print("---------------------------------")
        print(f"We are removing {index} row, it's price was {parsed_w_indices[index - 1][1][0]}")
        temp_idx.remove(index)  # remove row from solution
        temp_price -= parsed_w_indices[index - 1][1][0]  # subtracting price of row
        for item in parsed_w_indices[index - 1][1][2]:  # for every item in row that is being removed
            deleted.append(int(item))  # adding item that we are going to delete to deleted list
            to_complete.remove(int(item))  # removing that item from to_complete list
        print(f"This row had such items as: {deleted}")

        for row in parsed_w_indices:  # for every next row in parsed data
            #  if it's not the same row and all items in row are deleted list - add this row
            if row[0] != index and all(int(position) in deleted for position in row[1][2]):
                print(f"WE FOUND ROW TO ADD, it's row {row[0]} with price {row[1][0]} and items {row[1][2]}")
                temp_idx.append(row[0])  # add row index to temporary variable
                temp_idx.sort()  # sort indices to better understanding
                temp_price += row[1][0]  # adding price of new row
                for item in row[1][2]:
                    to_complete.append(int(item))  # add each item to list
                    to_complete.sort()  # sort list to compare properly
                    deleted.remove(int(item))  # remove item from list of deleted items

            if to_complete == completed:  # check if we completed our list with items and if yes then
                print(f'prior price was {working_price}, and new price is {temp_price}')
                if working_price > temp_price:  # check, maybe new solution worse then previous
                    working_idx = temp_idx.copy()  # if solution is better - change list of indices
                    working_price = temp_price  # and change new price
                    print("New solution is better, we will take this", working_price)
                    print(f"Indices now are: {temp_idx}")
                else:
                    temp_idx = working_idx.copy()  # if not - return to previous state of indices
                    temp_price = working_price  # and return to prievious price
                    print("New solution cost more, we don't agree")
                break

        if to_complete != completed:  # if after checking all rows we didn't find needed items for completing list
            print("There is no row with such items to fill, return deleted")
            # returning deleted previously
            for item in deleted:
                to_complete.append(int(item))
            to_complete.sort()
            # clearing list of deleted items
            deleted.clear()
            # readding index of row
            temp_idx = working_idx.copy()
            print(f"row index was retunred: {temp_idx}")
            # readding price of that row
            temp_price = working_price
            print("price was returned to", temp_price)

    print("---------------------------------")
    print("initial idx: ", initial_solution_idx)
    print("initial price: ", initial_solution_price)
    print("result inx:", working_idx)
    print("result price:", working_price)
    print("---------------------------------")

    print("Items in each new row INITIAL SOLUTION:")
    for index in initial_solution_idx:
        print(parsed_w_indices[index - 1])
    print("---------------------------------")

    print("Items in each new row AFTER USING HILL CLIMBING:")
    for index in working_idx:
        print(parsed_w_indices[index - 1])
    print("---------------------------------")

    with open("result.txt", "a") as result_file:
        result_file.write(str(initial_solution_price) + "," + str(working_price) + "\n")  # add prices to result file
        result_file.close()


if __name__ == "__main__":

    for i in range(500):  # 500 iterations
        do_hill_climbing(lines)

    data = pd.read_csv("result.txt", sep=",", header=None)  # take the file to visualize
    data.columns = ["initial", "hillclimbing"]  # column names

    the_best = min(data.hillclimbing)  # find the best one to print it in the console
    print(f"The best value is {the_best}")

    plt.scatter(range(500), data.initial, color="red")  # red dots for initial price
    plt.scatter(range(500), data.hillclimbing, color="green")  # green dots for prices after hill climbing
    plt.ylabel("red - initial, green - hill climbing")
    plt.xlabel("iterations")
    plt.show()  # draw everything
