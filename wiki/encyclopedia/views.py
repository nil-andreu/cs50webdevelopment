from random import randint #In order to make the random view

from django import forms #For the form of creating new users
from django.shortcuts import render

from . import util

#To be able to make the conversion to markdown
from markdown2 import Markdown
markdowner = Markdown()
#This conversion is a quick usage shown in the repository: https://github.com/trentm/python-markdown2

class Searcher(forms.Form):
    title = forms.CharField(label='', 
        widget=forms.TextInput(
            attrs={
                'placeholder':'Search for the title'
            }
        ))

class CreatePage(forms.Form):
    title = forms.CharField(label='Title',
        widget=forms.TextInput(
            attrs = {
                'placeholder':'Title of the Page'
            }
        ))

    content = forms.CharField(label='Content',
        widget=forms.Textarea(
            attrs = {
                'placeholder':'The content of the Page'
            }
        ))

class EditPage(forms.Form):
    title = forms.CharField()
    content = forms.CharField(label='Content',
    widget = forms.Textarea)

#And now we start the views (a list of them)
def index(request):
    titles = util.list_entries() #We use the util for listing the entries
    search = [] #For the elements searched

    if request.method == 'POST':
        form = Searcher(request.POST)

        #Now we are going to search for this value
        if form.is_valid():

            #We will obtain the value that is inside of the form
            query = form.cleaned_data["title"]

            #Going to do a for loop for all titles that entries has
            for title in titles: 

                #There is a match between what the user and a title
                if query.lower() == title.lower():

                    #We will obtain the page if there is a match between the entries and the queryset
                    page = util.get_entry(query)
                    page_md = markdowner.convert(page)

                    return render(request, "encyclopedia/post.html", {
                        'title':title, #We pass to the view the title and the page
                        'page': page_md,
                        'form':Searcher()
                    })

                #As if the queryset does not match excactly an entry, we will look for substrings
                if query.lower() in title.lower():
                    search.append(title) #We will append the title which matches a substring
                    return render(request, "encyclopedia/search.html", {
                        'search':search,

                        #In this page we also have the sidebar input that will need to display
                        "form": Searcher() 
                    })

        else:
            #If what is inside of the form is not valid, we return the page with the info
            return render(request, "encyclopedia/index.html",{
                'form':Searcher()
            })

    #If there is no post method (nothing is searched), i will render the index.html with the entries
    return render(request, "encyclopedia/index.html", {
        "titles": titles,
        'form':Searcher()
    })

#The view that will allow us to see a page in detail
def page(request, title):
    page = util.get_entry(title)

    #If there is a possible result
    if page:
        page_md = markdowner.convert(page)
        return render(request, "encyclopedia/post.html", {
            "page": page_md,
            'title': title,
            "form": Searcher()
        })

    else:
        return render(request, "encyclopedia/error.html", {
            'error': "Page not found"
        })

#The view that will allow us to edit the post
def edit(request, title):
    if request.method == 'POST':

        edit = EditPage(request.POST) 
        
        if edit.is_valid():
            title = edit.cleaned_data["title"]
            content = edit.cleaned_data["content"]
            util.save_entry(title, content)

            #And we will redirect to the new page
            page = util.get_entry(title)
            page_md = markdowner.convert(page)

            return render(request, "encyclopedia/post.html", {
                'title': title,
                'form': Searcher(),
                'page': page_md
            })

    else: 

        #We will get the page
        content = util.get_entry(title)

        #And will set the initial value of the form of the edit with the content
        edit = EditPage(initial={'title':title,'content':content})

        return render(request, "encyclopedia/edit.html", {
            'title':title,
            'form':Searcher(),
            'edit': edit
        })

        

#The view that will allow us to create a new page
def new(request):
    if request.method == 'POST':
        new_page = CreatePage(request.POST)

        if new_page.is_valid():
            title = new_page.cleaned_data["title"]
            content = new_page.cleaned_data["content"]

            #We will make sure that this does not exist
            if title in util.list_entries():
                return render(request, "encyclopedia/error.html", {
                    'error': 'Page already exist',
                    'form' : Searcher()
                })
            else:
                #If it is correct and does not exist, will redirect
                util.save_entry(title, content)

                page = util.get_entry(title)
                page_md = markdowner.convert(page)

                return render(request, "encyclopedia/post.html", {
                    'page': page,
                    'title': title,
                    'form': Searcher()
                })
    
    else: #If is not a post
        return render(request, "encyclopedia/create.html", {
            'form': Searcher(),
            'create': CreatePage()
        })

#Define the random page
def random(request):
    if request.method == 'GET':

        #First we will cratea a list with the possible numbers, and obtain the length
        pages = util.list_entries()
        length = len(pages)        

        #The random number integer in a range (from 0 to length-1 as it is indexed )
        rand = randint(0, length-1)

        #We will obtain the page that corresponds to that number 
        title = pages[rand]
        page = util.get_entry(title)
        page_md = markdowner.convert(page)
        return render(request, "encyclopedia/post.html", {
            'page':page_md,
            'title': title,
            'form': Searcher()
        })

