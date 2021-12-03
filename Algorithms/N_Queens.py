import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
queens = 8
'''
The solution is gonna be stored in a list and this list
is going to be interpreted as follows:
Let n be a column number of the chessboard,
then solution[n] is the row number where the queen is
placed for that n-th column
'''
solution = [0 for x in range(queens)]
solutions = []
pad="------"
def safe(possible_x, possible_y):
    #First placed queen
    if possible_y == 0:
        return True
    #Iterate trought columns that are behind the current one
    for col in range(0, possible_y):
        #If we are on the same row as a placed queen,is not safe
        if possible_x == solution[col]:
            return False
        '''
        If we substract the row number that a previous placed queen has (solution[col])
        from the current testing row (possible_x) and that is equal to
        the current testing column (possible_y) minus the column number
        that a previous placed queen has (col), then we have an attacking
        diaogonal queen,i.e,is not safe.
        Notice that col is the column number that a previous placed queen has
        because all previous columns have a queen placed
        '''
        if abs(possible_y - col) == abs(possible_x - solution[col]):
            return False
    return True

def placeQueenOnColumn(col):
    for row in range(queens):
        #Next iteration if not safe to place a queen
        if not safe(row, col):
            continue
        else:
            #Its safe to place a queen on (row,col)
            solution[col] = row
            if col == (queens - 1):
                #We have a complete solution. Let's add it to the list
                solutions.append(solution.copy())
            else:
                #Move to the next column to check where to place the queen
                placeQueenOnColumn(col + 1)

print(f"\n\t{pad}Running the N-queens problem with {queens} queens{pad}")
placeQueenOnColumn(0)
print(f"\t{pad}There are {len(solutions)} solutions.{pad}")
while True:
    print(f"\t{pad}Input 0 to exit program{pad}")
    solution_number=int(input(f"\t{pad}Which solution number would you like to draw?{pad}\nSolution Number:"))-1
    if solution_number<0 or solution_number>92:
        break
    #Defining the chessboard (queensXqueens). Only 0
    board=np.zeros([queens,queens],dtype=int).tolist()
    i=0
    #Parsing a solution contained in one of the lists in solutions to a 2d array
    for row in solutions[solution_number]:
        board[row][i]=1
        i+=1
    #Ploting
    ax=sns.heatmap(board,linewidths=.8,cbar=False,linecolor='black',cmap='Reds',center=0.4)
    plt.show()
