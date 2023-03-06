def game_field():
    row_column = {1: [1, 2, 3, 4, 5, 6, 7, 8, 9], 2: [1, 2, 3, 4, 5, 6, 7, 8, 9], 3: [1, 2, 3, 4, 5, 6, 7, 8, 9], 4: [1, 2, 3, 4, 5, 6, 7, 8, 9], \
                  5: [1, 2, 3, 4, 5, 6, 7, 8, 9], 6: [1, 2, 3, 4, 5, 6, 7, 8, 9], 7: [1, 2, 3, 4, 5, 6, 7, 8, 9], 8: [1, 2, 3, 4, 5, 6, 7, 8, 9], \
                  9: [1, 2, 3, 4, 5, 6, 7, 8, 9]}

    for key in row_column.keys():
        while True:
            for number in row_column[key]:

                print("(X)".format(key=key, number=number), end=" ")
            
            print("\n")
            break

# You should be able to call cell_id on a row_column[key][column] and get the id
class Cell_id:
    def __init__(self, row, column):
        self.row = row
        self.column = column
    def __str__(self):
        return "{row}{column}".format(row=self.row, column=self.column)

# givet information on the cell, has it been pressed? Is it a bomb?
class Cell:
    def __init__(self, id, been_pressed=False, is_bomb=False):
        self.id = id
        self.been_pressed = been_pressed
        self.is_bomb = is_bomb
    
    def __repr__(self):
        return '''Cell {cellid}, it has{pressed} been pressed, and it is{bomb} a bomb'''.format(cellid=self.id, \
                                                                                        pressed="" if self.been_pressed else " not", bomb="" if self.is_bomb else " not" )
    
    def clicked(self):
        self.been_pressed = True
        if self.is_bomb:
            print("You clicked on a bomb, you busted!")
        # should check the adjacent cells 
    
    def become_bomb(self):
        self.is_bomb = True

def check_for_bombs(row, column):
    #checks row - 1: column -1, column, column +1
    #       row: column -1, column +1
    #       row +1: column -1, column, column +1
    for key, value in game_field.row_column.items():
        if key == row:
            for cell in value:
                Cell(Cell_id(key, cell))

check_for_bombs(3, 3)
cell_one = Cell(Cell_id(1,1))
print(cell_one)
cell_one.clicked()
print(cell_one)
cell_one.become_bomb()
print(cell_one)




# rules: if the adjacent 8 cells do not include a bomb, show the adjacent cells
# if there are adjacent cells with bombs, show the amount of bombs in the area