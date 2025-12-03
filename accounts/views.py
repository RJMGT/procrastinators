from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Sum, Q
from django.utils import timezone
from .models import Post, Like, Dislike, ABTestPageView, ABTestButtonClick
import random


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


def signup_view(request):
    """Handle user signup with email, username, and password."""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validation
        errors = []
        
        if not username:
            errors.append('Username is required.')
        elif User.objects.filter(username=username).exists():
            errors.append('Username already exists.')
        
        if not email:
            errors.append('Email is required.')
        elif User.objects.filter(email=email).exists():
            errors.append('Email already exists.')
        
        if not password:
            errors.append('Password is required.')
        elif len(password) < 8:
            errors.append('Password must be at least 8 characters long.')
        
        if password != password_confirm:
            errors.append('Passwords do not match.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, 'Account created successfully! Please sign in.')
            return redirect('login')
    
    return render(request, 'accounts/signup.html')


@login_required
def home_view(request):
    """Home page feed showing all posts."""
    posts = Post.objects.all().annotate(
        like_count=Count('likes'),
        dislike_count=Count('dislikes')
    ).order_by('-created_at')
    
    # Get which posts the current user has liked/disliked
    user_liked_posts = set(
        Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    )
    user_disliked_posts = set(
        Dislike.objects.filter(user=request.user).values_list('post_id', flat=True)
    )
    
    context = {
        'posts': posts,
        'user_liked_posts': user_liked_posts,
        'user_disliked_posts': user_disliked_posts,
        'active_tab': 'home',
    }
    return render(request, 'accounts/home.html', context)


@login_required
def create_post_view(request):
    """Create a new post."""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        hours_procrastinated = request.POST.get('hours_procrastinated')
        
        # Validation
        errors = []
        
        if not title:
            errors.append('Title is required.')
        
        if not description:
            errors.append('Description is required.')
        
        if not hours_procrastinated:
            errors.append('Hours procrastinated is required.')
        else:
            try:
                hours = float(hours_procrastinated)
                if hours < 0:
                    errors.append('Hours procrastinated must be a positive number.')
            except ValueError:
                errors.append('Hours procrastinated must be a valid number.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            post = Post.objects.create(
                title=title,
                description=description,
                hours_procrastinated=hours_procrastinated,
                author=request.user
            )
            messages.success(request, 'Post created successfully!')
            return redirect('home')
    
    context = {
        'active_tab': 'create',
    }
    return render(request, 'accounts/create_post.html', context)


@login_required
def leaderboard_view(request):
    """Leaderboard showing posts with filtering options."""
    sort_by = request.GET.get('sort', 'likes')  # Default: sort by likes
    
    posts = Post.objects.annotate(
        like_count=Count('likes'),
        dislike_count=Count('dislikes')
    )
    
    if sort_by == 'time':
        posts = posts.order_by('-created_at')
    elif sort_by == 'dislikes':
        posts = posts.order_by('-dislike_count', '-created_at')
    else:  # Default: sort by likes
        posts = posts.order_by('-like_count', '-created_at')
    
    context = {
        'posts': posts,
        'active_tab': 'leaderboard',
        'current_sort': sort_by,
    }
    return render(request, 'accounts/leaderboard.html', context)


@login_required
def user_leaderboard_view(request):
    """Leaderboard showing users ranked by total hours procrastinated."""
    users = User.objects.annotate(
        total_hours=Sum('posts__hours_procrastinated')
    ).filter(total_hours__isnull=False).order_by('-total_hours')
    
    context = {
        'users': users,
        'active_tab': 'user_leaderboard',
    }
    return render(request, 'accounts/user_leaderboard.html', context)


@login_required
def like_post_view(request, post_id):
    """Like or unlike a post. Ensures mutual exclusivity with dislikes."""
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        
        # CRITICAL: Remove any existing dislike first to ensure mutual exclusivity
        # If user had disliked this post, remove the dislike before toggling like
        Dislike.objects.filter(user=request.user, post=post).delete()
        
        # Toggle like: create if doesn't exist, delete if it exists
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            # Unlike: delete the like (user clicked like on an already liked post)
            like.delete()
            liked = False
        else:
            # Like: created a new like
            liked = True
        
        # Get updated counts
        like_count = post.get_like_count()
        dislike_count = post.get_dislike_count()
        
        return JsonResponse({
            'liked': liked,
            'disliked': False,  # Always False since we removed any dislike above
            'like_count': like_count,
            'dislike_count': dislike_count
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def dislike_post_view(request, post_id):
    """Dislike or undislike a post. Ensures mutual exclusivity with likes."""
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        
        # CRITICAL: Remove any existing like first to ensure mutual exclusivity
        # If user had liked this post, remove the like before toggling dislike
        Like.objects.filter(user=request.user, post=post).delete()
        
        # Toggle dislike: create if doesn't exist, delete if it exists
        dislike, created = Dislike.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            # Undislike: delete the dislike (user clicked dislike on an already disliked post)
            dislike.delete()
            disliked = False
        else:
            # Dislike: created a new dislike
            disliked = True
        
        # Get updated counts
        like_count = post.get_like_count()
        dislike_count = post.get_dislike_count()
        
        return JsonResponse({
            'disliked': disliked,
            'liked': False,  # Always False since we removed any like above
            'like_count': like_count,
            'dislike_count': dislike_count
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def check_new_posts_view(request):
    """API endpoint to check for new posts since a given timestamp."""
    if request.method == 'GET':
        since = request.GET.get('since')
        
        if since:
            try:
                # Parse ISO format timestamp
                from datetime import datetime
                since_str = since.replace('Z', '+00:00')
                since_datetime = datetime.fromisoformat(since_str)
                if timezone.is_naive(since_datetime):
                    since_datetime = timezone.make_aware(since_datetime)
                posts = Post.objects.filter(created_at__gt=since_datetime).annotate(
                    like_count=Count('likes'),
                    dislike_count=Count('dislikes')
                ).order_by('-created_at')
            except (ValueError, AttributeError, TypeError):
                # Fallback: return no posts if parsing fails
                posts = Post.objects.none()
        else:
            posts = Post.objects.none()
        
        posts_data = []
        for post in posts:
            posts_data.append({
                'id': post.id,
                'title': post.title,
                'description': post.description,
                'hours_procrastinated': str(post.hours_procrastinated),
                'author': post.author.username,
                'created_at': post.created_at.isoformat(),
                'like_count': post.like_count,
                'dislike_count': post.dislike_count,
            })
        
        return JsonResponse({
            'new_posts': posts_data,
            'count': len(posts_data)
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def abtest_view(request):
    """A/B test endpoint showing team nicknames and a randomized button."""
    # Randomly choose between Variant A ("kudos") and Variant B ("thanks")
    variant = random.choice(['A', 'B'])
    button_text = 'kudos' if variant == 'A' else 'thanks'
    
    # Track page view
    ABTestPageView.objects.create(
        variant=variant,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    team_nicknames = ['enthusiastic-partridge', 'sparkling-raccoon', 'aggressive-grouse', 'happy-stingray']
    
    context = {
        'team_nicknames': team_nicknames,
        'button_text': button_text,
        'variant': variant,
    }
    return render(request, 'accounts/abtest.html', context)


def get_client_ip(request):
    """Get the client's IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def abtest_button_click_view(request):
    """Track button clicks for the A/B test."""
    if request.method == 'POST':
        variant = request.POST.get('variant')
        
        if variant not in ['A', 'B']:
            return JsonResponse({'error': 'Invalid variant'}, status=400)
        
        # Track button click
        ABTestButtonClick.objects.create(
            variant=variant,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Get total click counts by variant
        click_count_a = ABTestButtonClick.get_click_count_by_variant('A')
        click_count_b = ABTestButtonClick.get_click_count_by_variant('B')
        
        return JsonResponse({
            'success': True,
            'click_count_a': click_count_a,
            'click_count_b': click_count_b,
        })
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

