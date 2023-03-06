
bomb_field = {1: [0, 0, 0, 0, 0, 0, 0, 0, 0], 2: [0, 0, 0, 0, 0, 0, 0, 0, 0], 3: [0, 1, 0, 0, 0, 0, 0, 0, 0], \
              4: [0, 0, 0, 0, 0, 0, 0, 0, 0], 5: [0, 0, 0, 0, 0, 0, 0, 0, 0], 6: [0, 0, 0, 0, 0, 0, 0, 0, 0], \
                7: [0, 0, 0, 0, 0, 0, 0, 0, 0], 8: [0, 0, 0, 0, 0, 0, 0, 0, 0], 9: [0, 0, 0, 0, 0, 0, 0, 0, 0]}

visual_field = {1: [0, 0, 0, 0, 0, 0, 0, 0, 0], 2: [0, 0, 0, 0, 0, 0, 0, 0, 0], 3: [0, 0, 0, 0, 0, 0, 0, 0, 0], \
              4: [0, 0, 0, 0, 0, 0, 0, 0, 0], 5: [0, 0, 0, 0, 0, 0, 0, 0, 0], 6: [0, 0, 0, 0, 0, 0, 0, 0, 0], \
                7: [0, 0, 0, 0, 0, 0, 0, 0, 0], 8: [0, 0, 0, 0, 0, 0, 0, 0, 0], 9: [0, 0, 0, 0, 0, 0, 0, 0, 0]}

def click_cell(row, column):
    cell = bomb_field[row][column]
    if cell == 1:
        print("You clicked on a bomb, you busted!")
        return busted
    else:
        print("You're okay")
    visual_field[row][column] = 1


def bombs_nearby(row, column):
    #checks row - 1: column -1, column, column +1
    #       row: column -1, column +1
    #       row +1: column -1, column, column +1    
    adjacent_cells = []
    try:
        adjacent_cells = bomb_field[row-1][column-1:column+2]
    except KeyError:
        pass
    try:
        adjacent_cells.extend(bomb_field[row][column-1:column+2])
    except KeyError:
        pass
    try:
        adjacent_cells.extend(bomb_field[row+1][column-1:column+2])
    except KeyError:
        pass
    bombs_nearby = 0
    for cell in adjacent_cells:
        if cell == 1:
            bombs_nearby += 1
    return bombs_nearby

# show visual field
def show_field():
    for key in visual_field.keys():
        while True:
            for number in visual_field[key]:
                if number == 0:
                    print("(X)".format(key=key, number=number), end=" ")
                elif number == 1:
                    print(" {bombs} ".format(bombs=bombs_nearby(key, number)), end=" ")
                else:
                    continue
            print("\n")
            break

class Playing():
    def play(self):
        busted = False
        while not busted:
            print("*************************")
            show_field()
            print("*************************")
            user_row = int(input("which row would you like to click? "))
            while user_row > 8:
                user_row = int(input("You can pick a number between 0 and 8 "))
            user_column = int(input("which column? "))
            while user_column > 8:
                user_column = int(input("You can pick a number between 0 and 8 "))
            click_cell(user_row, user_column)

            cell = bomb_field[user_row][user_column]
            if cell == 1:
                print("You clicked on a bomb, you busted!")
                return busted
            else:
                continue
                

game_one = Playing()
game_one.play()




# rules: if the adjacent 8 cells do not include a bomb, show the adjacent cells
# if there are adjacent cells with bombs, show the amount of bombs in the area