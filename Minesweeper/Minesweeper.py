
game_field = {1: [1, 0, 0, 0, 0, 0, 0, 0, 0], 2: [0, 1, 0, 0, 0, 0, 0, 0, 0], 3: [0, 0, 0, 0, 0, 0, 0, 0, 0], \
              4: [0, 0, 0, 0, 0, 0, 0, 0, 0], 5: [0, 0, 0, 0, 0, 0, 0, 0, 0], 6: [0, 0, 0, 0, 0, 0, 0, 0, 0], \
                7: [0, 0, 0, 0, 0, 0, 0, 0, 0], 8: [0, 0, 0, 0, 0, 0, 0, 0, 0], 9: [0, 0, 0, 0, 0, 0, 0, 0, 0]}
# for key in game_field.keys():
#     while True:
#         for number in game_field[key]:
#             print("(X)".format(key=key, number=number), end=" ")
#         print("\n")
#         break

def check_for_bombs(row, column):
    cell = game_field[row][column]
    print(cell)
    if cell == 1:
        print("You clicked on a bomb, you busted!")
    else:
        print("You're okay")

    #checks row - 1: column -1, column, column +1
    #       row: column -1, column +1
    #       row +1: column -1, column, column +1    
    adjacent_cells = game_field[row-1][column-1:column+2]
    adjacent_cells.extend(game_field[row][column-1:column+2])
    adjacent_cells.extend(game_field[row+1][column-1:column+2])
    bombs_nearby = 0
    for cell in adjacent_cells:
        if cell == 1:
            bombs_nearby += 1
    return bombs_nearby

check_for_bombs(3, 2)




# rules: if the adjacent 8 cells do not include a bomb, show the adjacent cells
# if there are adjacent cells with bombs, show the amount of bombs in the area