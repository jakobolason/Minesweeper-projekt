bomb_field = {1: [0, 0, 0, 0, 0, 0, 0, 0, 0], 2: [0, 0, 0, 0, 0, 0, 0, 0, 0], 3: [0, 0, 0, 0, 0, 0, 0, 0, 0], \
               4: [0, 0, 0, 0, 0, 0, 0, 0, 0], 5: [0, 0, 0, 0, 0, 0, 0, 0, 0], 6: [0, 0, 0, 0, 0, 0, 0, 0, 0], \
                 7: [0, 0, 0, 0, 0, 0, 0, 0, 0], 8: [0, 0, 0, 0, 0, 0, 0, 0, 0], 9: [0, 0, 0, 0, 0, 0, 0, 0, 0]}

visual_field = {1: [0, 0, 0, 0, 0, 0, 0, 0, 0], 2: [0, 0, 0, 0, 0, 0, 0, 0, 0], 3: [0, 0, 0, 0, 0, 0, 0, 0, 0], \
              4: [0, 0, 0, 0, 0, 0, 0, 0, 0], 5: [0, 0, 0, 0, 0, 0, 0, 0, 0], 6: [0, 0, 0, 0, 0, 0, 0, 0, 0], \
                7: [0, 0, 0, 0, 0, 0, 0, 0, 0], 8: [0, 0, 0, 0, 0, 0, 0, 0, 0], 9: [0, 0, 0, 0, 0, 0, 0, 0, 0]}

def click_cell(row, column, player=True):
    cell = bomb_field[row][column]
    if player:
        if cell == 1:
            print("You clicked on a bomb, you busted!")
        else:
            print("You're okay")
    visual_field[row][column] = 1


def bombs_nearby(row, column):
    #checks row - 1: column -1, column, column +1
    #       row: column -1, column +1
    #       row +1: column -1, column, column +1    
    adjacent_cells = []
    try:
        adjacent_cells.extend(bomb_field[row-1][column-1:column+2])
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

def flood_fill(row, column):
    if bombs_nearby(row, column) != 0:
        return
    adjacent_cells = []
    for new_row in range(max(1, row-1), min(row+2, len(bomb_field)+1)):
        for new_column in range(max(1, column-1), min(column+2, len(bomb_field)+1)):
            if bomb_field[new_row][new_column] == 0 and visual_field[new_row][new_column] == 0:
                adjacent_cells.append((new_row, new_column))
    
    for new_row, new_column in adjacent_cells:
        visual_field[new_row][new_column] = 1
        print(new_row, new_column)


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
            print("*"*40)
            show_field()
            print("*"*40)
            user_row = int(input("which row would you like to click? "))
            while user_row > 8 and user_row < 0:
                user_row = int(input("You can pick a number between 0 and 8 "))
            user_column = int(input("which column? "))
            while user_column > 8 and user_column < 0:
                user_column = int(input("You can pick a number between 0 and 8 "))
            click_cell(user_row, user_column)
            flood_fill(user_row, user_column)

            cell = bomb_field[user_row][user_column]
            if cell == 1:
                print("You clicked on a bomb, you busted!")
                return busted
            else:
                continue
                

game_one = Playing()
game_one.play()




# rules: if the adjacent 8 cells do not include a bomb, show the adjacent cells \
#  if there are adjacent cells with bombs, show the amount of bombs in the area