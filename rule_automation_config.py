PRESCREEN_EVALUATION = {'Primary Applicant has age' : 'MinimumAgeofApplicant',
				 'Co-Applicant has age ' : 'MinimumAgeofCo-Applicant',
				 'Primary applicant has valid SSN' : 'SSNNotIssued-Applicant',
				 'Co-Applicant has valid SSN' : 'SSNNotIssued-CoApplicant',
				 'Maximum Age of Vehicle' : 'MaximumAgeofVehicle',
				 'Minimum Amount Financed ' : 'MinimumAmounttoFinance'
				}
				
PRESCREEN_DECISION = {'If rules score < {X}, set Decision status to PENDING \n(If rule fails, REFER)' : 'PendingReferRule'}

COMMON = {'Primary applicant has gross monthly income' : 'GrossMonthlyIncome-Applicant',
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
				
DEROGATORY_EVALUATION = {'Combined Number of 30,60,90 days Delinquencies in past {X} months <= {Y}' : 'Numberof306090HistoricalDelinquencies'}





TEST_COMPID = 'mich320'
TEST_USER = 'mdadurian'
TEST_PASS = 'Wafflefries12@'



AUTO_INDIRECT = 'Auto Indirect'
MARINE = 'Marine'
RV = 'RV'


DEFAULT_LITE = 'DL4 Lite Profile'



WORKBOOK = 'Marine Underwriting Rules 3.28.18.xlsx'
WORKSHEET = 'Underwriting Rules'