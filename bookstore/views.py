import datetime
import itertools
import operator
from datetime import timedelta

from bootstrap_modal_forms.mixins import PassRequestMixin
from django.contrib import auth, messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path, reverse, reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,UpdateView)

from . import models
from .forms import BookForm, BookForm1, UserForm
from .models import Book, DeleteRequest, Feedback, User
# Shared Views
def login_form(request):
	return render(request, 'bookstore/login.html')


def logoutView(request):
	logout(request)
	return redirect('home')


def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('dashboard')
            elif user.is_librarian:
                return redirect('librarian')
            else :
                return redirect('publisher')
            
        else:
            messages.info(request, "Invalid username or password")
            return redirect('home')

def register_form(request):
    return render(request, 'bookstore/register.html')

def registerView(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password = make_password(password)

        a = User(username=username, email=email, password=password)
        a.save()
        messages.success(request, 'Account was created successfully')
        return redirect('home')
    else:
        messages.error(request, 'Registration fail, try again later')
        return redirect('regform')




















			


# Publisher views
@login_required
def publisher(request):
	return render(request, 'publisher/home.html')


@login_required
def uabook_form(request):
    choice = ['1', '0', '1', '1', '1']
    choice = {'choice': choice}
    return render(request, 'publisher/add_book.html')


@login_required
def request_form(request):
	return render(request, 'publisher/delete_request.html')


@login_required
def feedback_form(request):
	return render(request, 'publisher/send_feedback.html')

@login_required
def about(request):
	return render(request, 'publisher/about.html')	


@login_required
def usearch(request):
    query = request.GET['query']
    print(type(query))


    #data = query.split()
    data = query
    print(len(data))
    if( len(data) == 0):
        return redirect('publisher')
    else:
                a = data

                # Searching for It
                qs5 =models.Book.objects.filter(id__iexact=a).distinct()
                qs6 =models.Book.objects.filter(id__exact=a).distinct()

                qs7 =models.Book.objects.all().filter(id__contains=a)
                qs8 =models.Book.objects.select_related().filter(id__contains=a).distinct()
                qs9 =models.Book.objects.filter(id__startswith=a).distinct()
                qs10 =models.Book.objects.filter(id__endswith=a).distinct()
                qs11 =models.Book.objects.filter(id__istartswith=a).distinct()
                qs12 =models.Book.objects.all().filter(id__icontains=a)
                qs13 =models.Book.objects.filter(id__iendswith=a).distinct()




                files = itertools.chain(qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13)

                res = []
                for i in files:
                    if i not in res:
                        res.append(i)


                # word variable will be shown in html when user click on search button
                word="Searched Result :"
                print("Result")

                print(res)
                files = res




                page = request.GET.get('page', 1)
                paginator = Paginator(files, 10)
                try:
                    files = paginator.page(page)
                except PageNotAnInteger:
                    files = paginator.page(1)
                except EmptyPage:
                    files = paginator.page(paginator.num_pages)
   


                if files:
                    return render(request,'publisher/result.html',{'files':files,'word':word})
                return render(request,'publisher/result.html',{'files':files,'word':word})



@login_required
def delete_request(request):
    if request.method == 'POST':
        book_id = request.POST['delete_request']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username
        user_request = username + "  want book with id  " + book_id + " to be deleted"

        a = DeleteRequest(delete_request=user_request)
        a.save()
        messages.success(request, 'Request was sent')
        return redirect('request_form')
    else:
        messages.error(request, 'Request was not sent')
        return redirect('request_form')



@login_required
def send_feedback(request):
    if request.method == 'POST':
        feedback_text = request.POST['feedback']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username
        feedback = f"{username} says {feedback_text}"

        a = Feedback(feedback=feedback)
        a.save()
        messages.success(request, 'Feedback was sent')
        return redirect('feedback_form')
    else:
        messages.error(request, 'Feedback was not sent')
        return redirect('feedback_form')






















class UBookListView(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'publisher/book_list.html'
	context_object_name = 'books'
	paginate_by = 20

	def get_queryset(self):
		return Book.objects.order_by('-id')

import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Book
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Book


def calculate(request, pk):
    book = get_object_or_404(Book, id=pk)
    
    desc = int(book.desc)
    Nands = int(book.Nands)
    author = int(book.author)
    year = int(book.year)
    publisher = int(book.publisher)
    produit2 = (year + author + desc) - Nands
    produit3 = produit2-publisher
    book.UAP=produit3
    book.produit = produit2
    book.save()
    return redirect('publisher')

        
@login_required

def uabook(request):
    choice = ['1', '0', '1', '2']
    context = {'choice': choice}
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day

    # Format day and month to two digits
    if len(str(day)) == 1:
        day = "0" + str(day)
    if len(str(month)) == 1:
        month = "0" + str(month)

    today = f"{year}-{month}-{day}"
    time = str(now.hour) + ":" + str(now.minute)

    if request.method == 'POST':
        title = request.POST.get('title')
        year = int(request.POST.get('year', 0))
        publisher = request.POST.get('publisher')
        author = int(request.POST.get('author', 0))
        desc = int(request.POST.get('desc',0))
        Nands = int(request.POST.get('Nands', 0)) 
        book = Book(
            title=title,
            year=year,
            date=today,
            time=time,
            publisher=publisher,
            author=author,
            desc=desc,
            Nands=Nands,
        )
        book.save()
        messages.success(request, 'Product was uploaded successfully')
        return redirect('publisher')

    return render(request, 'your_template.html', context)


        


class detailc(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'dashboard/detailc.html'
	context_object_name = 'books'
	paginate_by = 20

	def get_queryset(self):
		return Book.objects.order_by('-id')
def detail1(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        type = request.POST.get('type')
        fiche = request.POST.get('fiche')
        implutation = request.POST.get('implutation')
        book.type = type
        book.fiche = fiche
        book.implutation = implutation
        book.save()

        messages.error(request, 'Request Marked as Non conforme')
        return redirect('CF') 
    else:
        context = {'book': book}
        return render(request, 'detail.html', context)
        return redirect('detail', pk=pk)  























# Librarian views
def librarian(request):
	book = Book.objects.all().count()
	user = User.objects.all().count()

	context = {'book':book, 'user':user}

	return render(request, 'librarian/home.html', context)


@login_required
def labook_form(request):
	return render(request, 'librarian/add_book.html')


@login_required
def labook(request):
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    if len(str(day)) == 1:
        day = "0" + str(day)
    if len(str(month)) == 1:
        month = "0" + str(month)
    
    today = str(year) + "/" + str(month) + str(day)
    time = str(now.hour) + ":" + str(now.minute)
    
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        year = request.POST['year']
        publisher = request.POST['publisher']
        desc = request.POST['desc']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username

        a = Book(title=title, author=author, year=year, publisher=publisher,date=today, time=time, uploaded_by=username, user_id=user_id)
        a.save()
        messages.success(request, 'Book was uploaded successfully')
        return redirect('llbook')
    else:
        messages.error(request, 'Book was not uploaded successfully')
        return redirect('llbook')


class LBookListView(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'librarian/book_list.html'
	context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		return Book.objects.order_by('-id')


class LManageBook(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'librarian/manage_books.html'
	context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		return Book.objects.order_by('-id')


class LDeleteRequest(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'librarian/controleF.html'
	context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		return Book.objects.order_by('-id')


class LViewBook(LoginRequiredMixin,DetailView):
	model = Book
	template_name = 'librarian/book_detail.html'

	
class LEditView(LoginRequiredMixin,UpdateView):
	model = Book
	form_class = BookForm
	template_name = 'librarian/edit_book.html'
	success_url = reverse_lazy('lmbook')
	success_message = 'Data was updated successfully'
class LDeleteView(LoginRequiredMixin,DeleteView):
	model = Book
	template_name = 'librarian/confirm_delete.html'
	success_url = reverse_lazy('lmbook')
	success_message = 'Data was deleted successfully'



class LDeleteBook(LoginRequiredMixin,DeleteView):
	model = Book
	template_name = 'librarian/confirm_delete2.html'
	success_url = reverse_lazy('librarian')
	success_message = 'Data was deleted successfully'
 
class control(LoginRequiredMixin,DetailView):
	model = Book
	template_name = 'librarian/controle.html'
class confrome(LoginRequiredMixin,DetailView):
	model = Book
	template_name = 'librarian/conforme.html'
 
class detail(LoginRequiredMixin,DetailView):
	model = Book
	template_name = 'librarian/detail.html'

def conforme1(request, pk):
    choice = ['1', '0', 'Non conforme', 'conforme']
    book = get_object_or_404(Book, pk=pk)
    context1 = {'choice': choice, 'book': book}
    
    if request.method == 'POST':
        conforme = request.POST.get('conforme')
        print("conforme value:", conforme)
        
        if conforme == 'Non conforme':
            book.save()
            return redirect('detail', pk=pk)  
        elif conforme == 'conforme':
            book.save()
            messages.success(request, 'Request marked as conforme')
            return redirect('CF') 
        else:
            return render(request, 'librarian/detail.html', context1)
    
    return render(request, 'librarian/detail.html', context1)

@login_required
def Update(request, pk):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=pk)
        now = datetime.datetime.now()
        time1 = str(now.hour) + ":" + str(now.minute)
        time1_obj = datetime.datetime.strptime(time1, "%H:%M")
        time2_obj = datetime.datetime.strptime(book.time2, "%H:%M")
        time_diff = time1_obj - time2_obj
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_difference = f"{hours}:{minutes}"
        book.status = True
        book.time1 = time1
        book.time_difference = time_difference
        book.save()
    return redirect('conforme', pk=pk)
    
@login_required
def lsearch(request):
    query = request.GET['query']
    print(type(query))


    #data = query.split()
    data = query
    print(len(data))
    if( len(data) == 0):
        return redirect('publisher')
    else:
                a = data

                # Searching for It
                qs5 =models.Book.objects.filter(id__iexact=a).distinct()
                qs6 =models.Book.objects.filter(id__exact=a).distinct()

                qs7 =models.Book.objects.all().filter(id__contains=a)
                qs8 =models.Book.objects.select_related().filter(id__contains=a).distinct()
                qs9 =models.Book.objects.filter(id__startswith=a).distinct()
                qs10 =models.Book.objects.filter(id__endswith=a).distinct()
                qs11 =models.Book.objects.filter(id__istartswith=a).distinct()
                qs12 =models.Book.objects.all().filter(id__icontains=a)
                qs13 =models.Book.objects.filter(id__iendswith=a).distinct()




                files = itertools.chain(qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13)

                res = []
                for i in files:
                    if i not in res:
                        res.append(i)


                # word variable will be shown in html when user click on search button
                word="Searched Result :"
                print("Result")

                print(res)
                files = res
                page = request.GET.get('page', 1)
                paginator = Paginator(files, 10)
                try:
                    files = paginator.page(page)
                except PageNotAnInteger:
                    files = paginator.page(1)
                except EmptyPage:
                    files = paginator.page(paginator.num_pages)

                if files:
                    return render(request,'librarian/result.html',{'files':files,'word':word})
                return render(request,'librarian/result.html',{'files':files,'word':word})


















# Admin views

def dashboard(request):
    book = Book.objects.all().count()
    user = User.objects.all().count()
    context = {
        'book': book,
        'user': user,
    }
    
    return render(request, 'dashboard/home.html',context)


def create_user_form(request):
    choice = ['1', '0', 'Publisher', 'Admin', 'Librarian','consulter']
    choice = {'choice': choice}

    return render(request, 'dashboard/add_user.html', choice)


class ADeleteUser(SuccessMessageMixin, DeleteView):
    model = User
    template_name='dashboard/confirm_delete3.html'
    success_url = reverse_lazy('aluser')
    success_message = "Data successfully deleted"
    

class AEditUser(SuccessMessageMixin, UpdateView): 
    model = User
    form_class = UserForm
    template_name = 'dashboard/edit_user.html'
    success_url = reverse_lazy('aluser')
    success_message = "Data successfully updated"

class ListUserView(generic.ListView):
    model = User
    template_name = 'dashboard/list_users.html'
    context_object_name = 'users'
    paginate_by = 4

    def get_queryset(self):
        return User.objects.order_by('-id')

def create_user(request):
    choice = ['1', '0', 'Publisher', 'Admin', 'Librarian']
    choice = {'choice': choice}
    if request.method == 'POST':
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            username=request.POST['username']
            userType=request.POST['userType']
            email=request.POST['email']
            password=request.POST['password']
            password = make_password(password)
            print("User Type")
            print(userType)
            if userType == "Publisher":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_publisher=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('aluser')
            elif userType == "Admin":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_admin=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('aluser')
            elif userType == "Librarian":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_librarian=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('aluser')    
            else:
                messages.success(request, 'Member was not created')
                return redirect('create_user_form')
    else:
        return redirect('create_user_form')


class ALViewUser(DetailView):
    model = User
    template_name='dashboard/user_detail.html'



@login_required
def aabook_form(request):
	return render(request, 'dashboard/add_book.html')
@login_required
def aabook(request):
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    if len(str(day)) == 1:
        day = "0" + str(day)
    if len(str(month)) == 1:
        month = "0" + str(month)

    today = str(year) + "/" + str(month) + str(day)
    time = str(now.hour) + ":" + str(now.minute)
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        year = request.POST['year']
        publisher = request.POST['publisher']
        desc = request.POST['desc']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username

        a = Book(title=title, author=author, year=year, publisher=publisher,desc=desc, date=today, time=time, uploaded_by=username, user_id=user_id)
        a.save()
        messages.success(request, 'Book was uploaded successfully')
        return redirect('albook')
    else:
        messages.error(request, 'Book was not uploaded successfully')
        return redirect('aabook_form')


class ABookListView(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'dashboard/book_list.html'
	context_object_name = 'books'
	paginate_by = 20

	def get_queryset(self):
		return Book.objects.order_by('-id')



class AManageBook(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'dashboard/manage_books.html'
	context_object_name = 'books'
	paginate_by = 20

	def get_queryset(self):
		return Book.objects.order_by('-id')


class pDeleteBook(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Book
    template_name = 'publisher/confirm_delete.html'
    success_url = reverse_lazy('publisher')
    success_message = 'product was  deleted successfully'  
    


class ADeleteBook(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Book
    template_name = 'dashboard/confirm_delete2.html'
    success_url = reverse_lazy('ambook')
    success_message = 'Request was  deleted successfully'  
    
    

class ADeleteBookk(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard')
    success_message = 'Data was deleted successfully'

    
class AViewBook(LoginRequiredMixin,DetailView):
	model = Book
	template_name = 'dashboard/book_detail.html'



class charts(LoginRequiredMixin,DetailView):
	model = Book
	template_name = 'dashboard/html/charts.html'






class AEditView(LoginRequiredMixin,UpdateView):
	model = Book
	form_class = BookForm
	template_name = 'dashboard/edit_book.html'
	success_url = reverse_lazy('ambook')
	success_message = 'Data was updated successfully'

class AEditrequest(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Book
    form_class = BookForm1
    template_name = 'dashboard/edit_request.html'
    success_message = 'Data was updated successfully'

    def get_success_url(self):
        return reverse('detailc', kwargs={'pk': self.object.pk})

class PEditrequest(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Book
    form_class = BookForm1
    template_name = 'publisher/edit_product.html'
    success_message = 'Data was updated successfully'

    def get_success_url(self):
        return reverse('detailp', kwargs={'pk': self.object.pk})




class ADeleteRequest(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'dashboard/detailc.html'
	context_object_name = 'books'
	paginate_by = 20

	def get_queryset(self):
		return Book.objects.order_by('-id')


class AFeedback(LoginRequiredMixin, ListView):
    model = Feedback
    template_name = 'dashboard/charts.html'
    context_object_name = 'feedbacks'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = Book.objects.all()
        cs_no = Book.objects.filter(urgent='zeineb').count()
        cs_no = int(cs_no)
        print('Number of reservoir Are',cs_no)


        ce_no = Book.objects.filter(urgent='mouna').count()
        ce_no = int(ce_no)
        print('Number of contact Are',ce_no)
        
        ce = Book.objects.filter(urgent='mohamed').count()
        ce = int(ce)
        print('Number of contact Are',ce_no)
        
        cr = Book.objects.filter(urgent='Salim').count()
        cr = int(cr)
        print('Number of contact Are',ce_no)
        
        course_list = ['zeineb', 'mouna','mohamed' ,'Salim']
        number_list = [cs_no, ce_no, ce , cr]
        context = {'course_list':course_list,'number_list':number_list }
        return  context
    
class control1(LoginRequiredMixin,DetailView):
	model = Book
	template_name = 'dashboard/urgent.html'


def controll1(request, pk):
    choice = ['1','0','urgent', 'Normal']
    context1 = {'choice': choice}
    if request.method == 'POST':
        controle = request.POST.get('controle')
        print("controle value:", controle)
        if controle == 'urgent':
            book = get_object_or_404(Book, pk=pk) 
            book.is_admin=True
            book.save()
            return redirect('ambook')
        elif controle == 'Normal':
            book = get_object_or_404(Book, pk=pk) 
            book.is_admin=False
            book.save()
            return redirect('ambook')
        else:
            return render(request, 'dashboard/urgent.html', context1)
    else:
        return render(request, 'dashboard/urgent.html', context1)

        
def controll(request,pk):
    now = datetime.datetime.now()
    time2 = str(now.hour) + ":" + str(now.minute)

    if request.method == 'POST':
        book = get_object_or_404(Book, pk=pk)
        urgent = request.POST.get('urgent')
        book.urgent = urgent
        book.time2 = time2
        book.save()
        return redirect('lmbook')
    else:
        return redirect('cnbook')
    
class control(LoginRequiredMixin,DetailView):
    model = Book
    template_name = 'librarian/controle.html'

def asearch(request):
    query = request.GET['query']
    print(type(query))
    #data = query.split()
    data = query
    print(len(data))
    if( len(data) == 0):
        return redirect('dashborad')
    else:
                a = data

                # Searching for It
                qs5 =models.Book.objects.filter(id__iexact=a).distinct()
                qs6 =models.Book.objects.filter(id__exact=a).distinct()

                qs7 =models.Book.objects.all().filter(id__contains=a)
                qs8 =models.Book.objects.select_related().filter(id__contains=a).distinct()
                qs9 =models.Book.objects.filter(id__startswith=a).distinct()
                qs10 =models.Book.objects.filter(id__endswith=a).distinct()
                qs11 =models.Book.objects.filter(id__istartswith=a).distinct()
                qs12 =models.Book.objects.all().filter(id__icontains=a)
                qs13 =models.Book.objects.filter(id__iendswith=a).distinct()




                files = itertools.chain(qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13)

                res = []
                for i in files:
                    if i not in res:
                        res.append(i)


                # word variable will be shown in html when user click on search button
                word="Searched Result :"
                print("Result")

                print(res)
                files = res




                page = request.GET.get('page', 1)
                paginator = Paginator(files, 10)
                try:
                    files = paginator.page(page)
                except PageNotAnInteger:
                    files = paginator.page(1)
                except EmptyPage:
                    files = paginator.page(paginator.num_pages)


                if files:
                    return render(request,'dashboard/result.html',{'files':files,'word':word})
                return render(request,'dashboard/result.html',{'files':files,'word':word})
            #controle final
            
class CFListView(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'librarian/controleF.html'
	context_object_name = 'books'
	paginate_by = 20
	def get_queryset(self):
		return Book.objects.order_by('-id')
            
@login_required
def cfbook_form(request):
    return render(request, 'librarian/cfo.html')
@login_required
def cfbook(request):
    choice = ['1', '0', '1', '2']
    context = {'choice': choice}
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day

    if len(str(day)) == 1:
        day = "0" + str(day)
    if len(str(month)) == 1:
        month = "0" + str(month)

    today = f"{year}-{month}-{day}"
    time2 = f"{now.hour}:{now.minute}"

    if request.method == 'POST':
        title = request.POST.get('title')
        year = request.POST.get('year')
        publisher = request.POST.get('publisher')
        author = request.POST.get('author')
        desc = request.POST.get('desc')
        Nands = request.POST.get('Nands')
        UAP = request.POST.get('UAP')
        urgent = request.POST.get('urgent')
        controle = request.POST.get('controle')
        produit=request.POST.get('produit')
        print("controle value:", controle)

        if controle == 'urgent':
            is_admin = True
        elif controle == 'Normal':
            is_admin = False
        else:
            messages.error(request, 'Invalid control value')
            return redirect('cfbook_form')

        if publisher == "1":
            book = Book(
                title=title,
                year=year,
                date=today,
                time2=time2,
                is_publisher=True,
                author=author,
                desc=desc,
                Nands=Nands,
                UAP=UAP,
                urgent=urgent,
                is_admin=is_admin,
                produit=produit
            )
            book.save()
            messages.success(request, 'Book was uploaded successfully')
            return redirect('CF')
        elif publisher == "2":
            book = Book(
                title=title,
                year=year,
                date=today,
                time2=time2,
                is_publisher=False,
                author=author,
                desc=desc,
                Nands=Nands,
                UAP=UAP,
                urgent=urgent,
                is_admin=is_admin,
                produit=produit
            )
            book.save()
            messages.success(request, 'Book was uploaded successfully')
            return redirect('CF')
        else:
            messages.error(request, 'Invalid publisher information')
            return redirect('cfbook_form')
    else:
        return render(request, 'cfo.html', context)
class detailp(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'publisher/book_list.html'
	context_object_name = 'books'
	paginate_by = 20

