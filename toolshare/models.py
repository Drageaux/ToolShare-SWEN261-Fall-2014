from django.db import models 
from django.contrib.auth.models import User #allows for the use of a extended User model
from django.db.models.signals import post_save

# Create your models here.
class ShareZone(models.Model):
	name = models.CharField(max_length=25, unique=True)
	zipcode = models.CharField(max_length=5)
	has_shed = models.BooleanField(default=False)
	
	is_active = models.BooleanField(default=False)
	is_declined = models.BooleanField(default=False)
	#community_shed = models.OneToOneField(Shed)
	#users = a list of users in the ShareZone
	#admins = a list of admins in the ShareZone
	#tools = a list of tools " "
	#shed = one to one relationship with the shed
	

class ToolShareUser(models.Model):
	user = models.OneToOneField(User) #connect this with the typical django user model
	phone_number = models.CharField(max_length=10)
	
	street = models.CharField(max_length=25)
	city = models.CharField(max_length=15)
	state = models.CharField(max_length=2)
	
	zipcode = models.CharField(max_length=5)
	birth_date = models.DateField()
	#rating = models.IntegerField()

	share_zone = models.ForeignKey("ShareZone")
	#tool_list = a list of tools the user is the owner of.
	#borrowed_tools = a list of tools the user has rented
	#user_history = a list of transactions involving the user

        #my_messages = a list of messages
	
	#user permissions for active users, admin users, and super_admin users
	is_active = models.BooleanField(default=False)
	is_declined = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	is_super_admin = models.BooleanField(default=False)
	
	
class UserManager(models.Manager):
	def get_active_users(self):
		return self.filter(is_active=True)
		
		
class Tool(models.Model):
	name = models.CharField(max_length=50)
	current_location = models.CharField(max_length=50)
	condition = models.CharField(max_length=50)
	status = models.CharField(max_length=50)
	description = models.CharField(max_length=250)
	model_number = models.CharField(max_length=50)
	is_power_tool = models.BooleanField()
	is_available = models.BooleanField(default=True)
	is_in_shed = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True) #for removing purposes

	owner = models.ForeignKey('ToolShareUser', related_name='owner')
	current_user = models.ForeignKey('ToolShareUser', related_name='current_user')
	#share_zone = models.ForeignKey("ShareZone", unique=True)
	#shed_tool_list = models.ForeignKey("Shed", unique=True)

	
class Shed(models.Model):
	address = models.CharField(max_length=100)
	max_num_tools = models.IntegerField()
	current_num_tools = models.IntegerField()

	share_zone = models.OneToOneField("ShareZone")
	#shedToolList = a list of tools in the shed
	#availableTools = a list of available tools in the shed
	#history = models.ForeignKey("Transaction")

		
class Transaction(models.Model):
	start_date = models.DateTimeField('rental start date')
	end_date = models.DateTimeField('rental end date', null=True)
	rating = models.FloatField(null=True)
	description = models.CharField(null=True, max_length=250)
	returned = models.BooleanField(default=False)
	
	tool = models.ForeignKey("Tool")
	borrower = models.ForeignKey('ToolShareUser', related_name='trans_borrower')
	owner = models.ForeignKey('ToolShareUser', related_name='trans_owner')
	shed = models.ForeignKey("Shed", null=True)

		
class ToolRequest(models.Model):
	requester = models.ForeignKey('ToolShareUser', related_name='requester')
	requestee = models.ForeignKey('ToolShareUser', related_name='requestee')
	tool = models.ForeignKey('Tool', related_name='tool')
	replied_status = models.BooleanField(default=False) # if False then request will appear on owner's request page
	can_request = models.BooleanField(default=False) # if False then borrower cannot request any more 
													 #(prevent spam/if tool is used by the same borrower)
													 
													 
class Message(models.Model):
	sender = models.ForeignKey('ToolShareUser', related_name='sender')
	receiver = models.ForeignKey('ToolShareUser', related_name='receiver')
	subject = models.CharField(max_length=50)
	message_body = models.CharField(max_length=1000)
	read = models.BooleanField(default=False)
	archived = models.BooleanField(default=False)
	deleted = models.BooleanField(default=False)
	in_inbox = 1
	in_trash = 2
	in_archive = 3

class MemberRating(models.Model):
	member = models.ForeignKey('ToolShareUser', related_name='member')
	memberrating = models.CharField(max_length=50)
	membercomment = models.CharField(max_length=50)
	
class ToolRating(models.Model):
	thisTool = models.ForeignKey('Tool', related_name='thisTool')
	preCondition = models.CharField(max_length=50)
	postCondition = models.CharField(max_length=50)
	toolrating = models.CharField(max_length=50)
	toolcomment = models.CharField(max_length=500)
