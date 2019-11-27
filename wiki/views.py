from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from wiki.models import Page
from wiki.forms import PageForm


class PageListView(ListView):
    """ Renders a list of all Pages. """
    model = Page

    def get(self, request):
        """ GET a list of Pages. """
        pages = self.get_queryset().all()
        return render(request, 'list.html', {
          'pages': pages
        })

class PageDetailView(DetailView):
    """ Renders a specific page based on it's slug."""
    model = Page

    def get(self, request, slug):
        """ Returns a specific wiki page by slug. """
        page = self.get_queryset().get(slug__iexact=slug)
        return render(request, 'page.html', {
          'page': page
        })

class PageCreateView(FormView):
    """ Renders a form page to create a new page."""
    template_name = 'create_page.html'
    form_class = PageForm
    success_url = '/'

    def post(self, request):
        page_form = PageForm(request.POST)
        if page_form .is_valid():
            page = page_form.save(commit=False)
            page.author = User.objects.get(id=request.POST['author'])
            page.save()
            return HttpResponseRedirect(reverse_lazy('wiki-create-page'))
        else:
            return render(request, self.template_name, {'form': page_form})


    def form_vaild(self, form):
        return super().form_valid(form)
