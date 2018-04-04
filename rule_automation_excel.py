import xlrd
import csv
import rule_automation as automator

prescreen_evaluations_rules = {'Primary Applicant has age' : 'MinimumAgeofApplicant',
				 'Co-Applicant has age' : 'MinimumAgeofCo-Applicant',
				 'Primary applicant has valid SSN' : 'SSNNotIssued-Applicant',
				 'Co-Applicant has valid SSN' : 'SSNNotIssued-CoApplicant',
				 'Maximum Age of Vehicle' : 'MaximumAgeofVehicle',
				 'Minimum Amount Financed' : 'MinimumAmounttoFinance'
				}
				
prescreen_decision_rules = {'If rules score < {X}, set Decision status to PENDING' : 'PendingReferRule'}

common_rules = {'Primary applicant has gross monthly income' : 'GrossMonthlyIncome-Applicant',
				'Co-Applicant has gross monthly income' : 'GrossMonthlyIncome-CoApplicant',
				'Applicant at Current Address' : 'TimeatCurrentResidence-Applicant',
				'CoApplicant at Current Address' : 'TimeatCurrentResidence-CoApplicant',
				'Primary Applicant at current employment' : 'TimeatCurrentEmployment-Applicant',
				'Co-Applicant at current employment' : 'TimeatCurrentEmployment-CoApplicant',
				'Primary Applicant Self Employed' : 'SelfEmployed-AnyApplicant',
				'CoAPplicant Self Employed' : 'SelfEmployed-CoApplicant',
				'Primary Applicant DTI' : 'Debttoincome-Applicant',
				'CoApplicant DTI' : 'Debttoincome-CoApplicant',
				'Primary Applicant (Non-Spousal) Debt to Income (DTI)' : 'DebtoIncomeApplicant-NonSpousal',
				'CoApplicant (Non-Spousal) Debt to Income (DTI)' : 'DebttoIncomeCoApplicant-NonSpousal',
				'Combined Debt to Income (DTI)' : 'DebttoIncome-Combined',
				'Outstanding Unsecured Revolving Debt (Maximum)' : 'OutstandingUnsecuredRevolvingDebt-Maximum',
				'Vehicle is New and LTV' : 'LTV-NewVehicle',
				'Vehicle is Used and LTV' : 'LTV-UsedVehicle',
				'Applicant Credit Score' : 'CreditScore-Applicant',
				'Co-Applicant Credit Score' : 'CreditScore-CoApplicant',
				'Primary Applicant File time in Bureau' : 'MinimumFileTimeinCreditBureau-Applicant',
				'Co-Applicant File time in Bureau' : 'MinimumFileTimeinCreditBureau-CoApplicant',
				'Applicant Number of Trade Lines' : 'MinimumNumberofTradelines-Applicant',
				'CoApplicant Number of Trade Lines' : 'MinimumNumberofTradelines-CoApplicant'
				}
				
derogatory_evaluation_rules = {'Combined Number of 30,60,90 days Delinquencies in past {X} months <= {Y}' : 'Numberof306090HistoricalDelinquencies'}
				

rule_set = ''

workbook_link = 'Marine Underwriting Rules 3.28.18.xlsx'
worksheet_name = 'Underwriting Rules'

def open_file(workbook_link, worksheet_name):
	workbook = xlrd.open_workbook(workbook_link)
	worksheet = workbook.sheet_by_name(worksheet_name)

def parse_excel():

	rownum = 2
	while rownum < worksheet.nrows:
		row = worksheet.row(rownum)
		if row[1].value == "" and row[2].value == "" and row[3].value == "":
			if 'Pre-Screen Evaluation' in row[0].value:
				rule_set = 'Prescreen'
			elif 'Pre-Screen Decision' in row[0].value:
				rule_set = 'Prescreen (Decision)'
			elif 'Common-Evaluation' in row[0].value:
				rule_set = 'Common'
			elif 'Credit-Derogatory' in row[0].value:
				rule_set = 'Common-Credit Derogatory'
			
		
		
		#print(rule_type)
		rownum += 1

print(rule_set)	
	
#rule_type = worksheet.cell(2,0)




#print(worksheet.cell(3,1).value)
