from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from .forms import LoginForm
from .auth_backend import CustomAuthenticationBackend
from .models import Utilisateur, Agent,Postew,Unite
from django.core.paginator import Paginator
from django.db.models import Q 
from django.db import connection 
from django.core.mail import send_mail
from django.conf import settings


def page_acc(request):
    # Get the logged-in user
    if not 'user_id' in request.session:
        return HttpResponseRedirect(reverse('login')) 
    user = Utilisateur.objects.get(matricule=request.session['user_id'])

    # Retrieve the search query
    search_query = request.GET.get("search", "")

    # Create a query filter
    query_filter = Q(nom__icontains=search_query) | Q(prenom__icontains=search_query) | Q(matricule__icontains=search_query)

    # Determine the list of employees
    if user.is_admin:
        employees = Agent.objects.filter(query_filter)
    else:
        agent = Agent.objects.get(matricule=user.matricule)
        employees = Agent.objects.filter(unite=agent.unite).filter(query_filter)

    # Implement pagination with 20 employees per page
    paginator = Paginator(employees, 7)
    page_number = int(request.GET.get("page", 1))  # Convert to integer
    page = paginator.get_page(page_number)

    # Calculate start and end range for pagination
    start = max(1, page.number - 3)  # Ensure 'start' is at least 1
    end = min(paginator.num_pages, page.number + 3)  # Ensure 'end' doesn't exceed total pages

    # Render the template with the computed values
    return render(
        request,
        'main/page_employes.html',
        {
            'user': user,
            'page': page,
            'search_query': search_query,
            'page_range': range(start, end + 1),  # Pass the page range to the template
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
            request.session['user_id'] = user.matricule.matricule  # Save the user ID in the session
            return redirect('home')  # Redirect to the home page
        else:  # If authentication fails
            # Add a non-field error to the form
            form.add_error(None, 'matricule ou mot de passe invalide')
    return render(request, 'main/login.html', {'form': form}) 


def logout_view(request):
    # Manually clear session data to "log out" the user
    if 'user_id' in request.session:
        del request.session['user_id']  
    return HttpResponseRedirect(reverse('login'))  
def home_view(request):
    if not 'user_id' in request.session:
        return HttpResponseRedirect(reverse('login')) 
    user=Utilisateur.objects.get(matricule=request.session['user_id'])
    agent=Agent.objects.get(matricule=user.matricule)
    context={
        'agent':agent,
        'user':user
    }
    return render(request,'main\home.html',context=context)
def admin_view(request):
    if not 'user_id' in request.session:
        return HttpResponseRedirect(reverse('login'))
    user=Utilisateur.objects.get(matricule=request.session['user_id'])
    agent=Agent.objects.get(matricule=user.matricule)
    utilisateurs=Utilisateur.objects.exclude(matricule=user.matricule)
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
                new_agent=Agent.objects.get(matricule=matricule)
                new_user = Utilisateur(matricule=new_agent)
                new_user.nom = new_agent.nom
                if new_user.nom !=None:
                    new_user.prenom = new_agent.prenom
                else:
                    new_user.prenom = new_agent.nom
                new_user.set_password(password)  
                new_user.is_admin = False  
                new_user.save() 
                return redirect('page_admin')
            except Exception as e:
                    form.add_error(None, 'erreur lutilisateur n etait pas cree')
    return render(request,'main/page_admin.html',{'form':form,'agent':agent,'user':user,'utilisateurs':utilisateurs})
def suprimmer_view(request,matricule):
    try:
        ag=get_object_or_404(Agent,matricule=matricule)
        user=get_object_or_404(Utilisateur,matricule=ag)
        user.delete()
        return redirect('page_admin')
    except Utilisateur.DoesNotExist:
            return HttpResponse("utilisateur n'existe pas ") 

def contact_view(request):
    if not 'user_id' in request.session:
        return HttpResponseRedirect(reverse('login'))
    if request.method == "POST":
        name = request.POST.get('Name')  # Retrieve data from the form
        email = request.POST.get('Email')
        message = request.POST.get('message')

        if name and email and message:
            # Send an email with the contact form data
            subject = f"Contact from {name}"
            email_message = f"Message from {name} ({email}):\n\n{message}"

            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEVELOPER_EMAIL],  # Developer's email
            )

            # Redirect to a success page to avoid resubmission
            return HttpResponse("contact_success")
    return render(request,'main/contact_us.html')
def profile_view(request,matricule):
    if not 'user_id' in request.session:
        return HttpResponseRedirect(reverse('login'))
    user=Utilisateur.objects.get(matricule=request.session['user_id'])
    agent=Agent.objects.get(matricule=matricule)
    unite=Unite.objects.get(codeuni=agent.unite)
    poste=Postew.objects.get(codepos=agent.codepw)
    context={
        'user':user,
        'agent':agent,
        'unite':unite,
        'poste':poste,
    }
    return render(request,'main/page_profile.html',context=context)
def attestation_view(request,matricule):
    if not 'user_id' in request.session:
        return HttpResponseRedirect(reverse('login'))
    user=Utilisateur.objects.get(matricule=request.session['user_id'])
    agent=Agent.objects.get(matricule=matricule)
    post=Postew.objects.get(codepos=agent.codepw)
    context={
        'user':user,
        'agent':agent,
        'post':post
    }
    return render(request,'main/page_attestation.html',context=context)
from django.db import connection
from django.http import JsonResponse

from django.db import connection



from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection

def ats_view(request, matricule):
    procedure_name = 'releve_emo_p'
    matag = '25923'
    date = '2023-05-08'
    nbmois = 12

    try:
        with connection.cursor() as cursor:
            cursor.execute(
            """
            SET NOCOUNT ON
            DECLARE	@return_value int,
		@date2 nvarchar(10)

SELECT	@date2 = N'2024-02-15'

EXEC	@return_value = [dbo].[releve_emo_p_mois]
		@matag = N'25923',
		@date = N'2023-03-01',
		@date2 = @date2 OUTPUT

SELECT	@date2 as N'@date2'

SELECT	'Return Value' = @return_value


            """,
            
        )
            results = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            
            # Construct a list of dictionaries where each dictionary represents a row
            data = []
            for row in results:
                row_data = {}
                for col_name, value in zip(columns, row):
                    row_data[col_name] = value
                data.append(row_data)
            
            context = {
                'results': data,  # Pass the list of dictionaries as context
            }
            
            if not results:
                return JsonResponse({'error': 'No results found'}, status=404)

        return render(request, 'main/page_ats.html', context=context)
    
    except Exception as e:
        # Handle any exceptions
        return JsonResponse({'error': str(e)}, status=500)


