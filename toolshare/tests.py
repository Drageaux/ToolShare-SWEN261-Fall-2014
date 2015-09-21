from django.test import TestCase
from toolshare.models import *
from django.contrib.auth.models import User
from datetime import *

# Create your tests here.
class ToolShareTestCase(TestCase):
	def setUp(self):
		tUser1 = ToolShareUser.objects.create(user = User.objects.create_user(username = "admin", password = "admin", first_name = "Random", last_name = "Guy"),
											  phone_number = "123456780",
											  street = "1 Lomb Memorial Drive",
											  city = "Rochester",
											  state = "NY",
											  zipcode = "14623",
											  birth_date = date(1995,8,28),
											  share_zone = ShareZone.objects.create(name = "Lololand",
																				   zipcode = "14623"))
		
		Tool.objects.create(name = "Hammer",
							current_location = "14623",
							condition = "5",
							description = "This is a hammer",
							model_number = "12345",
							is_power_tool = True,
							owner = tUser1,
							current_user = tUser1)
		

		tUserSuperBoss = ToolShareUser.objects.create(user = User.objects.create_user(username = "chris", password = "awesome", first_name = "Chris", last_name = "Hardtogetz"),
													  phone_number = "2837662000",
													  street = "1 Lomb Memorial Drive",
													  city = "Rochester",
													  state = "NY",
													  zipcode = "14623",
													  birth_date = date(1975,1,1),
													  is_super_admin = True,
													  is_admin = True,
													  is_active = True,
													  share_zone = ShareZone.objects.create(name = "SWEN261",
																						    zipcode = "14623"))
																							
		tUser2 = ToolShareUser.objects.create(user = User.objects.create_user(username = "borrower1", password = "123456", first_name = "Random", last_name = "Guy"),
											  phone_number = "123456780",
											  street = "1 Lomb Memorial Drive",
											  city = "Rochester",
											  state = "NY",
											  zipcode = "14623",
											  birth_date = date(2008,5,20),
											  share_zone = ShareZone.objects.get(name = "SWEN261",
																				   zipcode = "14623"))
		Tool.objects.create(name = "Grading Criteria",
							current_location = "14623",
							condition = "3",
							description = "This is a judgment book",
							model_number = "NO_mercy",
							is_power_tool = True,
							owner = tUserSuperBoss,
							current_user = tUserSuperBoss)

		
	def test_user_is_created(self):
		testFirstUser = ToolShareUser.objects.get(birth_date = date(1995,8,28), phone_number = "123456780")
		self.assertEqual(testFirstUser.zipcode,"14623")
	
	def test_user_age(self):
		testUser = ToolShareUser.objects.get(birth_date = date(1995,8,28), state = "NY")
		age = date.today().year-testUser.birth_date.year
		self.assertEqual(age >= 10,True)
		testUser2 = ToolShareUser.objects.get(birth_date = date(2008,5,20))
		age = date.today().year-testUser2.birth_date.year
		self.assertEqual(age >= 10,False)
	
	def test_underage_borrowing(self):
		testUser2 = ToolShareUser.objects.get(birth_date = date(2008,5,20))
		if age = date.today().year-testUser2.birth_date.year >= 10:
			
	
	def test_tool_is_active(self):
		hammer = Tool.objects.get(name = "Hammer")
		self.assertEqual(hammer.is_active, True)
		
	def test_sharezone_is_created(self):
		testSharezone = ShareZone.objects.get(name = "Lololand",zipcode = ToolShareUser.objects.get(birth_date = date(1995,8,28)).zipcode)
		