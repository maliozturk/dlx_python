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
Trotter-Johnson (a minimal change) ordering.

Note that for our purposes here, permutations are represented as lists,
with P[i] = j meaning that P maps i to j.

By Sebastian Raaphorst, 2009."""

from . import combfuncs


def rank(n, P):
    """Return the rank of a permutation P in Sn."""

    rk = 0
    for j in xrange(2,n+1):
        k = 1
        i = 0
        while P[i] != j-1:
            if P[i] < j-1:
                k += 1
            i += 1
        if rk % 2 == 0:
            rk = j*rk + j - k
        else:
            rk = j*rk + k - 1
    return rk


def unrank(n, rk):
    """Return the permutation of rank rk in Sn."""

    P = [0] * n
    r2 = 0

    # Keep track of factorials to avoid repeated computation.
    fac = 1
    nfac = reduce(lambda x,y:x*y, range(1,n+1), 1)

    for j in xrange(2,n+1):
        fac *= j
        r1 = (rk * fac) / nfac
        k = r1 - j * r2

        if r2%2 == 0:
            for i in range(j-2,j-k-2,-1):
                P[i+1] = P[i]
            P[j-k-1] = j-1
        else:
            for i in range(j-2,k-1,-1):
                P[i+1] = P[i]
            P[k] = j-1
        r2 = r1
    return P


def succ(n, P):
    """Return the successor of the permutation P in Sn.
    If there is no successor, we return None."""

    def _permParity(n, P):
        """Determine the number of cycles in P."""

        alpha = [0] * n
        c = 0
        for j in xrange(n):
            if alpha[j] == 0:
                c += 1
                alpha[j] = 1
                i = j
                while P[i] != j:
                    i = P[i]
                    alpha[i] = 1
        return (n-c)%2

    st = 0
    rho = P[:]
    Pn = P[:]
    m = n

    while m > 1:
        d = rho.index(m-1)
        rho[d:m-1] = rho[d+1:m]

        par = _permParity(m-1, rho)
        if par == 1:
            if d == m-1:
                m -= 1
            else:
                Pn[st+d], Pn[st+d+1] = Pn[st+d+1], Pn[st+d]
                break
        else:
            if d == 0:
                m -= 1
                st += 1
            else:
                Pn[st+d], Pn[st+d-1] = Pn[st+d-1], Pn[st+d]
                break

    return (None if m == 1 else Pn)


def all(n):
    """A generator to create all permutations in Sn."""

    P = range(n)
    while P != None:
        yield P
        P = succ(n, P)
