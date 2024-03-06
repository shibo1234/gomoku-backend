from .node import Node


class BoardParent:
    DIRECTIONS =[
        [0,1],
        [1,0],
        [1,1],
        [1,-1]
    ]

    def __init__(self, board_size: int):
        self.board = [[None for _ in range(board_size)] for _ in range(board_size)]
        self.board_size = board_size
        self.winner = 0
        self.isTerminated = False

    def addNode(self, x: int, y: int, player: int):
        '''
        Add a new stone to the board.
        :param player: the player who adds this stone
        :param x: the x coordinate of the new stone
        :param y: the y coordinate of the new stone
        :return: None
        '''
        if not self.isTerminated:
            if self.board[x][y] is None:
                self.board[x][y] = Node(x, y, player)
                self.update(x, y, player)
            else:
                print('Invalid move')

    def isValidCoordinate(self, x: int) -> bool:
        '''
        Checks if the coordinate are valid.
        :param x: the x coordinate of the new stone
        :return: true if the coordinates are valid, false otherwise
        '''
        return 0 <= x < self.board_size

    def getPlayer(self, x: int, y: int) -> int:
        '''
        Returns the player of the stone at the given position. Invalid coordinates will return None.
        :param x: the x coordinate
        :param y: the y coordinate
        :return: the player of the stone at the given position
        '''
        if not self.isValidCoordinate(x) or not self.isValidCoordinate(y):
            return 0
        elif self.board[x][y] is None:
            return 0
        else:
            return self.board[x][y].player

    def update(self, x: int, y: int, player: int):
        '''
        Update a new stone to the board.
        :param x: the x coordinate of the new stone
        :param y: the y coordinate of the new stone
        :param player:
        :return: None
        '''

        self.board[x][y] = Node(x, y, player)

        for i in range(4):
            dx, dy = BoardParent.DIRECTIONS[i]
            newX1 = x + dx
            newY1 = y + dy
            newX2 = x - dx
            newY2 = y - dy
            count1 = 0
            count2 = 0
            if self.getPlayer(newX1, newY1) == player:
                count1 = self.board[newX1][newY1].counts[i]
            if self.getPlayer(newX2, newY2) == player:
                count2 = self.board[newX2][newY2].counts[i]

            count = count1 + 1 + count2

            if count == 5:
                self.winner = player
                self.isTerminated = True

            self.board[x][y].setCount(i, count)

            # for j in range(count1 - 1):
            #     newnewX = newX1 + dx * (j + 1)
            #     newnewY = newY1 + dy * (j + 1)
            #     self.board[newnewX][newnewY].setCount(i, count)
            #
            # for j in range(count2 - 1):
            #     newnewX = newX2 - dx * (j + 1)
            #     newnewY = newY2 - dy * (j + 1)
            #     self.board[newnewX][newnewY].setCount(i, count)
            for direction in [(dx, dy), (-dx, -dy)]:
                step = 1
                while True:
                    new_x = x + direction[0] * step
                    new_y = y + direction[1] * step

                    if not self.isValidCoordinate(new_x) or not self.isValidCoordinate(new_y):
                        break
                    if self.getPlayer(new_x, new_y) != player:
                        break
                    self.board[new_x][new_y].setCount(i, count)
                    step += 1

    def get_winner(self) -> int:
        '''
        Return the winner of the game.
        :return: the winner of the game
        '''
        return self.winner

    def is_terminated(self) -> bool:
        '''
        Return whether the game is terminated.
        :return: whether the game is terminated
        '''
        return self.isTerminated

    def reset(self):
        '''
        Reset the board.
        :return: None
        '''
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.winner = 0
        self.isTerminated = False



