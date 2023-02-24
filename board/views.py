from django.shortcuts import render,redirect
from .models import Board,Joinlook,SalaryRecord
from django.db.models import F, Sum, Count, Case, When
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from datetime import date, timedelta,datetime
from django.http import HttpResponse
import json
from acc.models import User

def index(request):
    if request.user.is_anonymous:
        return redirect("acc:login")
    b = Board.objects.all()
    b = b.order_by('date','hour','min')
    jl = Joinlook.objects.filter(board__isnull=False)

    cate = request.GET.get("cate", "")
    kw = request.GET.get("kw", "")
    f = request.GET.get("fdate")
    l = request.GET.get("ldate")

    if kw:
        if cate == "gn":
            if l :
                b = Board.objects.filter(date__range=(f,l),gn__startswith=kw)
            else:
                b = Board.objects.filter(date__range=(date.today() , date.today() + timedelta(days=60)),gn__startswith=kw)
                b = b.order_by('date','hour','min')
        elif cate == "cos":
            b = Board.objects.filter(course__startswith=kw)
            b = b.order_by('date','hour','min')
        elif cate == "ho":
            b = Board.objects.filter(hour__startswith=kw)
            b = b.order_by('date','hour','min')
        elif cate == "wri":
            try:
                from acc.models import User
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u)
                b = b.order_by('date','hour','min')
            except:
                b = Board.objects.none()
        elif cate == "con":
                jl2 = Joinlook.objects.filter(board__isnull=False).filter(j_name__startswith=kw)
                jl =Joinlook.objects.filter(board__isnull=False)
                b= []

                for j in jl2:
                    b.append(j.board.id)
                    
                b = list(set(b))

                b = Board.objects.filter(pk__in=b).order_by('date','hour','min')
    else:
        b = Board.objects.all()
        b = b.order_by('date','hour','min')
    
    if kw == "`":
            b = Board.objects.filter(date__range=(f , date.today() + timedelta(days=60)))
            b = b.order_by('date','hour','min')

    context = {
        "bset" : b,
        "p": jl,
        
    }

    return render(request,'board/index.html',context)

def book(request):
    if request.user.is_anonymous:
        return redirect("acc:login")
    b = Board.objects.all()
    b = b.order_by('date','hour','min')
    jl = Joinlook.objects.filter(board__isnull=False)
    context = {
        "bset" : b,
        "p": jl,
        
    }

    return render(request,'board/book.html',context)

def mybook(request):

    if request.user.is_anonymous:
        return redirect("acc:login")

    jl = Joinlook.objects.filter(board__isnull=False).filter(j_writer=request.user)
    jl2 =Joinlook.objects.filter(board__isnull=False)

    b= []

    for j in jl:
        b.append(j.board.id)
    
    b = list(set(b))

    b = Board.objects.filter(pk__in=b).order_by('date','hour','min')

    context = {
        "bset" : b,
        "p": jl2,
        
    }

    return render(request,'board/mybook.html',context)

def upbook(request):
    if request.user.is_anonymous:
        return redirect("acc:login")
    b = Board.objects.filter(writer=request.user)
    b = b.order_by('date','hour','min')
    jl = Joinlook.objects.filter(board__isnull=False)
    context = {
        "bset" : b,
        "p": jl,
        
    }

    return render(request,'board/upbook.html',context)

def create(request):
    if request.user.is_anonymous:
        return redirect("acc:login")

    if request.method == "POST":
        r = request.POST.get("rg")
        g = request.POST.get("gn")
        d = request.POST.get("cdate")
        c = request.POST.get("course")
        h = request.POST.get("hour")
        m = request.POST.get("min")
        b = request.POST.get("bname")
        p = request.POST.get("pee")
        s = request.POST.get("rq")
        me = request.POST.get("memo")
        try:
            Board(rg = r, gn = g , date = d , course = c  ,hour = h , min = m , bname = b , pee = p , rq = s , memo = me ,writer=request.user).save()
            return redirect("board:index")
        except:
            pass
    return render(request, "board/create.html")

def sell(request,bpk):
    b = Board.objects.get(id=bpk)
    jl = b.joinlook_set.all()
    context = {
        "r" : jl,
        "b" : b
    }
    if request.method == "POST":
        jn = request.POST.get("jname")
        jt = request.POST.get("jtag")
        jc = request.POST.get("jcall")

        joinlook = Joinlook(board = b,j_writer=request.user,j_name = jn,j_tag = jt,j_count = jc)

        if jt == "양도":
            b.join_count += 4
            joinlook.join_count = 4

            b.save()
        else:
            b.join_count += len(jt)

            joinlook.join_count = len(jt)
        
            b.save()
        
        
        joinlook.save()
        return redirect("board:index")

    return render(request, "board/sell.html",context)
def update(request,bpk):
    b = Board.objects.get(id=bpk)
    if request.method == "POST":
        if request.user == b.writer:
            r = request.POST.get("brg")
            g = request.POST.get("bgn")
            d = request.POST.get("bcdate")
            c = request.POST.get("bcourse")
            h = request.POST.get("bhour")
            m = request.POST.get("bmin")
            bn = request.POST.get("bbname")
            p = request.POST.get("bpee")
            s = request.POST.get("brq")
            me = request.POST.get("bmemo")
            b.rg,b.gn,b.date,b.course,b.hour,b.min,b.bname,b.pee,b.rq,b.memo = r,g,d,c,h,m,bn,p,s,me
            print(r,g,d,c,h,m,bn,p,s,me)
            b.save()
            return redirect('board:upbook')
    context = {
        "b" : b
    }

    return render(request,"board/update.html",context)   

def cancle(request,bpk):
    j = Joinlook.objects.get(id = bpk)
    b = j.board

    if request.method == "POST":
        j.delete()

        jt =  j.j_tag

        if jt == "양도":
            b.join_count -= 4
        else:
            b.join_count -= len(jt)
        
        b.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def tcancle(request,bpk):
    b = Board.objects.get(id=bpk)

    if request.method == "POST":

        b.delete()

    return redirect("board:upbook")

def mysell(request):
    if request.user.is_anonymous:
        return redirect("acc:login")
    
    b = Board.objects.filter(writer=request.user)
    b = b.order_by('date','hour','min')
    jl = Joinlook.objects.filter(board__isnull=False)
    exitSalaryRecord = SalaryRecord.objects.filter(user=request.user,year=datetime.now().year, month=datetime.now().month)
    if exitSalaryRecord.exists():
        salaryRecord = exitSalaryRecord[0]
    else:
        salaryRecord = {'price':0,'join_count':0}

    context = {
        "bset" : b,
        "p": jl,
        "salaryRecord": salaryRecord
        
    }

    return render(request,"board/mysell.html",context)

def deposit(request):
    if request.user.is_anonymous:
        return redirect("acc:login")
    
    joinlooks = Joinlook.objects.filter(deposit_request=True, deposit_status=False)
    refundJoinlooks = Joinlook.objects.filter(refund_request=True, deposit_status=True)

    context = {
        "joinlooks" : joinlooks,
        "refundJoinlooks" : refundJoinlooks
    }

    return render(request,"board/deposit.html",context)


def requestDeposit(request):
    if request.method == "POST":
        joinlook_id = request.POST['joinookId']
        joinlook=Joinlook.objects.get(id=joinlook_id)

        if joinlook.deposit_request ==False:
            joinlook.deposit_request = True
            message = "true"
        else:
            joinlook.deposit_request = False
            message = "false"
        joinlook.save()
        context = {'message': message,
                   }
        return HttpResponse(json.dumps(context), content_type="application/json")

def confirmDeposit(request):
    if request.method == "POST":
        joinlook_id = request.POST['joinookId']
        joinlook=Joinlook.objects.get(id=joinlook_id)

        joinlook.deposit_status = True
        joinlook.save()

        user = User.objects.get(id=joinlook.j_writer.id)
        user.sell_count += joinlook.join_count
        user.save()
        
        exitSalaryRecord = SalaryRecord.objects.filter(user=user,year=datetime.now().year, month=datetime.now().month)
        if exitSalaryRecord.exists():
            salaryRecord = exitSalaryRecord[0]
            if joinlook.board.gn == "파가니카":
                salaryRecord.price += 4000 * joinlook.join_count
            else:
                salaryRecord.price += 5000 * joinlook.join_count
            salaryRecord.join_count += joinlook.join_count
            
            
        else:
            salaryRecord = SalaryRecord(user=user,year=datetime.now().year, month=datetime.now().month)
            if joinlook.board.gn == "파가니카":
                salaryRecord.price = 4000 * joinlook.join_count
            else:
                salaryRecord.price = 5000 * joinlook.join_count
            salaryRecord.join_count = joinlook.join_count

        salaryRecord.save()

        message = "success"
        context = {'message': message,
                   }
        return HttpResponse(json.dumps(context), content_type="application/json")
    
def requestRefund(request):
    if request.method == "POST":
        joinlook_id = request.POST['joinookId']
        joinlook=Joinlook.objects.get(id=joinlook_id)

        if joinlook.refund_request == False:
            joinlook.refund_request = True
            message = "true"
        else:
            joinlook.refund_request = False
            message = "false"
        joinlook.save()
        context = {'message': message,
                   }
        return HttpResponse(json.dumps(context), content_type="application/json")
    
def confirmRefund(request):
    if request.method == "POST":
        joinlook_id = request.POST['joinookId']
        joinlook=Joinlook.objects.get(id=joinlook_id)

        joinlook.deposit_status = False
        joinlook.refund_request = False
        joinlook.deposit_request = False
        joinlook.save()

        user = User.objects.get(id=joinlook.j_writer.id)
        user.sell_count -= joinlook.join_count
        user.save()

        exitSalaryRecord = SalaryRecord.objects.get(user=user,year=datetime.now().year, month=datetime.now().month)
        if joinlook.board.gn == "파가니카":
            exitSalaryRecord.price -= 4000 * joinlook.join_count
        else:
            exitSalaryRecord.price -= 5000 * joinlook.join_count
        exitSalaryRecord.join_count -= joinlook.join_count
        exitSalaryRecord.save()

        message = "success"
        context = {'message': message,
                   }
        return HttpResponse(json.dumps(context), content_type="application/json")