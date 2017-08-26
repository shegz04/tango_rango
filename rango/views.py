from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]

    page_list = Page.objects.order_by('-views')[:5]
    #page_list.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages':page_list}
    return render(request, 'rango/index.html', context_dict)


def about(request):
    context_dict = {'name': "Segun"}
    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        # Find the supplied category name slug. the get method raises an exception if not found
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all associated pages
        pages = Page.objects.filter(category=category)

        # Add results list to the template context under name pages
        context_dict['pages'] = pages

        context_dict['category'] = category

    except Category.DoesNotExist:
        # Do nothing
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    # If it is a http post
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # Save the new category to the database
            form.save(commit=True)
            # Send the user back to the index page which will display the newly added category
            return index(request)
        else:
            # If the supplied form contains errors, print them to the terminal
            print(form.errors)

    # Otherwise for everything else, including form not found, render the form again
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)



def register(request):
    # If registration succeeds set registered value to True. Initial value is False
    # This way the template knows that registration was successful

    registered = False

    # Because this is a form data
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid:
            # Save the user's form to the database
            user = user_form.save()
            # Hash the password and update the user object
            user.set_password(user.password)
            user.save()

            # Delay saving the userprofile instance untill finally ready to avoid integrity problems
            # Because most users add their details such as pictures after signing up
            profile = profile_form.save(commit=False)
            profile.user = user

            # Check if user provided picture, if yes put in UserProfile model instance
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now save the UserProfile model instance
            profile.save()

            # Update registered to True to indicate that the template registration succeeded
            registered = True
        else:
            # Invalid form or forms. Print problem to the terminal
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST. So render forms agin using two model form instances
        # They will be blank and ready for user input
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context
    return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use django to see if username and password match
        user = authenticate(username=username, password=password)

        # If authenticated the user object is returend
        if user:
            # Check if the account is valid and active
            # If true, log them in and send them to the homepage
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used
                return HttpResponse("Your Rango account is disabled")
        else:
            # An inactive account was used
            print("invalid login details: {0}, {1}".format(username, password))
            HttpResponse("Invalid login details supplied")

    # If the request is not a HTTP POST display form again
    else:
        # There's nothing to return
        return  render(request, 'rango/login.html', {})


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('index'))
