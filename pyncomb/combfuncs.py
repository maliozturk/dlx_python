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

"""Various combinatorial functions used by the pyncomb library, and
useful in and of their own right."""

# _C represents the binomial lookup table, and _Cmax indicates how much of it
# we have computed thus far. We can compute combinations up to _Cmax, so in the
# default case, we can compute _C[0][0].
from functools import reduce

_Cmax = 0
_C = [[1]]

def binom(n, k, store=True):
    """Calculate the binomial coefficient C(n,k) = n!/k!(n-k)!.

    This is done using dynamic programming. If store is True, the final
    result and all intermediate computations are stored in a lookup table
    so that future function calls can be done in constant time.

    The caching lookup table should be used unless you have very specific reasons
    not to do so, as the binomial table is used in many other functions in pyncomb.
    If store is False, the binomial coefficient is fully calculated, which is very
    inefficient."""

    global _Cmax
    global _C

    if n <= _Cmax:
        return (_C[n][k] if k >= 0 and k <= n else 0)

    # Use dynamic programming to fill in the rest.
    if store:
        # We fill in all entries of the table from Cmax to n.
        for i in range(_Cmax+1,n+1):
            _C.append([(_C[i-1][j] if j < i else 0) + (_C[i-1][j-1] if j > 0 else 0) for j in range(i+1)])
        _Cmax = n
        return _C[n][k]

    else:
        # This should only be done for large parameters that we will see infrequently.
        # Due to the fact that we are unlikely to see them again or not often, we do
        # not want to dedicate memory to extend Pascal's triangle as it will seldom be
        # used.
        return reduce(lambda a,b: a*(n-b)/(b+1), xrange(k), 1)


def permCount(n,k):
    """Calculate P(n,k) = n!/(n-k)!, the number of permutations over n objects, taking
    k of them at a time."""

    return binom(n,k) * reduce(lambda a,b:a*b, xrange(1,k+1), 1)


def createLookup(B):
    """Process B to create a reverse lookup scheme that is appropriate for
    any of the libraries in pyncomb that allow for one or more base sets to
    be specified.

    Let rev(K) be the reverse lookup dictionary of a list K, i.e. if
    K[i] = j, then rev(K)[j] = i.

    If B is an integer, then return B.
    If B is a flat list, then return a pair (B,rev(B)).
    If B is a list of lists / integers, then return a list Bn with:
       1. Bn[i] = B[i] if B[i] is an integer.
       2. Bn[i] = (B[i], rev(B[i])) if B[i] is a list.

    For example, createLookup can translate a base set specification of:
        [4,['a','b','c'],[11,22]]
    which represents three base sets [0,1,2,3], ['a','b','c'], [11,22].
    The returned data will consist of base sets with their reverse lookup
    data and can be used as the B parameter in any function."""

    # Handle integers.
    if type(B) == int:
        return B

    # Handle flat lists.
    if reduce(lambda a,b:a and b, [type(i) != list for i in B], True):
        return (B, dict([(B[i], i) for i in range(len(B))]))

    # Handle nested lists.
    Bn = []
    for D in B:
        if type(D) == int:
            Bn.append(D)
        else:
            Bn.append((D, dict([(D[i],i) for i in xrange(len(D))])))
    return Bn
