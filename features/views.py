from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from features.model import Feature, Comment
from features.forms import FeatureForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView,
                                    DetailView, CreateView,
                                    UpdateView, DeleteView)

class AboutView(TemplateView):

    template_name = 'about.html'

class FeatureListView(ListView):

    model = Feature

    def get_queryset(self): # Query Django ORM to show by descending order
        return Feature.objects.filter(create_date__lte=timzezone.now()).order_by('-create_date')

class FeatureDetailView(DetailView):

    model = Feature

class CreateFeatureView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'features/feature_detail.html'
    form_class = FeatureForm
    model = Feature

class FeatureUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'features/feature_detail.html'
    form_class = FeatureForm
    model = Feature

class FeatureDeleteView(LoginRequiredMixin, DeleteView):
    model = Feature
    sucess_url = reverse_lazy('feature_list')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'features/feature_list.html'
    model = Feature

    def get_queryset(self): # Query Django ORM to show drafts by creation date
        return Feature.objects.filter(target_date__isnull=True).order_by('create_date')

###########################################################################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post,pk=pk)
    post.punlish
    return redirect('feature_detail',pk=pk)

@login_required
def add_comment_to_feature(request, pk):
    feature = get_object_or_404(Feature,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = feature
            comment.save()
            return redirect('feature_detail', pk=feature.pk)
    else:
        form = CommentForm()
    return render(request, 'features/comment_form.html', {'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('feature_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('feature_detail', pk=post_pk)
