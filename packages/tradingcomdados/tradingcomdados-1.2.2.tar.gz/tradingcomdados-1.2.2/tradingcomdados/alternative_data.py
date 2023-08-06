import pandas as pd

import functools
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def _logging_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.debug(f"function {func.__name__} called with args {signature}")
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.exception(
                f"Exception raised in {func.__name__}. exception: {str(e)}"
            )
            raise e

    return wrapper


@_logging_error
def _standardize_df():
    url = "https://raw.githubusercontent.com/victorncg/financas_quantitativas/main/IBOV.csv"
    df = pd.read_csv(
        url, encoding="latin-1", sep="delimiter", header=None, engine="python"
    )
    df = pd.DataFrame(df[0].str.split(";").tolist())
    df.columns = list(df.iloc[1])
    df[2:][["Código", "Ação", "Tipo", "Qtde. Teórica", "Part. (%)"]]
    df.reset_index(drop=True, inplace=True)

    return df


@_logging_error
def ibov_composition(assets: str = "all", mode: str = "df", reduction: bool = True):

    """
  This function captures the latest composition of IBOV. It is updated every 4 months.

  :param assets : you can pass a list with the desired tickets. Default = 'all'
  :type: str
  :param mode: you can return either the whole dataframe from B3, or just the list containing the tickers which compose IBOV. Default = 'df'
  :type: str
  :param reduction: you can choose whether the result should come with the reduction and theorical quantitiy provided by B3. Default = True
  :type: bool

  """

    df = _standardize_df()

    if reduction == False:
        df = df[:-2]

    if assets != "all":
        df = df[df["Código"].isin(assets)]

    if mode == "list":
        df = list(df.Código)

    return df
