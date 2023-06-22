from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import EmployeeDetail, Leave
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.
#@user_passes_test(lambda u: u.is_superuser)   ##this page only show to super user 
@login_required(login_url='login')
def home(request):
    emp = EmployeeDetail.objects.all()
    
    context = {
        "emp": emp,
    }
    return render(request, 'employee/dashboard.html', context)

@login_required(login_url='login')
def emp_home(request):
    if request.user.is_superuser:
        return redirect('home')  #
    else:
        emp = EmployeeDetail.objects.get(user=request.user) 
        #print(emp)

        context = {
            "emp": emp,
        }
        return render(request, 'employee/emp_base.html', context)

def about(request):
    return render(request, 'employee/about.html')

@login_required(login_url='login')
def register(request):
    error = ""
    if request.method == 'POST':
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        ec = request.POST['empcode']
        em = request.POST['email']
        pwd = request.POST['pwd']
        print(fn, ln, ec, em, pwd)
        try:
            user = User.objects.create_user(first_name=fn, last_name=ln, username=em, password=pwd)
            EmployeeDetail.objects.create(user=user, empcode=ec)
            return redirect('home')
            error = "no"
        except:
            error="yes"

            
    return render(request, 'employee/registration.html', locals())


def login_request(request):
    error = ""
    if request.method == 'POST':
          u = request.POST.get('email')
          p = request.POST.get('password')
          user = authenticate(request, username=u, password=p)
          if user is not None:
              login(request, user)
              error = "no"
              return redirect('emp_home')
          else:
              error = "yes"
          
    return render(request, 'employee/login.html', locals())

# def login_request(request):
#     error = ""
#     if request.method == 'POST':
#           u = request.POST.get('email')
#           p = request.POST.get('password')
#           user = authenticate(request, username=u, password=p)
#           if user is not None:
#               login(request, user)
#               if user.is_staff is None:
#                   return redirect('emp_home')
#               elif user.is_superuser:
#                   return redirect('home')
#               error = "no"
#               #return redirect('emp_home')
#           else:
#               error = "yes"
          
#     return render(request, 'employee/login.html', locals())

          



def logout_view(request):
    logout(request)
    return redirect('login')


def profile(request):
    error = ""
    user = request.user
    employee = EmployeeDetail.objects.get(user = user)
    if request.method == 'POST':
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        ec = request.POST['empcode']
        em = request.POST['emailid']
        contact = request.POST['contact']
        designation = request.POST['designation']
        dept = request.POST['department']
        jdate = request.POST['jdate']
        gender = request.POST['gender']
        profile_pic =request.FILES.get('image')

        employee.user.first_name = fn
        employee.user.last_name = ln
        employee.empcode = ec
        employee.empdept = dept
        employee.designation = designation
        employee.contact = contact
        employee.gender = gender
        employee.profile_image = profile_pic

        if jdate:
            employee.joiningdate = jdate




        print(fn, ln, ec, em, dept, designation, contact, jdate, gender)
        try:
            employee.save()
            employee.user.save()
            error = "no"
        except:
            error="yes"

    
    return render(request, 'employee/profile.html', locals())


@login_required(login_url='login')
def leaveApply(request):
    
    if request.method == 'POST':
        leave_type = request.POST['leave_type']
        s_d = request.POST['start_date']
        e_d = request.POST['end_date']
        res = request.POST['reason']
        print(leave_type, s_d, e_d, res)
       
        # Save the leave application data
        
        leave = Leave(
            employee=request.user,
            leave_type=leave_type,
            start_date=s_d,
            end_date=e_d,
            reason=res
        )
            
        leave.save()
        return HttpResponseRedirect("leaveApply")
    
    # Retrieve leave data for the current user
    leave_data = Leave.objects.filter(employee=request.user)
    #leave_data = Leave.objects.all()  ##its for all user data show in every page, this is not done 
    context = {
        "leave_data": leave_data,
        
    }

                   
    return render(request, 'employee/leaveApply_01.html', context)


def deleteLeave(request, id):
    leave = Leave.objects.get(id = id)
    leave.delete()
    return redirect('leaveApply')


def leave_report(request):
    leave_report = Leave.objects.all()
    pass