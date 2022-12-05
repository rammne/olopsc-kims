from django.shortcuts import render
from .models import Item, Inventory, AcceptedRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime

def login_page(request):
	page = 'login'

	if request.user.is_authenticated:
		return redirect('kims-bag')

	if request.method == 'POST':
		username = request.POST.get('username').lower()
		password = request.POST.get('password')
		try:
			user = User.objects.get(username=username)
		except:
			messages.error(request, 'User not found')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('kims-bag')
		else:
			messages.error(request, 'Username or Password does not exist')

	context = {'page':page}
	return render(request, 'kims/login_register.html', context)

def logout_user(request):
	logout(request)
	return redirect('login') 

def register_page(request):
	form = UserRegistrationForm()

	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		olopsc_email = request.POST.get('email').split('@')
		if olopsc_email[1] == 'olopsc.edu.ph' and User.objects.filter(email=request.POST.get('email')).exists() == False:
			if form.is_valid():
				user = form.save(commit=False)
				user.username = user.username.lower()
				messages.success(request, 'Account Created!')
				user.is_active = False
				user.save()
				current_site = get_current_site(request)
				mail_subject = 'Activation link has been sent to your email'
				message = render_to_string('kims/acc_active_email.html', {
						'user': user,
						'domain': current_site.domain,
						'uid': urlsafe_base64_encode(force_bytes(user.pk)),
						'token':account_activation_token.make_token(user),
						'protocol': 'https' if request.is_secure() else 'http',
					})
				to_email = form.cleaned_data.get('email')
				email = EmailMessage(mail_subject, message, to=[to_email])
				email.send()

				return HttpResponse('Please confirm your email address to complete the registration')
		else:
			messages.warning(request, 'OLOPSC gmail required or you entered an existing one')
	else:
		form = UserRegistrationForm()
			
	context = {'form':form,}
	return render(request, 'kims/login_register.html', context)

def activate(request, uidb64, token):
	User = get_user_model()
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		messages.success(request, 'Thank you for your email confirmation. Now you can login')
		return redirect('login')
	else:
		return HttpResponse('Activation link is invalid!')

@login_required(login_url='login')
def bag(request):
	z = request.GET.get('z') if request.GET.get('z') != None else ''
	items = Item.objects.filter(Q(inventory__name__icontains=z) | Q(name__icontains=z))
	objs = AcceptedRequest.objects.filter(student_id=request.user.id) #SORT AND SEARCH UNFINISHED
	page = 'bag'
	#user_item_list = request.user.items.filter(Q(inventory__name__icontains=z) | Q(name__icontains=z))
	if request.method == 'GET':
		if request.GET.get('Revert'):
			for obj in objs:
				if obj.item.name == request.GET.get('Revert'):
					item = Item.objects.get(name=request.GET.get('Revert'))
					AcceptedRequest.objects.filter(student_id=request.user.id).filter(item=item.id).update(status=4)
					return redirect('kims-bag')

	context = {
		'items': items,
		'inventories':Inventory.objects.all(),
		'page':page,
		'objs':objs
	}
	return render(request, 'kims/base.html', context)

def inventory(request):
	z = request.GET.get('z') if request.GET.get('z') != None else ''
	page = 'inventory'
	context = {
		'items': Item.objects.filter(Q(inventory__name__icontains=z) | Q(name__icontains=z)),
		'inventories':Inventory.objects.all(),
		'page':page
	}
	return render(request, 'kims/base.html', context)

def item_detailed_view(request, pk):
	user = request.user
	item = Item.objects.get(id=pk)
	if request.method == 'GET':
		if request.GET.get('Request'):
			AcceptedRequest.objects.create(student=user, item=item)
			item.quantity -= 1
			item.save()
			return redirect('kims-bag')
	context = {'item': Item.objects.get(id=pk)}
	return render(request, 'kims/item_detail.html', context)

def requests(request):
	objs = AcceptedRequest.objects.all()

	if request.method == 'GET':
		if request.GET.get('Accept'):
			obj_list = request.GET.get('Accept').split('|')
			user = User.objects.get(username=obj_list[0])
			item = Item.objects.get(name=obj_list[1])
			AcceptedRequest.objects.filter(student_id=user.id).filter(item_id=item.id).update(status=2)
			#print(AcceptedRequest.objects.filter(student_id=user.id).filter(item_id=item.id)[0].status != 2)
			aq = AcceptedRequest.objects.get(student_id=user.id, item_id=item.id)
			aq.__history_date = datetime.now()
			aq.save()
		elif request.GET.get('Decline'):
			obj_list = request.GET.get('Decline').split('|')
			user = User.objects.get(username=obj_list[0])
			item = Item.objects.get(name=obj_list[1])
			print(AcceptedRequest.objects.filter(student_id=user.id).filter(item_id=item.id)[0].status != 2)
			AcceptedRequest.objects.filter(student_id=user.id).filter(item_id=item.id).update(status=3)
			if AcceptedRequest.objects.filter(student_id=user.id).filter(item_id=item.id)[0].status == 2:
				print(AcceptedRequest.objects.get(student_id=user.id, item_id=item.id).status)
		elif request.GET.get('Returned'):
			obj_list = request.GET.get('Returned').split('|')
			user = User.objects.get(username=obj_list[0])
			item = Item.objects.get(name=obj_list[1])
			AcceptedRequest.objects.filter(student_id=user.id).filter(item_id=item.id).delete()
			i = Item.objects.get(name=item)
			i.quantity += 1
			i.save() 

		if request.GET.get('Remark'):
			obj_list = request.GET.get('Remark').split('|')
			user = User.objects.get(username=obj_list[0])
			item = Item.objects.get(name=obj_list[1])
			#item_remark = request.GET.get('itemRemark') if request.GET.get('itemRemark') != None else ''
			AcceptedRequest.objects.filter(student_id=user.id).filter(item_id=item.id).update(remarks=request.GET.get('itemRemark'))

	context = {'objs': objs}
	return render(request, 'kims/requests.html', context)

def history_view(request):
	z = request.GET.get('z') if request.GET.get('z') != None else ''
	page = 'history'
	item_accepted_date = AcceptedRequest.history.filter(student_id=request.user.id).filter(history_type='+')
	user_id = None
	for user in User.objects.all():
		if user.username == z:
			user_id = user.id

	if request.user.is_staff:
		item_returned_date = AcceptedRequest.history.filter(student_id=user_id).filter(history_type='-') if user_id != None else AcceptedRequest.history.filter(history_type='-')
	else:
		item_returned_date = AcceptedRequest.history.filter(student_id=user.id).filter(history_type='-')

	context = {
		'items': Item.objects.filter(Q(inventory__name__icontains=z) | Q(name__icontains=z)),
		'inventories':Inventory.objects.all(),
		'page':page,
		'item_accepted_date':item_accepted_date,
		'item_returned_date':item_returned_date,
	}
	return render(request, 'kims/base.html', context)

'''def groups_view(request):
	context = {'page': 'groups_view'}
	return render(request, 'kims/base.html', context)'''

def about_page(request):
	page = 'about'
	context = {'page': page}
	return render(request, 'kims/about.html', context)