from functools import reduce
import pyncomb
import dlx
from itertools import permutations


class DesignDLX(dlx.DLX):
    def __init__(self, t, v, k):
        self.t = t
        self.v = v
        self.k = k

        # Populate the columns variable.
        columns = list(pyncomb.ksubsetlex.all(v, t))
        # print(columns)
        # Now create the rows, one for each k-set.
        rows = [[pyncomb.ksubsetlex.rank(v, T) for T in pyncomb.ksubsetlex.all(
            pyncomb.combfuncs.createLookup(S), t)] for S in pyncomb.ksubsetlex.all(v, k)]
        #print(rows)
        #print(len(rows))
        # Add a field to each column to indicate that it is primary.
        dlx.DLX.__init__(self, [(c, dlx.DLX.PRIMARY) for c in columns])
        self.rowsByLexOrder = self.appendRows(rows)

    def printSolution(self, solution):
        return [list(set(reduce(lambda x, y: x + y, self.getRowList(i), []))) for i in solution]


def solutions_list(design):
    (t, v, k) = (design.t, design.v, design.k)
    design_list = list(design.solve())
    new_list = []
    for d in design_list:
        new_list.append(design.printSolution(d))
    print(f"---DESIGN ({v}, {k}, {1}) DONE ---".center(50, "-"))
    print("Number of designs found: %d" % len(design_list))
    r = (v - 1) / (k - 1)
    b = (v * r) / k
    print(f'Design parameters(v,b,r,k,lambda):\nv:{v}, b:{b}, r:{r}, k:{k}, lambda:{1}')
    return new_list


design_13_4_1 = DesignDLX(2,13,4)

sol_list_731 = solutions_list(design_13_4_1)



def permuted_list(primitive_list):
    perm = permutations(primitive_list)

    # counting permunations and adding each permutation to a list. Permutations will return tuples @first.
    a = []
    count = 0
    for i in list(perm):
        count += 1
        a.append(i)

    # converting tuples to lists, because lists are easier to work with.
    perm_list = []
    for tuple in a:
        temp_list = []
        for item in tuple:
            temp_list.append(item)
        perm_list.append(temp_list)

    return perm_list


tempo_list = permuted_list(sol_list_731[0])

print(tempo_list)
print(len(tempo_list))

# incidence structure, @sage ---> Automorphism Group
