# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 09:26:03 2023

@author: chucker1
"""

class PatchGenerator:
    """
    PatchGenerator class generates patches of specified size within given dimensions with optional overlap.

    Args:
        xsize (int): Total size along the x-axis.
        ysize (int): Total size along the y-axis.
        x_patch_size (int): Patch size along the x-axis.
        y_patch_size (int): Patch size along the y-axis.
        x_overlap (int, optional): Overlap size in the x-axis. Defaults to 0.
        y_overlap (int, optional): Overlap size in the y-axis. Defaults to 0.
    
    Raises:
        ValueError: If x_patch_size is larger than xsize or y_patch_size is larger than ysize.
    """

    def __init__(self, xsize, ysize, x_patch_size, y_patch_size, x_overlap=0, y_overlap=0):
        if x_patch_size > xsize:
            raise ValueError("x_patch_size cannot be larger than xsize.")
        if y_patch_size > ysize:
            raise ValueError("y_patch_size cannot be larger than ysize.")
            
        self.xsize = xsize
        self.ysize = ysize
        self.x_patch_size = x_patch_size
        self.y_patch_size = y_patch_size
        self.x_overlap = x_overlap
        self.y_overlap = y_overlap
        self.current_i = 0
        self.current_j = 0


    def __iter__(self):
        """
        Returns the iterator object.

        Returns:
            PatchGenerator: Iterator object.
        """
        return self


    def __next__(self):
        """
        Generates the next patch.

        Returns:
            tuple: Block information as (i, j, rows, cols), where
                i (int): Starting position along the y-axis.
                j (int): Starting position along the x-axis.
                rows (int): Number of rows in the patch.
                cols (int): Number of columns in the patch.
        
        Raises:
            StopIteration: If the end of the iteration is reached.
        """
        if self.current_i >= self.ysize:
            raise StopIteration

        i = self.current_i
        j = self.current_j

        if i + self.y_patch_size < self.ysize:
            rows = self.y_patch_size
        else:
            rows = self.ysize - i

        if j + self.x_patch_size < self.xsize:
            cols = self.x_patch_size
        else:
            cols = self.xsize - j

        self.current_j += self.x_patch_size - self.x_overlap
        if self.current_j >= self.xsize:
            self.current_j = 0
            self.current_i += self.y_patch_size - self.y_overlap

        return (i, j, rows, cols)


if __name__ == "__main__":
    patch_generator = PatchGenerator(100, 80, 10, 20, y_overlap=2, x_overlap=3)
    for patch in patch_generator:
        row_start, cols_start, row_end, cols_end = patch
        print("row_start, cols_start, row_end, cols_end")
        print(row_start, cols_start, row_end, cols_end)
        