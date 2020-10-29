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
co-lex ordering.

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

    k = len(K)
    rk = 0
    for i in xrange(k):
        n = (K[k-i-1] if type(B) == int else B[1][K[k-i-1]])
        rk += (0 if k-i > n else combfuncs.binom(n,k-i))
    return rk


def unrank(B, k, rk):
    """Return the k-subset of rank rk in base set B."""

    x = (B-1 if type(B) == int else len(B[0])-1)

    K = [0] * k
    for i in xrange(k):
        while combfuncs.binom(x,k-i) > rk:
            x -= 1
        K[k-i-1] = (x if type(B) == int else B[0][x])
        rk -= combfuncs.binom(x,k-i)
    return K


def succ(B, K):
    """Return the successor of the k-subset K in base set B.
    If there is no successor, we return None."""

    # Find the lowest element i in K such that i+1 is not in
    # K. Remove i and substitute with i+1. Reset the list from
    # 0 to i-1, and copy from i+1 on.
    k = len(K)
    maxelem = (B-1 if type(B) == int else B[0][-1])
    for i in xrange(k):
        if i < k-1:
            nextelem = (K[i]+1 if type(B) == int else B[0][B[1][K[i]]+1])
            if K[i+1] != nextelem:
                return (range(i) if type(B) == int else B[0][:i]) + [nextelem] + K[i+1:]
        else:
            if K[i] < maxelem:
                nextelem = (K[i]+1 if type(B) == int else B[0][B[1][K[i]]+1])
                return (range(i) if type(B) == int else B[0][:i]) + [nextelem]

    return None
        

def all(B, k):
   """A generator to create all k-subsets over the specified base set B."""

   # Make the base set, creating a copy of B if B is a pair as described in
   # the module introduction; thus, if B changes, the iterator does not
   # become invalid.
   Bn = (B if type(B) == int else (B[0][:], dict(B[1])))
   K = (range(k) if type(B) == int else Bn[0][:k])
   while K != None:
       yield K
       K = succ(Bn, K)
