# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestSAETeacher():
  def setup_method(self, method):
    self.driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_sAETeacher(self):
    # Test name: SAE-Teacher
    # Step # | name | target | value
    # 1 | open | /auth/login | 
    self.driver.get("http://localhost:4200/auth/login")
    # 2 | setWindowSize | 1185x688 | 
    self.driver.set_window_size(1185, 688)
    # 3 | click | id=username | 
    self.driver.find_element(By.ID, "username").click()
    # 4 | type | id=username | vcomparrot
    self.driver.find_element(By.ID, "username").send_keys("vcomparrot")
    # 5 | click | css=.p-password-input | 
    self.driver.find_element(By.CSS_SELECTOR, ".p-password-input").click()
    # 6 | type | css=.p-password-input | Test1234567!
    self.driver.find_element(By.CSS_SELECTOR, ".p-password-input").send_keys("Test1234567!")
    # 7 | mouseDown | css=.p-button-label | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-button-label")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 8 | mouseUp | css=.p-ink | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-ink")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 9 | click | css=.p-ripple | 
    self.driver.find_element(By.CSS_SELECTOR, ".p-ripple").click()
    # 10 | mouseDown | linkText=Utilisateurs | 
    element = self.driver.find_element(By.LINK_TEXT, "Utilisateurs")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 11 | mouseUp | css=.p-ink-active | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-ink-active")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 12 | click | linkText=Utilisateurs | 
    self.driver.find_element(By.LINK_TEXT, "Utilisateurs").click()
    # 13 | mouseDown | css=li:nth-child(1) > .list-none > li:nth-child(1) li:nth-child(1) > .p-ripple | 
    element = self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(1) > .list-none > li:nth-child(1) li:nth-child(1) > .p-ripple")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 14 | mouseUp | css=.p-ink-active | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-ink-active")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 15 | click | css=li:nth-child(1) > .list-none > li:nth-child(1) li:nth-child(1) > .p-ripple | 
    self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(1) > .list-none > li:nth-child(1) li:nth-child(1) > .p-ripple").click()
    # 16 | runScript | window.scrollTo(0,0) | 
    self.driver.execute_script("window.scrollTo(0,0)")
    # 17 | click | css=.ng-star-inserted:nth-child(2) > td .p-button-danger | 
    self.driver.find_element(By.CSS_SELECTOR, ".ng-star-inserted:nth-child(2) > td .p-button-danger").click()
    # 18 | click | css=.p-element:nth-child(2) > .p-button-danger | 
    self.driver.find_element(By.CSS_SELECTOR, ".p-element:nth-child(2) > .p-button-danger").click()
    # 19 | mouseDown | linkText=Utilisateurs | 
    element = self.driver.find_element(By.LINK_TEXT, "Utilisateurs")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 20 | mouseUp | css=.p-ink-active | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-ink-active")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 21 | click | linkText=Utilisateurs | 
    self.driver.find_element(By.LINK_TEXT, "Utilisateurs").click()
    # 22 | click | linkText=Étudiants | 
    self.driver.find_element(By.LINK_TEXT, "Étudiants").click()
    # 23 | mouseDown | linkText=Enseignants | 
    element = self.driver.find_element(By.LINK_TEXT, "Enseignants")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 24 | mouseUp | css=.p-ink-active | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-ink-active")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 25 | click | linkText=Enseignants | 
    self.driver.find_element(By.LINK_TEXT, "Enseignants").click()
    # 26 | click | css=.p-element:nth-child(2) > .p-ripple | 
    self.driver.find_element(By.CSS_SELECTOR, ".p-element:nth-child(2) > .p-ripple").click()
    # 27 | click | id=username | 
    self.driver.find_element(By.ID, "username").click()
    # 28 | type | id=username | Homps
    self.driver.find_element(By.ID, "username").send_keys("Homps")
    # 29 | click | id=nom | 
    self.driver.find_element(By.ID, "nom").click()
    # 30 | type | id=nom | Homps
    self.driver.find_element(By.ID, "nom").send_keys("Homps")
    # 31 | click | id=prenom | 
    self.driver.find_element(By.ID, "prenom").click()
    # 32 | type | id=prenom | Marc
    self.driver.find_element(By.ID, "prenom").send_keys("Marc")
    # 33 | click | id=email | 
    self.driver.find_element(By.ID, "email").click()
    # 34 | type | id=email | marc.homps@gmail.com
    self.driver.find_element(By.ID, "email").send_keys("marc.homps@gmail.com")
    # 35 | click | css=.p-password-input | 
    self.driver.find_element(By.CSS_SELECTOR, ".p-password-input").click()
    # 36 | type | css=.p-password-input | Marc1234567!
    self.driver.find_element(By.CSS_SELECTOR, ".p-password-input").send_keys("Marc1234567!")
    # 37 | click | id=initial | 
    self.driver.find_element(By.ID, "initial").click()
    # 38 | type | id=initial | MH
    self.driver.find_element(By.ID, "initial").send_keys("MH")
    # 39 | click | id=desktop | 
    self.driver.find_element(By.ID, "desktop").click()
    # 40 | mouseDown | css=.w-full | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".w-full")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 41 | mouseUp | css=.p-ink-active | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-ink-active")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 42 | click | css=.w-full | 
    self.driver.find_element(By.CSS_SELECTOR, ".w-full").click()
    # 43 | mouseDown | css=.ng-star-inserted > .list-none > li > .list-none > li:nth-child(2) .font-medium | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".ng-star-inserted > .list-none > li > .list-none > li:nth-child(2) .font-medium")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 44 | mouseUp | css=.p-ink-active | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-ink-active")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 45 | click | linkText=Formations | 
    self.driver.find_element(By.LINK_TEXT, "Formations").click()
    # 46 | runScript | window.scrollTo(0,0) | 
    self.driver.execute_script("window.scrollTo(0,0)")
    # 47 | mouseDown | linkText=Parcours | 
    element = self.driver.find_element(By.LINK_TEXT, "Parcours")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 48 | mouseUp | css=.p-ink-active | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-ink-active")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 49 | click | linkText=Parcours | 
    self.driver.find_element(By.LINK_TEXT, "Parcours").click()
    # 50 | mouseDown | linkText=Salles de classe | 
    element = self.driver.find_element(By.LINK_TEXT, "Salles de classe")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 51 | mouseUp | css=.p-ink-active | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-ink-active")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 52 | click | linkText=Salles de classe | 
    self.driver.find_element(By.LINK_TEXT, "Salles de classe").click()
    # 53 | runScript | window.scrollTo(0,0) | 
    self.driver.execute_script("window.scrollTo(0,0)")
    # 54 | mouseDown | css=.p-element > .p-ripple | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-element > .p-ripple")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 55 | mouseUp | css=.p-ink-active | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-ink-active")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 56 | click | css=.p-element > .p-ripple | 
    self.driver.find_element(By.CSS_SELECTOR, ".p-element > .p-ripple").click()
    # 57 | mouseOver | css=.p-ink-active | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-ink-active")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    # 58 | mouseOut | css=.p-ink-active | 
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element, 0, 0).perform()
    # 59 | click | id=name | 
    self.driver.find_element(By.ID, "name").click()
    # 60 | type | id=name | B2-04
    self.driver.find_element(By.ID, "name").send_keys("B2-04")
    # 61 | click | css=.p-inputnumber-button-up | 
    self.driver.find_element(By.CSS_SELECTOR, ".p-inputnumber-button-up").click()
    # 62 | click | css=.p-inputnumber-button-up | 
    self.driver.find_element(By.CSS_SELECTOR, ".p-inputnumber-button-up").click()
    # 63 | click | css=.p-inputnumber-button-up | 
    self.driver.find_element(By.CSS_SELECTOR, ".p-inputnumber-button-up").click()
    # 64 | doubleClick | css=.p-inputnumber-button-up | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-inputnumber-button-up")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    # 65 | click | css=.p-inputnumber-button-up | 
    self.driver.find_element(By.CSS_SELECTOR, ".p-inputnumber-button-up").click()
    # 66 | click | css=.p-inputnumber-button-up | 
    self.driver.find_element(By.CSS_SELECTOR, ".p-inputnumber-button-up").click()
    # 67 | click | css=.p-inputnumber-button-up | 
    self.driver.find_element(By.CSS_SELECTOR, ".p-inputnumber-button-up").click()
    # 68 | click | css=.p-inputnumber-button-up | 
    self.driver.find_element(By.CSS_SELECTOR, ".p-inputnumber-button-up").click()
    # 69 | click | css=.p-inputnumber-button-up | 
    self.driver.find_element(By.CSS_SELECTOR, ".p-inputnumber-button-up").click()
    # 70 | click | css=.p-inputnumber-button-up | 
    self.driver.find_element(By.CSS_SELECTOR, ".p-inputnumber-button-up").click()
    # 71 | click | css=.p-inputnumber-button-up | 
    self.driver.find_element(By.CSS_SELECTOR, ".p-inputnumber-button-up").click()
    # 72 | mouseDown | css=.p-button-primary .p-button-label | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-button-primary .p-button-label")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 73 | mouseUp | css=.p-ink-active | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-ink-active")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 74 | click | css=.p-button-primary > .p-ripple | 
    self.driver.find_element(By.CSS_SELECTOR, ".p-button-primary > .p-ripple").click()
    # 75 | mouseOver | css=.p-ink-active | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-ink-active")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    # 76 | mouseOver | css=.p-button-primary .p-button-label | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-button-primary .p-button-label")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    # 77 | mouseDown | linkText=Équipements | 
    element = self.driver.find_element(By.LINK_TEXT, "Équipements")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 78 | mouseUp | css=.p-ink-active | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-ink-active")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 79 | click | linkText=Équipements | 
    self.driver.find_element(By.LINK_TEXT, "Équipements").click()
    # 80 | mouseDown | css=.p-element > .p-ripple | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-element > .p-ripple")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 81 | mouseUp | css=.p-ink-active | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-ink-active")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 82 | click | css=.p-element > .p-ripple | 
    self.driver.find_element(By.CSS_SELECTOR, ".p-element > .p-ripple").click()
    # 83 | mouseOver | css=.p-ink-active | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-ink-active")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    # 84 | click | id=equipmentName | 
    self.driver.find_element(By.ID, "equipmentName").click()
    # 85 | type | id=equipmentName | Projecteur
    self.driver.find_element(By.ID, "equipmentName").send_keys("Projecteur")
    # 86 | mouseDown | css=.p-button-primary .p-button-label | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-button-primary .p-button-label")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 87 | mouseUp | css=.p-ink-active | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-ink-active")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 88 | click | css=.p-button-primary > .p-ripple | 
    self.driver.find_element(By.CSS_SELECTOR, ".p-button-primary > .p-ripple").click()
    # 89 | mouseOut | css=.p-ink-active | 
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element, 0, 0).perform()
    # 90 | mouseDown | css=.pi-chevron-up | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".pi-chevron-up")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 91 | mouseUp | css=.p-ink-active | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".p-ink-active")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 92 | click | css=.m-3 | 
    self.driver.find_element(By.CSS_SELECTOR, ".m-3").click()
    # 93 | click | linkText=Se déconnecter | 
    self.driver.find_element(By.LINK_TEXT, "Se déconnecter").click()
    # 94 | close |  | 
    self.driver.close()
  
