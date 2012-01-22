from django.views.generic import TemplateView

from archive.models import Post
from search.forms import SearchForm

class MainView(TemplateView):
    template_name = 'home/main.html'
    def get_context_data(self, **kwargs):
        data = super(MainView, self).get_context_data(**kwargs)
        posts = Post.objects.filter(parent=None).order_by('-date_created')[:15]

        form = SearchForm(self.request.GET or None)
        if form.is_valid():
            posts = form.search()

        data['posts'] = posts
        data['form'] = form
        return data

