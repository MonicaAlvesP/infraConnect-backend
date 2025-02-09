import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Token

@csrf_exempt
def register(request):
  if request.method == 'POST':
    try:
      data = json.loads(request.body)
      username = data.get('username')
      password = data.get('password')

      if not username or not password:
        return JsonResponse({'error': 'Username and password are required.'}, status=400)

      if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists.'}, status=400)

      user = User.objects.create_user(username=username, password=password)

      import secrets
      token_key = secrets.token_hex(20)
      token = Token.objects.create(user=user, key=token_key)

      return JsonResponse({'message': 'User registered successfully!', 'token': token.key})

    except Exception as e:
      return JsonResponse({'error': str(e)}, status=400)

  return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt
def login_view(request):
  if request.method == 'POST':
    try:
      data = json.loads(request.body)
      username = data.get('username')
      password = data.get('password')

      user = authenticate(username=username, password=password)

      if user is not None:
        login(request, user)

        token, created = Token.objects.get_or_create(user=user)

        return JsonResponse({
          'message': 'Login successful!', 
          'token': token.key,
          'is_staff': user.is_staff
          })

      return JsonResponse({'error': 'Invalid credentials.'}, status=400)

    except Exception as e:
      return JsonResponse({'error': str(e)}, status=400)

  return JsonResponse({'error': 'Invalid request method.'}, status=405)
