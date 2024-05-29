from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from .forms import *
from .auth_backend import CustomAuthenticationBackend
from .models import Utilisateur, Agent,Postew,Unite,HistAgent
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
    page_name = "Employés"


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
    paginator = Paginator(employees, 7)
    page_number = int(request.GET.get("page", 1))  # Convert to integer
    page = paginator.get_page(page_number)

    start = max(1, page.number - 3) 
    end = min(paginator.num_pages, page.number + 3)  

    return render(
        request,
        'main/page_employes.html',
        {
            'user': user,
            'page': page,
            'search_query': search_query,
            'page_range': range(start, end + 1), 
            'page_name': page_name, # Pass the page range to the template
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
        return redirect('page_admin') 
def home_view(request):
    if not 'user_id' in request.session:
        return HttpResponseRedirect(reverse('login')) 
    user=Utilisateur.objects.get(matricule=request.session['user_id'])
    agent=Agent.objects.get(matricule=user.matricule)
    page_name = "Bienvenue dans la Gestion des Documents des Employés"
    page_name2 = "Gérez, suivez et partagez facilement les documents des employés."
    context={
        'agent':agent,
        'user':user,
        'page_name':page_name,
        'page_name2':page_name2,
        
    }
    return render(request,'main\home.html',context=context)
def admin_view(request):
    if 'user_id' not in request.session:
        return HttpResponseRedirect(reverse('login'))
    
    user = Utilisateur.objects.get(matricule=request.session['user_id'])
    agent = Agent.objects.get(matricule=user.matricule)
    
    # Filter users, excluding the current user
    
    form = LoginForm(request.POST or None)
    if form.is_valid():
        matricule = form.cleaned_data['matricul']
        password = form.cleaned_data['password']
        if Utilisateur.objects.filter(matricule=matricule).exists():
            form.add_error('matricul', 'Il existe un utilisateur avec ce matricule')
        elif not Agent.objects.filter(matricule=matricule).exists():
            form.add_error('matricul', 'Il n\'existe pas un agent avec ce matricule')
        else:
            try:
                new_agent = Agent.objects.get(matricule=matricule)
                new_user = Utilisateur(matricule=new_agent)
                new_user.nom = new_agent.nom
                new_user.prenom = new_agent.prenom if new_agent.prenom else new_agent.nom
                new_user.set_password(password)
                new_user.is_admin = False
                new_user.save()
                return redirect('page_admin')
            except Exception as e:
                form.add_error(None, 'Erreur: l\'utilisateur n\'était pas créé')

    search_query = request.GET.get("search", "")
    query_filter = Q(nom__icontains=search_query) | Q(prenom__icontains=search_query) 
    utilisateurs = Utilisateur.objects.filter(matricule__nom__isnull=False).exclude(matricule__nom='')

    utilisateurs = utilisateurs.filter(query_filter)

    paginator = Paginator(utilisateurs,7)
    page_number = int(request.GET.get("page", 1))
    page = paginator.get_page(page_number)

    # Calculate the range for pagination control
    start = max(1, page.number - 1)
    end = min(paginator.num_pages, page.number + 1)
    page_range = range(start, end + 1)

    return render(request, 'main/page_admin.html', {
        'form': form,
        'agent': agent,
        'user': user,
        'page': page,
        'utilisateurs':utilisateurs,
        'search_query': search_query,
        'page_range': page_range,
    })
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
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Utilisateur, Agent, Unite, Postew, HistAgent

def profile_view(request, matricule):
    if not 'user_id' in request.session:
        return HttpResponseRedirect(reverse('login'))
    
    user = get_object_or_404(Utilisateur, matricule=request.session['user_id'])
    agent = get_object_or_404(Agent, matricule=matricule)
    unite = get_object_or_404(Unite, codeuni=agent.unite)
    poste = get_object_or_404(Postew, codepos=agent.codepw)
    hist = HistAgent.objects.filter(matricule=matricule).order_by('exercice', 'mois')
    
    grouped_hist = group_histories(hist)
    
    context = {
        'user': user,
        'agent': agent,
        'unite': unite,
        'poste': poste,
        'hist': grouped_hist,
    }
    return render(request, 'main/page_profile.html', context=context)

def group_histories(histories):
    grouped_hist = []
    if not histories:
        return grouped_hist
    
    current_group = {
        'start': (int(histories[0].exercice), int(histories[0].mois)),
        'end': (int(histories[0].exercice), int(histories[0].mois)),
        'status': histories[0].statut,
        'details': [histories[0]],
    }
    
    for i in range(1, len(histories)):
        current = histories[i]
        previous = histories[i - 1]
        
        if current.sitadmin == previous.sitadmin and (
            (int(current.exercice) == int(previous.exercice) and int(current.mois) == int(previous.mois) + 1) or
            (int(current.exercice) == int(previous.exercice) + 1 and int(current.mois) == 1 and int(previous.mois) == 12)
        ):
            current_group['end'] = (int(current.exercice), int(current.mois))
            current_group['details'].append(current)
        else:
            grouped_hist.append(current_group)
            current_group = {
                'start': (int(current.exercice), int(current.mois)),
                'end': (int(current.exercice), int(current.mois)),
                'status': current.statut,
                'details': [current],
            }
    
    grouped_hist.append(current_group)
    
    return grouped_hist

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

def relve_emo_view(request, matricule, date_debut ):
    if 'user_id' not in request.session:
        return HttpResponseRedirect(reverse('login'))
    try:
        with connection.cursor() as cursor:
            cursor.execute(
            """
            SET NOCOUNT ON; 

            exec [dbo].[releve_emo_p_mois] %s, %s,%s
            
            """,
            (matricule, date_debut,date_debut)
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

        return render(request, 'main/page_relve.html', context=context)
    
    except Exception as e:
        # Handle any exceptions
        return JsonResponse({'error': str(e)}, status=500)

def document_view(request):
    if 'user_id' not in request.session:
        return HttpResponseRedirect(reverse('login'))
    user = Utilisateur.objects.get(matricule=request.session['user_id'])
    agent = Agent.objects.get(matricule=user.matricule)

    if request.method == 'POST':
        form_rel = relve_Form(request.POST)
        form_attes = attestation_Form(request.POST)
        form_ats = ats_Form(request.POST)

        if form_rel.is_valid():
            cleaned_data = form_rel.cleaned_data
            if Agent.objects.filter(matricule=cleaned_data['matricule1']).exists():
                return redirect('relve_emo', matricule=cleaned_data['matricule1'], date_debut=cleaned_data['date_debut'])
            else:
                form_rel.add_error('matricule1', 'Il n\'existe pas un agent avec ce matricule')
        elif form_ats.is_valid():
            cleaned_data = form_ats.cleaned_data
            if Agent.objects.filter(matricule=cleaned_data['matricule2']).exists():
                return redirect('ats_per', matricule=cleaned_data['matricule2'], date=cleaned_data['date'], nbrmois=cleaned_data['nbrmois'])
            else:
                form_ats.add_error('matricule2', 'Il n\'existe pas un agent avec ce matricule')

        elif form_attes.is_valid():
            cleaned_data = form_attes.cleaned_data
            return redirect('attestation', matricule=cleaned_data['matricule3'])

        
    else:
        form_rel = relve_Form()
        form_attes = attestation_Form()
        form_ats = ats_Form()

    context = {
        'user': user,
        'agent': agent,
        'form_rel': form_rel,
        'form_ats': form_ats,
        'form_attes': form_attes,
    }
    return render(request, 'main/documents.html', context=context)
def ats_per_view(request, matricule, date, nbrmois):
    if 'user_id' not in request.session:
        return HttpResponseRedirect(reverse('login'))
    try:
        with connection.cursor() as cursor:
            query = f"""
            SET NOCOUNT ON; 
            DECLARE @return_value int

            EXEC @return_value = [dbo].[ats_periode_60_nb]
                @matag = N'{matricule}',
                @date = '{date}',
                @nb_mois = {nbrmois}

            SELECT 'Return Value' = @return_value
            """
            cursor.execute(query)
            results = cursor.fetchall()

            columns = [col[0] for col in cursor.description]

            # Exclude 'matag' and 'mois' columns
            display_columns = [col for col in columns if not (col.startswith('matag') or col.startswith('mois'))]

            # Calculate sums for each base column
            base_columns = [col for col in display_columns if col.startswith('base')]
            sums = {base: 0 for base in base_columns}
            data = []
            for row in results:
                row_data = {col_name: value for col_name, value in zip(columns, row)}
                data.append(row_data)
                for base in base_columns:
                    sums[base] += float(row_data[base])

            # Calculate total sum and average
            total_sum = sum(sums.values())
            average_sum = total_sum / nbrmois if nbrmois else 0

            context = {
                'results': data,
                'sums': sums,
                'display_columns': display_columns,  # Pass only the display columns to the template
                'total_sum': total_sum,
                'average_sum': average_sum,
                'nbrmois':nbrmois,

            }

            if not results:
                return JsonResponse({'error': 'No results found'}, status=404)

        return render(request, 'main/page_ats.html', context=context)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
