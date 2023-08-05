from typing import Union, Dict
import pandas as pd


class Data:
    """
    A class used to represent single-case data in a structured format.

    This class accepts data either as a pandas DataFrame or as a dictionary and 
    stores it internally as a DataFrame for further manipulation and analysis. It 
    provides properties to manage the phase variable and dependent variables present
    in the data.

    Any variable with datatype of float is assumed to be a dependent variable. The 

    Args:
        data (Union[pd.DataFrame, Dict]): The data set. Must be either a pandas DataFrame 
        or a dictionary.
    
    Raises:
        ValueError: If the provided data is not a pandas DataFrame or a dictionary.
    """

    def __init__(self, data: Union[pd.DataFrame, Dict]):
        """
        Constructs and initializes the Data object.
        """

        if isinstance(data, dict):
            self._df = pd.DataFrame(data)
        elif isinstance(data, pd.DataFrame):
            self._df = data.copy()
        else:
            raise ValueError("data must be a pd.DataFrame or a dict")

        self._pvar = None

        # float columns are assumend to be dependent variables
        self._dvars = [col for col in self._df.columns if self._df[col].dtype == float]

    @property
    def pvar(self):
        """
        Property that gets the phase variable of the Data object.

        Returns:
            str: The name of the phase variable column in the data frame.
        """
        return self._pvar
    
    @pvar.setter
    def pvar(self, pvar: str):
        """
        Property that sets the phase variable of the Data object.

        Args:
            pvar (str): The name of the phase variable column to be set.

        Raises:
            ValueError: If the provided pvar is not a column name in the DataFrame.
        """
        if pvar not in self._df.columns:
            raise ValueError("pvar must be the name of a column in the data frame")
        self._pvar = pvar

    @property
    def dvars(self):
        """
        Property that gets the names of the dependent variable columns.

        These are identified as any columns in the DataFrame with float datatype.

        Returns:
            List[str]: The names of the dependent variable columns.
        """
        return self._dvars

