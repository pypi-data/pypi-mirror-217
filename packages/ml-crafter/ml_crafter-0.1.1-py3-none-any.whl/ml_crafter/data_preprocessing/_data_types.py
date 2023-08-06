import re
import pandas as pd


def get_column_data_types(dataframe):
    """
    Get the data type of each column in a dataframe.

    Parameters:
    dataframe (pandas.DataFrame): The dataframe to analyze.

    Returns:
    pandas.DataFrame: A dataframe containing two columns: 'Column' (column names) and 'Data Type' (corresponding data types).
    """
    column_data_types = pd.DataFrame({
        'Column': dataframe.columns,
        'raw_data_type': dataframe.dtypes.astype(str)
    })
    return column_data_types


def get_data_type(value):
    if isinstance(value, int):
        return 'int'
    elif isinstance(value, str):
        try:
            float_val = float(value)
            return 'float/int'
        except ValueError:
            return 'str'
    else:
        if 'timestamps' in str(type(value)):
            return 'date'
        return  re.sub(r"(\s|'|\[|\]|<|>)", '',str(type(value))).replace('class','')


def get_num_vals(value):
    if isinstance(value, int) or isinstance(value, float):
        return value

    elif isinstance(value, str):
        try:
            float_val = float(value)
            return float_val
        except ValueError:
            return 'str'


def is_feature_continuous(df, feature, c=0.15):
    """

    c : To idenfy if a numerical column is ordinal (categorical), check the number of unique values
        compared to the total number of values. This parameter is the ratio between the two


    """

    df_na_dropped = df[feature].dropna()

    # Apply the function to a column and return all values in a list
    num_values = df_na_dropped.apply(get_num_vals).tolist()
    # numerical values after removing str items if there is any
    num_values_without_str = [i for i in num_values if i != 'str']

    num_values_without_str_count = len(num_values_without_str)
    num_unique_val_count = len(set(num_values_without_str))

    # for string cols
    if len(num_values_without_str) == 0:
        return 0

    # if a column contains string and numerical both, we need to identify what type is the majority
    # if there more string items than numerical the column likely to be string and there numericals
    # by mistake
    elif len(num_values_without_str) < len(num_values) * 0.5:
        return 0
        # if there is only one unique numeric value in a column, it's not an important column
        # and we cant say its a numerical categorical (ordinal) column therefore classify it as continuous
        # thats the reason for having num_unique_val_count > 1 condition below
    elif num_unique_val_count / num_values_without_str_count <= c and num_unique_val_count > 1:
        return 0
    else:
        return 1


def get_majority_feature_type(df, feature):
    """

    """


    df_dropped_na = df[feature].dropna()

    df_dropped_na['dtype'] = df_dropped_na.apply(get_data_type)

    majority_data_type = df_dropped_na['dtype'].value_counts().sort_values().tail(1).index[0]

    return majority_data_type


def is_column_binary(df, column):
    unique_values = df[column].unique()
    if len(unique_values) == 2 and set(unique_values) == {0, 1}:
        return 1
    else:
        return 0


def get_inferred_data_type(feature, identified_data_type, Is_Binary, is_continuous, majority_data_type,
                           Num_of_diff_datatypes):
    if not isinstance(identified_data_type, list):
        identified_data_type = [identified_data_type]

    if Num_of_diff_datatypes == 1:
        if 'date' in identified_data_type[0]:
            return 'date'
        elif Is_Binary == 1:
            return 'binary'
        elif is_continuous == 1:
            return 'continuous'
        elif 'str' in identified_data_type[0]:
            return 'string_categorical'
        else:
            return 'numerical_categorical'

    elif Num_of_diff_datatypes > 1:
        if is_continuous == 1:
            return 'continuous'

        elif majority_data_type in ['int', 'float', 'float/int'] and is_continuous == 0:
            return 'numerical_categorical/binary'

        elif majority_data_type == 'str':
            return 'string_categorical'
        elif majority_data_type == 'date':
            return 'date'
        else:
            return 'error'

def count_nans(df, feature):
    nan_count = df[feature].isna().sum()
    return nan_count


def run_data_type_analysis(df, c=0.15):
    """
        c : To idenfy if a numerical column is ordinal (categorical), check the number of unique values
        compared to the total number of values. This parameter is the ratio between the two

    """

    df_dtypes = get_column_data_types(df)

    object_columns = df.select_dtypes(include='object').columns
    date_columns = object_columns[df[object_columns].apply(lambda x: pd.to_datetime(x, errors='coerce').notna().all())]

    df_dtypes['infer_date_dtype'] = df.columns.to_series().apply(lambda x: 'date' if x in date_columns \
        else df_dtypes.loc[x, 'raw_data_type'])

    df_dtypes['actual_data_types'] = [(list(df[i].dropna().apply(get_data_type).unique()) if i in object_columns \
                                           else df_dtypes.loc[i, 'infer_date_dtype']) for i in df_dtypes.index]

    df_dtypes['Num_of_diff_datatypes'] = df_dtypes['actual_data_types'].apply(
        lambda x: len(x) if isinstance(x, list) else 1)

    df_dtypes['is_continuous'] = df_dtypes['Column'].apply(lambda r: is_feature_continuous(df, r, c=c))

    df_dtypes['majority_data_type'] = df_dtypes['Column'].apply(lambda r: get_majority_feature_type(df, r))

    df_dtypes['Is_Binary'] = df_dtypes['Column'].apply(lambda x: is_column_binary(df, x))

    df_dtypes['inferred_data_type'] = df_dtypes.apply(lambda row: get_inferred_data_type(row['Column']
                                                                                         , row['actual_data_types']
                                                                                         , row['Is_Binary']
                                                                                         , row['is_continuous']
                                                                                         , row['majority_data_type']
                                                                                         ,
                                                                                         row['Num_of_diff_datatypes']),
                                                      axis=1)

    df_dtypes['nan_count'] = df_dtypes['Column'].apply(lambda x: count_nans(df, x))

    df_dtypes = df_dtypes[['Column', 'raw_data_type','actual_data_types', 'inferred_data_type', 'Num_of_diff_datatypes','nan_count']]

    df_dtypes = df_dtypes.loc[df_dtypes.index != 'dtype']

    return df_dtypes



