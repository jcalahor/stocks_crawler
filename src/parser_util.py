class Parser(object):
    def __init__(self, buffer):
        self.index = 0
        self.buffer = buffer

    def move_to(self, token):
        res = self.buffer.find(token, self.index)
        if res > -1:
            self.index = res + len(token)
            return True
        return False

    def extract_between(self, start, end):
        res1 = self.buffer.find(start, self.index)

        if res1 > -1:
            res2 = self.buffer.find(end, res1)
            if res2 > -1:
                res1 = res1 + len(start)
                return self.buffer[res1: res2]
        return None











