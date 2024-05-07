from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm
from .auth_backend import CustomAuthenticationBackend
from .models import Utilisateur, Agent
from django.core.paginator import Paginator
from django.db.models import Q  
def main(request):
    user=Utilisateur.objects.get(matricule=request.session['user_id'])
    agent=Agent.objects.get(matricule=user.matricule)
    return render(request,'main\base.html',{'agent':agent,})
def page_acc(request):
    # Get the logged-in user
    user = Utilisateur.objects.get(matricule=request.session['user_id'])

    # Retrieve the search query
    search_query = request.GET.get("search", "")  # Get the search term from the query parameter

    # Create a Q object to filter by multiple fields
    query_filter = Q(nom__icontains=search_query) | Q(prenom__icontains=search_query) | Q(matricule__icontains=search_query)

    # Determine the list of employees based on user role
    if user.is_admin:
        # Admin can search all employees, applying the query filter
        employees = Agent.objects.filter(query_filter)
    else:
        agent = Agent.objects.get(matricule=user.matricule)  # Fetch the associated Agent
        # Non-admins can only search within their unit
        employees = Agent.objects.filter(unite=agent.unite).filter(query_filter)

    # Implement pagination with 20 employees per page
    paginator = Paginator(employees, 20)  # Define the page size
    page_number = request.GET.get("page", 1)  # Get the current page number
    page = paginator.get_page(page_number)  # Retrieve the current page

    # Render the template with the paginated page and search query
    return render(
        request,
        'main/page_employes.html',
        {
            'user': user,
            'page': page,
            'search_query': search_query,  # Pass the search query to the template
        }
    )
# Login view
def login_view(request):
    form = LoginForm(request.POST or None)  # Initialize the form with POST data
    
    if request.method == 'POST' and form.is_valid():
        matricule = form.cleaned_data['matricul']
        password = form.cleaned_data['password']

        # Use the custom authentication backend to authenticate the user
        user = CustomAuthenticationBackend().authenticate(request, matricule, password)

        if user:  # If authentication is successful
            request.session['user_id'] = user.matricule  # Save the user ID in the session
            return redirect('home')  # Redirect to the home page
        else:  # If authentication fails
            # Add a non-field error to the form
            form.add_error(None, 'Invalid matricul or password.')

    return render(request, 'main/login.html', {'form': form})  # Render the login template with errors
def home_view(request):
    user=Utilisateur.objects.get(matricule=request.session['user_id'])
    agent=Agent.objects.get(matricule=user.matricule)
    context={
        'agent':agent,
        'user':user
    }
    return render(request,'main\home.html',context=context)
def admin_view(request):
    user=Utilisateur.objects.get(matricule=request.session['user_id'])
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
# from django.db import connection

# with connection.cursor() as cursor:
#     # Exécutez la procédure stockée (remplacez le nom de la procédure et les arguments)
#     cursor.callproc('nom_de_la_procedure', [arg1, arg2, ...])

#     # Récupérez les résultats (si la procédure stockée renvoie des données)
#     results = cursor.fetchall()