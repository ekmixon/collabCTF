import json
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve, Resolver404, NoReverseMatch, reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.http import require_safe, require_POST, require_GET
import sys

from collabCTF.tools import crypto
from competition.forms import HashForm, RotForm, BaseConversionForm, XorForm, RegistrationForm, LoginForm
from competition.models import Competition


def home(request):
    return render_to_response('index.html')


def profile(request):
    return render_to_response('profile.html')


def settings(request):
    return render_to_response('settings.html')


def about(request):
    return render_to_response('about.html')


def ctfoverview(request):
    return render_to_response('ctf/overview.html')


def ctfchallenge(request):
    return render_to_response('ctf/challenge/overview.html')


@require_safe
def reports(request):
    data = {
        'ctfs': Competition.objects.order_by('-start_time')
    }
    return render_to_response('reports.html', data, RequestContext(request))


def about(request):
    return render_to_response('about.html')


def profile(request):
    return render_to_response('profile.html')


def settings(request):
    return render_to_response('settings.html')


@require_GET
def sidebar(request):
    url = request.GET.get('url', None)
    if url is not None:
        try:
            resolved = resolve(url)
            view_name = resolved.view_name
        except (Resolver404, NoReverseMatch):
            view_name = 'index'
    else:
        view_name = 'index'
    data = {
        'ctfs': Competition.objects.prefetch_related('challenges'),
        'view_name': view_name,
        'url': url
    }

    return render_to_response('sidebar.html', data)


@require_safe
def ctf_tools(request):
    data = {
        'hash_form': HashForm(),
        'rot_form': RotForm(),
        'base_conversion_form': BaseConversionForm(),
        'xor_form': XorForm()
    }
    return render_to_response('ctftools.html', data, RequestContext(request))


def register(request):
    if request.method == 'GET':
        form = RegistrationForm()
        data = {
            'register_form': form
        }
        return render_to_response('register.html', data, RequestContext(request))

    elif request.method == 'POST':
        form = RegistrationForm(request.POST)
        data = {
            'form': form
        }

        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            data['user'] = user
            return redirect(reverse('index'))

        return render_to_response('register.html', data, RequestContext(request))

@require_safe
def login(request):
    data = {
        'login_form': LoginForm()
    }

    return render_to_response('login.html', data, RequestContext(request))

@require_POST
def hash_val(request):
    form = HashForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        value = cd['value']
        if sys.version_info.major == 3:
            value = value.encode('utf8')

        jdata = json.dumps({
            'result': crypto.hash(cd['hash_type'], value)
        })
        return HttpResponse(jdata, content_type='application/json')

    else:
        jdata = json.dumps({
            'error': form.errors
        })
        return HttpResponseBadRequest(jdata, content_type='application/json')


@require_POST
def rot_val(request):
    form = RotForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        jdata = json.dumps({
            'result': crypto.rot(cd['rot_type'], cd['value'], cd['encode'])
        })
        return HttpResponse(jdata, content_type='application/json')
    else:
        jdata = json.dumps({
            'error': form.errors
        })
        return HttpResponseBadRequest(jdata, content_type='application/json')


@require_POST
def base_conversion_val(request):
    form = BaseConversionForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        jdata = json.dumps({
            'result': crypto.base_conversions(cd['value'], cd['base'], cd['currBase'])
        })
        return HttpResponse(jdata, content_type='application/json')
    else:
        jdata = json.dumps({
            'error': form.errors
        })
        return HttpResponseBadRequest(jdata, content_type='application/json')


@require_POST
def xor_val(request):
    form = XorForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        jdata = json.dumps({
            'result': crypto.xor_tool(cd['value'], cd['key'])
        })
        return HttpResponse(jdata, content_type='application/json')
    else:
        jdata = json.dumps({
            'error': form.errors
        })
        return HttpResponseBadRequest(jdata, content_type='application/json')
