from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm
from .auth_backend import CustomAuthenticationBackend
from .models import Utilisateur, Agent
def main(request):
    user=Utilisateur.objects.get(id=request.session['user_id'])
    agent=Agent.objects.get(matricule=user.matricule)
    return render(request,'main\base.html',{'agent':agent,})

def page_acc(request):
    user=Utilisateur.objects.get(id=request.session['user_id'])
    agent=Agent.objects.get(matricule=user.matricule)
    if user.is_admin:
        employees=Agent.objects.all()
        return render(request, 'main/page_employes.html', {'user':user,'agent':agent,'employees':employees})  
    else:
        employees=list(Agent.objects.filter(unite=agent.unite))
        employees*=20
        return render(request, 'main/page_employes.html', {'user':user,'employees':employees,'agent':agent}) 

# Login view
def login_view(request):
    form = LoginForm(request.POST or None)  # Initialize the form with POST data
    
    if request.method == 'POST' and form.is_valid():
        matricule = form.cleaned_data['matricul']
        password = form.cleaned_data['password']

        # Use the custom authentication backend to authenticate the user
        user = CustomAuthenticationBackend().authenticate(request, matricule, password)

        if user:  # If authentication is successful
            request.session['user_id'] = user.id  # Save the user ID in the session
            return redirect('employes')  # Redirect to the home page
        else:  # If authentication fails
            # Add a non-field error to the form
            form.add_error(None, 'Invalid matricul or password.')

    return render(request, 'main/login.html', {'form': form})  # Render the login template with errors
def home_view(request):
    user=Utilisateur.objects.get(id=request.session['user_id'])
    agent=Agent.objects.get(matricule=user.matricule)
    context={
        'agent':agent,
        'user':user
    }
    return render(request,'main\home.html',context=context)
def admin_view(request):
    user=Utilisateur.objects.get(id=request.session['user_id'])
    agent=Agent.objects.get(matricule=user.matricule)
    form=LoginForm(request.POST or None )
    if form.is_valid():
        matricule = form.cleaned_data['matricul']
        password = form.cleaned_data['password']
        if Utilisateur.objects.filter(matricule=matricule).exists():
            form.add_error('matricul','Il existe un utilisateur avec ce matricule ')
        elif not Agent.objects.filter(matricule=matricule).exists():
              form.add_error('matricul','Il nexiste pas un agent avec ce matricule ')
        else:
            try:
                new_user = Utilisateur(matricule=matricule)
                new_user.set_password(password)  
                new_user.is_admin = False  
                new_user.save() 
                return HttpResponse("nouveau utilisateur cree ")
            except Exception as e:
                    form.add_error(None, 'erreur lutilisateur n etait pas cree')
    return render(request,'main/page_admin.html',{'form':form,'agent':agent,'user':user})
def contact_view(request):
    return render(request,'main/contact_us.html')