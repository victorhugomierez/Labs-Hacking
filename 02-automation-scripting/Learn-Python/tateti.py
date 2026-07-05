from random import randrange

def display_board(board):
    # The function accepts one parameter containing the board's current status
    # and prints it out to the console.
    for row in board:
        print("+-------+-------+-------+")
        print("|       |       |       |")
        print(f"|   {row[0]}   |   {row[1]}   |   {row[2]}   |")
        print("|       |       |       |")
    print("+-------+-------+-------+")


def enter_move(board):
    # The function accepts the board's current status, asks the user about their move, 
    # checks the input, and updates the board according to the user's decision.
    while True:
        try:
            move = int(input("Enter your move: "))
            if move < 1 or move > 9:
                print("Invalid move! Choose a number between 1 and 9.")
                continue
            
            # Mapeo de número 1-9 a coordenadas de la matriz [row][column]
            row = (move - 1) // 3
            col = (move - 1) % 3
            
            # Si la casilla contiene un número (está libre), se puede jugar
            if board[row][col] not in ['X', 'O']:
                board[row][col] = 'O'
                break
            else:
                print("That square is already occupied! Try another one.")
        except ValueError:
            print("Please enter a valid integer.")


def make_list_of_free_fields(board):
    # The function browses the board and builds a list of all the free squares; 
    # the list consists of tuples, while each tuple is a pair of row and column numbers.
    free_squares = []
    for r in range(3):
        for c in range(3):
            if board[r][c] not in ['X', 'O']:
                free_squares.append((r, c))
    return free_squares


def victory_for(board, sign):
    # The function analyzes the board's status in order to check if 
    # the player using 'O's or 'X's has won the game
    
    # Comprobar Filas
    for r in range(3):
        if board[r][0] == board[r][1] == board[r][2] == sign:
            return True
            
    # Comprobar Columnas
    for c in range(3):
        if board[0][c] == board[1][c] == board[2][c] == sign:
            return True
            
    # Comprobar Diagonales
    if board[0][0] == board[1][1] == board[2][2] == sign:
        return True
    if board[0][2] == board[1][1] == board[2][0] == sign:
        return True
        
    return False


def draw_move(board):
    # The function draws the computer's move and updates the board.
    free_fields = make_list_of_free_fields(board)
    
    if free_fields:
        # Selecciona una tupla (row, col) al azar de la lista de campos libres
        random_index = randrange(len(free_fields))
        row, col = free_fields[random_index]
        board[row][col] = 'X'


# --- CONFIGURACIÓN E INICIO DEL JUEGO ---

# Inicializar el tablero en su estado base
board = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Regla del escenario: La máquina siempre toma el centro ('X' en la casilla 5) en su primer turno
board[1][1] = 'X'

# Mostrar el tablero con el primer movimiento de la máquina
display_board(board)

# Bucle principal de juego
while True:
    # --- TURNO DEL USUARIO ---
    enter_move(board)
    display_board(board)
    
    if victory_for(board, 'O'):
        print("You won!")
        break
        
    if not make_list_of_free_fields(board):
        print("It's a tie!")
        break

    # --- TURNO DE LA COMPUTADORA ---
    print("Computer's move:")
    draw_move(board)
    display_board(board)
    
    if victory_for(board, 'X'):
        print("Computer won!")
        break
        
    if not make_list_of_free_fields(board):
        print("It's a tie!")
        break