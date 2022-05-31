import unittest
from game.components import load_component_types

class TestComponents(unittest.TestCase):
    def test_load_component_types(self):

        component_types = load_component_types("data/component_types.txt")

        for component_type in component_types:
            print(component_type.name)

        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()