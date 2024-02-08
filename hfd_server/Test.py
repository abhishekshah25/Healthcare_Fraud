from sklearn.preprocessing import StandardScaler
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


test_file_path = sys.argv[1]
beneficiary_file_path = sys.argv[2]
inpatient_file_path = sys.argv[3]
outpatient_file_path = sys.argv[4]

Test = pd.read_csv(test_file_path)
Test_Beneficiary = pd.read_csv(beneficiary_file_path)
Test_Inpatient = pd.read_csv(inpatient_file_path)
Test_Outpatient = pd.read_csv(outpatient_file_path)


# Test = pd.read_csv("Test-1542969243754.csv")
# Test_Beneficiary = pd.read_csv("Test_Beneficiarydata-1542969243754.csv")
# Test_Inpatient = pd.read_csv("Test_Inpatientdata-1542969243754.csv")
# Test_Outpatient = pd.read_csv("Test_Outpatientdata-1542969243754.csv")


Test_Beneficiary = Test_Beneficiary.replace({'ChronicCond_Alzheimer': 2, 'ChronicCond_Heartfailure': 2, 'ChronicCond_KidneyDisease': 2,
                                             'ChronicCond_Cancer': 2, 'ChronicCond_ObstrPulmonary': 2, 'ChronicCond_Depression': 2,
                                             'ChronicCond_Diabetes': 2, 'ChronicCond_IschemicHeart': 2, 'ChronicCond_Osteoporasis': 2,
                                             'ChronicCond_rheumatoidarthritis': 2, 'ChronicCond_stroke': 2}, 0)

Test_Beneficiary = Test_Beneficiary.replace({'RenalDiseaseIndicator': 'Y'}, 1)


Test_Beneficiary[["ChronicCond_Alzheimer", "ChronicCond_Heartfailure", "ChronicCond_KidneyDisease", "ChronicCond_Cancer", "ChronicCond_ObstrPulmonary", "ChronicCond_Depression", "ChronicCond_Diabetes", "ChronicCond_IschemicHeart", "ChronicCond_Osteoporasis", "ChronicCond_rheumatoidarthritis", "ChronicCond_stroke", "RenalDiseaseIndicator"]] = Test_Beneficiary[[
    "ChronicCond_Alzheimer", "ChronicCond_Heartfailure", "ChronicCond_KidneyDisease", "ChronicCond_Cancer", "ChronicCond_ObstrPulmonary", "ChronicCond_Depression", "ChronicCond_Diabetes", "ChronicCond_IschemicHeart", "ChronicCond_Osteoporasis", "ChronicCond_rheumatoidarthritis", "ChronicCond_stroke", "RenalDiseaseIndicator"]].apply(pd.to_numeric)


# calculate patient risk score by summing up all risk scores
Test_Beneficiary['Patient_Risk_Score'] = Test_Beneficiary['ChronicCond_Alzheimer'] + Test_Beneficiary['ChronicCond_Heartfailure'] + \
    Test_Beneficiary['ChronicCond_KidneyDisease'] + Test_Beneficiary['ChronicCond_Cancer'] +\
    Test_Beneficiary['ChronicCond_ObstrPulmonary'] + Test_Beneficiary['ChronicCond_Depression'] +\
    Test_Beneficiary['ChronicCond_Diabetes'] + Test_Beneficiary['ChronicCond_IschemicHeart'] +\
    Test_Beneficiary['ChronicCond_Osteoporasis'] + Test_Beneficiary['ChronicCond_rheumatoidarthritis'] +\
    Test_Beneficiary['ChronicCond_stroke'] + \
    Test_Beneficiary['RenalDiseaseIndicator']


Test_Beneficiary = Test_Beneficiary.replace({'Gender': 2}, 0)


Test_Beneficiary['DOB'] = pd.to_datetime(
    Test_Beneficiary['DOB'], format='%Y-%m-%d')
Test_Beneficiary['DOD'] = pd.to_datetime(
    Test_Beneficiary['DOD'], format='%Y-%m-%d')

Test_Beneficiary['Birth_Year'] = Test_Beneficiary['DOB'].dt.year
Test_Beneficiary['Birth_Month'] = Test_Beneficiary['DOB'].dt.month

Test_Beneficiary['Patient_Age'] = round(
    ((Test_Beneficiary['DOD'] - Test_Beneficiary['DOB']).dt.days)/365)
Test_Beneficiary.Patient_Age.fillna(round(((pd.to_datetime(
    '2009-12-01', format='%Y-%m-%d')-Test_Beneficiary['DOB']).dt.days)/365), inplace=True)


Test_Beneficiary['isDead'] = 0
Test_Beneficiary.loc[Test_Beneficiary.DOD.notna(), 'isDead'] = 1


Test_Inpatient['ClaimStartDt'] = pd.to_datetime(
    Test_Inpatient['ClaimStartDt'], format='%Y-%m-%d')
Test_Inpatient['ClaimEndDt'] = pd.to_datetime(
    Test_Inpatient['ClaimEndDt'], format='%Y-%m-%d')


Test_Inpatient['AdmissionDt'] = pd.to_datetime(
    Test_Inpatient['AdmissionDt'], format='%Y-%m-%d')
Test_Inpatient['DischargeDt'] = pd.to_datetime(
    Test_Inpatient['DischargeDt'], format='%Y-%m-%d')


Test_Inpatient['Hospitalization_Duration'] = (
    (Test_Inpatient['DischargeDt'] - Test_Inpatient['AdmissionDt']).dt.days)+1
Test_Inpatient['Claim_Period'] = (
    (Test_Inpatient['ClaimEndDt'] - Test_Inpatient['ClaimStartDt']).dt.days)+1


Test_Inpatient['ExtraClaimDays'] = np.where(Test_Inpatient['Claim_Period'] > Test_Inpatient['Hospitalization_Duration'],
                                            Test_Inpatient['Claim_Period'] - Test_Inpatient['Hospitalization_Duration'], 0)


# Get the months and year of claim start and claim end

Test_Inpatient['ClaimStart_Year'] = Test_Inpatient['ClaimStartDt'].dt.year
Test_Inpatient['ClaimStart_Month'] = Test_Inpatient['ClaimStartDt'].dt.month


Test_Inpatient['ClaimEnd_Year'] = Test_Inpatient['ClaimEndDt'].dt.year
Test_Inpatient['ClaimEnd_Month'] = Test_Inpatient['ClaimEndDt'].dt.month


# Get the month and year of Admission_Year and Admission_Month

Test_Inpatient['Admission_Year'] = Test_Inpatient['AdmissionDt'].dt.year
Test_Inpatient['Admission_Month'] = Test_Inpatient['AdmissionDt'].dt.month


Test_Inpatient['Discharge_Year'] = Test_Inpatient['DischargeDt'].dt.year
Test_Inpatient['Discharge_Month'] = Test_Inpatient['DischargeDt'].dt.month


Test_Outpatient['ClaimStartDt'] = pd.to_datetime(
    Test_Outpatient['ClaimStartDt'], format='%Y-%m-%d')
Test_Outpatient['ClaimEndDt'] = pd.to_datetime(
    Test_Outpatient['ClaimEndDt'], format='%Y-%m-%d')


# Get the months and year of claim start and claim end

Test_Outpatient['ClaimStart_Year'] = Test_Outpatient['ClaimStartDt'].dt.year
Test_Outpatient['ClaimStart_Month'] = Test_Outpatient['ClaimStartDt'].dt.month


Test_Outpatient['ClaimEnd_Year'] = Test_Outpatient['ClaimEndDt'].dt.year
Test_Outpatient['ClaimEnd_Month'] = Test_Outpatient['ClaimEndDt'].dt.month
# Calculate Claim_Period = ClaimEndDt - ClaimStartDt


Test_Outpatient['Claim_Period'] = (
    (Test_Outpatient['ClaimEndDt'] - Test_Outpatient['ClaimStartDt']).dt.days)+1


Test_Inpatient['Inpatient_or_Outpatient'] = 1
Test_Outpatient['Inpatient_or_Outpatient'] = 0

# Merge inpatient and outpatient dataframes based on common columns

common_columns_test = [
    idx for idx in Test_Outpatient.columns if idx in Test_Inpatient.columns]
Inpatient_Outpatient_Merge_Te = pd.merge(
    Test_Inpatient, Test_Outpatient, left_on=common_columns_test, right_on=common_columns_test, how='outer')

# Merge beneficiary details with inpatient and outpatient data
Inpatient_Outpatient_Beneficiary_Merge_Te = pd.merge(Inpatient_Outpatient_Merge_Te, Test_Beneficiary,
                                                     left_on='BeneID', right_on='BeneID', how='inner')

Final_Dataset_Test = pd.merge(
    Inpatient_Outpatient_Beneficiary_Merge_Te, Test, how='inner', on='Provider')

print(Final_Dataset_Test.shape)


Final_Dataset_Test['IP_OP_TotalReimbursementAmt'] = Final_Dataset_Test['IPAnnualReimbursementAmt'] + \
    Final_Dataset_Test['OPAnnualReimbursementAmt']
Final_Dataset_Test['IP_OP_AnnualDeductibleAmt'] = Final_Dataset_Test['IPAnnualDeductibleAmt'] + \
    Final_Dataset_Test['OPAnnualDeductibleAmt']


Final_Dataset_Test = Final_Dataset_Test.fillna(0).copy()


def create_feature_using_groupby(Test_df, gruopby_col, operation_col, operation):
    '''
    This function groupby the 'Train_df' and 'Test_df' dataframe by 'gruopby_col' and performs 'operation' on 'operation_col'
    '''

    for col in operation_col:
        # create new column name for the dataframe
        new_col_name = 'Per'+''.join(gruopby_col)+'_'+operation+'_'+col
        print(new_col_name)

        Test_df[new_col_name] = Test_df.groupby(
            gruopby_col)[col].transform(operation)
    return Test_df


columns = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt', 'OPAnnualReimbursementAmt',
           'OPAnnualDeductibleAmt', 'Patient_Age', 'NoOfMonths_PartACov', 'NoOfMonths_PartBCov', 'Hospitalization_Duration', 'Claim_Period', 'Patient_Risk_Score']

Final_Dataset_Test = create_feature_using_groupby(
    Final_Dataset_Test, ['Provider'], columns, 'mean')

columns = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
           'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Patient_Age', 'Hospitalization_Duration', 'Claim_Period', 'Patient_Risk_Score']

Final_Dataset_Test = create_feature_using_groupby(
    Final_Dataset_Test, ['BeneID'], columns, 'mean')

columns = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
           'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Patient_Age', 'Hospitalization_Duration', 'Claim_Period', 'Patient_Risk_Score']

Final_Dataset_Test = create_feature_using_groupby(
    Final_Dataset_Test, ['AttendingPhysician'], columns, 'mean')

columns = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
           'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Patient_Age', 'Hospitalization_Duration', 'Claim_Period', 'Patient_Risk_Score']

Final_Dataset_Test = create_feature_using_groupby(
    Final_Dataset_Test, ['OperatingPhysician'], columns, 'mean')

columns = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
           'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Patient_Age', 'Hospitalization_Duration', 'Claim_Period', 'Patient_Risk_Score']

Final_Dataset_Test = create_feature_using_groupby(
    Final_Dataset_Test, ['OtherPhysician'], columns, 'mean')


columns = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
           'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Patient_Age', 'Hospitalization_Duration', 'Claim_Period', 'Patient_Risk_Score']

Final_Dataset_Test = create_feature_using_groupby(
    Final_Dataset_Test, ['DiagnosisGroupCode'], columns, 'mean')


columns = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
           'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Patient_Age', 'Hospitalization_Duration', 'Claim_Period', 'Patient_Risk_Score']

Final_Dataset_Test = create_feature_using_groupby(
    Final_Dataset_Test, ['ClmAdmitDiagnosisCode'], columns, 'mean')


columns = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
           'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Patient_Age', 'Hospitalization_Duration', 'Claim_Period', 'Patient_Risk_Score']

Final_Dataset_Test = create_feature_using_groupby(
    Final_Dataset_Test, ['ClmProcedureCode_1'], columns, 'mean')

columns = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
           'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Patient_Age', 'Hospitalization_Duration', 'Claim_Period', 'Patient_Risk_Score']

Final_Dataset_Test = create_feature_using_groupby(
    Final_Dataset_Test, ['ClmProcedureCode_2'], columns, 'mean')


columns = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
           'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Patient_Age', 'Hospitalization_Duration', 'Claim_Period', 'Patient_Risk_Score']

Final_Dataset_Test = create_feature_using_groupby(
    Final_Dataset_Test, ['ClmProcedureCode_3'], columns, 'mean')


columns = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
           'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Patient_Age', 'Hospitalization_Duration', 'Claim_Period', 'Patient_Risk_Score']

Final_Dataset_Test = create_feature_using_groupby(
    Final_Dataset_Test, ['ClmProcedureCode_4'], columns, 'mean')


columns = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
           'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Patient_Age', 'Hospitalization_Duration', 'Claim_Period', 'Patient_Risk_Score']

Final_Dataset_Test = create_feature_using_groupby(
    Final_Dataset_Test, ['ClmProcedureCode_5'], columns, 'mean')


columns = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
           'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Patient_Age', 'Hospitalization_Duration', 'Claim_Period', 'Patient_Risk_Score']

Final_Dataset_Test = create_feature_using_groupby(
    Final_Dataset_Test, ['ClmProcedureCode_6'], columns, 'mean')


columns = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
           'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Patient_Age', 'Hospitalization_Duration', 'Claim_Period', 'Patient_Risk_Score']

Final_Dataset_Test = create_feature_using_groupby(
    Final_Dataset_Test, ['ClmDiagnosisCode_1'], columns, 'mean')


columns = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
           'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Patient_Age', 'Hospitalization_Duration', 'Claim_Period', 'Patient_Risk_Score']

Final_Dataset_Test = create_feature_using_groupby(
    Final_Dataset_Test, ['ClmDiagnosisCode_2'], columns, 'mean')


columns = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
           'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Patient_Age', 'Hospitalization_Duration', 'Claim_Period', 'Patient_Risk_Score']

Final_Dataset_Test = create_feature_using_groupby(
    Final_Dataset_Test, ['ClmDiagnosisCode_3'], columns, 'mean')


columns = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
           'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Patient_Age', 'Hospitalization_Duration', 'Claim_Period', 'Patient_Risk_Score']

Final_Dataset_Test = create_feature_using_groupby(
    Final_Dataset_Test, ['ClmDiagnosisCode_4'], columns, 'mean')


columns = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
           'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Patient_Age', 'Hospitalization_Duration', 'Claim_Period', 'Patient_Risk_Score']

Final_Dataset_Test = create_feature_using_groupby(
    Final_Dataset_Test, ['ClmDiagnosisCode_5'], columns, 'mean')


columns = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
           'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Patient_Age', 'Hospitalization_Duration', 'Claim_Period', 'Patient_Risk_Score']

Final_Dataset_Test = create_feature_using_groupby(
    Final_Dataset_Test, ['ClmDiagnosisCode_6'], columns, 'mean')


# Count the claims per provider
Final_Dataset_Test = create_feature_using_groupby(
    Final_Dataset_Test, ['Provider'], ['ClaimID'], 'count')


columns = ['ClaimID']
grp_by_cols = ['BeneID', 'AttendingPhysician', 'OtherPhysician', 'OperatingPhysician', 'ClmAdmitDiagnosisCode', 'ClmProcedureCode_1',
               'ClmProcedureCode_2', 'ClmProcedureCode_3', 'ClmProcedureCode_4', 'ClmProcedureCode_5', 'ClmDiagnosisCode_1', 'ClmDiagnosisCode_2',
               'ClmDiagnosisCode_3', 'ClmDiagnosisCode_4', 'ClmDiagnosisCode_5', 'ClmDiagnosisCode_6', 'DiagnosisGroupCode']
for ele in grp_by_cols:
    lst = ['Provider', ele]
    Final_Dataset_Test = create_feature_using_groupby(
        Final_Dataset_Test, lst, columns, 'count')


print(Final_Dataset_Test.shape)


remove_columns = ['BeneID', 'ClaimID', 'ClaimStartDt', 'ClaimEndDt', 'AttendingPhysician', 'OperatingPhysician', 'OtherPhysician',
                  'ClmDiagnosisCode_1', 'ClmDiagnosisCode_2', 'ClmDiagnosisCode_3', 'ClmDiagnosisCode_4', 'ClmDiagnosisCode_5',
                  'ClmDiagnosisCode_6', 'ClmDiagnosisCode_7', 'ClmDiagnosisCode_8', 'ClmDiagnosisCode_9', 'ClmDiagnosisCode_10',
                  'ClmProcedureCode_1', 'ClmProcedureCode_2', 'ClmProcedureCode_3', 'ClmProcedureCode_4', 'ClmProcedureCode_5',
                  'ClmProcedureCode_6', 'ClmAdmitDiagnosisCode', 'AdmissionDt', 'ClaimStart_Year', 'ClaimStart_Year', 'ClaimStart_Month',
                  'ClaimEnd_Year', 'ClaimEnd_Month', 'Admission_Year', 'Admission_Month', 'Discharge_Year', 'Discharge_Month',
                  'DischargeDt', 'DiagnosisGroupCode', 'DOB', 'DOD', 'Birth_Year', 'Birth_Month', 'State', 'County']


Final_Dataset_Test_FE = Final_Dataset_Test.drop(columns=remove_columns, axis=1)


# Convert type of Gender and Race to categorical feature

Final_Dataset_Test_FE.Gender = Final_Dataset_Test_FE.Gender.astype('category')


Final_Dataset_Test_FE.Race = Final_Dataset_Test_FE.Race.astype('category')


# Do one hot encoding for gender and Race

Final_Dataset_Test_FE = pd.get_dummies(
    Final_Dataset_Test_FE, columns=['Gender', 'Race'])


Final_Dataset_Provider_Test = Final_Dataset_Test_FE.groupby(
    ['Provider'], as_index=False).agg('sum')

print(Final_Dataset_Provider_Test.shape)

model = pickle.load(open('model.pkl', 'rb'))

x_test = Final_Dataset_Provider_Test.drop(axis=1, columns=['Provider'])


standard_scaler = StandardScaler()
standard_scaler.fit(x_test)

x_test_std = standard_scaler.transform(x_test)

y_predict = model.predict(x_test_std)

print(y_predict[:20])

unique, counts = np.unique(y_predict, return_counts=True)
a = dict(zip(unique, counts))
print(a)

fraud = (a[1]/(a[0]+a[1]))*100

print('Fraud percentage', round(fraud, 2))

final_result = {
    'total_cnt': a[0] + a[1],
    'non_fraud_cnt': a[0],
    'fraud_cnt': a[1],
    'fraud_prcnt': round(fraud, 2)
}

print(final_result)
