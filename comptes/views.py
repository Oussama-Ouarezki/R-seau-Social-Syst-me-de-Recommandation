from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in immediately after registration
            messages.success(request, f'Compte créé pour {user.username}!')
            return redirect('publications:feed')
    else:
        form = UserRegisterForm()
    return render(request, 'comptes/register.html', {'form': form})

@login_required
def profile_view(request, username=None):
    if username:
        user_p = get_object_or_404(User, username=username)
    else:
        user_p = request.user
    
    # Check friendship status if viewing another profile
    is_friend = False
    pending_request = False
    if request.user != user_p:
        from amis.models import Friendship
        is_friend = Friendship.are_friends(request.user, user_p)
        pending_request = Friendship.has_pending_request(request.user, user_p)

    # Calculate friends count
    from amis.models import Friendship
    friends_count = Friendship.get_friends(user_p).count()

    common_friends_count = 0
    if request.user != user_p:
        user_friends = set(Friendship.get_friends(request.user))
        profile_friends = set(Friendship.get_friends(user_p))
        common_friends_count = len(user_friends.intersection(profile_friends))

    context = {
        'profile_user': user_p,
        'profile': user_p.profile,
        'is_friend': is_friend,
        'pending_request': pending_request,
        'friends_count': friends_count,
        'common_friends_count': common_friends_count,
    }
    return render(request, 'comptes/profile.html', context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Votre compte a été mis à jour!')
            return redirect('comptes:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'comptes/profile_edit.html', context)
