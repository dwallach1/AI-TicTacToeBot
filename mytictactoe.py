#from GameApp import check_win
# ^^ I was having import problems on my machine so I copied the check_win funcion into my code
#by David Wallach (daw647)

class mmNode:
    def __init__(self, beta=float("infinity"), alpha=float("-infinity"), parent=None, isLeaf=False, isMaxNode=False, board=None, score=None, symbol=None, childeren=None):
        self.beta = beta
        self.alpha = alpha
        self.parent = parent
        self.isLeaf = isLeaf
        self.isMaxNode = isMaxNode
        self.board = board
        self.score = score
        self.symbol = symbol
        self.children = childeren

#recursively makes the tree of possible outcomes
def makeTree(node, rootSymbol):
    score = evalBoard(leafNode=node, mySymbol=node.symbol, rootSymbol=rootSymbol)
    if score is not -1:
        node.score = score
        node.isLeaf = True
        node.isMaxNode = True
        return
    node.children = makeChildren(node=node, mysymbol=node.symbol)
    for c in node.children:
        makeTree(c, rootSymbol)
    return node

#finds all children of the node given to it
def makeChildren(node, mysymbol):
    children = []
    newBoard = list(node.board)
    childSymbol = nextTurn(mysymbol)
    childMax = False
    if node.isMaxNode == False:
        childMax = True
    for i,val in enumerate(newBoard):
        if val == 0:
            if childSymbol == "X":
                newBoard[i] = 1
            else:
                newBoard[i] = -1
            newNode = mmNode(beta=float("infinity"), alpha=float("-infinity"), parent=node, isLeaf=False, isMaxNode=childMax, board=newBoard, score=None, symbol=childSymbol)
            children.append(newNode)
            newBoard = list(node.board)
    return children

#evaluates the current state to see if it is an endstate or not
#and if so, then defines its score numerically
def evalBoard(leafNode, mySymbol, rootSymbol):
    result = check_win(leafNode.board)
    gameOver = True
    for i,val in enumerate(leafNode.board):
        if val == 0:
            gameOver = False
            break
    if result == "No Winner" and gameOver == False:
        return -1
    elif result == "No Winner" and gameOver == True:
        return 0
    elif result == rootSymbol:
        return 10
    else:
        return -10

#copied from GameApp.py because the import call was giving an error for unknown reason
def check_win(board):
    threes = ((1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),(1,5,9),(3,5,7))
    for each in threes:
        total = board[each[0]-1] + board[each[1]-1] + board[each[2]-1]
        if total == -3:
            return "O"
        elif total == 3:
            return "X"
    return "No Winner"

#simply changes the turn from level to level of the tree to simulate possible games
def nextTurn(mySymbol):
    if mySymbol == "X":
        return "O"
    else:
        return "X"

#finds height of current tree we are examining
def findHeight(node):
    treeHeight = 0
    for i, val in enumerate(node.board):
        if val == 0:
            treeHeight += 1
    return treeHeight+1

#use alpha beta pruning to update values of the tree and find the optimum move
def prune(node, alpha, beta, treeHeight, rootSymbol):
    score = evalBoard(node, node.symbol, rootSymbol=rootSymbol)
    if treeHeight == 0 or score is not -1:
        return score

    if node.isMaxNode:
        for c in node.children:
            alpha = max(alpha, prune(c, alpha, beta, treeHeight-1, rootSymbol))
            if alpha >= beta:
                break
        return alpha
    else:
        for c in node.children:
            beta = min(beta, prune(c, alpha, beta, treeHeight-1, rootSymbol))
            if alpha >= beta:
                break
        return beta

#updates the current tree representation with by changing the score of the
#nodes based on the min max alpha beta pruning method defined under prune
def updateValues(node, rootSymbol):
    for c in node.children:
        c.score = prune(c, float("-infinity"), float("infinity"),treeHeight=findHeight(c), rootSymbol=rootSymbol)
    return node

#this finds the child node of the root node with the highest value
#it then finds the index in which that child had moved and makes that move
def findNode(node):
    alpha = float("-infinity")
    i = None
    for j,val in enumerate(node.children):
        if val.score > alpha:
            alpha = val.score
            i = j

    for k in range(len(node.board)):
        if node.board[k] is not node.children[i].board[k]:
            return k+1
    return None



def mymove(board,mysymbol):
    print("Machine's move is: ...")
    count = 0
    for i,val in enumerate(board):
        if val is not 0:
            count += 1
    if count == 0:
        return 1  #if this is first move, all possible simulations have a score of 0 therefore make this a base case and return first position
    rootNode = mmNode(beta=float("infinity"),alpha=float("-infinity"), parent=None, isLeaf=False, isMaxNode=True, score=None,board=board, symbol=mysymbol)
    tree = makeTree(rootNode, nextTurn(mysymbol))
    updatedTree = updateValues(tree, nextTurn(mysymbol))
    return findNode(updatedTree)
