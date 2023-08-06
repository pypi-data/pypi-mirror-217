# cephes4py

cephes4py is a Python interface to the HCephes library, which is a reformatted version of Netlib Cephes. It provides a convenient way to access the functionality of the HCephes library within Python. cephes4py has been updated to ensure compatibility with modern Numba releases (specifically tested on version 0.57.0).

## Motivation
The motivation behind developing cephes4py was the need to use SciPy special functions within Numba functions running in nopython mode. Unfortunately, this was not possible due to compatibility issues. Since many of SciPy's special functions are actually wrappers of Cephes functions, I decided to create my own bindings to Cephes that were compatible with Numba.

Although cephes4py is much less "batteries included", I have conducted a preliminary experiment that suggests some performance improvements as well. You can refer to [this notebook](/workspaces/cephes4py/test.ipynb) for more details.

# No Argument Validation
It is important to note that cephes4py does not perform validation of the arguments passed to the underlying C-functions. This decision was made because validating even a single argument in Python could potentially double the execution time. Additionally, it would require wrapping the functions with the validation code, which makes them uncompatible with Numba. Therefore, I have chosen to leave the responsibility and freedom of argument validation to you. Please refer to [FUNCTIONS.txt](./FUNCTIONS.txt) or [interface.h](cephes4py/interface.h) to see the expected parameter and return types.

In the event that you provide invalid arguments, Hcephes will display an error message and return a fallback value. Please keep in mind that an argument can be considered invalid even if the data type is correct. For example, the binomial distribution function requires arguments to be positive, with the parameter `p` ranging from 0 to 1 and `k` being smaller than `n`. Once again, please consult [FUNCTIONS.txt](./FUNCTIONS.txt) for more information.

## Cephes Function Bindings
For a list of available Cephes functions and their descriptions, please refer to [FUNCTIONS.txt](./FUNCTIONS.txt). Please note that I have not tested all of the functions extensively, but as long as the parameters and return types are scalar-valued, they should work properly. If you intend to pass Numpy arrays as arguments, things get a little more involved as you'll have to get the pointer to its buffer:
```python
a = np.zeros(10, dtype=np.float64)
pointer = cephes4py.from_buffer("double[]", a)
function_you_want_to_use(pointer)
```

## Installation
To install cephes4py, please follow these steps:

1. Install the [hcephes](https://github.com/limix/hcephes) binary. It is recommended to compile it from source, but you will need Cmake to do so. You can use the following command to install it:
   ```sh
   curl -fsSL https://git.io/JerYI | GITHUB_USER=limix GITHUB_PROJECT=hcephes bash
   ```
2. Navigate to the root directory of this repository.
3. Install the cephes4py package by running the following command:
   ```sh
   pip install .
   ```
4. You're all set! You can now use cephes4py in your Python code:
   ```python
   import cephes4py
   
   # Example usage
   bdtr = cephes4py.bdtr(4, 6, 0.3)

   # You can even use the function in Numba-jitted functions running in nopython mode:
   @nb.njit
   def nb_bdtr(k, n, p):
     return cephes4py.bdtr(k, n, p)

   bdtr = nb_bdtr(4, 6, 0.3)
   ```
