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


"""
#Select rule set to edit
prescreen = 'Prescreen'
prescreen_link = browser.find_element_by_link_text(prescreen)
prescreen_link.click()
"""

rule_set = ''
rule = ''
rule_value = ''
rule_score = ''
rule_data = []

#workbook_link = 'Marine Underwriting Rules 3.28.18.xlsx'
#worksheet_name = 'Underwriting Rules'

def open_file(workbook_link, worksheet_name):
	workbook = xlrd.open_workbook(workbook_link)
	worksheet = workbook.sheet_by_name(worksheet_name)
	return worksheet
	
def fix_rule_value(rule_value):
	tokens = rule_value.split()
	if len(tokens) > 1:
		if tokens[1] == 'years':
			return int(tokens[0])
	return int(float(tokens[0]))
		
		

def parse_excel():
	counter = 0
	rule_type_set = False
	worksheet = open_file(config.WORKBOOK, config.WORKSHEET)
	#rownum = 2
	print("Num rows:", worksheet.nrows)
	for rownum in range(2,worksheet.nrows):
		row = worksheet.row(rownum)
		if row[1].value == "" and row[2].value == "" and row[3].value == "" and rule_type_set == False:
			if 'Pre-Screen Evaluation' in row[0].value:
				rule_set = 'Prescreen'
			elif 'Pre-Screen Decision' in row[0].value:
				rule_set = 'Prescreen (Decision)'
			elif 'Common-Evaluation' in row[0].value:
				rule_set = 'Common'
			elif 'Credit-Derogatory' in row[0].value:
				rule_set = 'Common-Credit Derogatory'
			
			print(rule_set)
			rule_type_set = True
			go_to_rule_type(rule_set)
			
		elif row[2].value != "":
			if rule_set == 'Prescreen':
				
				rule = config.PRESCREEN_EVALUATION[row[0].value]
				print("Rule:",rule)
				if rule == 'SSNNotIssued-Applicant' or rule == 'SSNNotIssued-CoApplicant':
					continue
				print(row[2].value)
				rule_value = fix_rule_value(str(row[2].value))
				rule_score = row[3].value
				print(rule_value)
				rule_data = [rule, rule_value, rule_score]
				
				go_to_rule(rule)
				update_rule(rule, rule_value)
				counter += 1
				
				if counter == 4:
					print("prescreen done")
					back_button = browser.find_element_by_xpath("//*[contains(text(), 'Back')]")
					back_button.click()
					rule_type_set = False
			
			elif rule_set == 'Prescreen (Decision)':
				rule = config.PRESCREEN_DECISION[row[0].value]
				print(rule)
				rule_value = fix_rule_value(str(row[2].value))
				rule_score = row[3].value
				print(rule_value)
				rule_data = [rule, rule_value, rule_score]
				
				go_to_rule(rule)
				update_rule(rule, rule_value)
				counter += 1
				
				if counter == 5:
					print("prescreen decision done")
					back_button = browser.find_element_by_xpath("//*[contains(text(), 'Back')]")
					back_button.click()
					rule_type_set = False
				
			
		
		#print(rule_type)
		#rownum += 1

def go_to_rule_type(rule_type):
	browser.find_element_by_link_text(rule_type).click()
	
def go_to_rule(rule_name):
	sleep(2)
	browser.refresh()
	update_link = browser.find_element_by_link_text(rule_name)
	update_link.click()
	
"""
#Select rule name
rule_name = 'MaximumAgeofVehicle'
rule_value = '25'
rule_score = '2'

sleep(2)
edit_buttons = browser.find_elements_by_class_name('fa-pencil-square-o')
"""
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
		
def update_rule(rule_name, rule_value):
	
	sleep(2)
	field_inputs = browser.find_elements_by_xpath("//input")
	field_inputs[1].clear()
	field_inputs[1].send_keys(str(rule_value))
	
	"""
	for i in range(len(field_inputs)):
		print(i)
		field_inputs[i].clear()
		field_inputs[i].send_keys(rule_value)
	"""
	
	validate_save_back()
	
"""
for i in range (len(edit_buttons)):
	sleep(1)
	browser.refresh()
	
	
	#existing_name = browser.find_element_by_id('formly_1_input_ruleName_0')
	#existing_name = existing_name.get_attribute('value')
	
	#instead of rule_name, get value from dictionary. rules from excel sheet will be mapped to rule names on website
	#if rule_name == existing_name:
	
	#Update description
	update_description(rule_name, rule_value)
	
	
	update_rule(rule_name, rule_value)

	sleep(1)
"""	
	
def set_loan_type(loan_type):
	browser.find_element_by_id(loan_type).click()
	
def set_rule_profile(rule_profile):
	browser.find_element_by_partial_link_text(rule_profile).click()
	
	
	
#if __name__ == '__main__':

#Get website
browser = webdriver.Chrome()
browser.get('https://test.decisionlender.solutions/tci/#/auth/login/?returnTo=%2Fauth%2Flogin%2F')
browser.maximize_window()
browser.implicitly_wait(10)

#Sign in
compid = browser.find_element_by_id("companyid")
user = browser.find_element_by_id('username')
password = browser.find_element_by_id('password')

compid.send_keys(config.TEST_COMPID)
user.send_keys(config.TEST_USER)
password.send_keys(config.TEST_PASS)

login_attempt = browser.find_element_by_xpath("//*[@type='submit']")
login_attempt.submit()

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
loan_type = config.AUTO_INDIRECT
set_loan_type(loan_type)


#Set rule profile here
rule_profile = config.DEFAULT_LITE
set_rule_profile(rule_profile)

#Get rules to edit
#worksheet = parser.open_file(config.WORKBOOK, config.WORKSHEET)
parse_excel()




print("SUCCESS")