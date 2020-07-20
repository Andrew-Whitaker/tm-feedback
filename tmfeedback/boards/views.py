
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator

from .models import Board, Topic, Post
from .forms import NewTopicForm, PostMessageForm


class BoardIndexView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boards/boards_index.html'


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-last_update').annotate(replies=Count('posts') - 1)
    return render(request, 'boards/topics.html', {'board': board, 'topics': topics})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.started_by = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', board_pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'boards/new_topic.html', {'board': board, 'form': form})


def topic_posts(request, board_pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=board_pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'boards/topic_posts.html', {'topic': topic})


@login_required
def reply_to_topic(request, board_pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=board_pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostMessageForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            topic.last_update = timezone.now()
            topic.save()
            return redirect('topic_posts', board_pk=board_pk, topic_pk=topic_pk)
    else:
        form = PostMessageForm()
    return render(request, 'boards/reply_to_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'boards/edit_post.html'
    pk_url_kwarg = 'post_pk'
    content_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        topic = post.topic
        topic.last_update = timezone.now()
        topic.save()
        return redirect('topic_posts', board_pk=post.topic.board.pk, topic_pk=post.topic.pk)

