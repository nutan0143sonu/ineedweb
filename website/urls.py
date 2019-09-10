
from django.conf.urls import url

from .views import *

app_name = 'website'


urlpatterns = [
    # USER REGISTRATION 
    url(r'^register-email/$', RegisterEmailView.as_view()),
    url(r'signup/$', SignUpView.as_view()),
    url(r'^email-verify/(?P<uidb64>[0-9A-Za-z_\-]+)/$', EmailVerifyView.as_view()),
    url(r'^image-upload/$',ImageUploadView.as_view()),
    url(r'^update-image/$',UpdateImage.as_view()),


    # employer singup
    url(r"^employer-singup/$",EmployerSignUpView.as_view()),
    url(r"^employer-profile/$",EmployerProfile.as_view()),


    #User Login
    url(r'^login/$', LoginView.as_view()),

    #User Change Password
    url(r'^change-password/$',ChangePasswordView.as_view()),

    #User complete Profile
    url(r'^profile/$',ProfileView.as_view()),
    url(r'^job-seeker-edit-profile-step1/$',JobSeekerEditProfileStep1.as_view()),
    url(r'^job-seeker-edit-profile-step2/$',JobSeekerEditProfileStep2.as_view()),
    url(r'^job-seeker-edit-profile-step3/$',JobSeekerEditProfileStep3.as_view()),



    #Forgot Password
    url(r'^forget/$', ForgetPasswordView.as_view()),
    url(r'^reset-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<time>[0-9A-Za-z_\-]+)/$', ResetPasswordView.as_view()),

    #Get api
    url(r'^industry/$', IndustryView.as_view()),
    url(r'^area/$', AreaView.as_view()),
    url(r'^tools-and-language/$', ToolsAndLanguageView.as_view()),

    #User Availability abd Location
    url(r"^working-hour/$",WorkingHourView.as_view()),
    url(r"^availability-location/$",AvailabilityAndLocationView.as_view()),
    url(r"^get-availability-location/$",GetAvailabilityAndLocationView.as_view()),


   #User Employment history
    url(r"^employment-history/$",EmploymentHistoryView.as_view()),
    url(r"^employment-history-delete/$",EmploymentHistoryDeleteView.as_view()),
    url(r"^get-employment-history/$",GetEmploymentHistoryView.as_view()),
    
    #User Education history
    url(r"^user-education/$",UserEducationView.as_view()),
    url(r"^user-education-delete/$",UserEducationDeleteView.as_view()),
    url(r"^get-user-education/$",GetUserEducationView.as_view()),
   
   #User Speaking language
    url(r"^user-language/$",UserLanguageView.as_view()),
    url(r"^get-user-language/$",GetUserLanguageView.as_view()),
    
    #user Personal detail
    url(r"^language/$",SpeakingLanguageView.as_view()),
    
    #Post Job
    url(r"^post-job-step1/$",PostJobView.as_view()),
    url(r"^post-job-step2/$",PostJobStep2.as_view()),
    url(r"^post-job-step3/$",PostJobStep3.as_view()),
    url(r"^post-job-step4/$",PostJobStep4.as_view()),
    #Get Employer Posted Job
    url(r"^get-posted-job/$",GetPostedJobView.as_view()),
    url(r"^get-single-posted-job/$",SinglePostedJobView.as_view()),
    url(r"^delete-single-posted-job/$",SinglePostedJobDeletion.as_view()),

     #Edit Post Job
    url(r"^edit-post-job-step1/$",EditPostedJobStep1.as_view()),

    #notification
    url(r"^notification-get/$",NotificationAllGet.as_view()),
    url(r"^notification-seen/$",NotificationSeen.as_view()),
    url(r"^get-single-notification/$",GetSingleNotification.as_view()),

    #salary
    url(r"^salary/$",SalaryPerHourView.as_view()),

    #Location
    url(r"^location/$",LocationView.as_view()),

    #Matching Job
    url(r"^matching-job/$",MatchingJob.as_view()),

    #user favourite Job
    url(r"^user-favourite/$",UserFavouriteJobView.as_view()),
    url(r"^get-user-favourite/$",GetUserFavouriteJobView.as_view()),

    
    #User Apply
    url(r"^user-apply-job/$",UserApplyJobView.as_view()),
    url(r"^user-apply-job-resume/$",UserResumeUploadView.as_view()),

    #User Applied Job
    url(r"^user-applied-job/$",UserAppliedJob.as_view()),


    #Employer Active Job
    url(r"^employer-active-job/$",EmployerActiveJob.as_view()),

    #Employer job Applicant
    url(r"^employer-job-applicant/$",EmployerJobApplicant.as_view()),
    url(r"^all-applicant-of-posted-job/$",AllApplicantOfPostedJob.as_view()),

    #Chat
    url(r"^accept-applicant/$",ApplicationAcceptance.as_view()),
    # url(r"^chat/$",MessageView.as_view()),
    url(r"^attachment-chat/$",MessageAttachment.as_view()),
    url(r"^get-chat/$",GetMessageView.as_view()),
    url(r"^get-all-acceped-applicant/$",GetallMessage.as_view()),

    #Employer Profile editing
    url(r"^user_company_edit/$",UserCompanyEditView.as_view()),
    url(r"^user_company_industry_edit/$",UserIndustryEditView.as_view()),

    #jobseeker job
    url(r"^employer-approved-job/$",EmployerApprovedJob.as_view()),
    url(r"^get-job-seeker-active-job/$",GetUserActiveJob.as_view()),
    url(r"^post-job-seeker-complete-job/$",JobSeekerCompletedJob.as_view()),
    url(r"^get-job-seeker-pending-job/$",JobSeekerPendingJob.as_view()),
    url(r"^get-job-seeker-complete-job/$",JobSeekerCompletedJobView.as_view()),
    
    #employer Complete Job
    url(r"^post-employer-complete-job/$",EmployerCompleteJobForJobSeeker.as_view()),
    url(r"^get-employer-complete-job$",EmployerCompleteJob.as_view()),

    #Top Skill
    url(r"^top-skill-jobseeker/$",TopSkillJobSeekerView.as_view()),
    url(r"^top-skill-company/$",TopSkillCompanyView.as_view()),

    #ContactUs
    url(r"^post-contact-us/$",PostContactUsView.as_view()),
    
    #Lokking for
    url(r"^jobseeker/$",JobSeekerView.as_view()),
    url(r"^company/$",CompanyView.as_view()),

    #Top 10 Company
    url(r"^top-10-company/$",Top10Company.as_view()),
    url(r"^top-10-jobseeker/$",Top10JobSeeker.as_view()),


    #Invite People
    url(r"^invite/$",Invite.as_view()),

    url(r"^job-seeker-testing/$",JobSeekerTestingView.as_view()),

    #paypal
    url(r'^paypals',PayPal.as_view()),
    url(r'^execute',Excute.as_view()),
    url(r'^cancel',Cancel.as_view()),




]