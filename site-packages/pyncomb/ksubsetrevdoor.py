#!/usr/bin/env python
#
# Copyright 2009 Sebastian Raaphorst.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""An implementation of basic combinatorial k-subset operations using
a revolving door (minimal change) ordering.

Note that for our purposes here, sets are represented as lists as
ranking, unranking, and successor functions need a total order on the
elements of the set.

For the base set B, if B is an integer, we assume that our base set is
[0,...,B-1]. Otherwise, assume that B is a pair consisting of:
   1. a list representing the base set
   2. a reverse lookup dict, mapping elements of the base set to their
      position in the total order.
   Example: [0,3,4,2], {0:0, 3:1, 4:2, 2:3}
Note that we require B to contain the reverse lookup information to
speed up the algorithms here; otherwise, we would need to call index on
our base set many times, which would increase complexity by a factor of
the length of the base set.

By Sebastian Raaphorst, 2009."""

from . import combfuncs


def rank(B, K):
    """Return the rank of k-subset K in base set B."""

    block = (K if type(B) == int else [B[1][i] for i in K])
    k = len(block)
    return sum([(1 if i%2 == k%2 else -1) * combfuncs.binom(block[i-1]+1,i) for i in xrange(k,0,-1)]) + (0 if k%2 == 0 else -1)


def unrank(B, k, rk):
    """Return the k-subset of rank rk in base set B."""

    v = (B if type(B) == int else len(B[0]))

    K = [0] * k
    for i in xrange(k,0,-1):
        while combfuncs.binom(v,i) > rk:
            v -= 1
        K[i-1] = v
        rk = combfuncs.binom(v+1,i) - rk - 1
    return (K if type(B) == int else [B[0][i] for i in K])


def succ(B, K):
    """Return the successor of the k-subset K in base set B.
    If there is no successor, we return None."""

    v = (B if type(B) == int else len(B[0]))
    Kn = (K if type(B) == int else [B[1][i] for i in K]) + [v]
    k = len(K)

    j = 0
    while j < k and Kn[j] == j:
        j += 1

    if k%2 == j%2:
        if j == 0:
            Kn[0] -= 1
        else:
            Kn[j-1] = j
            Kn[j-2] = j-1
    else:
        if Kn[j+1] != Kn[j] + 1:
            Kn[j-1] = Kn[j]
            Kn[j] += 1
        else:
            Kn[j+1] = Kn[j]
            Kn[j] = j

    if Kn[:k] == range(k):
        return None
    return (Kn[:k] if type(B) == int else [B[0][i] for i in Kn[:k]])


def all(B, k):
    """A generator to create all subsets over the specified base set B."""

   # Make the base set, creating a copy of B if B is a pair as described in
   # the module introduction; thus, if B changes, the iterator does not
   # become invalid.
    Bn = (B if type(B) == int else (B[0][:], dict(B[1])))
    K = (range(k) if type(B) == int else Bn[0][:k])
    while K != None:
        yield K
        K = succ(Bn, K)

