# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 14:55:01 2023

@author: chucker1
"""

import unittest
import sys # added!
sys.path.append("..") # added!
from src.patch_indices.patch_indices import PatchGenerator

class PatchGeneratorTestCase(unittest.TestCase):
    def test_patch_generation(self):
        patch_generator = PatchGenerator(100, 80, 10, 20, y_overlap=2, x_overlap=3)

        expected_patches = [
            (0, 0, 20, 10), # First block
            (0, 7, 20, 10), # Second block with overlap
            (0, 14, 20, 10), # Third block with overlap
            (0, 21, 20, 10)  # Fourth block with overlap and adjusted size
        ]

        generated_patches = list(patch_generator)[:4]

        self.assertEqual(len(generated_patches), len(expected_patches))

        for expected, generated in zip(expected_patches, generated_patches):
            self.assertEqual(expected, generated)
    
            
    def test_patch_size_exception(self):
        # Test case where x_block_size is larger than xsize
        with self.assertRaises(ValueError):
            generator1 = PatchGenerator(100, 80, 120, 20, y_overlap=2, x_overlap=3)

        # Test case where y_block_size is larger than ysize
        with self.assertRaises(ValueError):
            generator2 = PatchGenerator(100, 80, 10, 100, y_overlap=2, x_overlap=3)

if __name__ == '__main__':
    unittest.main()
    
