from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Post, Like
from .forms import PostForm, CommentForm
from amis.models import Friendship

@login_required
def feed(request):
    """
    Fil d'actualité : affiche les posts de l'utilisateur et de ses amis.
    """
    # Récupérer les amis
    friends = Friendship.get_friends(request.user)
    
    # Créer une liste d'auteurs (amis + soi-même)
    authors = list(friends)
    authors.append(request.user)
    
    # Récupérer les posts
    posts = Post.objects.filter(author__in=authors).order_by('-created_at')
    
    # Formulaire pour nouveau post
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m() # Sauvegarder les relations ManyToMany (interests)
            messages.success(request, 'Votre post a été publié !')
            return redirect('publications:feed')
    else:
        form = PostForm()
        
    # Posts likés par l'utilisateur (pour l'affichage)
    liked_post_ids = set(request.user.likes.values_list('post_id', flat=True))

    context = {
        'posts': posts,
        'form': form,
        'liked_post_ids': liked_post_ids
    }
    return render(request, 'publications/feed.html', context)

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('publications:post_detail', pk=pk)
    else:
        comment_form = CommentForm()
        
    context = {
        'post': post,
        'comment_form': comment_form
    }
    return render(request, 'publications/post_detail.html', context)

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        # Si le like existait déjà, on le supprime (unlike)
        like.delete()
        liked = False
    else:
        liked = True
        
    # Retourner JSON pour AJAX ou rediriger
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked, 
            'count': post.get_likes_count()
        })
    
    return redirect(request.META.get('HTTP_REFERER', 'publications:feed'))

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        post.delete()
        messages.success(request, 'Post supprimé.')
    return redirect('publications:feed')

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Commentaire ajouté !')
    return redirect(request.META.get('HTTP_REFERER', 'publications:feed'))
