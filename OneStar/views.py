#coding: utf8
from django.shortcuts import render
from django.shortcuts import render_to_response,RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission,User
import django.contrib.auth.context_processors
import NineStars.runOrder
import json
import time
from django.http import HttpResponse
from OneStar.models import ProjectList
from OneStar.setupdb import dbUpdate
import subprocess
# Create your views here.

@login_required
def index(request):
    """
    if use about perms like this :
        {% if perms.OneStar.can_view %}
            some test context
        {% endif %}
    needs to add context_instance=RequestContext(request) to {}.
    example :
        return render_to_response('index.html',{'user': request.user},context_instance=RequestContext(request))
    """
    return render_to_response('index.html',{'user': request.user},context_instance=RequestContext(request))

@login_required()
def test(request):
    if request.method == 'POST':
        #print request.POST.getlist('SLan')[0]
        dragonball = request.POST.get('DBsh')

        if dragonball == "Cdban":
            Slist = " ".join(request.POST.getlist('SLan'))
            Cdban_cmd = "python /data/makepack/dban.py {0}".format(Slist)
            Cdban = NineStars.runOrder.Order('192.168.1.213', 'ssh-salt', cmd=Cdban_cmd)
            Cdban_out = Cdban.ssh_connect(request.user.username)
            return render_to_response('test.html', {'user': request.user, 'test':Cdban_out},context_instance=RequestContext(request))
        elif dragonball == "Cdbios":
            Slist = " ".join(request.POST.getlist('SLios'))
            Cdbios_cmd = "python /data/makeiospack/dbios.py {0}".format(Slist)
            Cdbios = NineStars.runOrder.Order('192.168.1.213', 'ssh-salt', cmd=Cdbios_cmd)
            Cdbios_out = Cdbios.ssh_connect(request.user.username)
            return render_to_response('test.html', {'test':Cdbios_out},context_instance=RequestContext(request))
        elif dragonball == "Cdbiosbg":
            Slist = " ".join(request.POST.getlist('SLiosbg'))
            Cdbiosbg_cmd = "python /data/makeios-bgpack/dbiosbg.py {0}".format(Slist)
            Cdbiosbg = NineStars.runOrder.Order('192.168.1.213', 'ssh-salt', cmd=Cdbiosbg_cmd)
            Cdbiosbg_out = Cdbiosbg.ssh_connect(request.user.username)
            return render_to_response('test.html', {'test':Cdbiosbg_out},context_instance=RequestContext(request))
        elif dragonball == "Udban":
            Utemp = []
            for i in request.POST.getlist('SLan'):
                Udban_cmd = "salt 'dban' newup.update 'android' '{0}' 'all=True' 'test=True'  --out=csv".format(i)
                Udban = NineStars.runOrder.Order('192.168.1.213', 'ssh-salt', cmd=Udban_cmd)
                Udban_out = Udban.ssh_connect(request.user.username)
                Utemp+=Udban_out
            return render_to_response('test.html', {'test':Utemp},context_instance=RequestContext(request))
        elif dragonball == "Udbios":
            Utemp = []
            for i in request.POST.getlist('SLios'):
                Udbios_cmd = "salt 'dbios' newup.update 'ios' '{0}' 'all=True' 'test=True'  --out=csv".format(i)
                Udbios = NineStars.runOrder.Order('192.168.1.213', 'ssh-salt', cmd=Udbios_cmd)
                Udbios_out = Udbios.ssh_connect(request.user.username)
                Utemp+=Udbios_out
            return render_to_response('test.html', {'test':Utemp},context_instance=RequestContext(request))
        elif dragonball == "Udbiosbg":
            Utemp = []
            for i in request.POST.getlist('SLiosbg'):
                Udbiosbg_cmd = "salt 'dbiosbg' newup.update 'iosbg' '{0}' 'all=True' 'test=True'  --out=csv".format(i)
                Udbiosbg = NineStars.runOrder.Order('192.168.1.213', 'ssh-salt', cmd=Udbiosbg_cmd)
                Udbiosbg_out = Udbiosbg.ssh_connect(request.user.username)
                Utemp+=Udbiosbg_out
            return render_to_response('test.html', {'test':Utemp},context_instance=RequestContext(request))
        elif dragonball == "Udbansql":
            Utemp = []
            for i in request.POST.getlist('SLan'):
                Udbansql_cmd = "salt 'dban' newup.update 'android' '{0}' 'test=True'  --out=csv".format(i)
                Udbansql = NineStars.runOrder.Order('192.168.1.213', 'ssh-salt', cmd=Udbansql_cmd)
                Udbansql_out = Udbansql.ssh_connect(request.user.username)
                Utemp+=Udbansql_out
            return render_to_response('test.html', {'test':Utemp},context_instance=RequestContext(request))
        elif dragonball == "Udbiossql":
            Utemp = []
            for i in request.POST.getlist('SLios'):
                Udbiossql_cmd = "salt 'dbios' newup.update 'ios' '{0}' 'test=True'  --out=csv".format(i)
                Udbiossql = NineStars.runOrder.Order('192.168.1.213', 'ssh-salt', cmd=Udbiossql_cmd)
                Udbiossql_out = Udbiossql.ssh_connect(request.user.username)
                Utemp+=Udbiossql_out
            return render_to_response('test.html', {'test':Utemp},context_instance=RequestContext(request))
        elif dragonball == "Udbiosbgsql":
            Utemp = []
            for i in request.POST.getlist('SLiosbg'):
                Udbiosbgsql_cmd = "salt 'dbiosbg' newup.update 'iosbg' '{0}' 'test=True'  --out=csv".format(i)
                Udbiosbgsql = NineStars.runOrder.Order('192.168.1.213', 'ssh-salt', cmd=Udbiosbgsql_cmd)
                Udbiosbgsql_out = Udbiosbgsql.ssh_connect(request.user.username)
                Utemp+=Udbiosbgsql_out
            return render_to_response('test.html', {'test':Utemp},context_instance=RequestContext(request))
        elif dragonball == "Ures":
            Ures_cmd1 = "salt 'resource-server' cmd.run 'svn up /usr/local/dbonline/UpdateServer/resources/dbu2/' && "
            Ures_cmd2 = "salt 'resource-server' cmd.run 'svn up /usr/local/dbonline/UpdateServer/resources/iosdbu/' "
            Ures_cmd = Ures_cmd1 + Ures_cmd2
            Ures = NineStars.runOrder.Order('192.168.1.213', 'ssh-salt', cmd=Ures_cmd)
            Ures_out = Ures.ssh_connect(request.user.username)
            return render_to_response('test.html', {'test':Ures_out},context_instance=RequestContext(request))
        else:
            return render_to_response('test.html', {'test':['your web code is error']})

    else:
        return render_to_response('test.html',{'user': request.user},context_instance=RequestContext(request))


FIB=[0,1]
def jqqo():
    global FIB
    FIB.append(FIB[-1] + FIB[-2])
    return FIB

def jqq(request):
    return render_to_response("dist/page/index.html", { 'fib_sequence' : [0,1] })

def jqqoo(request):
    fib_sequence = jqqo()
    return render_to_response("dist/page/fib.html",{ 'fib_sequence' : fib_sequence })

def ref(request):
    res = time.time()
    return render_to_response("ref.html", { 'res':res })

def refp(request):
    #res = time.time()
    with open('/NineStars/OneStar/one','r') as f:
        res = f.readlines()
    return HttpResponse(res,{"xx":"xx"})

def dsearch(request):
    #A=ProjectList.objects.values()
    A1=ProjectList.objects.filter(id=1)
    print A1[0].workdir
    #A1=ProjectList.objects.all()
    CF="com/huayi/djgame2/dragonball/common/config/system/"
    #make output dir
    TargetDir='/data/DB/DBAndroid/'
    #make output sub dir
    SerTag='db'
    #make a distinction between android and ios platform.
    MPlat='android'
    #make package source dir
    WorkDir="/data/shell/servertest/"
    #update about new jar and rename.
    subprocess.Popen('svn up', shell=True, cwd=WorkDir).communicate()
    subprocess.Popen('cp serverB.jar r-server.jar', shell=True, cwd=WorkDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    #print ConfigList
    for i in [1,2,3,4]:
        print "{0}-{1}-{2}".format(MPlat, SerTag, i)
        ConfigList={'ConfigFile':'PortConfigure.conf','CF':CF,'sId':i,'TDIR':TargetDir,'UDIR':CF,'STag':SerTag,'A_I':MPlat,'WDir':WorkDir}

        dbUpdate.Update_Jar(ConfigList)
    #A = A1.values()
    return render_to_response("dsearch.html", {'A':A1})

