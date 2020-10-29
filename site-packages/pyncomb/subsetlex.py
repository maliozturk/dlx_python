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

"""An implementation of basic combinatorial subset opertions using
lexicographic ordering.

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


def rank(B, S):
    """Return the rank of the subset S in base set B."""

    return reduce(lambda a,b: a | b, [1 << (i if type(B) == int else B[1][i]) for i in S], 0)


def unrank(B, rk):
    """Return the subset of rank rk in base set B."""

    return [(i if type(B) == int else B[0][i]) for i in xrange((B if type(B) == int else len(B[0]))) if (1 << i) & rk]


def succ(B, S):
    """Return the successor of the subset S in base set B."""

    # This consists of including the smallest element, and if it is already
    # included, omitting it and then trying to include the next highest
    # element. This is the exact same algorithm as ranking, adding 1, and then
    # unranking, so we simply perform these two steps to get the desired
    # result. Check if we have overflowed and return None if necessary.
    Sn = unrank(B,rank(B,S)+1)
    return (None if Sn == [] else Sn)


def all(B):
    """A generator to create all subsets over the specified base set."""

    # Make the base set, creating a copy of B if B is a pair as described in
    # the module introduction; thus, if B changes, the iterator does not
    # become invalid.
    Bn = (B if type(B) == int else (B[0][:], dict(B[1])))
    K = []
    while K != None:
        yield K
        K = succ(Bn, K)

