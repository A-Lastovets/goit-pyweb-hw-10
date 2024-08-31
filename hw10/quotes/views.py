from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Author, Quote
from django.contrib import messages
from datetime import datetime

def home(request):
    return render(request, 'home.html')


def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to='quotes:signup')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Зберігаємо нового користувача
            login(request, user)  # Автоматичний вхід нового користувача
            return redirect(to='quotes:add_author')
        else:
            return render(request, 'registration/signup.html', context={"form": form})

    return render(request, 'registration/signup.html', context={"form": RegisterForm()})


def loginuser(request):
    if request.user.is_authenticated:
        return redirect(to='quotes:base')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='registration:login')

        login(request, user)
        return redirect(to='quotes:add_author')

    return render(request, 'registration/login.html', context={"form": LoginForm()})

@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='quotes:home')

@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='quotes:profile')

    profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'registration/profile.html', {'profile_form': profile_form})

@login_required
def add_author(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        born_date = request.POST.get('born_date')
        born_location = request.POST.get('born_location')
        description = request.POST.get('description')

        # Перетворюємо born_date з формату YYYY-MM-DD у об'єкт Date
        try:
            born_date = datetime.strptime(born_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Incorrect date format. It should be YYYY-MM-DD.')
            return redirect('quotes:add_author')

        # Перевіряємо, чи існує вже такий автор
        if Author.objects.filter(fullname=fullname).exists():
            messages.error(request, 'Author with this fullname already exists.')
        else:
            try:
                Author.objects.create(fullname=fullname, born_date=born_date, born_location=born_location, description=description)
                messages.success(request, 'Author added successfully.')
            except Exception as e:
                messages.error(request, f'An error occurred while adding the author. Error details: {e}')
        
        return redirect('quotes:add_author')
    
    return render(request, 'quotes/add_author.html')

@login_required
def add_quote(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        author_id = request.POST.get('author')
        
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            messages.error(request, f'Author with ID {author_id} does not exist.')
            return redirect('quotes:add_quote')
        
        if Quote.objects.filter(text=text, author=author).exists():
            messages.error(request, 'This quote already exists.')
        else:
            Quote.objects.create(text=text, author=author)
            messages.success(request, 'Quote added successfully.')
        
        return redirect('quotes:add_quote')
    
    authors = Author.objects.all()
    return render(request, 'quotes/add_quote.html', {'authors': authors})


def author_list(request):
    authors = Author.objects.all()
    return render(request, 'quotes/author_list.html', {'authors': authors})

def quote_list(request):
    quotes = Quote.objects.all()
    return render(request, 'quotes/quote_list.html', {'quotes': quotes})

def author_page(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    return render(request, 'quotes/author_page.html', {'author': author})

def author_quotes(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    quotes = Quote.objects.filter(author=author).order_by('text')  # Сортування за текстом цитати
    return render(request, 'quotes/author_quotes.html', {'author': author, 'quotes': quotes})