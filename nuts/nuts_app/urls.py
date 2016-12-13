
from django.conf.urls import url, include
from django.contrib import admin

import django.contrib.auth.views

import views

urlpatterns = [
    
    url(r'^$', views.display_view.display_home, name='display_home'),

    # bw: search plan
    url(r'^search-plan', views.plan.search_plan, name='search_plan'),

    
    url(r'^home', views.display_view.display_home, name='display_home'),

    # bw: account manage 
    url(r'^login$', django.contrib.auth.views.login, {'template_name':'nuts/login.html'}, name='login'),
    url(r'^logout$', django.contrib.auth.views.logout_then_login, name='logout'),
    url(r'^register$', views.account_manage_view.register, name='register'),
    url(r'^confirm-registration/(?P<username>\w+)/(?P<token>[a-z0-9\-]+)/$', views.account_manage_view.confirm_registration, name='confirm'),

    # built-in methods for password reset
    url(r'^password-reset/done/$', django.contrib.auth.views.password_reset_done, {'template_name':'account/password_reset_done.html'}, name='password_reset_done'),
    url(r'^password-reset/$', django.contrib.auth.views.password_reset, {'template_name':'account/password_reset_form.html'}, name='password_reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', django.contrib.auth.views.password_reset_confirm, {'template_name':'account/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done/$', django.contrib.auth.views.password_reset_complete, {'template_name':'account/password_reset_complete.html'}, name='password_reset_complete'),

    # bw: show profile of every user
    url(r'^show-profile/(?P<user_id>\d+)/$', views.profile_view.show_profile, name='show_profile'),

    url(r'^edit-profile', views.profile_view.edit_profile, name='edit_profile'),
    url(r'^photo/(?P<user_id>\d+)/$', views.profile_view.get_photo, name='get_photo'),
    url(r'^change-password', views.profile_view.change_password, name='change_password'),

    # lutingw: plan
    url(r'^create-plan', views.plan.create_plan, name='create_plan'),
    url(r'^get-todo', views.plan.get_todo_plan, name='get_todo_plan'),
    url(r'^get-doing', views.plan.get_doing_plan, name='get_doing_plan'),
    url(r'^get-done', views.plan.get_done_plan, name='get_done_plan'),
    url(r'^view-plan/(?P<id>\d+)$', views.plan.view_plan, name='view_plan'),
    url(r'^my-plan', views.plan.my_plan, name='my_plan'),
    url(r'^view-all-plan', views.plan.view_all_plan, name='view_all_plan'),
    url(r'^edit-plan/(?P<id>\d+)$', views.plan.edit_plan, name='edit_plan'),
    url(r'^delete-plan/(?P<id>\d+)$', views.plan.delete_plan, name='delete_plan'),
    url(r'^update-state/(?P<id>\d+)$', views.plan.update_state, name='update_state'),
    

    # liu3: display
    url(r'^more-nuts', views.display_view.global_plans, name='global_plans'),
    url(r'^eat_plan/(?P<do_follow>\S+)/(?P<id>\d+)$', views.social_view.eat_plan, name='eat_plan'),

    url(r'^follow_user/(?P<do_follow>\S+)/(?P<id>\d+)$', views.social_view.follow_user, name='follow_user'),
    url(r'^get_all_public', views.display_view.get_all_public, name='get_all_public'),
    url(r'^get_all_eat', views.display_view.get_all_eat, name='get_all_eat'),
    url(r'^get_all_follow', views.display_view.get_all_follow, name='get_all_follow'),
    url(r'^view_all_mine$', views.plan.view_all_mine, name='view_all_mine'),

    url(r'^create_range_plan', views.plan.create_range_plan, name='create_range_plan'),
    url(r'^edit-plan-time', views.plan.edit_plan_time, name='edit-plan-time'),

    url(r'^get_message', views.display_view.get_message, name='get_message'),
    
    # bw: add comment
    url(r'^add-comment', views.display_view.add_comment),
    # bw: like plan
    url(r'^like_plan/(?P<do_like>\S+)/(?P<id>\d+)$', views.social_view.like_plan, name='like_plan'),
    




    
]
