from enum import Enum
import copy


class Bank(Enum):
    FAR = "FAR"
    RIVER = "RIVER"
    CUR = "CUR"


class River:
    def __init__(self, far_bank, cur_bank, boat_capacity):
        assert(isinstance(far_bank, dict) and isinstance(cur_bank, dict))
        self.far_bank = far_bank
        self.cur_bank = cur_bank
        self.num_actors = len(far_bank) + len(cur_bank)
        self.boat = River.Boat(boat_capacity)

    def __str__(self):
        cur_bank_str = ", ".join('{} {}'.format(k, v) for k, v in self.cur_bank.items())
        far_bank_str = ", ".join('{} {}'.format(k, v) for k, v in self.far_bank.items())
        return "River cur_bank: " + cur_bank_str + " far_bank: " + far_bank_str + " boat: " + self.boat.__str__()

    def numMissionary(self):
        return self.cur_bank[Missionary()] + self.far_bank[Missionary()]

    def numCannibal(self):
        return self.cur_bank[Cannibal()] + self.far_bank[Cannibal()]

    class Boat:
        def __init__(self, capacity):
            self.location = Bank.CUR
            self.occupants = dict({Missionary(): 0, Cannibal(): 0})
            self.capacity = capacity

        def __eq__(self, other):
            if isinstance(other, self.__class__):
                if (self.location == other.location and
                        self.occupants[Missionary()] == other.occupants[Missionary()] and
                        self.occupants[Cannibal()] == other.occupants[Cannibal()]):
                    return True
                return False
            else:
                return False

        def __hash__(self):
            # use the hashcode of self.ssn since that is used
            # for equality checks as well
            return hash((self.__class__, self.location, self.occupants[Missionary()], self.occupants[Cannibal()]))

        def __str__(self):
            occupants_str = ", ".join('{} {}'.format(k, v) for k, v in self.occupants.items())
            return self.location.__str__() + " " + occupants_str

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if (self.far_bank[Missionary()] == other.far_bank[Missionary()] and
                    self.cur_bank[Missionary()] == other.cur_bank[Missionary()] and
                    self.far_bank[Cannibal()] == other.far_bank[Cannibal()] and
                    self.cur_bank[Cannibal()] == other.cur_bank[Cannibal()] and self.boat.__eq__(other.boat)):
                return True
            return False
        else:
            return False

    def __hash__(self):
        # use the hashcode of self.ssn since that is used
        # for equality checks as well
        return hash((self.__class__,
                    self.far_bank[Missionary()],
                    self.cur_bank[Missionary()],
                    self.far_bank[Cannibal()],
                    self.cur_bank[Cannibal()],
                    self.boat.__hash__(), self.num_actors))


class Node:
    def __init__(self, val, parent):
        self.val = val
        self.parent = parent
        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1

    def getPathToNode(self, path=[]):
        if self.parent is None:
            return path.append(self)
        else:
            self.parent.getPathToNode(path)
            path.append(self)
            return path

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.val.__eq__(other.val):
                return True
            return False
        else:
            return False

    def __hash__(self):
        # use the hashcode of self.ssn since that is used
        # for equality checks as well
        return hash((self.__class__, self.val.__hash__()))

    def __str__(self):
        return self.val.__str__()


class Missionary:
    def __init__(self):
        return None

    def __str__(self):
        return "Missionary"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.__class__)


class Cannibal:
    def __init__(self):
        return None

    def __str__(self):
        return "Cannibal"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.__class__)


class MissionaryCannibalProblem:
    def __init__(self, numMissionaries=3, numCannibals=3, heuristic=None):
        if heuristic is None:
            self.heuristic = self.numRemainingOnCurBank
        else:
            self.heuristic = heuristic
        self.numMissionaries = numMissionaries
        self.numCannibals = numCannibals

    def __str__(self):
        return """The missionaries and cannibals problem is usually stated as follows.
                  N (usually 3) missionaries and N cannibals are on one side of a river,
                  along with a boat that can hold up to K (usually 2) people. Find a way to get
                  everyone to the other side without ever leaving a group of mis- sionaries
                  in one place outnumbered by the cannibals in that place. This problem is
                  famous in AI because it was the subject of the first paper that approached
                  problem formulation from an analytical viewpoint (Amarel, 1968)."""

    def isValid(self, river):
        assert(isinstance(river, River))
        assert(isinstance(river.cur_bank, dict))
        assert(isinstance(river.far_bank, dict))
        return ((river.cur_bank[Missionary()] >= river.cur_bank[Cannibal()] or river.cur_bank[Missionary()] == 0) and
                (river.far_bank[Missionary()] >= river.far_bank[Cannibal()] or river.far_bank[Missionary()] == 0))

    def isFinished(self, river):
        assert(isinstance(river, River))
        return (river.far_bank[Missionary()] == self.numMissionaries and
                river.far_bank[Cannibal()] == self.numCannibals)

    def numRemainingOnCurBank(self, river):
        assert(isinstance(river, River))
        return river.cur_bank[Missionary()] + river.cur_bank[Cannibal()]

    def score(self, node):
        assert(isinstance(node, Node))
        assert(isinstance(node.val, River))
        return node.depth + self.heuristic(node.val)

    def moveMissionaryOnBoat(self, boat, bank, num):
        # print("Missionary before ", boat.occupants[Missionary()])
        # print("num ", num)
        if bank[Missionary()] >= num:
            bank[Missionary()] -= num
            boat.occupants[Missionary()] += num
            return True
        return False
        # print("Missionary after ", boat.occupants[Missionary()])

    def moveCannibalOnBoat(self, boat, bank, num):
        # print("Cannibal before ", boat.occupants[Cannibal()])
        # print("num ", num)
        if bank[Cannibal()] >= num:
            bank[Cannibal()] -= num
            boat.occupants[Cannibal()] += num
            return True
        return False
        # print("Cannibal after ", boat.occupants[Cannibal()])

    def expandBank(self, node, bank):
        assert(node.val.boat.location == Bank.CUR or node.val.boat.location == Bank.FAR)
        river = node.val
        expanded = []
        history = set([(0, 0)])

        for i in range(river.boat.capacity + 2):
            for c in range(i):
                for m in range(river.boat.capacity + 1 - c):
                    if (c, m) in history:
                        continue
                    else:
                        history.add((c, m))
                    nodeChild = Node(copy.deepcopy(node.val), node)
                    validChild = True
                    if (bank == Bank.CUR):
                        validChild = validChild & self.moveMissionaryOnBoat(nodeChild.val.boat, nodeChild.val.cur_bank, m)
                        validChild = validChild & self.moveCannibalOnBoat(nodeChild.val.boat, nodeChild.val.cur_bank, c)
                    elif (bank == Bank.FAR):
                        validChild = validChild & self.moveMissionaryOnBoat(nodeChild.val.boat, nodeChild.val.far_bank, m)
                        validChild = validChild & self.moveCannibalOnBoat(nodeChild.val.boat, nodeChild.val.far_bank, c)
                    if (validChild):
                        nodeChild.val.boat.location = Bank.RIVER
                        expanded.append(nodeChild)
        return expanded

    def offLoad(self, boat, bank, bank_side):
        bank[Missionary()] += boat.occupants[Missionary()]
        boat.occupants[Missionary()] = 0
        bank[Cannibal()] += boat.occupants[Cannibal()]
        boat.occupants[Cannibal()] = 0
        boat.location = bank_side

    def expandBoat(self, node):
        expanded = []
        childFar = Node(copy.deepcopy(node.val), node)
        self.offLoad(childFar.val.boat, childFar.val.far_bank, Bank.FAR)
        expanded.append(childFar)

        childCur = Node(copy.deepcopy(node.val), node)
        self.offLoad(childCur.val.boat, childCur.val.cur_bank, Bank.CUR)
        expanded.append(childCur)

        return expanded

    def expand(self, node):
        assert(isinstance(node, Node))
        assert(isinstance(node.val, River))
        boat = node.val.boat
        expanded = []

        if boat.location == Bank.CUR:
            expanded.extend(self.expandBank(node, Bank.CUR))
        elif boat.location == Bank.FAR:
            expanded.extend(self.expandBank(node, Bank.FAR))
        elif boat.location == Bank.RIVER:
            expanded.extend(self.expandBoat(node))
        else:
            assert(False)
        return expanded


class SearchRiverAI:
    def __init__(self, river=River(dict({Missionary(): 0, Cannibal(): 0}), dict({Missionary(): 3, Cannibal(): 3}), 2)):
        self.root = Node(river, None)
        self.problem = MissionaryCannibalProblem(river.numMissionary(), river.numCannibal(), None)

    def startSearch(self, method):
        method([self.root], set([]))

    def aStarSearch(self, fringe, history=dict()):
        while(True):
            bestNode = None
            bestNodeScore = 0
            if len(fringe) == 0:
                return None

            fringe = [node for node in fringe if self.problem.isValid(node.val)]
            fringe = [node for node in fringe if node not in history or history[node] > node.depth]
            for node in fringe:
                if bestNode is None:
                    bestNode = node
                    bestNodeScore = self.problem.score(node)
                else:
                    if bestNodeScore < self.problem.score(node):
                        bestNode = node
                        bestNodeScore = self.problem.score(node)

            # check if finished
            if self.problem.isFinished(bestNode.val):
                return bestNode

            fringe.remove(bestNode)
            fringe.extend(self.problem.expand(bestNode))
            history[bestNode] = bestNode.depth


if __name__ == "__main__":
    ai = SearchRiverAI()
    finishedNode = ai.aStarSearch([ai.root])
    print("=============PATH===============")
    path = finishedNode.getPathToNode()
    for node in path:
        print(node)
