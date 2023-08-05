import numpy as np
from typing import List, Tuple, Union

import pandas as pd

def nap(data: pd.DataFrame,
        dvars: Union[List[str], str],
        pvar: str,
        decreasing: bool = False,
        phases: Tuple[str, str] = ("A", "B")) -> pd.Series:
    """
    Calculate the Nonoverlap Pairs (NAP) between two phases in a single-case data frame.

    Args:
        data (pd.DataFrame): A single-case data frame.
        dvar (str): One or more dependent variables to calculate NAP for.
        pvar (str): The name of the phase variable.
        decreasing (bool, optional): If you expect data to be lower in the second phase,
            set decreasing=True. Default is decreasing=False.
        phases (Tuple[str, int], optional): A tuple of two column names in the data frame
            indicating the two phases that should be compared. Default is ("A", "B").

    Returns:
        nap values: The calculated NAP values in a pd.Series.
    """

    if isinstance(dvars, str):
        dvars = [dvars]

    if pvar not in data.columns:
        raise ValueError("pvar must be the name of a column in the data frame")

    if len(phases) != 2:
        raise ValueError("phases must be a tuple of two phase names")
    
    if phases[0] not in data[pvar].values or phases[1] not in data[pvar].values:
        raise ValueError("phases must be a tuple of two phase names that are present in the data frame")
    
    
    

    nap_values = {}
    for dvar in dvars:
        if dvar not in data.columns:
            raise ValueError("dvar must be the name of a column in the data frame")
        
        phase1_data = data.loc[data[pvar] == phases[0], dvar].values
        phase2_data = data.loc[data[pvar] == phases[1], dvar].values

        non_overlapping_pairs = 0
        total_pairs = 0

        for value1 in phase1_data:
            for value2 in phase2_data:
                total_pairs += 1
                if decreasing:
                    if value2 < value1:
                        non_overlapping_pairs += 1
                else:
                    if value2 > value1:
                        non_overlapping_pairs += 1

        nap_values[dvar] = non_overlapping_pairs / total_pairs

    return pd.Series(nap_values, name='nap')


def pnd(data: pd.DataFrame,
        dvars: Union[List[str], str],
        pvar: str,
        decreasing: bool = False,
        phases: Tuple[str, str] = ("A", "B")) -> pd.Series:
    """
    Calculate the Percent Non-overlapping Data (PND) between two phases in a single-case data frame.

    Args:
        data (pd.DataFrame): A single-case data frame.
        dvars (Union[List[str], str]): One or more dependent variables to calculate PND for.
        pvar (str): The name of the phase variable.
        decreasing (bool, optional): If you expect data to be lower in the second phase,
            set decreasing=True. Default is decreasing=False.
        phases (Tuple[str, str], optional): A tuple of two column names in the data frame
            indicating the two phases that should be compared. Default is ("A", "B").

    Returns:
        pnd_values (pd.Series): The calculated PND values in a pd.Series.
    """

    if isinstance(dvars, str):
        dvars = [dvars]

    if pvar not in data.columns:
        raise ValueError("pvar must be the name of a column in the data frame")

    if len(phases) != 2:
        raise ValueError("phases must be a tuple of two phase names")

    if phases[0] not in data[pvar].values or phases[1] not in data[pvar].values:
        raise ValueError("phases must be a tuple of two phase names that are present in the data frame")

    pnd_values = {}
    for dvar in dvars:
        if dvar not in data.columns:
            raise ValueError("dvar must be the name of a column in the data frame")

        phase1_data = data.loc[data[pvar] == phases[0], dvar].values
        phase2_data = data.loc[data[pvar] == phases[1], dvar].values

        extreme_value = max(phase1_data) if decreasing else min(phase1_data)
        non_overlapping_data = sum(value > extreme_value for value in phase2_data) if not decreasing else sum(value < extreme_value for value in phase2_data)

        pnd_values[dvar] = (non_overlapping_data / len(phase2_data)) * 100

    return pd.Series(pnd_values, name='pnd')
