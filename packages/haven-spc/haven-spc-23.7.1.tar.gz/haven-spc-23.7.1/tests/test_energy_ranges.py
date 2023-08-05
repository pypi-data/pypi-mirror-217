import unittest
import logging

import numpy as np

from haven import ERange, KRange, merge_ranges


logging.basicConfig(level=logging.INFO)


class EnergyRangeTests(unittest.TestCase):
    def test_e_range(self):
        """Test the ERange class for calculating energy points."""
        e_range = ERange(E_min=8300, E_max=8400, E_step=0.5, exposure=0.1)
        np.testing.assert_equal(e_range.energies(), np.arange(8300, 8400.5, 0.5))
        np.testing.assert_equal(e_range.exposures(), [0.1] * len(e_range.energies()))

    def test_k_range(self):
        E0 = 17038
        k_range = KRange(E_min=30, k_max=14, k_step=0.05, k_weight=1, exposure=1.0)
        # Verify the results compared to Shelly's spreadsheet
        np.testing.assert_almost_equal(k_range.wavenumbers()[0], 2.8060742521)
        np.testing.assert_almost_equal(k_range.wavenumbers()[-1], 14.006074252)
        energies = k_range.energies() + E0
        np.testing.assert_equal(energies[0], E0 + k_range.E_min)
        np.testing.assert_almost_equal(energies[-1], 17785.40463351)
        np.testing.assert_equal(k_range.exposures()[0], 1.0)
        np.testing.assert_almost_equal(
            k_range.exposures()[16], 1.28529317348436, decimal=3
        )

    def test_merge_ranges(self):
        e_range1 = ERange(1, 5, 1, exposure=0.5)
        e_range2 = ERange(5, 7, 0.5, exposure=1)
        merged, exposures = merge_ranges(e_range2, e_range1)
        # Test validity of the result
        np.testing.assert_equal(merged, [1, 2, 3, 4, 5, 5.5, 6, 6.5, 7])
        np.testing.assert_equal(
            exposures, [0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0]
        )
