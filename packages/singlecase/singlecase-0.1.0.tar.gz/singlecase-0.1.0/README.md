# Single Case Research Package

The Single Case Research package is a Python library designed to assist in conducting single-case research studies. It provides functions to calculate effect sizes and perform permutation tests between two phases in a single-case data frame.

More functionality will be added as the package is further developed

## Installation

You can install the package using pip:

```shell
pip install singlecase
```

## Functionality

The package currently includes the following functions:

### Effect Size Calculation

#### `nap(data: pd.DataFrame, dvars: Union[List[str], str], pvar: str, decreasing: bool = False, phases: Tuple[str, str] = ("A", "B")) -> pd.Series`

Calculate the Nonoverlap Pairs (NAP) between two phases in a single-case data frame.

- `data`: A single-case data frame.
- `dvars`: One or more dependent variables to calculate NAP for.
- `pvar`: The name of the phase variable.
- `decreasing`: If you expect data to be lower in the second phase, set `decreasing=True`. Default is `decreasing=False`.
- `phases`: A tuple of two column names in the data frame indicating the two phases that should be compared. Default is `("A", "B")`.

Returns the calculated NAP values in a Pandas Series.

#### `pnd(data: pd.DataFrame, dvars: Union[List[str], str], pvar: str, decreasing: bool = False, phases: Tuple[str, str] = ("A", "B")) -> pd.Series`

Calculate the Percent Non-overlapping Data (PND) between two phases in a single-case data frame.

- `data`: A single-case data frame.
- `dvars`: One or more dependent variables to calculate PND for.
- `pvar`: The name of the phase variable.
- `decreasing`: If you expect data to be lower in the second phase, set `decreasing=True`. Default is `decreasing=False`.
- `phases`: A tuple of two column names in the data frame indicating the two phases that should be compared. Default is `("A", "B")`.

Returns the calculated PND values in a Pandas Series.

### Permutation Test

#### `permutation_test(data: pd.DataFrame, dvars: Union[List[str], str], pvar: str, statistic: Union[str, Callable] = 'mean', phases: Tuple[str, str] = ("A", "B"), num_rounds: int = 10000, seed: int = None) -> pd.Series`

Perform a permutation test between two phases in a single-case data frame.

- `data`: A single-case data frame.
- `dvars`: One or more dependent variables to perform the permutation test on.
- `pvar`: The name of the phase variable.
- `statistic`: The statistic to be used in the permutation test (either 'mean', 'median', or a custom callable). Default is `'mean'`.
- `phases`: A tuple of two column names in the data frame indicating the two phases that should be compared. Default is `("A", "B")`.
- `num_rounds`: The number of iterations for the permutation test. Default is `10000`.
- `seed`: Random seed for reproducibility. Default is `None`.

Returns the calculated p-values in a Pandas Series.

## Usage

Here's a basic example demonstrating how to use the functions in the Single Case Research package:

```python
import pandas as pd
from singlecase.effectsize import nap, pnd
from singlecase.permtest import permutation_test

# Load your single-case data into a Pandas DataFrame



# Calculate NAP
nap_values = nap(data, dvars=['dependent_var1', 'dependent_var2'], pvar='phase_var')

# Calculate PND
pnd_values = pnd(data, dvars='dependent_var1', pvar='phase_var')

# Perform permutation test
p_values = permutation_test(data, dvars='dependent_var1', pvar='phase_var')

# Print the results
print("NAP Values:")
print(nap_values)

print("PND Values:")
print(pnd_values)

print("P-Values:")
print(p_values)
```

## License

This project is licensed under the BSD 3-clause license - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The Single Case Research package is being developed by Casper Wilstrup.

