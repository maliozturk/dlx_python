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

"""Combinatorial functions for manipulating tuples (represented as lists) over
mixed base sets, ordered by lexicographical ordering.

For example, say we want all tuples over the following sets:
          [0,1,2]
          ['a','b']
          [8,7,6,5]

Then these would consist of the 24 tuples:
   [0,'a',8], [0,'a',7], [0,'a',6], [0,'a',5],
   [0,'b',8], [0,'b',7], [0,'b',6], [0,'b',5],
   [1,'a',8], [1,'a',7], [1,'a',6], [1,'a',5],
   [1,'b',8], [1,'b',7], [1,'b',6], [1,'b',5],
   [2,'a',8], [2,'a',7], [2,'a',6], [2,'a',5],
   [2,'b',8], [2,'b',7], [2,'b',6], [2,'b',5].

For the mixed base representation, we allow the elements of the tuple to be
picked from specific base sets, represented in our function by B, which
consists of a list with entry i either:
A. a 2-tuple consisting of:
     1. a list of the possible values for position i in a tuple.
     2. a reverse lookup dict for the list of possible values.
   Example: [0,3,4,2], {0:0, 3:1, 4:2, 2:3}.
   We require the reverse lookup dict for efficient algorithms; otherwise, we
   would need to invoke many calls to the list index method.
B. an integer j, representing that the value for position i be taken from
   [0,...,j-1]. Note that this is more efficient as we do not need to perform
   lookups from a dictionary in order to execute the operations."""

def rank(B, T):
    """Return the rank of tuple T over the base represented by B.
    See the library description for how base representations work."""

    rank = 0
    posMult = 1
    for i in xrange(len(T)):
        idx = len(T)-i-1
        rank += (posMult * T[idx] if type(B[idx]) == int else posMult * B[idx][1][T[idx]])
        posMult *= (B[idx] if type(B[idx]) == int else len(B[idx][0]))
    return rank


def unrank(B, rk):
    """Return the tuple of rank rk over the base represented by B.
    See the library description for how base representations work."""

    T = [0] * len(B)
    posMult = reduce(lambda a,b:a*b, [(i if type(i) == int else len(i[0])) for i in B])

    for i in xrange(len(B)):
        # Adjust posMult to represent the seeker for position i.
        posMult /= (B[i] if type(B[i]) == int else len(B[i][0]))

        # Determine the index of the element in position i.
        idx = rk / posMult

        # Translate this to an actual element.
        T[i] = (idx if type(B[i]) == int else B[i][0][idx])

        # Now we have processed out the element in position i, so adjust the rank to
        # get the reduced rank.
        rk %= posMult

    return T


def succ(B, T):
    """Return the successor of the tuple T over the base represented by B.
    Returns None if T is the last tuple in the ordering.
    See the library description for how base representations work."""

    Tnew = T[:]
    for i in xrange(len(B)):
        # Increase the entry in position len(B)-i-1 if possible (i.e. we work
        # right-to-left).
        idx = len(B)-i-1

        if type(B[idx]) == int:
            Tnew[idx] = (Tnew[idx] + 1) % B[idx]

            # If we are not 0, then the increment was successful and we
            # can stop. Otherwise, we reached the end of the base set and
            # had to loop back to the beginning, so we must continue.
            if Tnew[idx] > 0:
                return Tnew

        else:
            # Move to the next position in the list.
            basis, lookup = B[idx]
            Tnew[idx] = basis[(lookup[Tnew[idx]] + 1) % len(basis)]

            # If we re not the first element in the base set, the increment
            # was successful and we can stop. otherwise, we reached the end
            # of the base set and had to loop back to the beginning, so we
            # must continue.
            if Tnew[idx] != basis[0]:
                return Tnew

    # We could not increment anything, and thus were at the end of the list.
    return None


def all(B):
    """A generator to create all tuples over the supplied mixed base B."""
    T = [(0 if type(B[i]) == int else B[i][0][0]) for i in xrange(len(B))]
    while T != None:
        yield T
        T = succ(B,T)
