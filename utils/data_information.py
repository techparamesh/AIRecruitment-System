import pandas as pd
from IPython.display import display


def data_info(df):
 
    print('########## Summary of scraped data ##########')
    print(df.info())

    # Number of rows and columns
    print('Number of rows: {}'.format(df.shape[0]))
    print('Number of columns: {}'.format(df.shape[1]))

    # Number of columns having missing values
    if df.columns.isna().sum() != 0:
        print('\nMissing values found \n')
        display(df.columns.isna().sum())
    else:
        print('\nNo missing values found \n')
        
    # Numerical/Continuous Columns
    print('Numerical/Continuous Columns')
    print('Total: {}'.format(len(df.select_dtypes(include=['int64', 'float', 'int']).columns)))
    display(df.select_dtypes('int64' and 'float' and 'int').describe())

    # Categorical Columns
    print('Categorical Columns')
    print('Total: {}'.format(len(df.select_dtypes(include='object').columns)))
    display(df.select_dtypes('object').describe())

    # Check for duplicated rows
    if df.duplicated().sum() != 0:
        print('\nDuplicate rows found \n')
        display(df[df.duplicated()])
    else:
        print('\nNo duplicate rows found \n')

    print('########## Summary Concluded ########## \n')