from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# from users.forms import UserRegisterForm
# from users.models import User

# from django.db import transaction
# from django.urls import reverse_lazy
# from django.views.generic import ListView, CreateView
#
# from users.forms import FamilyMemberFormSet
# from users.models import Profile
#
#
# class ProfileList(ListView):
#     model = Profile
#
#
# class ProfileFamilyMemberCreate(CreateView):
#     model = Profile
#     fields = ['first_name', 'last_name']
#     success_url = reverse_lazy('profile-list')
#
#     def get_context_data(self, **kwargs):
#         data = super(ProfileFamilyMemberCreate, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['familymembers'] = FamilyMemberFormSet(self.request.POST)
#         else:
#             data['familymembers'] = FamilyMemberFormSet()
#         return data
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         familymembers = context['familymembers']
#         with transaction.atomic():
#             self.object = form.save()
#
#             if familymembers.is_valid():
#                 familymembers.instance = self.object
#                 familymembers.save()
#         return super(ProfileFamilyMemberCreate, self).form_valid(form)
# TODO: Add validation of frontend and backend too
# def register(request):
#     if request.user.is_authenticated:
#         return redirect('ig_manager-dashboard')
#     else:
#         if request.method == 'POST':
#             form = UserRegisterForm(request.POST)
#             # TODO: validate on client side too
#             if form.is_valid():
#                 instance = form.save(commit=False)
#                 if User.objects.filter(email=instance.email).exists():
#                     messages.warning(request, f'Your mail already exist! Do you forgot your password? ')
#                 elif User.objects.filter(username=instance.username).exists():
#                     messages.warning(request, f'Same username already exist please choose another!')
#                 else:
#                     username = "lalalala"
#                     form.save()
#                     # email = form.cleaned_data.get('email')
#                     messages.success(request, f'Your account has been created! You are now able to log in')
#                     return redirect('login')
#         else:
#             form = UserRegisterForm()
#         return render(request, 'account/signup.html', {'form': form, "title": "Register"})
