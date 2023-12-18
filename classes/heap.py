class Heap():
 
    def __init__(self):
        self.array = []
        self.size = 0
        self.pos = []
 
    def newMinHeapNode(self, v, dist):
        minHeapNode = [v, dist]
        return minHeapNode
 
    # A utility function to swap two nodes
    # of min heap. Needed for min heapify
    def swapMinHeapNode(self, a, b):
        t = self.array[a]
        self.array[a] = self.array[b]
        self.array[b] = t
 
    # A standard function to heapify at given idx
    # This function also updates position of nodes
    # when they are swapped.Position is needed
    # for decreaseKey()
    def minHeapify(self, idx):
        smallest = idx
        left = 2*idx + 1
        right = 2*idx + 2
 
        if (left < self.size and
           self.array[left][1]
            < self.array[smallest][1]):
            smallest = left
 
        if (right < self.size and
           self.array[right][1]
            < self.array[smallest][1]):
            smallest = right
 
        # The nodes to be swapped in min
        # heap if idx is not smallest
        if smallest != idx:
 
            # Swap positions
            self.pos[self.array[smallest][0]] = idx
            self.pos[self.array[idx][0]] = smallest
 
            # Swap nodes
            self.swapMinHeapNode(smallest, idx)
 
            self.minHeapify(smallest)
 
    # Standard function to extract minimum
    # node from heap
    def extractMin(self):
 
        # Return NULL wif heap is empty
        if self.isEmpty() == True:
            return
 
        # Store the root node
        root = self.array[0]
 
        # Replace root node with last node
        lastNode = self.array[self.size - 1]
        self.array[0] = lastNode
 
        # Update position of last node
        self.pos[lastNode[0]] = 0
        self.pos[root[0]] = self.size - 1
 
        # Reduce heap size and heapify root
        self.size -= 1
        self.minHeapify(0)
 
        return root
 
    def isEmpty(self):
        return True if self.size == 0 else False
 
    def decreaseKey(self, v, dist):
 
        # Get the index of v in  heap array
 
        i = self.pos[v]
 
        # Get the node and update its dist value
        self.array[i][1] = dist
 
        # Travel up while the complete tree is
        # not heapified. This is a O(Logn) loop
        while (i > 0 and self.array[i][1] <
                  self.array[(i - 1) // 2][1]):
 
            # Swap this node with its parent
            self.pos[ self.array[i][0] ] = (i-1)//2
            self.pos[ self.array[(i-1)//2][0] ] = i
            self.swapMinHeapNode(i, (i - 1)//2 )
 
            # move to parent index
            i = (i - 1) // 2
 
    # A utility function to check if a given 
    # vertex 'v' is in min heap or not
    def isInMinHeap(self, v):
 
        if self.pos[v] < self.size:
            return True
        return False