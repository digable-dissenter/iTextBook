# Create your views here.
import subprocess
from string import join
from PIL import Image as PImage
from os.path import join as pjoin
import os
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


def readfile(request):
    """Main listing."""
    proc = subprocess.Popen("python /home/julian/itextbook/box/test.py", shell=True, stdout=subprocess.PIPE)
    script_response = proc.stdout.read()
    return render_to_response("box/sandbox.html", dict(script_response=script_response))


def readvar(request):
    """Main listing."""
    sum = "Julz"
    proc = subprocess.Popen('echo' + sum, shell=True, stdout=subprocess.PIPE)
    script_response = proc.stdout.read()
    return render_to_response("box/sandbox.html", dict(script_response=script_response))


def controlflow(request):
    proc = subprocess.Popen("python /home/julian/itextbook/box/if.py", shell=True, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # script_response = proc.stdout.read()
    # add if it work
    script_response = proc.communicate(input='2')[0]
    return render_to_response("box/sandbox.html", dict(script_response=script_response))


def jreadfile(request):
    """Main listing."""
    proc = subprocess.Popen("javac /home/julian/itextbook/box/HelloWorld.java", shell=True, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    proc1 = subprocess.Popen("java /home/julian/itextbook/box/HelloWorld.jar", shell=True, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    script_response = proc1.stdout.read()
    return render_to_response("box/sandbox.html", dict(script_response=script_response))


def createfile(request):
    # Let's create a file and write it to disk. should use student name and incremental number
    file_name = "jj.py"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(script_dir, 'submissions')
    try:
        os.makedirs(dest_dir)
    except OSError:
        pass  # already exists
    path = os.path.join(dest_dir, file_name)
    # Let's create some data:
    namelist = "Julian"
    # Create a file object:
    # in "write" mode
    FILE = open(path, "w")
    # Write all the lines at once:
    FILE.writelines(namelist)
    # Alternatively write them one by one:
    # for name in namelist:
    #	FILE.write(name)
    FILE.close()
    script_response = file_name + " created successfully"
    return render_to_response("box/sandbox.html", dict(script_response=script_response))
