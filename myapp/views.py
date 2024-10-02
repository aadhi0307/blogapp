from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render,redirect


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'ok','message':'account created successfully','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'PUT'])    
def edit_profile(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def login_user(request):
    username_or_email = request.data.get('username')  # Clarified to username_or_email
    password = request.data.get('password')
    print(f"Received username/email: {username_or_email}")
    print(f"Received password: {password}")

    if not username_or_email or not password:
        return Response({"error": "Please provide both username/email and password."}, status=status.HTTP_400_BAD_REQUEST)

    # Try to authenticate with username first
    user = authenticate(username=username_or_email, password=password)

    if user is None:
        # Try to authenticate with email if username doesn't work
        try:
            user = CustomUser.objects.get(username=username_or_email)
            if user.check_password(password):
                # User is found by email and password is correct
                print("User found by email and password is correct.")
            else:
                print("Password is incorrect for the user found by email.")
                user = None
        except CustomUser.DoesNotExist:
            print("No user found with this email.")
            user = None

    if user is not None:
        # Create token for the authenticated user
        token = AccessToken.for_user(user)
        return Response({
            'access': str(token), 
            'user': {
                'user_id':user.id,
                'username': user.username, 
                'email': user.email
            }
        }, status=status.HTTP_200_OK)
    else:
        print("Invalid credentials.")
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    


@api_view(['POST'])
def create_blog_post(request, user_id):
    # Fetch the user by ID; if not found, return a 404 response
    user = get_object_or_404(CustomUser, id=user_id)

    # Create the serializer with the provided data
    serializer = BlogPostSerializer(data=request.data)

    if serializer.is_valid():
        # Automatically set the user_id field to the logged-in user's ID
        blog_post = serializer.save(user_id=user.id)  # Automatically assign user_id
        return Response({
            'status': 'ok', 
            'message': 'Blog created successfully', 
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_blog_posts(request, user_id):
    # Fetch blog posts created by the user with the specified user_id
    blog_posts = BlogPost.objects.filter(user_id=user_id)
    
    # Paginate the results if needed
    paginator = PageNumberPagination()
    paginator.page_size = 10  # Number of posts per page
    result_page = paginator.paginate_queryset(blog_posts, request)

    serializer = BlogPostSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET', 'PUT'])
def update_blog_post(request, user_id, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id)

    # Check if the user is allowed to update this post
    if blog_post.user_id != user_id:
        return Response({'error': 'You do not have permission to edit this post.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        # Serialize the blog post details
        serializer = BlogPostSerializer(blog_post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BlogPostSerializer(blog_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Return the URL to redirect to the edit page along with the updated blog post data
            return Response({
                'status': 'ok',
                'message': 'Blog post updated successfully',
                'data': serializer.data,
                'redirect_url': f"/blog-posts/edit/{user_id}/{post_id}/"  # URL for the edit page
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Detail View
@api_view(['GET'])
def detail_blog_post(request, user_id, post_id):
    # Fetch the blog post by ID
    blog_post = get_object_or_404(BlogPost, id=post_id, user_id=user_id)

    # Serialize the blog post data
    serializer = BlogPostSerializer(blog_post)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Delete View
@api_view(['DELETE'])
def delete_blog_post(request, user_id, post_id):
    # Fetch the blog post by ID
    blog_post = get_object_or_404(BlogPost, id=post_id, user_id=user_id)

    # Delete the blog post
    blog_post.delete()
    return Response({'message': 'Blog post deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def detail_blog_post(request, user_id, post_id):
    # Fetch the blog post by ID
    blog_post = get_object_or_404(BlogPost, id=post_id, user_id=user_id)

    # Serialize the blog post data
    serializer = BlogPostSerializer(blog_post)
    return render(request, 'single_post.html', {
        'blog_post': serializer.data,
        'user_id': user_id  # Pass user_id to the template
    })

# New view for rendering the single post HTML
def detail_blog_post_view(request, user_id, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id, user_id=user_id)
    return render(request, 'single_post.html', {'blog_post': blog_post})

def edit_blog_post_view(request, user_id, post_id):
    # Fetch the blog post by ID and user ID
    blog_post = get_object_or_404(BlogPost, id=post_id, user_id=user_id)

    if request.method == 'POST':
        # Handle form submission
        blog_post.title = request.POST.get('title', blog_post.title)
        blog_post.content = request.POST.get('content', blog_post.content)
        blog_post.tags = request.POST.get('tags', blog_post.tags)
        blog_post.save()
        return redirect('detail_blog_post', user_id=user_id, post_id=post_id)

    # Render the edit page with the blog post data
    return render(request, 'edit_post.html', {'blog_post': blog_post})




def register_page(request):
    return render(request, 'register.html')

def login_page(request):
    return render(request, 'login.html')

def blog_page(request):
    return render(request,'blog.html')
def blog_list(request):
    return render(request,'blog_list.html')
def edit_profile1(request):
    return render(request,'edit_profile.html')
def single_post(request):
    return render(request,'single_post.html')
def edit_post(request):
    return render(request,'edit_post.html')

