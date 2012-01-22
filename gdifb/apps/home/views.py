from django.views.generic import TemplateView

from archive.models import Post

class MainView(TemplateView):
    template_name = 'home/main.html'
    def get_context_data(self, **kwargs):
        data = super(MainView, self).get_context_data(**kwargs)
        data['posts'] = Post.objects.filter(parent=None).order_by('-date_updated')[:5]

        data['thread_count'] = Post.objects.filter(parent=None).count()
        data['comment_count'] = Post.objects.exclude(parent=None).count()

        return data

