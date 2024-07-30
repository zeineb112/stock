from django.urls import include, path

from . import views

urlpatterns = [

# Shared URL's
path('', views.login_form, name='home'),
path('login/', views.loginView, name='login'),
path('logout/', views.logoutView, name='logout'),
path('regform/', views.register_form, name='regform'),
path('register/', views.registerView, name='register'),


# Librarian URL's
path('librarian/', views.librarian, name='librarian'),
path('labook_form/', views.labook_form, name='labook_form'),
path('labook/', views.labook, name='labook'),
path('llbook/', views.LBookListView.as_view(), name='llbook'),
path('ldrequest/', views.LDeleteRequest.as_view(), name='ldrequest'),
path('lsearch/', views.lsearch, name='lsearch'),
path('ldbook/<int:pk>', views.LDeleteBook.as_view(), name='ldbook'),
path('lmbook/', views.LManageBook.as_view(), name='lmbook'),
path('ldbookk/<int:pk>', views.LDeleteView.as_view(), name='ldbookk'),
path('lvbook/<int:pk>', views.LViewBook.as_view(), name='lvbook'),
path('lebook/<int:pk>', views.LEditView.as_view(), name='lebook'),
path('update/<str:pk>/', views.Update, name='update'), 
path('lebook/<int:pk>', views.LEditView.as_view(), name='lebook'),
path('mnbook/<int:pk>', views.controll1, name='mnbook'),
path('ccnbook/<int:pk>', views.control1.as_view(), name='ccnbook'),
path('conforme/<int:pk>', views.confrome.as_view(), name='conforme'),
path('conforme1/<int:pk>', views.conforme1, name='conforme1'),
path('detail/<int:pk>', views.detail.as_view(), name='detail'),
path('detail1/<int:pk>', views.detail1, name='detail1'),
path('detailc/<int:pk>', views.detailc.as_view(), name='detailc'),
path('detailp/<int:pk>', views.detailp.as_view(), name='detailp'),



# Publisher URL's
path('publisher/', views.UBookListView.as_view(), name='publisher'),
path('uabook_form/', views.uabook_form, name='uabook_form'),
path('uabook/', views.uabook, name='uabook'),
path('request_form/', views.request_form, name='request_form'),
path('delete_request/', views.delete_request, name='delete_request'),
path('feedback_form/', views.feedback_form, name='feedback_form'),
path('send_feedback/', views.send_feedback, name='send_feedback'),
path('about/', views.about, name='about'),
path('usearch/', views.usearch, name='usearch'),
path('ccbook/<int:pk>',views.controll, name='ccbook'),
path('cnbook /<int:pk>', views.control.as_view(), name='cnbook'),
path('cal/<int:pk>/', views.calculate, name='calculate'),


# Admin URL's
path('pdbook/<int:pk>', views.pDeleteBook.as_view(), name='pdbook'),
path('dashboard/', views.dashboard, name='dashboard'),
path('aabook_form/', views.aabook_form, name='aabook_form'),
path('aabook/', views.aabook, name='aabook'),
path('albook/', views.ABookListView.as_view(), name='albook'),
path('ambook/', views.AManageBook.as_view(), name='ambook'),
path('adbook/<int:pk>', views.ADeleteBook.as_view(), name='adbook'),
path('avbook/<int:pk>', views.AViewBook.as_view(), name='avbook'),
path('aebook/<int:pk>', views.AEditView.as_view(), name='aebook'),
path('adrequest/', views.ADeleteRequest.as_view(), name='adrequest'),
path('afeedback/', views.AFeedback.as_view(), name='afeedback'),
path('asearch/', views.asearch, name='asearch'),
path('adbookk/<int:pk>', views.ADeleteBookk.as_view(), name='adbookk'),
path('create_user_form/', views.create_user_form, name='create_user_form'),
path('aluser/', views.ListUserView.as_view(), name='aluser'),
path('create_use/', views.create_user, name='create_user'),
path('alvuser/<int:pk>', views.ALViewUser.as_view(), name='alvuser'),
path('aeuser/<int:pk>', views.AEditUser.as_view(), name='aeuser'),
path('aduser/<int:pk>', views.ADeleteUser.as_view(), name='aduser'),
path('admin_tools_stats/', include('admin_tools_stats.urls')),
path('CF/', views.CFListView.as_view(), name='CF'),
path('cfbook_form/', views.cfbook_form, name='cfbook_form'),
path('cfbook/', views.cfbook, name='cfbook'),
path('erequest/<int:pk>', views.AEditrequest.as_view(), name='erequest'),
path('prequest/<int:pk>', views.PEditrequest.as_view(), name='prequest'),


]
