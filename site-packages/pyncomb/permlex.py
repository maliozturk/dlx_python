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

"""An implementation of basic combinatorial permutation operations using
lexicographic ordering.

Note that for our purposes here, permutations are represented as lists,
with P[i] = j meaning that P maps i to j.

By Sebastian Raaphorst, 2009."""

from . import combfuncs


def rank(n, P):
    """Return the rank of a permutation P in Sn."""

    rk = 0
    Pn = P[:]

    # Calculate (n-1)!
    fac = reduce(lambda x,y:x*y, range(1,n), 1)

    # Now loop to calculate the rank.
    for j in xrange(n):
        rk += Pn[j] * fac
        if n != j+1:
            fac /= (n - j - 1)
        for i in range(j+1,n):
            if Pn[i] > Pn[j]:
                Pn[i] -= 1
    return rk


def unrank(n, rk):
    """Return the permutation of rank rk in Sn."""

    P = [0] * n

    # Store (j+1)! for calculation.

    fac = 1
    for j in xrange(n-1):
        fac *= (j+1)
        d = (rk % (fac * (j+2))) / fac
        rk -= d * fac
        P[n-j-2] = d
        for i in xrange(n-j-1,n):
            if P[i] > d-1:
                P[i] += 1
    return P


def succ(n, P):
    """Return the successor of the permutation P in Sn.
    If there is no successor, we return None."""

    Pn = P[:] + [-1]
    i = n-2
    while Pn[i+1] < Pn[i]:
        i -= 1
    if i == -1:
        return None

    j = n-1
    while Pn[j] < Pn[i]:
        j -= 1

    Pn[i], Pn[j] = Pn[j], Pn[i]
    Pn[i+1:n] = Pn[n-1:i:-1]
    return Pn[:-1]


def all(n):
    """A generator to create all permutations in Sn."""

    P = range(n)
    while P != None:
        yield P
        P = succ(n, P)

