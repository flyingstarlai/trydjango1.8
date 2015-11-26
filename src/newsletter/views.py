from django.shortcuts import render
from .forms import ContactForm, SignUpForm
from django.core.mail import send_mail
from django.conf import settings
from .models import SignUp


def home(request):
    title = 'Sign Up Now'
    form = SignUpForm(request.POST or None)
    context = {
        'title': title,
        'form': form,
    }

    if form.is_valid():
        instance = form.save(commit=False)
        full_name = form.cleaned_data.get('full_name')
        if not full_name:
            full_name = "izayoi"
        instance.full_name = full_name
        instance.save()
        context = {
            'title': 'thank you %s' % instance.full_name,
        }

    if request.user.is_authenticated and request.user.is_staff:
        queryset = SignUp.objects.all().order_by('-timestamp')
        context = {
            'queryset': queryset,
        }

    return render(request, "home.html", context)


def contact(request):
    form = ContactForm(request.POST or None)
    title = 'Contact Us'
    title_align_center = True
    if form.is_valid():
        form_email = form.cleaned_data.get('email')
        form_message = form.cleaned_data.get('message')
        form_full_name = form.cleaned_data.get('full_name')
        # print email, message, full_name
        # for key, value in form.cleaned_data.iteritems():
        #     print key, value
        subject = 'Site contact form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, 'flyingstarlai@gmail.com']
        contact_message = form_message
        send_mail(subject,
                  contact_message,
                  from_email,
                  to_email,
                  fail_silently=False)

    context = {
        'form': form,
        'title': title,
        'title_align_center': title_align_center,
    }

    return render(request, "forms.html", context)
