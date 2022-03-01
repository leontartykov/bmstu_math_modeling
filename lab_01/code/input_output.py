from distutils.log import error


def input_values() -> tuple:
    """
    Ввод исходных данных
    """
    left_board = 0; right_board = 0
    error_input = True
    while error_input == True:   
        left_board = input_board("left")
        right_board = input_board("right")

        if left_board >= right_board:
            print(f"\nОшибка: неверно заданы границы: левая ({left_board}), правая ({right_board})." + 
                   "Попробуйте еще раз.")
        else:
            error_input = False
    count_nodes = input_count_nodes()

    return (left_board, right_board, count_nodes)

def input_board(type_board: str) -> float:
    """
    Ввод границы отрезка
    """ 
    board = str()
    if type_board == "left":
        type_board = "левую"
    else:
        type_board = "правую"

    error_input = True
    while (error_input == True):
        board = input("Введите {} границу отрезка [x_min, x_max]: ".format(type_board))
        try:
            board = float(board)
            error_input = False
        except ValueError:
            print(f"\nОшибка: неверно введены данные ({board}). Попробуйте еще раз.")
            
    return board

def input_count_nodes() -> int:
    """
    Ввод количества узлов сетки
    """
    error_input = True
    count_nodes = str()
    while (error_input == True):
        count_nodes = input("Введите количество узлов сетки: ")
        try:
            count_nodes = int(count_nodes)
            error_input = False
            count_nodes = int(count_nodes)

            if count_nodes <= 0:
                error_input = True
                raise ValueError
        except ValueError:
            print(f"\nОшибка: неверно введены данные ({count_nodes})."+ 
                   "Попробуйте еще раз.")      

    return count_nodes
