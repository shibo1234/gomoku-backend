class Node:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player
        self.counts = [1 for _ in range(4)]

    def setCount(self, i: int, value: int) -> None:
        '''
        Set the ith count of self node.
        :param value: the new value of the ith count
        :param i: the index of the count ot be setted
        :return: None
        '''
        self.counts[i] = value

    def get_count(self) -> list[int]:
        '''
        Return the counts of the node in all directions.
        '''
        return self.counts
