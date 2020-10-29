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

"""Unit testing for the subsetlex module.

By Sebastian Raaphorst, 2009."""

import unittest
from . import subsetlex
from . import combfuncs

class Tester(unittest.TestCase):
    """Unit testing class for this module.
    We perform all operations over a given base set and check their
    interactions for correctness."""

    def setUp(self):
        self.B = combfuncs.createLookup(['a','b','c','d','e'])

    def testall(self):
        """Test the interactions between all functions."""

        v = (self.B if type(self.B) == int else len(self.B[1]))

        # We iterate over all subsets, and check their rank to make sure
        # it is as expected. Unrank the rank and make sure the unranked
        # set corresponds to what we have. This does not test succ
        # explicitly, but as this is called by all, it is implicitly tested.
        rk = 0
        for S in subsetlex.all(self.B):
            # Check to make sure that the rank of S is rk.
            self.assertEqual(subsetlex.rank(self.B, S), rk)

            # Check to make sure that unranking rk gives K.
            self.assertEqual(subsetlex.unrank(self.B, rk), S)

            # Increment the rank.
            rk += 1

        # Make sure that we saw the correct number of subsets.
        self.assertEqual(rk, 1 << v)


if __name__ == '__main__':
    unittest.main()

