import os

def populate():
	sz = ShareZone(is_active=True,name="Admin",zipcode="00000",has_shed=False)
	sz.save()
	u = User.objects.create_user(username="super",password="super",first_name="super",last_name="admin",email=" ")
	u.save()
	tu = ToolShareUser.objects.create(user=u,phone_number="1234567890",street="Temp",city="Temp",state="NY",zipcode=12345,birth_date=date.today(),share_zone=sz,is_active=True,is_declined=False,is_admin=True,is_super_admin=True)
	tu.save()

if __name__ == '__main__':
	print ("Starting population script...")
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
	from django.contrib.auth import authenticate
	from toolshare.models import *
	from django.contrib.auth.models import User, Permission
	from datetime import *
	populate()