from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

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
