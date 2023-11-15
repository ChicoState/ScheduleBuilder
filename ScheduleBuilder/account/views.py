from .forms import RegistrationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.conf import settings

from .models import Account
from friend.models import FriendList, FriendRequest
from friend.utils import get_friend_request_or_false
from friend.friend_request_status import FriendRequestStatus

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})

def account_view(request, *args, **kwargs):
	context = {}
	user_id = kwargs.get("user_id")
	try:
		account = Account.objects.get(pk=user_id)
	except:
		return HttpResponse("Something went wrong.")
	if account:
		context['id'] = account.id
		context['username'] = account.username
		context['email'] = account.email    
		try:
			friend_list = FriendList.objects.get(user=account)
		except FriendList.DoesNotExist:
			friend_list = FriendList(user=account)
			friend_list.save()

		friends = friend_list.friends.all()
		context['friends'] = friends
		is_self = True
		is_friend = False
		request_sent = FriendRequestStatus.NO_REQUEST_SENT.value 
		friend_requests = None
		user = request.user

		if user.is_authenticated and user != account:
			is_self = False
			if friends.filter(pk=user.id):
				is_friend = True
			else:
				is_friend = False
				if get_friend_request_or_false(sender=account, receiver=user) != False:
					request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
					context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
				elif get_friend_request_or_false(sender=user, receiver=account) != False:
					request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
				else:
					request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
		
		elif not user.is_authenticated:
			is_self = False
		else:
			try:
				friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
			except:
				pass

		context['is_self'] = is_self
		context['is_friend'] = is_friend
		context['request_sent'] = request_sent
		context['friend_requests'] = friend_requests
		context['BASE_URL'] = settings.BASE_URL
		
		return render(request, "account/profile.html", context)
      
def account_search_view(request):
	context = {}
	if request.method == "GET":
		search_query = request.GET.get("q")
		if search_query is not None and len(search_query) > 0:
			search_results = Account.objects.filter(email__icontains=search_query).filter(username__icontains=search_query).distinct()
			user = request.user
			accounts = [] 
			if user.is_authenticated:
				auth_user_friend_list = FriendList.objects.get(user=user)
				for account in search_results:
					accounts.append((account, auth_user_friend_list.is_mutual_friend(account)))
				context['accounts'] = accounts
			else:
				for account in search_results:
					accounts.append((account, False))
				context['accounts'] = accounts
	return render(request, "account/search_results.html", context)