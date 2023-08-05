import numpy as np
from typing import List, Tuple, Union, Callable    
import pandas as pd

def permutation_test(data: pd.DataFrame,
                     dvars: Union[List[str], str],
                     pvar: str,
                     statistic: Union[str, Callable] = 'mean',
                     phases: Tuple[str, str] = ("A", "B"),
                     num_rounds: int = 10000,
                     seed: int = None) -> pd.Series:
    """
    Perform a permutation test between two phases in a single-case data frame.

    Args:
        data (pd.DataFrame): A single-case data frame.
        dvars (Union[List[str], str]): One or more dependent variables to perform the permutation test on.
        pvar (str): The name of the phase variable.
        statistic (Union[str, Callable], optional): The statistic to be used in the permutation test
            (either 'mean', 'median', or a custom callable). Default is 'mean'.
        phases (Tuple[str, str], optional): A tuple of two column names in the data frame
            indicating the two phases that should be compared. Default is ("A", "B").
        num_rounds (int, optional): The number of iterations for the permutation test. Default is 10000.
        seed (int, optional): Random seed for reproducibility. Default is None.

    Returns:
        p_values (pd.Series): The calculated p-values in a pd.Series.
    """

    if isinstance(dvars, str):
        dvars = [dvars]

    if pvar not in data.columns:
        raise ValueError("pvar must be the name of a column in the data frame")

    if len(phases) != 2:
        raise ValueError("phases must be a tuple of two phase names")

    if phases[0] not in data[pvar].values or phases[1] not in data[pvar].values:
        raise ValueError("phases must be a tuple of two phase names that are present in the data frame")

    if isinstance(statistic, str):
        if statistic == 'mean':
            statistic = np.mean
        elif statistic == 'median':
            statistic = np.median
        else:
            raise ValueError("statistic must be either 'mean', 'median', or a callable")

    np.random.seed(seed)

    p_values = {}

    for dvar in dvars:
        if dvar not in data.columns:
            raise ValueError("dvar must be the name of a column in the data frame")

        phase1_data = data.loc[data[pvar] == phases[0], dvar].values
        phase2_data = data.loc[data[pvar] == phases[1], dvar].values

        phase1_data = phase1_data[~np.isnan(phase1_data)]
        phase2_data = phase2_data[~np.isnan(phase2_data)]

        observed_diff = statistic(phase2_data) - statistic(phase1_data)

        combined_data = np.concatenate((phase1_data, phase2_data))

        permuted_diffs = []
        for _ in range(num_rounds):
            np.random.shuffle(combined_data)
            permuted_phase1_data = combined_data[:len(phase1_data)]
            permuted_phase2_data = combined_data[len(phase1_data):]
            permuted_diff = statistic(permuted_phase2_data) - statistic(permuted_phase1_data)
            permuted_diffs.append(permuted_diff)

        permuted_diffs = np.array(permuted_diffs)
        p_value = (np.abs(permuted_diffs) >= np.abs(observed_diff)).sum() / num_rounds
        p_values[dvar] = p_value

    return pd.Series(p_values, name="p_value")
