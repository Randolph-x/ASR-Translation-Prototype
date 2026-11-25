import unittest
from simulation import simulate, confirm_correction
class SimulationTests(unittest.TestCase):
    def test_standard_high_confidence(self):
        result = simulate('climate')
        self.assertEqual(result['confidence'], 92)
        self.assertFalse(result['needs_review'])
    def test_low_confidence_requires_review(self):
        result = simulate('fifteen')
        self.assertTrue(result['needs_review'])
        self.assertIn('五十', result['translation'])
    def test_correction_changes_number(self):
        result = confirm_correction('fifteen')
        self.assertIn('十五', result['translation'])
        self.assertEqual(result['confidence'], 95)
        self.assertFalse(result['needs_review'])
    def test_unsupported_input(self):
        with self.assertRaises(ValueError): simulate('unknown')
    def test_energy_correction(self):
        self.assertIn('可能有助于', confirm_correction('energy')['translation'])
    def test_high_confidence_can_be_wrong(self):
        result = simulate('fifteen_high')
        self.assertEqual(result['confidence'], 94)
        self.assertFalse(result['needs_review'])
        self.assertIn('五十', result['translation'])
    def test_high_confidence_manual_correction(self):
        result = confirm_correction('fifteen_high')
        self.assertIn('十五', result['translation'])
        self.assertEqual(result['confidence'], 95)
        self.assertEqual(result['correction'], '')
    def test_normal_caption_unchanged(self):
        self.assertEqual(simulate('climate'), confirm_correction('climate'))
    def test_scenario_is_not_mutated(self):
        confirm_correction('fifteen_high')
        self.assertIn('五十', simulate('fifteen_high')['translation'])
if __name__ == '__main__': unittest.main()
