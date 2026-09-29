from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Complains,StudentProfile
from .forms import CompalinForm,Login_form,OverviewForm
from django.contrib import messages
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import os
from django.db.models import Count, Q
import matplotlib.pyplot as plt
import seaborn as sns
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm



# Create your views here.
@login_required
def Complain_create(request):
      if request.method=='POST':
           form=CompalinForm(request.POST,request.FILES,user=request.user)
           if form.is_valid():
               complain1= form.save(commit=False)
               complain1.student=request.user
               spobj=StudentProfile.objects.get(user=request.user)
               complain1.branch=spobj.branch
               complain1.batch=spobj.batch
               complain1.Gender=spobj.gender
               complain1.save()
               messages.success(request,"Your Complaint Submited Sucessfully !")
               return redirect('home')
           else:
                messages.error(request,"Complaint Submission Failed !")
      form=CompalinForm(user=request.user)
      return render(request,'complain_Create.html',{'form':form})
@login_required
def profile_view(request):
    user=request.user
    try:
        sobj=get_object_or_404(StudentProfile,user=user)
        student_detail=[user.email,user.username,sobj.Roll,sobj.batch,sobj.gender,sobj.is_hosteler]
    except:
         student_detail=[user.email,user.username,None,None]
    pendings=len(Complains.objects.filter(status='Pending',student=user))
    Inprogess=len(Complains.objects.filter(status='In Progress',student=user))
    Resolved=len(Complains.objects.filter(status='Resolved',student=user))
    Rejected=len(Complains.objects.filter(status='Rejected',student=user))
    total = Complains.objects.filter(student=user).count()
    Complain_list=Complains.objects.filter(student=user)
    return render(request,"profile.html",{'student_detail':student_detail,'Complains':Complain_list,
     'pendings':pendings,'Inprogess':Inprogess,'Resolved':Resolved,'Rejected':Rejected,'Total':total})                                 
def login_view(request):
     if request.method=="POST":
          form=Login_form(request,data=request.POST)
          if form.is_valid():
               print("Form is valid")
               user=form.get_user()
               login(request,user)
               return redirect("home")
          else:
               print(form.errors)
     form=Login_form()
     return render(request,"registration/login.html",{'form':form})
@login_required
def edit_View(request,complaint_id):
     edit_complain=Complains.objects.get(id=complaint_id)
     if request.method=="POST":
          form=CompalinForm(request.POST, request.FILES, instance=edit_complain)
          if form.is_valid():
               form.save()
               messages.success(request,"Complaint edited successfully.")
               return redirect("profile")
          else:
               messages.error(request,"Failed to edit the complaint.")
     form=CompalinForm(instance=edit_complain)
     return render(request,'complain_Create.html',{'form':form})
@login_required
def delete_View(request,complaint_id):
    Complaint1=Complains.objects.get(id=complaint_id)
    Complaint1.delete()
    return redirect("profile")
@login_required
def logout_view(request):
     if request.method=="POST":
          logout(request)
          return redirect("home")
     return redirect("home")
def PrivacyPolicy(request):
     return render(request,"Privacy.html")
def Details(request,complaint_id):
     complaint=Complains.objects.get(id=complaint_id)
     if request.method=="POST":
         form=OverviewForm(request.POST,instance=complaint)
         if form.is_valid():
              form.save()
              messages.success(request,"Overview Submited Sucessfuly")
              return redirect("c_detail",complaint_id=complaint_id)
         else:
              messages.error(request, "Please correct the errors below.")
     form=OverviewForm(instance=complaint)
     return render(request,'details.html',{"complaint":complaint,"form":form})
def P_progress(request):
     pass
@login_required
def download_complaint_pdf(request, complaint_id):
     complaint=Complains.objects.get(id=complaint_id)
     response=HttpResponse(content_type="application/pdf")

     response['Content-Disposition']=(f'attachment;filename="Complaint_{complaint.complaint_id}.pdf"')
     doc=SimpleDocTemplate(response)
     styles=getSampleStyleSheet()
     story=[]
     story.append(
          Paragraph("Complaint Report",styles['Title'])
     )
     story.append(Spacer(1, 20))
     story.append(Paragraph(
          f"Complaint ID:{complaint.complaint_id}",
          styles['Normal']
     )
      )
     story.append(
    Paragraph(
        f"Category: {complaint.complaint_catagory}",
        styles['Normal']
    )
)
     story.append(
    Paragraph(
        f"Branch: {complaint.branch}",
        styles['Normal']
    )
)
     story.append(
    Paragraph(
        f"Batch: {complaint.batch}",
        styles['Normal']
    )
)
     story.append(
    Paragraph(
        f"Status: {complaint.status}",
        styles['Normal']
    )
)
     story.append(
         Paragraph(
             f"Gender: {complaint.Gender}",
             styles['Normal']
         )
     )
     story.append(
    Paragraph(
        f"Description: {complaint.description}",
        styles['Normal']
    )
)
     remark = complaint.remark or "No Remark"
     story.append(Paragraph(
    f"Remark: {remark}",
    styles['Normal']
    ))
     if complaint.image:
       img = Image(complaint.image.path)
       img.width = 300
       img.height = 200
       story.append(Spacer(1, 20))
       story.append(img)
     doc.build(story)
     return response
@login_required
def C_summery(request):

    student_profile = StudentProfile.objects.get(user=request.user)

    branch = student_profile.branch
    batch = student_profile.batch

    complaints = Complains.objects.filter(
        branch=branch,
        batch=batch
    ).count()

    Resolved_Complaints = Complains.objects.filter(
        branch=branch,
        batch=batch,
        status='Resolved'
    ).count()

    Pending_Complaints = Complains.objects.filter(
        branch=branch,
        batch=batch,
        status='Pending'
    ).count()

    In_progress_Complaint = Complains.objects.filter(
        branch=branch,
        batch=batch,
        status='In Progress'
    ).count()

    Rejected_Complaint = Complains.objects.filter(
        branch=branch,
        batch=batch,
        status='Rejected'
    ).count()


    # Academic complaints

    Academic_total = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Academic'
    ).count()

    Academic_resolved = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Academic',
        status='Resolved'
    ).count()

    Academic_pending = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Academic',
        status='Pending'
    ).count()

    Academic_inprogres = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Academic',
        status='In Progress'
    ).count()

    Academic_rejected = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Academic',
        status='Rejected'
    ).count()


    # Infrastructure complaints

    Infrastructure_total = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Infrastructure'
    ).count()

    Infrastructure_resolved = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Infrastructure',
        status='Resolved'
    ).count()

    Infrastructure_pending = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Infrastructure',
        status='Pending'
    ).count()

    Infrastructure_inprogres = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Infrastructure',
        status='In Progress'
    ).count()

    Infrastructure_rejected = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Infrastructure',
        status='Rejected'
    ).count()


    # Library complaints

    Library_total = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Library'
    ).count()

    Library_resolved = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Library',
        status='Resolved'
    ).count()

    Library_pending = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Library',
        status='Pending'
    ).count()

    Library_inprogres = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Library',
        status='In Progress'
    ).count()

    Library_rejected = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Library',
        status='Rejected'
    ).count()


    # Hostel complaints

    Hostel_total = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Hostel'
    ).count()

    Hostel_resolved = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Hostel',
        status='Resolved'
    ).count()

    Hostel_pending = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Hostel',
        status='Pending'
    ).count()

    Hostel_inprogres = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Hostel',
        status='In Progress'
    ).count()

    Hostel_rejected = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Hostel',
        status='Rejected'
    ).count()


    # Transport complaints

    Transport_total = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Transport'
    ).count()

    Transport_resolved = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Transport',
        status='Resolved'
    ).count()

    Transport_pending = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Transport',
        status='Pending'
    ).count()

    Transport_inprogres = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Transport',
        status='In Progress'
    ).count()

    Transport_rejected = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Transport',
        status='Rejected'
    ).count()


    # Fees & Accounts complaints

    FeesandAccounts_total = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Fees & Accounts'
    ).count()

    FeesandAccounts_resolved = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Fees & Accounts',
        status='Resolved'
    ).count()

    FeesandAccounts_pending = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Fees & Accounts',
        status='Pending'
    ).count()

    FeesandAccounts_inprogres = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Fees & Accounts',
        status='In Progress'
    ).count()

    FeesandAccounts_rejected = Complains.objects.filter(
        branch=branch,
        batch=batch,
        complaint_catagory='Fees & Accounts',
        status='Rejected'
    ).count()


    # Pie chart data

    labels = [
        'Resolved',
        'Pending',
        'In Progress',
        'Rejected'
    ]

    values = [
        Resolved_Complaints,
        Pending_Complaints,
        In_progress_Complaint,
        Rejected_Complaint
    ]


    # Remove statuses whose value is 0

    chart_data = [
        (label, value)
        for label, value in zip(labels, values)
        if value > 0
    ]


    chart_path = os.path.join(
        settings.BASE_DIR,
        'static',
        'images',
        f'{branch}_{batch}.png'
    )


    # Generate chart only when complaints exist

    if chart_data:

        chart_labels = [item[0] for item in chart_data]

        chart_values = [item[1] for item in chart_data]


        plt.figure(figsize=(6, 6))

        plt.pie(
            chart_values,
            labels=chart_labels,
            autopct='%1.1f%%',
            startangle=90
        )

        plt.title('Complaint Status')

        plt.tight_layout()

        plt.savefig(chart_path)

        plt.close()


    return render(
        request,
        'complaint_Summary.html',
        {
            'branch': branch,
            'batch': batch,
            'complaints': complaints,

            'Resolved_Complaints': Resolved_Complaints,
            'Pending_Complaints': Pending_Complaints,
            'In_progress_Complaint': In_progress_Complaint,
            'Rejected_Complaint': Rejected_Complaint,

            'Academic_total': Academic_total,
            'Academic_resolved': Academic_resolved,
            'Academic_pending': Academic_pending,
            'Academic_inprogres': Academic_inprogres,
            'Academic_rejected': Academic_rejected,

            'Infrastructure_total': Infrastructure_total,
            'Infrastructure_resolved': Infrastructure_resolved,
            'Infrastructure_pending': Infrastructure_pending,
            'Infrastructure_inprogres': Infrastructure_inprogres,
            'Infrastructure_rejected': Infrastructure_rejected,

            'Library_total': Library_total,
            'Library_resolved': Library_resolved,
            'Library_pending': Library_pending,
            'Library_inprogres': Library_inprogres,
            'Library_rejected': Library_rejected,

            'Hostel_total': Hostel_total,
            'Hostel_resolved': Hostel_resolved,
            'Hostel_pending': Hostel_pending,
            'Hostel_inprogres': Hostel_inprogres,
            'Hostel_rejected': Hostel_rejected,

            'Transport_total': Transport_total,
            'Transport_resolved': Transport_resolved,
            'Transport_pending': Transport_pending,
            'Transport_inprogres': Transport_inprogres,
            'Transport_rejected': Transport_rejected,

            'FeesandAccounts_total': FeesandAccounts_total,
            'FeesandAccounts_resolved': FeesandAccounts_resolved,
            'FeesandAccounts_pending': FeesandAccounts_pending,
            'FeesandAccounts_inprogres': FeesandAccounts_inprogres,
            'FeesandAccounts_rejected': FeesandAccounts_rejected,
            'chart_filename': f'{branch}_{batch}.png',
        }
    )
@login_required
def change_password(request):
    if request.method=="POST":
        form=PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
             user=form.save()
             update_session_auth_hash(request, user)
             messages.success(
                request,
                "Your password has been changed successfully!"
            )
             return redirect('profile')
        else:
             messages.error(request,"Please correct the Error Below")
    else:
         form=PasswordChangeForm(request.user)
    return render(
        request,
        'changepassword.html',
        {'form': form}
    )