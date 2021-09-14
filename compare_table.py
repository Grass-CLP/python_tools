#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 21-4-26.
# email to LipsonChan@yahoo.com
#

import numpy as np
import pandas as pd  # pip install pandas>=1.1.0


def compare_table(table_x, table_y, keys) -> dict or None:
    """
    compare two pandas DataFrame with primary keys
    :param table_x: from
    :param table_y: to
    :param keys: multi primary keys (it would be join with '_')
    :return:  miss_col, more_col, miss_keys, more_keys, com_re_dt, com_df
    """

    miss_col = list(set(table_x.columns.tolist()) - set(table_y.columns.tolist()))
    more_col = list(set(table_y.columns.tolist()) - set(table_x.columns.tolist()))
    com_col = table_x.columns.tolist()
    _ = [com_col.remove(x) for x in miss_col]

    table_com_x = table_x[com_col]
    table_com_y = table_y[com_col]

    for k in keys:
        if k not in com_col:
            print(f"keys '{k}' do not exist")
            return None

    # format keys
    duplicates = dict()
    for k, df in {'x': table_com_x, 'y': table_com_y}.items():
        data_index = df[keys[0]].map(str)
        for i in range(1, len(keys)):
            data_index = data_index + '_' + df[keys[i]].map(str)

        # unique
        duplicated_index = df.index[data_index.duplicated()].tolist()
        duplicates[f"duplicated_{k}"] = data_index[duplicated_index].tolist()
        df.drop(index=duplicated_index, inplace=True)
        data_index.drop(index=duplicated_index, inplace=True)

        # set into index
        df.index = data_index

    # compare items sum
    com_re_dt = dict()
    miss_keys = list(set(table_com_x.index) - set(table_com_y.index))
    more_keys = list(set(table_com_y.index) - set(table_com_x.index))
    table_com_x = table_com_x[table_com_x.index.map(lambda x: x not in miss_keys)].sort_index()
    table_com_y = table_com_y[table_com_y.index.map(lambda x: x not in more_keys)].sort_index()
    com_num = len(table_com_x)

    # compare
    com_df = None
    if not table_com_y.empty and not table_com_x.empty:
        com_df = table_com_x.compare(table_com_y)
        diff_col = set([x[0] for x in com_df.columns])
        for c in diff_col:
            com_re_dt[c] = dict()
            com_re_dt[c]['miss'] = sum(pd.notna(com_df[c, 'self']) & pd.isna(com_df[c, 'other']))
            com_re_dt[c]['r_miss'] = sum(pd.isna(com_df[c, 'self']) & pd.notna(com_df[c, 'other']))
            com_re_dt[c]['diff'] = sum(pd.notna(com_df[c, 'self']) & pd.notna(com_df[c, 'other'])
                                       & (com_df[c, 'self'] != com_df[c, 'other']))
    else:
        print(f"table has not data to cmp, x:{not table_com_x.empty}, y:{not table_com_y.empty}")

    result = {}
    result.update(duplicates)
    result.update(dict(miss_col=miss_col, more_col=more_col,
                       miss_keys=miss_keys, more_keys=more_keys,
                       com_re_dt=com_re_dt, com_df=com_df, com_num=com_num))
    return result


if __name__ == "__main__":
    df = pd.DataFrame(
        {
            "col2": [1.0, 3.0, 2.0, np.nan, 5.0],
            "col1": ["a", "c", "b", "d", "a"],
            "col3": [1.0, 3.0, 2.0, 4.0, 5.0]
        },
        columns=["col2", "col1", "col3"],
    )

    df2 = pd.DataFrame(
        {
            "col1": ["a", "b", "c", "d", "f"],
            "col2": [1.0, np.nan, 4.0, 4.0, 5.0],
            "col4": [1.0, 2.0, 3.0, 4.0, 5.0],
        },
        columns=["col1", "col2", "col4"],
    )

    result = compare_table(df, df2, ['col1'])
    print(result)
    """
         col2      
         self other
    col1           
    b     2.0   NaN
    c     3.0   4.0
    d     NaN   4.0
    """
