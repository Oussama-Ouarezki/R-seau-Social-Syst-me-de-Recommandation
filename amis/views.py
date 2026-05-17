from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Friendship
from django.db.models import Q

@login_required
def friend_list(request):
    """Affiche la liste des amis."""
    friends = Friendship.get_friends(request.user)
    return render(request, 'amis/friend_list.html', {'friends': friends})

@login_required
def send_request(request, username):
    """Envoie une demande d'amitié."""
    to_user = get_object_or_404(User, username=username)
    
    if request.user == to_user:
        messages.warning(request, "Vous ne pouvez pas vous envoyer une demande à vous-même.")
        return redirect('publications:feed')
        
    # Vérifier si amitié existe déjà
    if Friendship.are_friends(request.user, to_user):
        messages.info(request, "Vous êtes déjà amis.")
        return redirect('comptes:profile_detail', username=username)
        
    # Vérifier si demande en attente
    if Friendship.has_pending_request(request.user, to_user) or \
       Friendship.has_pending_request(to_user, request.user):
        messages.info(request, "Une demande est déjà en cours.")
        return redirect('comptes:profile_detail', username=username)
    
    # Créer demande
    Friendship.objects.create(from_user=request.user, to_user=to_user, status='pending')
    messages.success(request, f"Demande envoyée à {to_user.username}.")
    return redirect('comptes:profile_detail', username=username)

@login_required
def accept_request(request, pk):
    """Accepte une demande d'amitié reçue."""
    friendship = get_object_or_404(Friendship, pk=pk, to_user=request.user)
    friendship.accept()
    messages.success(request, f"Vous êtes maintenant ami avec {friendship.from_user.username} !")
    return redirect('amis:pending_requests')

@login_required
def reject_request(request, pk):
    """Refuse une demande d'amitié reçue."""
    friendship = get_object_or_404(Friendship, pk=pk, to_user=request.user)
    friendship.reject()
    messages.info(request, "Demande refusée.")
    return redirect('amis:pending_requests')

@login_required
def pending_requests(request):
    """Affiche les demandes d'amitié reçues."""
    requests = Friendship.objects.filter(to_user=request.user, status='pending')
    return render(request, 'amis/pending_requests.html', {'requests': requests})

@login_required
def remove_friend(request, username):
    """Supprime un ami."""
    friend = get_object_or_404(User, username=username)
    
    # Trouver la relation (dans un sens ou dans l'autre)
    Friendship.objects.filter(
        Q(from_user=request.user, to_user=friend) | 
        Q(from_user=friend, to_user=request.user)
    ).delete()
    
    messages.success(request, f"{friend.username} retiré de vos amis.")
    return redirect('amis:friend_list')
