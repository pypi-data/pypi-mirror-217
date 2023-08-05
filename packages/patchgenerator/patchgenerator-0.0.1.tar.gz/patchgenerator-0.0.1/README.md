# `patchgenerator`

The `patchgenerator` is a simple tool to generate array indices, with or without overlap, to create numpy array patches. Only requires python.

# Example usage:

```
from patch_indices import PatchGenerator
patch_generator = PatchGenerator(100, 80, 10, 20, y_overlap=2, x_overlap=3)
for patch in patch_generator:
    row_start, cols_start, row_end, cols_end = patch
    print("row_start, cols_start, row_end, cols_end", row_start, cols_start, row_end, cols_end)
```