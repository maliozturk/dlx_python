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

"""Unit testing for the permtj module.

By Sebastian Raaphorst, 2009."""

import unittest
from . import permtj
from . import combfuncs

class Tester(unittest.TestCase):
    """Unit testing class for this module.
    We perform all operations and check their interactions for correctness."""

    def setUp(self):
        self.n = 5

    def testall(self):
        """Test the interactions between all functions."""

        # We iterate over all permutations, and check their rank to make sure
        # it is as expected. Unrank the rank and make sure the unranked
        # permutation corresponds to what we have. This does not test succ
        # explicitly, but as this is called by all, it is implicitly tested.
        rk = 0
        for P in permtj.all(self.n):
            # Check to make sure that the rank of K is rk.
            self.assertEqual(permtj.rank(self.n, P), rk)

            # Check to make sure that unranking rk gives K.
            self.assertEqual(permtj.unrank(self.n, rk), P)

            # Increment the rank.
            rk += 1

        # Make sure that we saw the correct number of permutations, namely n!
        self.assertEqual(rk, reduce(lambda x,y:x*y, range(1,self.n+1), 1))


if __name__ == '__main__':
    unittest.main()

