from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category, Page

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
