class CQueue:
    """
    An scalable circulate queue.

    Basic optoration provided:put, get, is_empty, rescale, clear
    """
    def __init__(self):
        self.__q = [0]
        self.__f = 0
        self.__r = 0
        self.__size = 1
        self.__is_empty = True

    def put(self, data):
        """
        Put *data* into the Queue
        """
        if self.__r == self.__f and not self.__is_empty:
            self.__q.extend([0 for i in range(0, self.__size + 1)])
            self.__q[self.__size: self.__size + self.__r] = self.__q[0: self.__r]
            self.__r += self.__size
            self.__size += self.__size + 1

        self.__q[self.__r] = data
        self.__r = (self.__r + 1) % self.__size
        self.__is_empty = False

    def get(self):
        """
        Pop the first element in the queue, pop *None* if the queue is empty.
        """
        if self.__is_empty:
            return None
        tmp = self.__q[self.__f]
        self.__f = (self.__f + 1) % self.__size
        if self.__f == self.__r:
            self.__is_empty = True
        return tmp

    def is_empty(self):
        """
        Return whether the queue is empty.
        """
        return self.__is_empty

    def rescale(self):
        """
        Resize the inner queue acording to number of current elements in queue. If there is *N* elements, the queue then
        would be *N+1* long
        """
        if self.__is_empty:
            self.__q = [0]
            self.__size = 1
            self.__r = 0
            self.__f = 0
            return
        if self.__r > self.__f:
            tmp = self.__q[self.__f: self.__r]
            tmp.append(0)
        else:
            tmp = [0 for i in range(0, self.__size - self.__f + self.__r + 1)]
            tmp[0: self.__size - self.__f] = self.__q[self.__f: self.__size]
            tmp[self.__size - self.__f: self.__size - self.__f + self.__r] = self.__q[0: self.__r]
        self.__q = tmp
        self.__size = len(tmp)
        self.__f = 0
        self.__r = len(tmp) - 1

    def clear(self, resize=False):
        self.__f = 0
        self.__r = 0
        if resize:
            self.__q = [0]
            self.__size = 1

    def get_queue_copy(self):
        """
        Get a copy of uncirculated version the inner queue.
        """
        self.rescale()
        return self.__q[0: self.__size - 1]
