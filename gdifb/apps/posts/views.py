from django.views.generic import DetailView, TemplateView

from archive.models import Post
from search.forms import SearchForm

class PostListView(TemplateView):
    template_name = 'posts/list.html'
    def get_context_data(self, **kwargs):
        data = super(PostListView, self).get_context_data(**kwargs)
        posts = Post.objects.filter(parent=None).order_by('-date_created')

        form = SearchForm(self.request.GET or None)
        if form.is_valid():
            posts = form.search()

        offset = int(self.request.GET.get('offset',0))

        data['posts'] = posts[offset:offset+15]
        return data
    
class PostDetailView(DetailView):
    context_object_name = 'post'
    model = Post
    template_name = 'posts/detail.html'
