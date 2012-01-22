from django import forms
from django.db.models import Q

from archive.models import Post
class SearchForm(forms.Form):
    keyword = forms.CharField(required = True)
    def search(self):
        posts = Post.objects.all()
        keywords = self.cleaned_data['keyword'].split(' ')
        query = Q()
        for keyword in keywords:
            query |= Q(member__name__icontains = keyword)
            query |= Q(message__icontains = keyword)
            query |= Q(link__icontains = keyword)
            query |= Q(link_name__icontains = keyword)
            
        posts = posts.filter(query).order_by('-date_created')

        return posts
