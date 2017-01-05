import heapq;


class PriorityQueue():
    """Implementation of a priority queue"""

    def __init__(self):
        self.queue = []
        self.current = 0    

    def pop(self):
        return heapq.heappop(self.queue)
        
    def remove(self, nodeId):
        for i in range(len(self.queue)):
            if self.queue[i][1]==nodeId:
                self.queue.pop(i)
                break;

    def __iter__(self):
        return self

    def __str__(self):
        return 'PQ:[%s]'%(', '.join([str(i) for i in self.queue]))

    def append(self, node):
        heapq.heappush(self.queue,node)

    def __contains__(self, key):
        self.current = 0
        return key in [n for _,n in self.queue]

    def __eq__(self, other):
        self.curent = 0
        return self == other
    
    def __getitem__(self, nodeId):
        for element in self.queue:
            if element[1]==nodeId:
                return element
        return None
    
    def clear(self):
        self.queue = []
        
    def __len__(self):
        return len(self.queue)

    __next__ = next
