import pandas as pd

from singlecase.data import Data

def nap(data: Data, decreasing: bool = False) -> pd.Series:
    """
    Calculate the Nonoverlap Pairs (NAP) between two phases in a single-case data frame.

    Args:
        data (singlecase.Data): A single-case data set.
        decreasing (bool, optional): If you expect data to be lower in the second phase,
            set decreasing=True. Default is decreasing=False.

    Returns:
        nap values: The calculated NAP values in a pd.Series.
    """

    pvar = data.pvar
    phases = data._df[pvar].unique()
    if len(phases) != 2:
        raise ValueError(f"Only two phases are supported. The following phases were found in the phase variable : {pvar}: {phases}")
    

    nap_values = {}

    df = data._df
    for dvar in data.dvars:
        
        phase1_data = df.loc[df[pvar] == phases[0], dvar].dropna().values
        phase2_data = df.loc[df[pvar] == phases[1], dvar].dropna().values

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


def pnd(data: Data, decreasing: bool = False) -> pd.Series:
    """
    Calculate the Percent Non-overlapping Data (PND) between two phases in a single-case data frame.

    Args:
        data (singlecase.Data): A single-case data set.
        decreasing (bool, optional): If you expect data to be lower in the second phase,
            set decreasing=True. Default is decreasing=False.
    Returns:
        pnd_values (pd.Series): The calculated PND values in a pd.Series.
    """

    pvar = data.pvar
    phases = data._df[pvar].unique()
    if len(phases) != 2:
        raise ValueError(f"Only two phases are supported. The following phases were found in the phase variable : {pvar}: {phases}")

    pnd_values = {}

    df = data._df
    for dvar in data.dvars:
        phase1_data = df.loc[df[pvar] == phases[0], dvar].dropna().values
        phase2_data = df.loc[df[pvar] == phases[1], dvar].dropna().values

        extreme_value = max(phase1_data) if decreasing else min(phase1_data)
        non_overlapping_data = sum(value > extreme_value for value in phase2_data) if not decreasing else sum(value < extreme_value for value in phase2_data)

        pnd_values[dvar] = (non_overlapping_data / len(phase2_data)) * 100

    return pd.Series(pnd_values, name='pnd')
