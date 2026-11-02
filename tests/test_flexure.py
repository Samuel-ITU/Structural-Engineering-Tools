import unittest
from rc_beam import BeamInput, calculate_flexure

class FlexureTests(unittest.TestCase):
    def setUp(self):
        self.x = BeamInput(300, 550, 40, 10, 20, 3, 28, 420, 150)

    def test_reference_hand_calculation(self):
        r = calculate_flexure(self.x)
        self.assertAlmostEqual(r.As_mm2, 942.4778, places=3)
        self.assertAlmostEqual(r.d_mm, 490)
        self.assertAlmostEqual(r.a_mm, 55.4399, places=3)
        self.assertAlmostEqual(r.Mn_knm, 183.008, delta=0.02)
        self.assertAlmostEqual(r.phi, 0.9)
        self.assertTrue(r.passes)

    def test_overload_fails(self):
        self.assertFalse(calculate_flexure(BeamInput(300,550,40,10,20,3,28,420,300)).passes)

    def test_invalid_geometry(self):
        with self.assertRaises(ValueError):
            calculate_flexure(BeamInput(300,50,40,10,20,3,28,420,10))

    def test_minimum_reinforcement(self):
        r = calculate_flexure(BeamInput(300,550,40,10,10,1,28,420,1))
        self.assertFalse(r.passes)

if __name__ == "__main__":
    unittest.main()
