from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.views import LoginView
from django.contrib import messages

def register(request):
    print("Inside")
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print("Here")
        if form.is_valid():
            print("Valid")
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below:")
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})

class CustomLoginView(LoginView):
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)