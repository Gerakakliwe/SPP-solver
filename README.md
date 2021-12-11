# SPP-solver
Set partitioning problem is being solved in this repo. Programming language that was used - Python 3.10.

Main information about structure of files and files themselves located in the OR-library (http://people.brunel.ac.uk/~mastjjb/jeb/orlib/sppinfo.html)

File with data named sppmw32.txt was chosen because it's the smallest one from the whole bunch of files in the OR-library repository.

First try - head-on_solution.py. It doens't have any optimisation, it's just a simple greedy algorithm. I tried to optimize it a little bit, using sorting (by lowest price and by the biggest amount of items in 1 row)
        
Second try - hill_climbing.py. In this one I've implemented Hill climbing (HC) algorithm. Firstly - we have to find initial solution. For that we use previous greedy algorithm without any sortings. After getting that initial solution, HC takes one row from it, removes it and it's items from the solution list and tries to fill the gaps with another rows and items. After that it checks new solution for the price difference and if new solution gave us better price - it's our choise. THe same thing we try to do with every row of initial solution.

Third try - random_hill_climbing.py. It's basically the same one as the last one, but data is randomed every time. Also I used multistart technique there. After running this file, 500 iterations happens, every iteration with completely random data for start. All those iterations are getting written into the result file result.txt. After all that, scatter diagramm is being built. On that scatter plot you can see red and green dots. Red dots - results before using hill climbing. Green - results after using the hill climbing.

![изображение](https://user-images.githubusercontent.com/54077352/145688837-15bd004e-11d1-4740-8dc5-320aa5440ad3.png)

Feel free to use information and code from this repo in your projects!
