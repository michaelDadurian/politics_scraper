from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import rule_automation_config as config
from time import sleep
import re
import xlrd
import csv
import rule_automation_config as config
import types
from selenium.common.exceptions import NoSuchElementException


		
def login():
	compid = browser.find_element_by_id("companyid")
	user = browser.find_element_by_id('username')
	password = browser.find_element_by_id('password')

	compid.send_keys(config.TEST_COMPID)
	user.send_keys(config.TEST_USER)
	password.send_keys(config.TEST_PASS)

	login_attempt = browser.find_element_by_xpath("//*[@type='submit']")
	login_attempt.submit()
	
	sleep(2)
	
		
rule_set = ''
rule = ''
rule_value = ''
rule_score = ''
rule_data = []

#workbook_link = 'Marine Underwriting Rules 3.28.18.xlsx'
#worksheet_name = 'Underwriting Rules'

def check_page(self, Rule):
	try:
		driver.find_element_by_partial_link_text(rule)
		
	except NoSuchElementException:
		print("No Element:", rule)
		return False
		
	return True
	
	
def open_file(workbook_link, worksheet_name):
	workbook = xlrd.open_workbook(workbook_link)
	worksheet = workbook.sheet_by_name(worksheet_name)
	return worksheet
	
	
	
	
def fix_rule_value(rule, rule_value):
	tokens = rule_value.split()
	print("tokens:", tokens)
		
	if 'age' in rule or 'Age' in rule or rule == 'PendingReferRule':
		return int(float(tokens[0]))
		
	if 'Employ' in rule or 'Residence' in rule:
		return int(float(tokens[0])) * 12
		
	if len(tokens) > 1:
		if tokens[1] == 'years':
			return int(tokens[0])
		if '$' in tokens[0]:
			value = tokens[0].replace('$', '')
			value = value.replace(',','')
			return [int(value), int(tokens[2])]
		if 'X' in tokens[0]:
			value_string = ' '.join(tokens)
			return re.findall(r'\d+', value_string)
	
	#Outstanding Unsecured Revolving
	if '%' in tokens[0]:
		value = tokens[0].replace('%','')
		return float(value)
		
	if int(tokens[0][0]) <= 1:
		return int(float(tokens[0]) * 100)
		
	return int(float(tokens[0]))
		
def get_rule_set(row):
	if 'Pre-Screen Evaluation' in row[0].value:
		rule_set = 'Prescreen'
	elif 'Pre-Screen Decision' in row[0].value:
		rule_set = 'Prescreen (Decision)'
	elif 'Common Evaluation' in row[0].value:
		rule_set = 'Common'
	elif 'Credit-Derogatory' in row[0].value:
		rule_set = 'Common-Credit Derogatory'
		
	return rule_set
	
def go_back():
	back_button = browser.find_element_by_xpath("//*[contains(text(), 'Back')]")
	back_button.click()
	
	
def parse_rule(row, rule):
	
	rule_value = fix_rule_value(rule, str(row[2].value))
	rule_score = row[3].value
	
	rule_obj = Rule(rule, [rule_value], rule_score, rule_set)
	rule_data.append(rule_obj)
	
	go_to_rule(rule)
	update_rule(rule, rule_value)

	

def parse_excel():
	counter = 0
	rule_type_set = False
	worksheet = open_file(config.WORKBOOK, config.WORKSHEET)
	rownum = 2
	rule_set = ''
	
	while rownum < worksheet.nrows:
		row = worksheet.row(rownum)
		print("curr row:", row)
		
		#Sets RuleSet and goes to correct page
		if row[1].value == "" and row[2].value == "" and row[3].value == "" and rule_type_set == False:
			rule_set = get_rule_set(row)
			rule_type_set = True
			go_to_rule_type(rule_set)
			
			
		
		#Extracts rule data and updates rule
		elif row[2].value != "" and row[3].value != 0:
			if rule_set == 'Prescreen':
				
				rule = config.PRESCREEN_EVALUATION[row[0].value]
				print("Rule:",rule)
				if rule == 'SSNNotIssued-Applicant' or rule == 'SSNNotIssued-CoApplicant':
					rownum += 1
					continue
				
				parse_rule(row, rule)
				counter += 1
				
				if counter == 4:
					print("prescreen done")
					go_back()
					rule_type_set = False
			
			elif rule_set == 'Prescreen (Decision)':
				rule = config.PRESCREEN_DECISION[row[0].value]
				
				parse_rule(row, rule)
				counter += 1
				
				if counter == 5:
					print("prescreen decision done")
					go_back()
					rule_type_set = False
				
			elif rule_set == 'Common':
				rule = config.COMMON[row[0].value]
				if rule == 'MaximumTermBasedOnAgeOfVehicle':
					values = []
					for i in range(0,7):
						values.append(int(worksheet.row(rownum+i)[2].value))
						
					rule_value = values
					rownum += 6
					
				elif rule == 'MaximumTermBasedOnAmountFinanced':
					values = []
					
					for i in range(0,2):
						value = fix_rule_value(rule, worksheet.row(rownum+i)[2].value)
						values.append(value)
					
					rule_value  = [val for sublist in values for val in sublist]
					rownum += 1
					
				else:

					rule_value = fix_rule_value(rule, str(row[2].value))
					rule_score = row[3].value
					
					
				for i in range (2,5):
					print("Searching for rule:", rule)
					if check_page(rule):
						go_to_rule(rule)
						update_rule(rule, rule_value)
						counter += 1
						break
					else:
						if i == 4: break
						browser.find_element_by_link_text(str(i)).click()
						
				if counter == 25:
					print("common done")
					go_back()
					rule_type_set = False
						
				
						
			elif rule_set == 'Common-Credit Derogatory':
				rule = config.DEROGATORY_EVALUATION[row[0].value]
				
				parse_rule(row, rule)
				counter += 1
				
				if counter == 26:
					break
				
					
		rownum += 1	
	
	print("Rule's updated")
		

def update_rule(rule_name, rule_value):
	
	sleep(2)
	field_inputs = browser.find_elements_by_xpath("//input")
	if rule_name == 'OutstandingUnsecuredRevolvingDebt-Maximum':
		new_input = "{}*${{applicants[0].currentEmployments[0].grossIncome}}".format(rule_value)
		field_inputs[2].clear()
		field_inputs[2].send_keys(new_input)
		
		browser.find_element_by_class_name('fa-times').click()
		
	elif rule_name == 'MaximumTermBasedOnAgeOfVehicle':
		j = 0
		
		for i in range(1, 14, 2):
			value = rule_value[j]
			print(value)
			field_inputs[i].clear()
			field_inputs[i].send_keys(value)
			
			j += 1
			
	
	elif rule_name == 'MaximumTermBasedOnAmountFinanced':
		j = 0
		for i in range(1, 5):
			field_inputs[i].clear()
			field_inputs[i].send_keys(str(rule_value[j]))
			
			j += 1
			
	elif 'MinimumNumberofTradelines' in rule_name:
		field_inputs[2].clear()
		field_inputs[2].send_keys(str(rule_value))
		
	elif 'Numberof306090' in rule_name:
		j = 0
		for i in range(2,4):
			field_inputs[i].clear()
			field_inputs[i].send_keys(rule_value[j])
			j += 1
	else:
		field_inputs[1].clear()
		field_inputs[1].send_keys(str(rule_value))
	
	
	validate_save_back()
	

def check_page(rule):
	#sleep(1)
	try:
		browser.find_element_by_partial_link_text(rule)
	except NoSuchElementException:
		print("No Element:", rule)
		return False
	return True
def go_to_rule_type(rule_type):
	browser.find_element_by_link_text(rule_type).click()
	
def go_to_rule(rule_name):
	print("HELLO", rule_name)
	sleep(1)
	update_link = browser.find_element_by_link_text(rule_name)
	update_link.click()
	

def validate_save_back():
	validate_button = browser.find_element_by_xpath("//*[contains(text(), 'Validate')]")
	validate_button.click()
	
	sleep(1)
	save_button = browser.find_element_by_xpath("//*[contains(text(), 'Save')]")
	save_button.click()
	
	sleep(1)
	back_button = browser.find_element_by_xpath("//*[contains(text(), 'Back')]")
	back_button.click()

def update_description(rule_name, rule_value):
	edit_buttons = browser.find_elements_by_class_name('fa-pencil-square-o')
	edit_buttons[i].click()
	sleep(1)
	
	curr_description = browser.find_element_by_xpath("//*[contains(@id,'_input_description')]")
	curr_description_value = curr_description.get_attribute('value');
	print(curr_description_value)
	
	existing_rule_value = int(re.search(r'\d+', curr_description_value).group())
	if existing_rule_value != rule_value:
		print(existing_rule_value, " ", rule_value)
		curr_description_tokens = curr_description_value.split()
		for j in range(len(curr_description_tokens)):
			if curr_description_tokens[j] == str(existing_rule_value):
				curr_description_tokens[j] = rule_value
				break
		updated_description = ' '.join(curr_description_tokens)
		print(updated_description)
		sleep(1)
		#browser.execute_script("arguments[0].value = arguments[1];", curr_description, updated_description);
		curr_description.clear()
		curr_description.send_keys(updated_description)
		sleep(1)
		
	sleep(1)
	update_button = browser.find_element_by_xpath("//*[contains(text(), 'Update')]")
	
	browser.execute_script("arguments[0].scrollIntoView();",update_button)
	update_button.click()
		


	
def set_loan_type(loan_type):
	browser.find_element_by_id(loan_type).click()
	
def set_rule_profile(rule_profile):
	browser.find_element_by_partial_link_text(rule_profile).click()
	
	
###################################################################################################################################################################################
	
	
#Get website
browser = webdriver.Chrome()
browser.get('https://test.decisionlender.solutions/tci/#/auth/login/?returnTo=%2Fauth%2Flogin%2F')
browser.maximize_window()
browser.implicitly_wait(10)

#Sign in
login()

#Go to rules
sleep(2)
search = browser.find_element_by_xpath("//input[@type='text']")
search.send_keys('Rules')

browser.find_element_by_link_text('Rules').click()

sleep(2)
#Select loan type
select_loan = browser.find_element_by_class_name('ui-select-container')
select_loan.click()

#Set loan type here
loan_type = config.MOTORCYCLE
set_loan_type(loan_type)


#Set rule profile here
rule_profile = config.DEFAULT_LITE
set_rule_profile(rule_profile)

#Get rules to edit
#worksheet = parser.open_file(config.WORKBOOK, config.WORKSHEET)
parse_excel()




print("SUCCESS")