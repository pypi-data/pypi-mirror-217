import os
from time import sleep
from typing import Union

import pandas as pd
from pandas.core.frame import DataFrame, Series
from tempfile import NamedTemporaryFile


def series_to_dataframe(
        df: Union[pd.Series, pd.DataFrame]
) -> (Union[pd.Series, pd.DataFrame], bool):
    dataf = df.copy()
    isseries = False
    if isinstance(dataf, pd.Series):
        columnname = dataf.name
        dataf = dataf.to_frame()

        try:
            dataf.columns = [columnname]
        except Exception:
            dataf.index = [columnname]
            dataf = dataf.T
        isseries = True

    return dataf, isseries


def get_tmpfile(suffix=".xlsx"):
    tfp = NamedTemporaryFile(delete=False, suffix=suffix)
    filename = tfp.name
    tfp.close()
    return filename


def edit_pandas_with_excel(dframe, sleeptime=3):
    """
    Use this function to quick edit your DataFrame with MS Excel.
    Of course, Pandas is a lot better than Excel, but if you have to change arbitrary values which don't have a clear pattern,
    a GUI is imho the best choice.

    #Here is an example:

    import pandas as pd
    from a_pandas_ex_excel_edit import pd_add_excel_editor

    #pd_add_excel_editor will add 2 new methods
    #pandas.Series.s_edit_in_excel
    #pandas.DataFrame.d_edit_in_excel
    pd_add_excel_editor()

    dframe = pd.read_csv("https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv")
    #Let's add a row with lists, a tough data type to handle
    dframe['list_in_columns'] = [[[1]*10]] * len(dframe)

             PassengerId  Survived  ...  Embarked                   list_in_columns
    0              1         0  ...         S  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    1              2         1  ...         C  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    2              3         1  ...         S  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    3              4         1  ...         S  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    4              5         0  ...         S  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    ..           ...       ...  ...       ...                               ...
    886          887         0  ...         S  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    887          888         1  ...         S  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    888          889         0  ...         S  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    889          890         1  ...         C  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    890          891         0  ...         Q  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    [891 rows x 13 columns]

    dframe.dtypes
    Out[6]:
    PassengerId          int64
    Survived             int64
    Pclass               int64
    Name                object
    Sex                 object
    Age                float64
    SibSp                int64
    Parch                int64
    Ticket              object
    Fare               float64
    Cabin               object
    Embarked            object
    list_in_columns     object
    dtype: object

    df = dframe.d_edit_in_excel() #DataFrames

    Out[7]:
         PassengerId  Survived  ...  Embarked                       list_in_columns
    0          10001      9999  ...   NOT YET  [[1, 99999, 1, 1, 1, 1, 1, 1, 1, 1]]
    1          10000         1  ...         C      [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    2           9999         1  ...   NOT YET      [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    3           9998         1  ...   NOT YET      [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    4           9997         0  ...         S      [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    ..           ...       ...  ...       ...                                   ...
    886          887         0  ...         S      [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    887          888         1  ...         S      [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    888          889         0  ...         S      [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    889          890         1  ...         C      [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    890          891         0  ...         Q      [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    [891 rows x 13 columns]

       df.dtypes
    Out[9]:
    PassengerId          uint16
    Survived             uint16
    Pclass                uint8
    Name                 string
    Sex                category
    Age                  object
    SibSp                 uint8
    Parch                 uint8
    Ticket               object
    Fare                float64
    Cabin              category
    Embarked           category
    list_in_columns      object #you can even edit lists, dicts and tuples with Excel!
    dtype: object

    df2 = dframe.Name.s_edit_in_excel() #Series

    df2
    Out[8]:
    0                                        HANNIBAL LECTOR
    1      Cumings, Mrs. John Bradley (Florence Briggs Th...
    2                                 Heikkinen, Miss. Laina
    3           Futrelle, Mrs. Jacques Heath (Lily May Peel)
    4                               Allen, Mr. William Henry
                                 ...
    886                                Montvila, Rev. Juozas
    887                         Graham, Miss. Margaret Edith
    888             Johnston, Miss. Catherine Helen "Carrie"
    889                                Behr, Mr. Karl Howell
    890                                  Dooley, Mr. Patrick
    Name: Name, Length: 891, dtype: string

        Parameters:
            dframe: Union[pd.Series, pd.DataFrame]
        Returns:
            Union[pd.Series, pd.DataFrame]

    """
    df, isseries = series_to_dataframe(dframe)
    tmpfile = get_tmpfile(suffix=".xlsx")
    df.to_excel(tmpfile, index=True, index_label=df.index.to_list(), na_rep='<NA>')
    os.startfile(tmpfile)
    sleep(sleeptime)
    while True:
        try:
            os.rename(tmpfile, tmpfile)
            sleep(sleeptime)
            break
        except OSError:
            sleep(sleeptime)
            continue
    try:
        df2 = pd.read_excel(tmpfile, index_col=0, dtype=df.dtypes.to_dict())
    except Exception:
        df2 = pd.read_excel(tmpfile, index_col=0)
        for key, item in df.dtypes.to_dict().items():
            try:
                df2[key] = df2[key].astype(item)
            except Exception:
                continue
    if isseries:
        df2 = df2[df2.columns[0]]
    try:
        os.remove(tmpfile)
    except Exception:
        pass
    return df2


def pd_add_excel_editor():
    DataFrame.d_edit_in_excel = edit_pandas_with_excel
    Series.s_edit_in_excel = edit_pandas_with_excel
