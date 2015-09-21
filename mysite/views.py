from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from toolshare.models import *
from django.contrib.auth.models import User, Permission
from datetime import *
from time import strptime

"""
User-related views
"""
def get_user_context(request):
	tuser = None
	for t in ToolShareUser.objects.all():
		if t.user.id == request.user.id:
			tuser = t
	return tuser

def index_view(request):
	if request.user.is_authenticated():
		template = loader.get_template("user.html")
		tuser = get_user_context(request)
		context = RequestContext(request, {'user_query_results':ToolShareUser.objects.filter(is_active=False, is_declined = False, share_zone_id=tuser.share_zone_id), 
										   'all_user_query_results':ToolShareUser.objects.all(),
										   'sharezone_query_results':ShareZone.objects.filter(is_active=False,is_declined=False),
										   'tool_query_results':Tool.objects.filter(is_active=True),
										   'transaction_query_results':Transaction.objects.all().order_by("-end_date"),
										   'tuser':tuser,
										   'number_of_requests':len(ToolRequest.objects.filter(requestee_id=request.user.id, replied_status=False)),
										   'number_of_unread_messages':len(Message.objects.filter(receiver=request.user.id, read=False, deleted=False, archived=False))})
		return HttpResponse(template.render(context))

	#direct to the login page
	c = {}
	c.update(csrf(request))
	
	return render_to_response('login.html', c)
	
def login_auth_view(request):
	#Get information returned from the login page.
	username = request.POST["username"]
	password = request.POST["password"]
	user = authenticate(username=username, password=password)
	#retrieve the user from the database
    
    #Log user into the database
	if(user is not None):
		if user.is_active:
			login(request, user)
			return HttpResponseRedirect("/home/")

    #invalid username / password entered
	return  HttpResponseRedirect("/invalid/")

def logout_view(request):
	#direct to the logout page
	logout(request)
	return HttpResponseRedirect("/home/")

def invalid_login_view(request):
	#direct to the invalid login page
    return render_to_response("invalid_login.html")
	
def register_user_account_view(request):
	#load registration template with a list of ShareZone to be selected
	this_month = date.today().month
	today = date.today().day
	this_year = date.today().year
	template = loader.get_template('registration.html')
	share_zone_query_results = ShareZone.objects.exclude(name='Admin')
	states = open("mysite/USstates.txt").read().split(" ")
	context = RequestContext(request, {"share_zone_query_results":share_zone_query_results,
									   "list_of_states":states,
									   "range_months":range(1,13),
									   "selected_month":this_month,
									   "range_days":range(1,32),
									   "selected_day":today,
									   "range_years":range(this_year,this_year-101,-1),
									   "selected_year":this_year})
	return HttpResponse(template.render(context))
	
def register_auth_view(request):
	this_year = date.today().year
	share_zone_query_results = ShareZone.objects.all()
	states = open("mysite/USstates.txt").read().split(" ")
	saved_content = {"share_zone_query_results":share_zone_query_results,
					 "list_of_states":states,
				     "username_input":request.POST["username"],
				     "email_input":request.POST["email"],
				     "first_name_input":request.POST["firstname"],
				     "last_name_input":request.POST["lastname"],
				     "phonenumber_input":request.POST["phonenumber"],
				     "street_input":request.POST["street_address"],
				     "city_input":request.POST["city"],
				     "state_input":request.POST["state"],
				     "zipcode_input":request.POST["zipcode"],
				     "range_months":range(1,13),
				     "selected_month":int(request.POST["birthmonth"]),
				     "range_days":range(1,32),
				     "selected_day":int(request.POST["birthday"]),
				     "range_years":range(this_year,this_year-101,-1),
				     "selected_year":int(request.POST["birthyear"]),
					 }
	if request.POST:
		birth_date = request.POST["birthyear"] + "-" + request.POST["birthmonth"] + "-" + request.POST["birthday"]
		try:
			try_birthdate = date(int(request.POST["birthyear"]), int(request.POST["birthmonth"]), int(request.POST["birthday"]))
			print(try_birthdate)
		except ValueError:
			template = loader.get_template("registration.html")
			saved_content["error_message"] = "Please select a valid date."
			context = RequestContext(request, saved_content)
			return HttpResponse(template.render(context))		
		admin = False
		active = False
		sz = None
		#create/join ShareZone process
		if request.POST.get("sz_radio") == "create":
			#search the database to check if the new ShareZone name is unique
			for zone in ShareZone.objects.all():
				if zone.name == request.POST["ShareZoneName"]:
					template = loader.get_template("registration.html")
					saved_content["error_message"] = "ShareZone name is already taken."
					context = RequestContext(request, saved_content)
					return HttpResponse(template.render(context))										   
			new_Share_Zone = ShareZone(name=request.POST["ShareZoneName"], zipcode=request.POST["zipcode"])
			new_Share_Zone.save()
			sz = ShareZone.objects.get(name=request.POST["ShareZoneName"])
			admin = True
			active = True
		else:
			sz = ShareZone.objects.get(id=request.POST["ChosenShareZone"])
			
		#search the database to check if the new username is unique
		for auth_user in User.objects.all():
			if request.POST["username"] == auth_user.username:
				template = loader.get_template("registration.html")
				share_zone_query_results = ShareZone.objects.all()
				saved_content["error_message"] = "Username is already taken."
				context = RequestContext(request, saved_content)
				return HttpResponse(template.render(context))
			
		#create a new user if there is no error								   
		newuser = ToolShareUser.objects.create(
			user = User.objects.create_user(username=request.POST["username"], 
											password=request.POST["password"], 
											first_name=request.POST["firstname"], 
											last_name=request.POST["lastname"], 
											email=request.POST["email"]),
			phone_number = request.POST["phonenumber"],
			street = request.POST["street_address"],
			city = request.POST["city"],
			state = request.POST["state"],
			zipcode = request.POST["zipcode"],
			birth_date = request.POST["birthyear"] + "-" + request.POST["birthmonth"] + "-" + request.POST["birthday"],
			share_zone = sz,
			is_admin = admin,
			is_active = active)
		
	return HttpResponseRedirect("/registration_success/")

def register_user_account_success_view(request):
	#direct to the successful registration page
	return render_to_response("registration_success.html")

def register_user_account_fail_view(request):
	#direct to the successful registration page
	return render_to_response("registration_fail.html")
	
def inactive_user_view(request, tuser_id):
	#set user to active
	tuser = ToolShareUser.objects.get(id = tuser_id)
	tuser.is_active = True
	tuser.is_declined = False
	tuser.save()
	return HttpResponseRedirect("/home/")
	
def decline_user_view(request, tuser_id):
	#set user declined permission to True
	tuser = ToolShareUser.objects.get(id = tuser_id)
	tuser.is_active = False
	tuser.is_declined = True
	tuser.save()
	return HttpResponseRedirect("/home/")

def make_admin_view(request, tuser_id):
	tuser = ToolShareUser.objects.get(id = tuser_id)
	tuser.is_active = True
	tuser.is_admin = True
	tuser.save()
	return HttpResponseRedirect("/home/")

def make_super_admin_view(request, tuser_id):
	tuser = ToolShareUser.objects.get(id = tuser_id)
	tuser.is_active = True
	tuser.is_declined = False
	tuser.is_admin = True
	tuser.is_super_admin = True
	tuser.save()
	return HttpResponseRedirect("/home/")
	
def inactive_sharezone_view(request, sharezone_id):
	#set sharezone to active
	sharezone = ShareZone.objects.get(id = sharezone_id)
	sharezone.is_active = True
	sharezone.is_declined = False
	sharezone.save()
	return HttpResponseRedirect("/home/")
	
def decline_sharezone_view(request, sharezone_id):
	#set sharezone to active
	sharezone = ShareZone.objects.get(id = sharezone_id)
	sharezone.is_active = False
	sharezone.is_declined = True
	sharezone.save()
	return HttpResponseRedirect("/home/")
	
def edit_user_profile_view(request):
	template = loader.get_template('edit_user_profile.html')
	this_year = date.today().year
	user = ToolShareUser.objects.get(id = request.user.id)
	states = open("mysite/USstates.txt").read().split(" ")
	context = RequestContext(request, {"email_input":user.user.email,
									   "first_name_input":user.user.first_name,
									   "last_name_input":user.user.last_name,
									   "phonenumber_input":user.phone_number,
									   "street_input":user.street,
									   "city_input":user.city,
									   "list_of_states":states,
									   "state_input":user.state,
									   "zipcode_input":user.zipcode,
									   "range_months":range(1,13),
									   "selected_month":user.birth_date.month,
									   "range_days":range(1,32),
									   "selected_day":user.birth_date.day,
									   "range_years":range(this_year,this_year-101,-1),
									   "selected_year":user.birth_date.year,
									   "tuser":get_user_context(request),
									   'number_of_requests':len(ToolRequest.objects.filter(requestee_id=request.user.id, replied_status=False)),
									   'number_of_unread_messages':len(Message.objects.filter(receiver=request.user.id, read=False, deleted=False, archived=False))})
	return HttpResponse(template.render(context))
	
def edit_user_profile_auth_view(request):
	template = loader.get_template('edit_user_profile.html')
	this_year = date.today().year
	user = ToolShareUser.objects.get(id = request.user.id)
	states = open("mysite/USstates.txt").read().split(" ")
	saved_content = {"email_input":request.POST["email"],
					 "first_name_input":request.POST["firstname"],
				     "last_name_input":request.POST["lastname"],
				     "phonenumber_input":request.POST["phonenumber"],
				     "street_input":request.POST["street_address"],
				     "city_input":request.POST["city"],
					 "list_of_states":states,
				     "state_input":request.POST["state"],
				     "zipcode_input":request.POST["zipcode"],
				     "range_months":range(1,13),
				     "selected_month":int(request.POST["birthmonth"]),
				     "range_days":range(1,32),
				     "selected_day":int(request.POST["birthday"]),
				     "range_years":range(this_year,this_year-101,-1),
				     "selected_year":int(request.POST["birthyear"]),
				     "tuser":get_user_context(request),
					 'number_of_requests':len(ToolRequest.objects.filter(requestee_id=request.user.id, replied_status=False)),
					 'number_of_unread_messages':len(Message.objects.filter(receiver=request.user.id, read=False, deleted=False, archived=False))}
	if request.POST:
		birth_date = request.POST["birthyear"] + "-" + request.POST["birthmonth"] + "-" + request.POST["birthday"]
		try:
			try_birthdate = date(int(request.POST["birthyear"]), int(request.POST["birthmonth"]), int(request.POST["birthday"]))
			print(try_birthdate)
		except ValueError:
			saved_content["error_message"] = "Please select a valid date."
			context = RequestContext(request, saved_content)
			return HttpResponse(template.render(context))	
		this_user_id = request.user.id
		this_user = ToolShareUser.objects.get(id = this_user_id)
		this_user.user.first_name = request.POST["firstname"]
		this_user.user.last_name = request.POST["lastname"]
		this_user.user.email = request.POST["email"]
		this_user.user.save()
		this_user.phone_number = request.POST["phonenumber"]
		this_user.street = request.POST["street_address"]
		this_user.city = request.POST["city"]
		this_user.state = request.POST["state"]
		this_user.zipcode = request.POST["zipcode"]
		this_user.birth_date = request.POST["birthyear"] + "-" + request.POST["birthmonth"] + "-" + request.POST["birthday"]
		this_user.save()
	return HttpResponseRedirect("/home/")

def transactions_view(request):
	template = loader.get_template("transactions.html")
	this_user_id = request.user.id
	borrow_requests = ToolRequest.objects.filter(requestee_id = this_user_id, replied_status = False)
	context = RequestContext(request, {"user_query_results":ToolShareUser.objects.all(),
									   "tool_query_results":Tool.objects.filter(is_active=True),
									   "transaction_query_results":Transaction.objects.all(),
									   "borrow_requests":borrow_requests,
									   'tuser':get_user_context(request),
									   'number_of_requests':len(ToolRequest.objects.filter(requestee_id=request.user.id, replied_status=False)),
									   'number_of_unread_messages':len(Message.objects.filter(receiver=request.user.id, read=False, deleted=False, archived=False))})
	return HttpResponse(template.render(context))
	
	
"""
ShareZone-related views
"""	
def sharezone_view(request, sharezone_id):
	tuser = get_user_context(request)
	if (tuser != None):
		template = loader.get_template("share_zone.html")
		sz = ShareZone.objects.get(id=sharezone_id)
		this_shed = Shed.objects.get( share_zone = sz )
		if ((tuser.share_zone.id == sz.id) or (tuser.is_super_admin)):
			context = RequestContext(request, {'username':request.user.username, 
											   'sharezone':sz,
											   'shed':this_shed,
											   'user_query_results':ToolShareUser.objects.all(), 
											   'tool_query_results':Tool.objects.filter(is_active=True), 
											   'transaction_query_results':Transaction.objects.all().order_by("-end_date"),
											   'id':request.user.id,
											   'tuser':get_user_context(request),
											   'number_of_requests':len(ToolRequest.objects.filter(requestee_id=request.user.id, replied_status=False)),
											   'number_of_unread_messages':len(Message.objects.filter(receiver=request.user.id, read=False, deleted=False, archived=False))})
			return HttpResponse(template.render(context))
	return HttpResponseRedirect("/home/")	

def shed_creation_view(request):
	if request.POST:
		shareZ = ShareZone.objects.get( id = request.user.toolshareuser.share_zone_id )
		new_shed = Shed(
			address = request.POST["address"],
			max_num_tools = request.POST["maxnum"],
			share_zone = shareZ,
			current_num_tools = 0)
		shareZ.has_shed =  True
		new_shed.save()
		shareZ.save()
	return HttpResponseRedirect("/shed_success/")
	
def shed_creation_success_view(request):
	template = loader.get_template("shed_success.html")
	shareZ = ShareZone.objects.get( id = request.user.toolshareuser.share_zone_id )
	context = RequestContext(request, {'sharezone': shareZ})
	return HttpResponse(template.render(context))
	
def other_users_view(request, this_user_id):
	if request.user.id == int(this_user_id): 
		return HttpResponseRedirect("/home/")
	else:
		template = loader.get_template("other_users.html")
		this_user = ToolShareUser.objects.get(id = this_user_id)
		context = RequestContext(request, {'tu':this_user, 
										   'user_query_results':ToolShareUser.objects.all(), 
										   'tool_query_results':Tool.objects.filter(is_active=True),
										   'transaction_query_results':Transaction.objects.all().order_by("-end_date"),
										   'tuser':get_user_context(request),
										   'number_of_requests':len(ToolRequest.objects.filter(requestee_id=request.user.id, replied_status=False)),
										   'number_of_unread_messages':len(Message.objects.filter(receiver=request.user.id, read=False, deleted=False, archived=False))})
		return HttpResponse(template.render(context))
		
def edit_shed_view(request):
	template = loader.get_template('edit_shed.html')
	shed = Shed.objects.get(id = request.POST["editshed"])
	context = RequestContext(request, {"shed_address":shed.address,
									   "shed":shed,
									   "tuser":get_user_context(request),
									   "shed_max_num_tools":shed.max_num_tools})
	return HttpResponse(template.render(context))

def edit_shed_auth_view(request, shed_id):
	template = loader.get_template('edit_shed.html')
	shed = Shed.objects.get(id = shed_id)
	shareZ = ShareZone.objects.get( id = shed.share_zone_id )
	saved_content =  {"shed_address":shed.address,
					   "shed":shed,
					   "tuser":get_user_context(request),
					   "shed_max_num_tools":shed.max_num_tools}
	if request.POST:
		shed_id = Tool.objects.get(id = shed_id)
		shed_id.address = request.POST["shed_location"]
		num = request.POST["shed_max"]
		if num < shed_id.current_num_tools:
			template = loader.get_template("edit_shed.html")
			saved_content["error_message"] = "Max tool number is less than current number of tools."
			context = RequestContext(request, saved_content)
			return HttpResponse(template.render(context))
		else: 
			shed_id.max_num_tools = num
		shed_id.save()
	return HttpResponseRedirect("/sharezone/"+str(shareZ.id))
	
	
"""
Tool-related views
"""	
def create_tool_view(request):
	template = loader.get_template('tool_creation.html')
	context = RequestContext(request, {'tuser':get_user_context(request),
									   'tuser_age':date.today().year-get_user_context(request).birth_date.year,
									   'number_of_requests':len(ToolRequest.objects.filter(requestee_id=request.user.id, replied_status=False)), 
									   'number_of_unread_messages':len(Message.objects.filter(receiver=request.user.id, read=False, deleted=False, archived=False))})
	return HttpResponse(template.render(context))
	
def create_tool(request):
	if request.user.is_authenticated():
		if request.POST:
			tuser = ToolShareUser.objects.get(id = request.user.id)
			# for tuser in ToolShareUser.objects.all():
				# if tuser.user == request.user:
					# cl = tuser.address
					# tuser2 = tuser
			newtool = Tool(	
				name = request.POST["toolname"],
				current_location = tuser.zipcode,
				owner = tuser,
				current_user = tuser,
				condition = request.POST["condition"],

				is_power_tool = request.POST.getlist('powertool'),
				description = request.POST["description"],
				model_number = request.POST["modelnumber"]
				)
			newtool.save()
	return HttpResponseRedirect("/tool_success/")

def edit_tool_view(request):
	template = loader.get_template('edit_tool.html')
	tool = Tool.objects.get(id = request.POST["edittool"])
	context = RequestContext(request, {"tool_name":tool.name,
									   "tool":tool,
									   "tuser":get_user_context(request),
									   "tool_description":tool.description,
									   "model_number":tool.model_number,
									   "tool_condition":tool.condition})
	return HttpResponse(template.render(context))

def edit_tool_auth_view(request, this_tool_id):
	template = loader.get_template('edit_tool.html')
	tool = Tool.objects.get(id = this_tool_id)
	saved_content = {"tool_name":tool.name,
					 "tool":tool,
					 "tuser":get_user_context(request),
					 "tool_description":tool.description,
					 "model_number":tool.model_number,
					 "tool_condition":tool.condition}
	if request.POST:
		this_tool_id = Tool.objects.get(id = this_tool_id)
		this_tool_id.name = request.POST["toolname"]
		this_tool_id.description = request.POST["description"]
		this_tool_id.model_number = request.POST["modelnumber"]
		this_tool_id.condition = request.POST["condition"]
		this_tool_id.save()
	return HttpResponseRedirect("/tool/"+str(tool.id))
	
def deregister_tool_view(request):
	template = loader.get_template('tool_deregistration.html')
	tool = Tool.objects.get(id = request.POST["deregistertool"])
	context = RequestContext(request, {'tuser':get_user_context(request),
									   'tool':tool})
	return HttpResponse(template.render(context))
	
def deregistering_tool(request, this_tool_id):
	if request.user.is_authenticated():
		tool = Tool.objects.get(id=this_tool_id)
		if tool.is_available:
			tool.is_active = False
			tool.save()
			return HttpResponseRedirect("/tool_deregistered/")
		else:
			return HttpResponseRedirect("/tool_unavailable/"+str(tool.id))
	return HttpResponseRedirect("/home/")
	
def tool_deregistered_view(request):
	return render_to_response("tool_deregistered.html")
	
def tool_creation_success_view(request):
	#direct to the successful tool creation page
	return render_to_response("tool_success.html")
	
def tool_view(request, this_tool_id):
	template = loader.get_template("tool.html")
	this_tool = Tool.objects.get(id = this_tool_id)
	owner = User.objects.get(id = this_tool.owner_id)
	my_id = request.user.id
	# check to see if request has been replied to prevent spamming
	for tool_request in ToolRequest.objects.all():
		if tool_request.requester_id == my_id and tool_request.tool_id == this_tool.id:
			can_request = tool_request.can_request
			context = RequestContext(request, {'this_tool':this_tool, 
											   'owner':owner, 
											   'my_id':my_id, 
											   'can_request':can_request, 
											   'tuser':get_user_context(request), 
											   'tuser_age':date.today().year-get_user_context(request).birth_date.year,
											   'number_of_requests':len(ToolRequest.objects.filter(requestee_id=request.user.id, replied_status=False)),
											   'number_of_unread_messages':len(Message.objects.filter(receiver=request.user.id, read=False, deleted=False, archived=False))})
			return HttpResponse(template.render(context))
	context = RequestContext(request, {'this_tool':this_tool, 
									   'owner':owner, 
									   'my_id':my_id, 
									   'can_request':True, 
									   'tuser':get_user_context(request), 
									   'tuser_age':date.today().year-get_user_context(request).birth_date.year,
									   'number_of_requests':len(ToolRequest.objects.filter(requestee_id=request.user.id, replied_status=False)),
									   'number_of_unread_messages':len(Message.objects.filter(receiver=request.user.id, read=False, deleted=False, archived=False))})
	return HttpResponse(template.render(context))
	
def accept_borrow_request_view(request, tool_request_id):
	if request.user.is_authenticated():	
		tool_request = ToolRequest.objects.get(id = tool_request_id)
		tool = Tool.objects.get(id = tool_request.tool_id)
		if tool.is_available and tool.is_active:
			owner = ToolShareUser.objects.get(id = tool.owner_id)
			borrower = ToolShareUser.objects.get(id = tool_request.requester_id)
			transaction = Transaction.objects.create(start_date=datetime.now(),
													tool=tool,
													borrower=borrower,
													owner=owner)
			tool_request.replied_status = True
			tool_request.save()
			tool.current_user_id = tool_request.requester_id
			tool.is_available = False
			tool.save()
		else:
			return HttpResponseRedirect("/tool_unavailable/"+str(tool.id))
	return HttpResponseRedirect("/home/")
	
def decline_borrow_request_view(request, tool_request_id):
	tool_request = ToolRequest.objects.get(id = tool_request_id)
	tool_request.replied_status = True
	tool_request.can_request = True
	tool_request.save()
	return HttpResponseRedirect("/transactions/")
	
def request_tool_view(request):
	if request.user.is_authenticated():	
		if request.POST:
			request_tool_id = request.POST["requesttool"]
			request_tool = Tool.objects.get(id = request_tool_id)
			request_requester = ToolShareUser.objects.get(id = request.user.id)
			request_requestee = ToolShareUser.objects.get(id = request_tool.owner_id)
			for req in ToolRequest.objects.all():
				if req.requester_id == request_requester.id and req.requestee_id == request_requestee.id and req.tool_id == request_tool.id:
					req.replied_status = False
					req.can_request = False
					req.save()
					return HttpResponseRedirect("/transaction_success/"+str(request_tool.id))
			new_tool_request = ToolRequest.objects.create(
				requester = request_requester,
				requestee = request_requestee,
				tool = request_tool)
		return HttpResponseRedirect("/transaction_success/"+str(request_tool.id))
	return HttpResponseRedirect("/home/")

def borrow_tool_view(request):
	if request.POST:
		if request.user.is_authenticated():
			borrow_tool = request.POST["borrowtool"]
			tool = Tool.objects.get(id = borrow_tool)
			if tool.is_available and tool.is_active:
				owner = ToolShareUser.objects.get(id = tool.owner_id)
				borrower = ToolShareUser.objects.get(id = request.user.id)
				shed = Shed.objects.get(id = owner.share_zone_id)
				transaction = Transaction.objects.create(start_date=datetime.now(),
													  	 tool=tool,
														 borrower=borrower,
														 owner=owner,
														 shed=shed)
				tool.current_user_id = request.user.id
				tool.is_available = False
				tool.save()
			else:
				return HttpResponseRedirect("/tool_unavailable/"+str(tool.id))
		return HttpResponseRedirect("/transaction_success/"+str(tool.id))
	return HttpResponseRedirect("/home/")
	
def return_tool_view(request):
	if request.user.is_authenticated():
		if request.POST:
			return_tool = request.POST["returntool"]
			tool = Tool.objects.get(id = return_tool)
			for req in ToolRequest.objects.all():
				if req.requester_id == tool.current_user_id and req.requestee_id == tool.owner_id and req.tool_id == tool.id:
					# set the tool_request.can_request to true so the borrower may send a request again
					req = ToolRequest.objects.get(tool_id = tool.id, requester_id = tool.current_user_id)
					req.can_request = True
					req.save()
			print(tool.id)
			transaction = Transaction.objects.get(returned=False, tool_id=tool.id, owner_id=tool.owner_id, borrower_id=tool.current_user_id)
			transaction.returned = True
			transaction.end_date = datetime.now()
			#transaction.rating = request.POST["rating"]
			#transaction.description = request.POST["description"]
			transaction.save()
			tool.current_user_id = tool.owner_id
			tool.is_available = True
			tool.save()
		return HttpResponseRedirect("/transaction_success/"+str(tool.id))
	return HttpResponseRedirect("/home/")
	
def transaction_rating_view(request):
	return 

def add_to_shed_view(request):
	if request.user.is_authenticated():
		if request.POST:
			shareZ = ShareZone.objects.get( id = request.user.toolshareuser.share_zone_id )
			if shareZ.has_shed == False:
				return HttpResponseRedirect("/no_shed/")
			else:
				share_shed = Shed.objects.get( share_zone_id = shareZ.id )
				if share_shed.current_num_tools < share_shed.max_num_tools:
					add_tool = request.POST["addtool"]
					tool = Tool.objects.get(id = add_tool)
					tool.is_in_shed = True
					tool.save()
					share_shed.current_num_tools += 1
					share_shed.save()
					return HttpResponseRedirect("/store_shed_success/")
				else:
					return HttpResponseRedirect("/shed_full/")
	return HttpResponseRedirect("/home/")
	
def remove_from_shed_view(request):
	if request.user.is_authenticated():
		if request.POST:
			remove_tool = request.POST["removetool"]
			tool = Tool.objects.get(id = remove_tool)
			tool.is_in_shed = False
			tool.save()
			shareZ = ShareZone.objects.get( id = request.user.toolshareuser.share_zone_id )
			share_shed = Shed.objects.get( share_zone_id = shareZ.id )
			share_shed.current_num_tools -= 1
			share_shed.save()
			return HttpResponseRedirect("/remove_tool_shed_success/")
	return HttpResponseRedirect("/home/")
	
def transaction_success(request, tool_id):
	template = loader.get_template("transaction_success.html")
	context = RequestContext(request, {"tool_id":tool_id, 'tuser':get_user_context(request)})
	return HttpResponse(template.render(context))
	
def no_shed(request):
	return render_to_response("no_shed.html")

def store_shed_success(request):
	return render_to_response("store_shed_success.html")
	
def remove_tool_shed_success(request):
	return render_to_response("remove_tool_shed_success.html")
	
def shed_full(request):
	return render_to_response("shed_full.html")
	
def tool_unavailable(request, this_tool_id):
	template = loader.get_template("tool_unavailable.html")
	context = RequestContext(request, {"tool_id":this_tool_id})
	return HttpResponse(template.render(context))

"""
Message Related Views
"""

def create_message(request):
	if request.user.is_authenticated():	
		if request.POST:
			muser = ToolShareUser.objects.get(id = request.user.id)
			newmessage = Message(	
				receiver = ToolShareUser.objects.get(id=request.POST["receiver"]),
				sender = muser,
				subject = request.POST["subject"],
				message_body = request.POST["message_body"],
				)
			newmessage.save()
	return HttpResponseRedirect("/message_sent_success/")

def create_message_view(request):
	template = loader.get_template('new_message.html')
	context = RequestContext(request, {'tuser':get_user_context(request),
									   'user_query_results':ToolShareUser.objects.all(),
									   'number_of_requests':len(ToolRequest.objects.filter(requestee_id=request.user.id, replied_status=False)),
									   'number_of_unread_messages':len(Message.objects.filter(receiver=request.user.id, read=False, deleted=False, archived=False))})
	return HttpResponse(template.render(context))
	
def message_sent_success_view(request):
	#direct to the successful tool creation page
	return render_to_response("message_sent_success.html")

def messages_view(request):
	#authenticate logged in user
	if request.user.is_authenticated():
		template = loader.get_template("messages.html")
		context = RequestContext(request, {'username':request.user.username,  
										   'user_query_results':ToolShareUser.objects.all(), 
										   'measles':Message.objects.all(), 
										   'id':request.user.id,
										   'tuser':get_user_context(request),
										   'number_of_requests':len(ToolRequest.objects.filter(requestee_id=request.user.id, replied_status=False)),
									       'number_of_unread_messages':len(Message.objects.filter(receiver=request.user.id, read=False, deleted=False, archived=False))})
		return HttpResponse(template.render(context))
		
	#direct to the login page
	c = {}
	c.update(csrf(request))
	
	return render_to_response('messages.html', c)
	
def archive_view(request):
	if request.user.is_authenticated():
		template = loader.get_template("archive.html")
		context = RequestContext(request, {'username':request.user.username,  
										   'user_query_results':ToolShareUser.objects.all(), 
										   'measles':Message.objects.filter(archived=True), 
										   'id':request.user.id,
										   'tuser':get_user_context(request),
										   'number_of_requests':len(ToolRequest.objects.filter(requestee_id=request.user.id, replied_status=False)),
										   'number_of_unread_messages':len(Message.objects.filter(receiver=request.user.id, read=False, deleted=False, archived=False))})
		return HttpResponse(template.render(context))
		
	c = {}
	c.update(csrf(request))
	
	return render_to_response('archive.html', c)

def trash_view(request):
	if request.user.is_authenticated():
		template = loader.get_template("trash.html")
		context = RequestContext(request, {'username':request.user.username,  
										   'user_query_results':ToolShareUser.objects.all(), 
										   'measles':Message.objects.filter(deleted=True), 
										   'id':request.user.id,
										   'tuser':get_user_context(request),
										   'number_of_requests':len(ToolRequest.objects.filter(requestee_id=request.user.id, replied_status=False)),
										   'number_of_unread_messages':len(Message.objects.filter(receiver=request.user.id, read=False, deleted=False, archived=False))})
		return HttpResponse(template.render(context))
		
	c = {}
	c.update(csrf(request))
	
	return render_to_response('trash.html', c)
	
def delete_message_view(request, mess_id, where):
	#send message to trash
	mess = Message.objects.get(id = mess_id)
	mess.deleted = True
	mess.archived = False
	mess.save()
	if where == "3":
		return HttpResponseRedirect("/archive/")
	else:
		return HttpResponseRedirect("/messages/")
	
def archive_message_view(request, mess_id, where):
	#send message to archive
	mess = Message.objects.get(id = mess_id)
	mess.deleted = False
	mess.archived = True
	mess.save()
	if where == "1":
		return HttpResponseRedirect("/messages/")
	elif where == "2":
		return HttpResponseRedirect("/trash/")
	else:
		return HttpResponseRedirect("/archive/")

def this_message_view(request, this_message_id):
	template = loader.get_template("this_message.html")
	this_message = Message.objects.get(id = this_message_id)
	this_message.read = True
	this_message.save()
	context = RequestContext(request, {'this_message':this_message, 
									   'tuser':get_user_context(request), 
									   'number_of_requests':len(ToolRequest.objects.filter(requestee_id=request.user.id, replied_status=False)),
									   'number_of_unread_messages':len(Message.objects.filter(receiver=request.user.id, read=False, deleted=False, archived=False))})
	return HttpResponse(template.render(context))

"""
Rating Related Views
"""
"""
def create_tool_rating(request):
	if request.user.is_authenticated():	
		if request.POST:
			tuser = ToolShareUser.objects.get(id = request.user.id)
			newrating = Rating(	
				receiver = ToolShareUser.objects.get(id=request.POST["receiver"]),
				sender = muser,
				subject = request.POST["subject"],
				message_body = request.POST["message_body"],
				)
			newmessage.save()
	return HttpResponseRedirect("")

def create_member_rating(request):
        if request.user.is_authenticated():
                if request.POST:
"""
