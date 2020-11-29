import copy
import numpy

class Game:

    """
    Klasa reprezentująca grę w kółko i krzyżyk w wersji 15x15
    """

    def __init__(self):
        self.letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
        self.board = [['.' for column in range(15)] for row in range(15)]
        self.winner = None
        self.players = ['X', 'O']
    
    def main(self):
        """
        Metoda uruchamiająca grę w kółko i krzyżyk
        """

        print('------------------------')
        print('Tic tac toe 15x15 version')

        self.printBoard()

        while self.isMovesLeft(self.board) and self.checkWinner(self.board) == None:

            move = input('Choose your move (A1, B7 etc.): ')
            self.updateBoard(move, self.players[0])
            if self.checkWinner(self.board) != None:
                break

            computer_move = self.findBestMove()
            print(f'My move is: {computer_move}')
            

            self.updateBoard(computer_move, self.players[1])
            self.printBoard()
            print('-------------------------------------------')

        self.winner = self.checkWinner(self.board)
        self.printBoard()
        print(f'The winner is {self.winner} player!')
        return

    def printBoard(self):
        """
        Metoda wyświetlająca planszę
        """

        print("    ",end="")
        for letter in self.letters:
            print(letter, end="  ")
        print("")
        for i in range(15):
            if i < 9:
                print(" ",end = "")
                print(i+1,end="  ")
                for j in range(15):
                    print(self.board[i][j], end="  ")
                print("")
            else:
                print(i+1,end="  ")
                for j in range(15):
                    print(self.board[i][j], end="  ")
                print("")

        return
    
    def updateBoard(self, point, value):
        """
        Metoda zmieniająca wybrane pole na 'X' lub 'O'
        """

        point_to_update = []
        if len(point) == 2:
            for i in range(len(self.letters)):
                if self.letters[i] == point[0]:
                    point_to_update.append(i)
            point_to_update.append(int(point[1])-1)
        elif len(point) == 3:
            for i in range(len(self.letters)):
                if self.letters[i] == point[0]:
                    point_to_update.append(i)
            point_to_update.append(int(point[1]+point[2])-1)
        self.board[point_to_update[1]][point_to_update[0]] = value

        return

    def checkWinner(self, board):
        """
        Metoda wskazująca zwycięzcę na danej planszy
        """
        
        winner = None
        # Sprawdzenie wygranej w poziomie
        for i in range(15):
            for j in range(10):
                if (board[i][j] == board[i][j+1] and board[i][j+1] == board[i][j+2]
                and board[i][j+2] == board[i][j+3] and board[i][j+3] == board[i][j+4]):
                    if board[i][j] == self.players[0]:
                        winner = 'X'
                    elif board[i][j] == self.players[1]:
                        winner = 'O'
        
        # Sprawdzenie wygranej w pionie
        for k in range(10):
            for l in range(15):
                if (board[k][l] == board[k+1][l] and board[k+1][l] == board[k+2][l]
                and board[k+2][l] == board[k+3][l] and board[k+3][l] == board[k+4][l]):
                    if board[k][l] == self.players[0]:
                        winner = 'X'
                    elif board[k][l] == self.players[1]:
                        winner = 'O'

        # Sprawdzenie wygranej na ukos spadający w dół od lewej
        for m in range(10):
            for n in range(10):
                if (board[m][n] == board[m+1][n+1] and board[m+1][n+1] == board[m+2][n+2]
                and board[m+2][n+2] == board[m+3][n+3] and board[m+3][n+3] == board[m+4][n+4]):
                    if board[m][n] == self.players[0]:
                        winner = 'X'
                    elif board[m][n] == self.players[1]:
                        winner = 'O'

        # Sprawdzenie wygranej na ukos ku górze od prawej
        for o in range(14, 4, -1):
            for p in range(10):
                if (board[o][p] == board[o-1][p+1] and board[o-1][p+1] == board[o-2][p+2]
                and board[o-2][p+2] == board[o-3][p+3] and board[o-3][p+3] == board[o-4][p+4]):
                    if board[o][p] == self.players[0]:
                        winner = 'X'
                    elif board[o][p] == self.players[1]:
                        winner = 'O'

        return winner

    def evaluate(self, board):
        """
        Metoda obliczająca sytuację na planszy
        """

        winner = self.checkWinner(board)
        if winner != None:
            if winner == self.players[0]:
                return 100000
            elif winner == self.players[1]:
                return -100000
        else:
            value = 0
            possibles = []
        
            columns = []
            for i in range(15):
                column = []
                for row in board:
                    column.append(row[i])
                columns.append(column)
            possibles.append(columns)
            
            rows = []
            for row in board:
                rows.append(row)
            possibles.append(rows)
            

            gameboard = numpy.array(board)
            diagonals1 = [gameboard.diagonal(i) for i in range(-13,13)]
            diagonals2 = [numpy.fliplr(gameboard).diagonal(i) for i in range(-13, 13)]
            possibles.append(diagonals1 + diagonals2)

            for possible_row in possibles:
                for row in possible_row:
                    points = 0
                    for i in range(len(row)-1):
                        if row[i] != '.':
                            if row[i+1] == row[i]:
                                points += 1
                            else:
                                if row[i] == self.players[0]:
                                    value += points**2
                                elif row[i] == self.players[1]:
                                    value -= points**2
                                points = 0

            return value
            
            

    
    def isMovesLeft(self, board):
        """
        Metoda sprawdzająca na planszy są jeszcze dostępne ruchy
        """

        for i in range(15):
            for j in range(15):
                if board[i][j] == '.':
                    return True
        return False


    def findBestMove(self):
        """
        Metoda znajdująca najkorzytniejszy ruch
        """

        best_val = 1000000000
        best_move_col = -1
        best_move_row = -1

        for move in self.findPossibleMoves(self.board):
                if self.board[move[0]][move[1]] == '.':
                    self.board[move[0]][move[1]] = 'O'
                    board = copy.deepcopy(self.board)
                    move_val = self.minimax(board, 3, -100000000, 100000000, True)
                    self.board[move[0]][move[1]] = '.'
                    if move_val < best_val:
                        best_move_col = move[1]
                        best_move_row = move[0]
                        best_val = move_val
    
        return self.letters[best_move_col] + str(best_move_row+1)
    
    def findPossibleMoves(self, board):
        possible_moves = []

        for i in range(15):
            for j in range(15):
                if i <= 13 and i >= 1 and j <= 13 and j >= 1:
                    if (board[i][j] == '.' and (board[i+1][j] != '.' or board[i][j+1] != '.' or board[i+1][j+1] != '.'
                    or board[i-1][j] != '.' or board[i][j-1] != '.' or board[i-1][j-1] != '.' or board[i-1][j+1] != '.'
                    or board[i+1][j-1] != '.')):
                        possible_moves.append([i,j])
                elif i == 0 and j >= 1 and j <= 13:
                    if (board[i][j] == '.' and (board[i+1][j] != '.' or board[i][j+1] != '.' or board[i+1][j+1] != '.'
                    or board[i][j-1] != '.' or board[i+1][j-1] != '.')):
                        possible_moves.append([i,j])
                elif i == 14 and j >= 1 and j <= 13:
                    if (board[i][j] == '.' and (board[i][j+1] != '.' or board[i-1][j] != '.' or board[i][j-1] != '.' 
                    or board[i-1][j-1] != '.' or board[i-1][j+1] != '.')):
                        possible_moves.append([i,j])
                elif j == 0 and i >= 1 and i <= 13:
                    if (board[i][j] == '.' and (board[i+1][j] != '.' or board[i][j+1] != '.' or board[i+1][j+1] != '.'
                    or board[i-1][j] != '.' or board[i-1][j+1] != '.')):
                        possible_moves.append([i,j])
                elif j == 14 and i >= 1 and i <= 13:
                    if (board[i][j] == '.' and (board[i+1][j] != '.' or board[i-1][j] != '.' or board[i][j-1] != '.' 
                    or board[i-1][j-1] != '.' or board[i+1][j-1] != '.')):
                        possible_moves.append([i,j])
                elif j == 0 and i == 0:
                    if (board[0][0] == '.' and (board[0][1] != '.' or board[1][1] != '.' or board[1][0] != '.')):
                        possible_moves.append([i,j])
                elif j == 14 and i == 0:
                    if (board[0][14] == '.' and (board[0][13] != '.' or board[1][14] != '.' or board[1][13] != '.')):
                        possible_moves.append([i,j])
                elif j == 0 and i == 14:
                    if (board[14][0] == '.' and (board[14][1] != '.' or board[13][1] != '.' or board[13][0] != '.')):
                        possible_moves.append([i,j])
                elif j == 14 and i == 14:
                    if (board[14][14] == '.' and (board[14][13] != '.' or board[13][14] != '.' or board[13][13] != '.')):
                        possible_moves.append([i,j])

        return possible_moves


    def minimax(self, board, depth, alpha, beta, isPlayerMove):
        """
        Metoda reprezentująca algorytm min max z przycinaniem alfa beta
        """

        score = self.evaluate(board)
        if depth == 0 or self.isMovesLeft(board) == False or score == 100000 or score == -100000:
            return score

        if isPlayerMove:
            best = -10000000
            for move in self.findPossibleMoves(board):
                if board[move[0]][move[1]] == '.':
                    board[move[0]][move[1]] = self.players[0]
                    val = self.minimax(board, depth-1, alpha, beta, False)
                    board[move[0]][move[1]] = '.'
                    best = max(best, val)
                    alpha = max(alpha, val)
                    if beta <= alpha:
                        break
            return best
            
        else:
            best = 10000000
            for move in self.findPossibleMoves(board):
                if board[move[0]][move[1]] == '.':
                    board[move[0]][move[1]] = self.players[1]
                    val = self.minimax(board, depth-1, alpha, beta, True)
                    board[move[0]][move[1]] = '.'
                    best = min(best, val)
                    beta = min(beta, val)
                    if beta <= alpha:
                        break
            return best         



ticTac = Game()
ticTac.main()



