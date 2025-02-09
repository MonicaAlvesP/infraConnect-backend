import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Post
from django.contrib.auth.models import User
from users.models import Token


def get_user_from_token(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if auth_header:
        parts = auth_header.split()
        if len(parts) == 2 and parts[0] == 'Token':
            token_key = parts[1]
            try:
                token = Token.objects.get(key=token_key)
                return token.user
            except Token.DoesNotExist:
                return None
    return None


@csrf_exempt
def posts_view(request):
    user = get_user_from_token(request)
    if user is None:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    if request.method == 'GET':
        posts = Post.objects.all().values(
            'id', 'title', 'content', 'author_id', 'created_at')
        posts_list = list(posts)
        return JsonResponse({'posts': posts_list})

    elif request.method == 'POST':
        if not user.is_staff:
            return JsonResponse({'error': 'Forbidden, only admin can create posts.'}, status=403)
        try:
            data = json.loads(request.body)
            title = data.get('title')
            content = data.get('content')
            if not title or not content:
                return JsonResponse({'error': 'Title and content are required.'}, status=400)
            post = Post.objects.create(
                title=title, content=content, author=user)
            return JsonResponse({'id': post.id, 'title': post.title, 'content': post.content}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            post_id = data.get('id')
            title = data.get('title')
            content = data.get('content')
            post = Post.objects.get(id=post_id)
            if post.author != user:
                return JsonResponse({'error': 'Forbidden, you are not the author of this post.'}, status=403)
            post.title = title
            post.content = content
            post.save()
            return JsonResponse({'id': post.id, 'title': post.title, 'content': post.content})
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            post_id = data.get('id')
            post = Post.objects.get(id=post_id)
            if post.author != user and not user.is_staff:
                return JsonResponse({'error': 'Forbidden, you are not the author of this post.'}, status=403)
            post.delete()
            return JsonResponse({'id': post_id})
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def post_detail_view(request, post_id):
    user = get_user_from_token(request)
    if user is None:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'id': post.id, 'title': post.title, 'content': post.content, 'author_id': post.author_id, 'created_at': post.created_at})

    elif request.method == 'PUT':
        if post.author != user and not user.is_staff:
            return JsonResponse({'error': 'Forbidden, you are not the author of this post.'}, status=403)
        try:
            data = json.loads(request.body)
            title = data.get('title')
            content = data.get('content')
            if not title or not content:
                return JsonResponse({'error': 'Title and content are required.'}, status=400)
            post.title = title
            post.content = content
            post.save()
            return JsonResponse({'id': post.id, 'title': post.title, 'content': post.content})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'DELETE':
        if post.author != user and not user.is_staff:
            return JsonResponse({'error': 'Forbidden, you are not the author of this post.'}, status=403)
        post.delete()
        return JsonResponse({'id': post_id})

    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)