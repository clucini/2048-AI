import random


class Board:
    def __init__(self):
        self.tiles = []
        for i in range(0,4):
            self.tiles.append([])
            for f in range(0,4):
                self.tiles[i].append(0)
        self.genTile()
        self.genTile()

    def print(self):
        for row in self.tiles:
            for tile in row:
                print(" " * (4 - int(len(str(tile)))) + str(tile) + "|", end='')
            print()

    def checkMove(self, dir):
        check = False
        #0 = down, 1 = up  2 = left  3 = right
        board = self
        if dir == 1:
            board = rotateBoard(self, 3)
        elif dir == 0:
            board = rotateBoard(self, 1) 
        elif dir == 3:
            board = rotateBoard(self, 2)

        for y in range(0,len(board.tiles)):
            for x in range(0,len(board.tiles[0])-1):
                if self.canMerge(board.tiles[y][x], board.tiles[y][x+1]):
                    check = True
        return check
    
    def canMerge(self, tile1, tile2):
        if tile1 == 0:
            return False
        elif tile1 == tile2:
            return True
        elif tile2 == 0:
            return True
        else:
            return False

    def genTile(self):
        new_element = 4 if random.randrange(100) > 89 else 2
        (i,j) = random.choice([(i,j) for i in range(len(self.tiles)) for j in range(len(self.tiles[0])) if self.tiles[i][j] == 0])
        self.tiles[i][j] = new_element

    def move(self, dir):
        if self.endGame():
            return 'over'
        if not self.checkMove(dir):
            print("Invalid move")
            return 'invalid'
        else:
            board = self
            if dir == 1:
                board = rotateBoard(self, 3)
            elif dir == 0:
                board = rotateBoard(self, 1) 
            elif dir == 3:
                board = rotateBoard(self, 2)

            for y in range(0, len(board.tiles)):
                board.tiles[y] = list(filter(lambda a: a != 0, board.tiles[y]))

            for y in range(0, len(board.tiles)):
                for x in range(0, len(board.tiles[y])-1):
                    if len(board.tiles[y]) > 1:
                        if board.canMerge(board.tiles[y][x], board.tiles[y][x+1]):
                            board.tiles[y][x] += board.tiles[y][x+1]
                            board.tiles[y][x+1] = 0
            
            for y in range(0, len(board.tiles)):
                board.tiles[y] = list(filter(lambda a: a != 0, board.tiles[y]))

            for row in board.tiles:
                for i in range(0, 4 -len(row)):
                    row.append(0)

            if dir == 1:
                board = rotateBoard(board, 1)
            elif dir == 0:
                board = rotateBoard(board, 3) 
            elif dir == 3:
                board = rotateBoard(board, 2)

            board.genTile()
            self.tiles = board.tiles
            self.print()
            print("-----------")
        return 'good'

    def endGame(self):
        if not self.checkMove(0) and not self.checkMove(1) and not self.checkMove(2) and not self.checkMove(3):
            print("GameOver")
            return True
        return False

    def score(self):
        sum = 0
        for row in range (len(self.tiles)):
            for col in range(len(self.tiles[row])):
                sum += self.tiles[row][col]
        return sum


def rotateBoard(board, num = 1):
        rBoard = board
        for i in range(0, num):
            newBoard = Board()
            for y in range(0,len(rBoard.tiles)):
                newBoard.tiles[y] = list(reversed([f[y] for f in rBoard.tiles]))
            rBoard = newBoard
        return rBoard


