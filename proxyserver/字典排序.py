import collections

class Solution:
    def inorderTraversal(self, root):
        stack, ret = [], []
        cur = root
        while stack or cur:
            if cur:
                stack.append(cur)
                cur = cur.left
            else:
                cur = stack.pop()
                ret.append(cur.val)
                cur = cur.right
        return ret


s=Solution()
s.inorderTraversal([1,2,3])

graph = {
    'A': ['B', 'C', 'D'],
    'B': ['A', 'E', 'F'],
    'C': ['A', 'D', 'F', 'G'],
    'D': ['A', 'C', 'G'],
    'E': ['B'],
    'F': ['B', 'C'],
    'G': ['C', 'D']
}


def DFS(start,graph):
    stack = []
    visited = []
    stack.append(start)
    visited.append(start)
    while stack:
        node = stack.pop()
        nodes = graph[node]
        for i in nodes:
            if i not in visited:
                stack.append(i)
                visited.append(i)
        print(node,end='\t')

DFS('A',graph)