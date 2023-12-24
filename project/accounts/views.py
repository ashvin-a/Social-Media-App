"""Views of accounts app"""
from django.http import HttpResponseRedirect,HttpRequest
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.views import View
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from posts.forms import PostForm,CommentForm
from posts.models import PostModel
from .models import ProfileDataModel, FollowersModel
from .forms import CreateUserForm,ProfileDataForm
from .functions import paginate


class RegisterUser(View):
    """
    This view is used to deal with the registering of new users
    """
    def get(self,request:HttpRequest):
        """Redirects the user to homepage after authentication."""
        if request.user.is_authenticated:
            return redirect('homepage')
        return render(request,'accounts/signup.html')

    def post(self,request:HttpRequest):
        """Creates a new user.
        
        Parameters
        ----------
        request : HttpRequest
            Request object

        Returns
        -------
        Callable
            Reverse url redirect or render page
        """
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            subject = 'Welcome - Social Media App'
            welcome = f'Hi {user}!'
            html_message = render_to_string('accounts/email.html',{
                'welcome':welcome
            })
            plain_message = strip_tags(html_message)
            message = EmailMultiAlternatives(
                subject=subject,from_email='settings.EMAIL_HOST_USER',
                body=plain_message,to=[email]
            )
            message.attach_alternative(html_message,'text/html')
            message.send()
            user = authenticate(request,username=user,password=password)
            if user is not None:
                login(request,user)
                return redirect('profile-page')
        context = {'form':form.errors}
        return render(request,'accounts/signup.html',context)


class LoginUser(View):
    """
    This view is involved in the logging in of the user 
    """
    def get(self,request:HttpRequest):
        """
        Redirects the user to homepage after authentication.
        """
        if request.user.is_authenticated:
            return redirect('homepage')
        return render(request,'accounts/login.html')

    def post(self,request:HttpRequest):
        """Logs the user after authentication.

        Parameters
        ----------
        request : HttpRequest
            Request object

        Returns
        -------
        Callable
            Reverse url redirect or render page
        """
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            if user.is_staff:
                return redirect('admin')
            print(request.user.is_active)
            return redirect('homepage')
        # if not request.user.is_active:
        #     messages.warning(request,'Your account is deactivated.\
        #                     Please contact support team')
        messages.warning(request,'Username or password is incorrect')
        return render(request,'accounts/login.html')


class Logout(View):
    """
    Logs out the user from session.
    """
    def get(self, request:HttpRequest):
        """
        Logs out the user.
        """
        logout(request)
        return redirect('login-page')


class PostListView(View):
    """
    This view renders the homepage(landing page) after user logs in.
    """
    def get(self,request:HttpRequest):
        """
        Used to display the contents in homepage.
        """
        form = PostForm()
        comment_form = CommentForm()
        user = request.user #?current user
        try:
            profile = ProfileDataModel.objects.get(user=request.user)
        except ProfileDataModel.DoesNotExist:
            profile = None

        follower = FollowersModel.objects.filter(user=user.id).count()
        following = FollowersModel.objects.filter(follower=user).count()
        author_id_list = FollowersModel.objects.filter(follower=user)\
                                            .values_list('user',flat=True)
        if request.user.is_superuser is True:
            posts = PostModel.objects.all().order_by('-created_on')
        else:
            posts = PostModel.objects.filter(Q(author_id=request.user.id)|\
                                            Q(author_id__in=author_id_list))\
                                            .order_by('-created_on')
        all_users = User.objects.exclude(Q(id=request.user.id)|\
                                        Q(id__in=author_id_list))
        page_obj = paginate(request,all_users)
        context = {
            'comment_form':comment_form,
            'post_list':posts,'form':form,
            'curr_user':user,'profile':profile,'all_users':page_obj,
            'following':following,'follower':follower
        }
        return render(request, 'accounts/homepage.html',context)

    def post(self, request:HttpRequest):
        """
        Updates the contents in homepage.
        """
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return HttpResponseRedirect('/')

        posts = PostModel.objects.all().filter(author_id=request.user.id)\
                                                .order_by('-created_on')
        context = {
            'post_list':posts,
            'form':form,
        }
        return render(request, 'accounts/homepage.html',context)


class EditProfileView(View):
    """
    This view enables user to edit their profile.
    """
    def get(self, request:HttpRequest):
        """
        Fetches the information already filled in edit profile page.
        """
        user = request.user
        try:
            profile = ProfileDataModel.objects.get(user=request.user)
        except ProfileDataModel.DoesNotExist:
            profile = None
        form = ProfileDataForm(instance=profile)
        if user.is_staff:
            return render(request,'accounts/edit_admin_profile.html',{'form':form,'curr_user':user})
        return render(request, 'accounts/edit_profile.html',{'form':form,'curr_user':user})

    def post(self, request:HttpRequest):
        """
        Fetches the information already filled in edit profile page.
        """
        try:
            profile = ProfileDataModel.objects.get(user=request.user)
        except ProfileDataModel.DoesNotExist:
            profile = None
        form = ProfileDataForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            if request.user.is_staff:
                return redirect('admin')
            return redirect('homepage')


class ProfileView(View):
    """
    This view renders the detailed profile page of each user.
    """
    def get(self, request:HttpRequest, profile_id:int):
        """Renders the profile page of user.

        Parameters
        ----------
        request : HttpRequest
            Response object
        profile_id : int
            The profile id of selected user

        Returns
        -------
        Callable
            Views the profile of selected user.
        """
        curr_user = request.user
        comment_form = CommentForm()
        user = User.objects.get(id=profile_id) #? the other user
        flag = FollowersModel.objects.filter(Q(follower=request.user)&\
                                            Q(user=user.id)).exists()
        follower = FollowersModel.objects.filter(user=user.id).count()
        following = FollowersModel.objects.filter(follower=user.id).count()
        posts = PostModel.objects.filter(author_id=user.id).order_by('-created_on')
        page_obj = paginate(request,posts)
        try:
            profile = ProfileDataModel.objects.get(user_id=user.id)
        except ProfileDataModel.DoesNotExist:
            profile = None
        context = {
            'curr_user':curr_user,'comment_form':comment_form,
            'profile':profile,'posts':page_obj,
            'flag':flag,'follower':follower,
            'following':following,
        }
        return render(request, 'accounts/profile.html', context)

    def post(self, request:HttpRequest, profile_id:int):
        """
        Updates the change in followers.
        """
        user_to_follow = User.objects.get(id=profile_id) 
        if 'follow' in request.POST:
            FollowersModel.objects.create(follower=request.user,
                                         user=user_to_follow)
        elif 'unfollow' in request.POST:
            FollowersModel.objects.filter(follower=request.user,
                                user=user_to_follow).delete()
        return HttpResponseRedirect(f'/profile/{user_to_follow.id}/')


class ConnectionView(View):
    """
    This view renders the detailed profile page of each user
    """
    def get(self, request:HttpRequest):
        """
        Views the users who are being followed and following the current user
        """
        curr_user = request.user
        profile = ProfileDataModel.objects.get(user=curr_user)
        followers = FollowersModel.objects.filter(user=request.user)
        following = FollowersModel.objects.filter(follower=request.user)
        context = {
            'profile':profile,
            'curr_user':curr_user,
            'followers':followers,
            'following':following,
        }
        return render(request,'accounts/connections.html',context)


class SearchView(View):
    """
    This view lists out all the users who have the search word as a part of their
    first name or last name
    """
    def get(self, request:HttpRequest):
        """
        Shows matching users
        """
        profile = ProfileDataModel.objects.get(user=request.user)
        followers = FollowersModel.objects.filter(user=request.user)
        following = FollowersModel.objects.filter(follower=request.user)
        context = {
            'profile':profile,
            'curr_user':request.user,
            'followers':followers,
            'following':following,
        }
        return render(request,'accounts/search.html',context)

    def post(self, request:HttpRequest):
        """
        Search for matching users
        """
        key = request.POST.get('search')
        profile = get_object_or_404(ProfileDataModel, user=request.user)
        user_list = ProfileDataModel.objects.filter(Q(first_name__icontains=key)|
                    Q(last_name__icontains=key)|
                    Q(user__username__icontains=key)).exclude(user=request.user)\
                    .order_by('-last_updated')
        context = {
            'user_list':user_list,'curr_user':request.user,'profile':profile
        }
        return render(request,'accounts/search.html',context)


class AdminView(View):
    """
    This is the landing page for admins.
    """
    def get(self, request:HttpRequest):
        """
        Renders admin homepage
        """
        return render(request,'accounts/admin.html',{'curr_user':request.user})


class ViewUsers(View):
    """
    Admin can manage users here.
    """
    def get(self, request:HttpRequest):
        """
        Views all the users.
        """
        all_users = ProfileDataModel.objects.exclude(Q(user=request.user.id))
        page_obj = paginate(request,all_users)
        context = {
            'curr_user':request.user,
            'all_users':page_obj
        }
        return render(request,'accounts/list_users.html',context)

    def post(self, request:HttpRequest):
        """
        Shows the matching result for search.
        """
        key = request.POST.get('search')
        user_list = ProfileDataModel.objects.filter(Q(first_name__icontains=key)|
                    Q(last_name__icontains=key)|
                    Q(user__username__icontains=key)).exclude(user=request.user)\
                    .order_by('-last_updated')
        page_obj = paginate(request,user_list)
        context = {
            'curr_user':request.user,
            'all_users':page_obj,
        }
        return render(request,'accounts/list_users.html',context)


class ViewPosts(View):
    """
    View all posts.
    """
    def get(self, request:HttpRequest):
        """
        Accumulates all posts.
        """
        form = PostForm()
        comment_form = CommentForm()
        posts = PostModel.objects.all().order_by('-created_on')
        page_obj = paginate(request,posts)
        context = {
            'comment_form':comment_form,
            'post_list':page_obj,'form':form,
            'curr_user':request.user,
        }
        return render(request,'accounts/list_posts.html',context)


class DeactivateUser(View):
    """
    Enables admin to modify access of the user.
    """
    def post(self, request:HttpRequest, user_id:int):
        """
        Deactivates users.
        """
        user = get_object_or_404(User, id=user_id)
        if request.user.is_staff:
            user.is_active = not user.is_active
            user.save()
        return redirect('all-users')
