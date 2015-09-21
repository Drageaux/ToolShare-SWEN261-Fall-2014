from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^admin/?$', include(admin.site.urls)), #superadmin urls

	url(r'^home/?$', 'mysite.views.index_view'), #connect login view to the url .../home
	url(r'^login_auth/?$', 'mysite.views.login_auth_view', name = 'login_auth_view'),
	url(r'^logout/?$', 'mysite.views.logout_view', name = 'logout_view'),
	url(r'^invalid/?$', 'mysite.views.invalid_login_view'),
	url(r"^registration_success/?$", "mysite.views.register_user_account_success_view"),
	url(r"^registration_fail/?$", "mysite.views.register_user_account_fail_view"),
	url(r"^registration/?$", "mysite.views.register_user_account_view", name = "registration"),
	url(r"^registration_auth/?$", "mysite.views.register_auth_view", name = "registration_auth"),
	url(r"^inactive_user/(?P<tuser_id>\d+)/?$", "mysite.views.inactive_user_view", name = "inactive_user"),
	url(r"^decline_user/(?P<tuser_id>\d+)/?$", "mysite.views.decline_user_view", name = "decline_user"),
	url(r"^make_admin/(?P<tuser_id>\d+)/?$", "mysite.views.make_admin_view", name = "make_admin"),
	url(r"^make_super_admin/(?P<tuser_id>\d+)/?$", "mysite.views.make_super_admin_view", name = "make_super_admin"),
	
	url(r"^edit_user_profile/?$", 'mysite.views.edit_user_profile_view', name = "edit_user"),	
	url(r"^edit_user_profile_auth/?$", 'mysite.views.edit_user_profile_auth_view', name = "edit_user_profile_auth"),
	
	url(r"^sharezone/(?P<sharezone_id>\d+)/?$", "mysite.views.sharezone_view", name = "sharezone"),
	url(r"^inactive_sharezone/(?P<sharezone_id>\d+)/?$", "mysite.views.inactive_sharezone_view", name = "sharezone"),
	url(r"^decline_sharezone/(?P<sharezone_id>\d+)/?$", "mysite.views.decline_sharezone_view", name = "sharezone"),
	
	url(r"^no_shed/?$", 'mysite.views.no_shed', name = "no_shed"),
	url(r"^shed_full/?$", 'mysite.views.shed_full', name = "shed_full"),
	url(r"^shed_creation/?$", 'mysite.views.shed_creation_view'),
	url(r"^shed_success/?$", 'mysite.views.shed_creation_success_view', name = "make_shed"),
	url(r"^edit_shed/?", 'mysite.views.edit_shed_view', name = "edit_shed"),
	url(r"^edit_shed_auth/(?P<shed_id>\d+)/?$", 'mysite.views.edit_shed_auth_view', "edit_shed_auth"),
	url(r"^user/(?P<this_user_id>\d+)/?$", "mysite.views.other_users_view", name = "other_users"),
	
	url(r"^register_tool/?$", 'mysite.views.create_tool', name = "register_tool"),
	url(r"^create_tool/?$", 'mysite.views.create_tool_view', name = "create_tool"),
	url(r"^edit_tool/?$", 'mysite.views.edit_tool_view', name = "edit_tool"),
	url(r"^edit_tool_auth/(?P<this_tool_id>\d+)/?$", 'mysite.views.edit_tool_auth_view', name = "edit_tool_auth"),
	url(r"^deregister_tool/?$", 'mysite.views.deregister_tool_view', name = "deregister_tool"),
	url(r"^deregistering_tool/(?P<this_tool_id>\d+)/?$", 'mysite.views.deregistering_tool', name = "deregistering_tool"),
	url(r"^tool_success/?$", 'mysite.views.tool_creation_success_view'),
	url(r"^tool_deregistered/?$", 'mysite.views.tool_deregistered_view'),

	url(r"^messages/?$", "mysite.views.messages_view", name = "messages"),
	url(r"^register_message/?$", "mysite.views.create_message", name = "register_message"),
	url(r"^new_message/?$", "mysite.views.create_message_view", name = "create_message"),
	url(r"^delete_message/(?P<mess_id>\d+)/(?P<where>\d+)/?$", "mysite.views.delete_message_view", name = "delete_message"),
	url(r"^archive_message/(?P<mess_id>\d+)/(?P<where>\d+)/?$", "mysite.views.archive_message_view", name = "archive_message"),
	url(r"^archive/?$", "mysite.views.archive_view", name = "archive"),
	url(r"^trash/?$", "mysite.views.trash_view", name = "trash"),
	url(r"^this_message/(?P<this_message_id>\d+)/?$", "mysite.views.this_message_view", name = "this_message"),
	url(r"^message_sent_success/?$", "mysite.views.message_sent_success_view", name = "new_message"),
	
	url(r"^tool/(?P<this_tool_id>\d+)/?$", "mysite.views.tool_view", name = "tool"),
	url(r"^tool_unavailable/(?P<this_tool_id>\d+)/?$", "mysite.views.tool_unavailable", name = "tool_unavailable"),
	url(r"^transactions/?$", 'mysite.views.transactions_view', name = "transactions"),
	url(r"^accept_borrow_request/(?P<tool_request_id>\d+)/?$", "mysite.views.accept_borrow_request_view", name = "accept_borrow_request"),
	url(r"^decline_borrow_request/(?P<tool_request_id>\d+)/?$", "mysite.views.decline_borrow_request_view", name = "decline_borrow_request"),
	url(r"^request_tool/?$", 'mysite.views.request_tool_view', name = "request_tool"),
	url(r"^borrow_tool/?$", 'mysite.views.borrow_tool_view', name = "borrow_tool"),
	url(r"^return_tool/?$", 'mysite.views.return_tool_view', name = "return_tool"),
	url(r"^add_to_shed/?$", 'mysite.views.add_to_shed_view', name = "add_to_shed"),
	url(r"^remove_from_shed/?$", 'mysite.views.remove_from_shed_view', name = "remove_from_shed"),
	url(r"^transaction_success/(?P<tool_id>\d+)/?$", 'mysite.views.transaction_success', name = "transaction_success"),
	url(r"^store_shed_success/?$", 'mysite.views.store_shed_success', name = "store_shed_success"),
	url(r"^remove_tool_shed_success/?$", 'mysite.views.remove_tool_shed_success', name = "remove_tool_shed_success")
)
