import pandas as pd
from sklearn.preprocessing import StandardScaler

def refresh(df):
    # remove meaningless and defective data, for example, remove NAN and change '60 months' to '60'
    newdf = df[['loan_amnt', 'term', 'int_rate', 'installment', 'grade', 'sub_grade', 'emp_length', 'annual_inc',\
                'verification_status', 'issue_d', 'loan_status']]
    for row in range(newdf.shape[0]):
        newdf.loc[i, 'term'] = newdf.loc[i, 'term'].split(' ')[0]
        newdf.loc[i, 'int_rate'] = str(int(newdf.loc[i, 'int_rate'][0:-1])/100)
        newdf.loc[i, 'grade'] = ord(newdf.loc[i, 'grade']) - ord('A') + 1
        newdf.loc[i, 'subgrade'] = newdf.loc[i, 'subgrade'][-1]

        newdf.loc[i, 'emp_length'] = newdf.loc[i, 'emp_length'].split(' ')[0]
        if newdf.loc[i, 'emp_length'][-1] == '+':
            newdf.loc[i, 'emp_length'] = newdf.loc[i, 'emp_length'][0:-1]
        if newdf.loc[i, 'verification_status'] == 'Not Verified':
            newdf.loc[i, 'verification_status'] = -1
        elif newdf.loc[i, 'verification_status'] == 'Source Verified':
            newdf.loc[i, 'verification_status'] = 1
        else:
            newdf.loc[i, 'verification_status'] = 0

        newdf.loc[i, 'issue_d'] = newdf.loc[i, 'issue_d'].split('-')[0]
        if newdf.loc[i, 'issue_d'] == 'Jun':
            newdf.loc[i, 'issue_d'] = 6
        elif newdf.loc[i, 'issue_d'] == 'Jul':
            newdf.loc[i, 'issue_d'] = 7
        elif newdf.loc[i, 'issue_d'] == 'Apr':
            newdf.loc[i, 'issue_d'] = 4
        elif newdf.loc[i, 'issue_d'] == 'May':
            newdf.loc[i, 'issue_d'] = 5
        elif newdf.loc[i, 'issue_d'] == 'March':
            newdf.loc[i, 'issue_d'] = 3

        if newdf.loc[i, 'loan_status'] in ['Current', 'Fully Paid']:
            newdf.loc[i, 'loan_status'] = 1                              # good loan
        elif newdf.loc[i, 'loan_status'] in ['Charged Off', 'Late (31-120 days)', 'Late (16-30 days)']:
            newdf.loc[i, 'loan_status'] = -1                             # bad loan
        if newdf.loc[i, 'loan_status'] in ['Default', 'In Grace Period']:
            newdf.loc[i, 'loan_status'] = 0                              # grey loan

    return newdf

def scale(df):
    scaler = StandardScaler()
    scaler.fit(df)
    df_scaled = scaler.transform(df)
    df_scaled = pd.DataFrame(df_scaled, columns=df.columns)
    return df_scaled

def PCA(df):
    return pd.DataFrame(pca.transform(df), index=df.index, columns=["PC1", "PC2", "PC3", "PC4", "PC5", "PC6", "PC7", \
                                                                    "PC8", "PC9", "PC10"])

def main():
    df = pd.read_excel('LoanStats_2016Q2.xls')
    df_refreshed = refresh(df)
    df_refreshed.to_excel('new_LoanStats_2016Q2.xlsx')
    print(df_refreshed(head))

    train_scaled = scale(df_refreshed.drop(['loan_status'], axis=1, inplace=False))
    train_PCA = PCA(train_scaled)
    train_result = df_refreshed['loan_status']

if __name__ == '__main__':
    main()