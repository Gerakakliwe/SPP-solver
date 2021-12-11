files = ["sppnw32.txt"]

for datafile in files:
    with open(datafile, "r") as file:  # Opening file
        print("---------------------------------")
        print(f"Working with {datafile.upper()}")
        rows_n_cols = file.readline().split()  # Reading first line with general information
        rows, cols = int(rows_n_cols[0]), int(rows_n_cols[1])  # Dividing first line into rows and cols
        print(f"There are {rows} rows and {cols} columns in file.")

        # Parsing all other data
        parsed = []
        for line in file:
            split_line = line.split()
            price = int(split_line[0])
            n = int(split_line[1])
            covered_rows = []
            for i in range(2, n + 2):
                covered_rows.append(split_line[i])

            parsed.append([price, n, covered_rows])

        sorted_by_price_asc = sorted(parsed)  # sorting by price, ascending
        sorted_by_n_asc = sorted(parsed, key=lambda x: x[1])  # sorted by quantity of items in 1 column, ascending.


        def calculations(data, sort_type):
            print("---------------------------------")
            ideal = [x for x in range(1, rows + 1)]
            working = []
            result_price = 0
            iterations = 0

            for row in data:
                iterations += 1
                if all(int(position) not in working for position in row[2]):
                    for item in row[2]:
                        working.append(int(item))
                        result_price += row[0]
                working.sort()
                # Trying to solve problem completely and find an ideal solution
                if working == ideal:
                    break

            print(f"Data was sorted by {sort_type}")
            print(f"While calculating, {iterations} iterations happened. Calculated price is {result_price}")

            # Calculating amount of not included item
            not_included = 0
            for item in ideal:
                if item not in working:
                    not_included += 1

            if not_included:
                print(f"{not_included} out of {rows} items weren't included.")
            else:
                print("All items were included. Problem solved.")


        calculations(sorted_by_price_asc, "price, ASC")
        calculations(sorted_by_n_asc, "amount in 1 column, ASC")
