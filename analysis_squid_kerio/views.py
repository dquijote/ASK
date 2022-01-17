import datetime
import math

from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import LogsKerio, LogsSquid, BlackListDomain, SliceTmp, LogsSquidTmp

from .form import filter_userForm, FilterIncidenceForm

# Create your views here.


def index(request):

    #return render(request, 'index.html')
    return render(request, 'analysis_squid_kerio/ask-index.html')


# Convert date to python format
def convert_date(date):
    month = date[0:2]
    day = date[3:5]
    year = date[6:]
    print((int(day)))
    print((int(month)))
    print((int(year)))

    print("day: " + day + "month: " + month + "year: " + year)
    python_date = datetime.date(int(year), int(month), int(day))
    return python_date





def report(request):
    query = LogsSquid.objects.all()[:5]
    query_kerio = LogsKerio.objects.all()[:5]
    context = {'query': query,
               'query_kerio':query_kerio}

    return render(request, 'analysis_squid_kerio/ask_tables.html', context)


def sortList(e):
    return e['ip_client']


# Show the diferent filter choose for the user
def report_filter(request):

    # Control to look for incidence
    incidence_ctrl = request.GET.get('incidence_ctrl')
    # Control to look for individual user incidence
    user_ctrl = request.GET.get('user_ctrl')
    #print("------ user control:" + user_ctrl)

    # if request.method == 'POST':        #create a form instance and populate it with data from the request:
    form = filter_userForm()

    #if filter_userForm(request.GET):
    # if form.is_valid():
    #     user_cell = form.cleaned_data['user_cell']
    #     date_start = form.cleaned_data['date_start']
    #     date_end = form.cleaned_data['date_end']
    form = filter_userForm(request.GET)
    userIncidenceForm = FilterIncidenceForm(request.GET)

    StartDateIncidence = request.GET.get('StarIncidence')
    EndDateIncidence = request.GET.get('EndIncidence')
    print("EndDateIncidence: " + str(EndDateIncidence) + "and typy:" + str(type(EndDateIncidence)))
    if request.GET.get('EndIncidence') is not None:
        StartDateIncidence = convert_date(request.GET.get('StarIncidence'))
    if EndDateIncidence is not None:
        EndDateIncidence = convert_date(request.GET.get('EndIncidence'))

    user_cell = request.GET.get('user_cell')
    date_start = request.GET.get('date_start')
    date_end = request.GET.get('date_end')
    print("type of date_end" + str(type(date_end)))
    if date_start is not None:
        date_start = convert_date(request.GET.get('date_start'))
    if date_end is not None:
        date_end = convert_date(request.GET.get('date_end'))


    page = request.GET.get('page')
    up_bl = request.GET.get('up_bl')
    down_bl = request.GET.get('down_bl')

    allBlackList = BlackListDomain.objects.all()

    # Next iteration in the black list
    slice_get = SliceTmp.objects.get(pk=1)
    if up_bl is not None:
        black_list_slice =BlackListDomain.objects.all()
        if black_list_slice.count()/slice_get.multiplier > slice_get.step:
            slice_get.start = slice_get.start + slice_get.multiplier
            slice_get.end = slice_get.end + slice_get.multiplier
            slice_get.step = slice_get.step + 1
            slice_get.save()
            print("-------Page is None, the step is up")
            print("-------Black list total:" + str(black_list_slice.count()))
            print("-------Black list / multiplier:" + str(black_list_slice.count()/slice_get.multiplier))
    if down_bl is not None:
        if slice_get.end > slice_get.multiplier:
            slice_get.start = slice_get.start - slice_get.multiplier
            slice_get.end = slice_get.end - slice_get.multiplier
            slice_get.step = slice_get.step - 1
            slice_get.save()
            print("-------In the slice, step is down")




    query = []
    query_kerio = []

    list_incidence_squid_user = []
# user_cell is not None and date_start is not None and

    if user_ctrl == 'active':
        print("----user control is active inside of if user_ctrl")
        query_user = LogsSquid.objects.filter(ip_client__contains=user_cell).filter(date_time__range=(date_start, date_end))

        log_squid_tmp = LogsSquidTmp()

        black_list_to_user = BlackListDomain.objects.all()[SliceTmp.objects.get(pk=1).start:SliceTmp.objects.get(pk=1).end]

        for bl in black_list_to_user:
            print("-------black objet in user:" + str(bl.domain))
            contains_incidence_user = query_user.filter(url__contains=bl.domain).order_by('date_time')
            if contains_incidence_user.count() > 0:
                for obj_s in contains_incidence_user:
                    log_squid_tmp = obj_s
                    log_squid_tmp.save()
                    #list_incidence_squid_user.append(obj_s)
                    print("--------obj_s:" + str(obj_s))

    # Look for incidence into the logs squid
    queryIncidenceSquid = []
    queryIncidenceKerio = []

    # Reset first time load
    if StartDateIncidence is None and page is None and user_cell is None and date_start is None:
        sliceResetFirstLoad = SliceTmp.objects.get(pk=1)
        sliceResetFirstLoad.start = 0
        sliceResetFirstLoad.end = sliceResetFirstLoad.multiplier
        sliceResetFirstLoad.step = 1
        sliceResetFirstLoad.save()

    list_incidence_squid = []
    list_incidence_kerio = []
    print("-------incidence ctrl: " + str(incidence_ctrl))
    print("-------StartDateIncidence: " + str(StartDateIncidence))
    if StartDateIncidence is not None and incidence_ctrl == 'active':
        query_squid = LogsSquid.objects.filter(date_time__range=(StartDateIncidence, EndDateIncidence))
        query_kerio = LogsKerio.objects.filter(date_time__range=(StartDateIncidence, EndDateIncidence))
        # [:SliceTmp.objects.get().end]
        # [:SliceTmp.objects.get().end]

        b_list = BlackListDomain.objects.all()
        slice = SliceTmp.objects.get(pk=1)

        blackListDomain = BlackListDomain.objects.all()[SliceTmp.objects.get(pk=1).start:SliceTmp.objects.get(pk=1).end]

        print("------slice inicio:" + str(SliceTmp.objects.get(pk=1).start))
        print("------slice fin:" + str(SliceTmp.objects.get(pk=1).end))



        #Reset entity slice
        if b_list.count()/slice.multiplier < slice.step:
            slice.start = 0
            slice.end = slice.multiplier
            slice.step = 0
            slice.save()


        list_tmp_incidence = []

        #print("-------many of query_squid:" + str(query_squid.count()))
        # print("-------many of query_kerio:" + str(query_kerio.count()))


        for bl in blackListDomain:
            print("-------black objet:" + str(bl.domain))
            contains_incidence = query_squid.filter(url__contains=bl.domain).order_by('ip_client')
            if contains_incidence.count() > 0:
                for obj_s in contains_incidence:
                    log_squid_tmp = obj_s
                    log_squid_tmp.save()
                    print()
                    #list_incidence_squid.append(obj_s)



    # Paginator Squid User
    #if user_ctrl == 'active':
    paginator = Paginator(list_incidence_squid_user, 35)
    print("-----------list_incidence_squid_user: " + str(list_incidence_squid_user))

    # Paginator Squid
    if incidence_ctrl == 'active':
        paginator = Paginator(list_incidence_squid, 35)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj_squid = paginator.get_page(page_number)
    #print("----page_obj_squid:" + str(page_obj_squid.next_page_number()))

    print("-----page_obj_squid.object_list(): " + str(page_obj_squid.__len__()))


    # Paginator Kerio
    paginator = Paginator(list_incidence_kerio, 35)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj_kerio = paginator.get_page(page_number)

    #print("--------Next page squid: " + str(page_obj_squid.next_page_number()))
    print("--------Page:" + str(page_number))
    print("--------StartDateIncidence:" + str(StartDateIncidence))
    print("--------EndDateIncidence:" + str(EndDateIncidence))
    #print("--------list kerio:" + str(page_obj_kerio.__len__()))
    if page_obj_squid.has_next():
        print("--------Paginator next page: " + str(page_obj_squid.next_page_number()))
    else:
        print("There are not next page")
        print("+++ page_obj_squid.has_next() is None: " + str(page_obj_squid.has_next()))


    # 59981255
    result_query = {}


    # redirect to a new URL:
    return render(request, 'analysis_squid_kerio/ask_tables_filter.html', {'form': form,
                                                                           'user_ctrl': user_ctrl,
                                                                           'incidence': userIncidenceForm,
                                                                           'user_cell': user_cell,
                                                                           'date_start': date_start,
                                                                           'date_end': date_end,
                                                                           'incidence_ctrl': incidence_ctrl,
                                                                           'StartDateIncidence': StartDateIncidence,
                                                                           'EndDateIncidence': EndDateIncidence,
                                                                           #'query': query,
                                                                           'query': page_obj_squid,
                                                                           'query_kerio': page_obj_kerio,
                                                                           'step': slice_get.step,
                                                                           'totalIter': math.floor(allBlackList.count()/slice_get.multiplier) + 1})


def report_filter_kerio(request):
    # Control to look for incidence
    incidence_ctrl = request.GET.get('incidence_ctrl')
    # Control to look for individual user incidence
    user_ctrl = request.GET.get('user_ctrl')
    # print("------ user control:" + user_ctrl)

    # if request.method == 'POST':        #create a form instance and populate it with data from the request:
    form = filter_userForm()

    # if filter_userForm(request.GET):
    # if form.is_valid():
    #     user_cell = form.cleaned_data['user_cell']
    #     date_start = form.cleaned_data['date_start']
    #     date_end = form.cleaned_data['date_end']
    form = filter_userForm(request.GET)
    userIncidenceForm = FilterIncidenceForm(request.GET)

    user_cell = request.GET.get('user_cell')
    date_start = request.GET.get('date_start')
    date_end = request.GET.get('date_end')

    page = request.GET.get('page')
    up_bl = request.GET.get('up_bl')
    down_bl = request.GET.get('down_bl')

    allBlackList = BlackListDomain.objects.all()

    # Next iteration in the black list
    slice_get = SliceTmp.objects.get(pk=1)
    if up_bl is not None:
        black_list_slice = BlackListDomain.objects.all()
        if black_list_slice.count() / slice_get.multiplier > slice_get.step:
            slice_get.start = slice_get.start + slice_get.multiplier
            slice_get.end = slice_get.end + slice_get.multiplier
            slice_get.step = slice_get.step + 1
            slice_get.save()
            print("-------Page is None, the step is up")
            print("-------Black list total:" + str(black_list_slice.count()))
            print("-------Black list / multiplier:" + str(black_list_slice.count() / slice_get.multiplier))
    if down_bl is not None:
        if slice_get.end > slice_get.multiplier:
            slice_get.start = slice_get.start - slice_get.multiplier
            slice_get.end = slice_get.end - slice_get.multiplier
            slice_get.step = slice_get.step - 1
            slice_get.save()
            print("-------In the slice, step is down")

    query = []
    query_kerio = []

    list_incidence_kerio_user = []
    # user_cell is not None and date_start is not None and

    if user_ctrl == 'active':
        print("----user control is active inside of if user_ctrl")
        query_user = LogsKerio.objects.filter(ip_addres__contains=user_cell).filter(
            date_time__range=(date_start, date_end))

        black_list_to_user = BlackListDomain.objects.all()[
                             SliceTmp.objects.get(pk=1).start:SliceTmp.objects.get(pk=1).end]

        for bl in black_list_to_user:
            print("-------black objet in user:" + str(bl.domain))
            contains_incidence_user = query_user.filter(url__contains=bl.domain).order_by('date_time')
            if contains_incidence_user.count() > 0:
                for obj_s in contains_incidence_user:
                    list_incidence_kerio_user.append(obj_s)
                    print("--------obj_s:" + str(obj_s))

    # Look for incidence into the logs kerio
    StartDateIncidence = request.GET.get('StarIncidence')
    EndDateIncidence = request.GET.get('EndIncidence')
    queryIncidenceSquid = []
    queryIncidenceKerio = []

    # Reset first time load
    if StartDateIncidence is None and page is None and user_cell is None and date_start is None:
        sliceResetFirstLoad = SliceTmp.objects.get(pk=1)
        sliceResetFirstLoad.start = 0
        sliceResetFirstLoad.end = sliceResetFirstLoad.multiplier
        sliceResetFirstLoad.step = 1
        sliceResetFirstLoad.save()

    list_incidence_squid = []
    list_incidence_kerio = []

    if StartDateIncidence is not None and incidence_ctrl == 'active':
        query_squid = LogsSquid.objects.filter(date_time__range=(StartDateIncidence, EndDateIncidence))
        query_kerio = LogsKerio.objects.filter(date_time__range=(StartDateIncidence, EndDateIncidence))
        # [:SliceTmp.objects.get().end]
        # [:SliceTmp.objects.get().end]

        b_list = BlackListDomain.objects.all()
        slice = SliceTmp.objects.get(pk=1)

        blackListDomain = BlackListDomain.objects.all()[SliceTmp.objects.get(pk=1).start:SliceTmp.objects.get(pk=1).end]

        # Reset entity slice
        if b_list.count() / slice.multiplier < slice.step:
            slice.start = 0
            slice.end = slice.multiplier
            slice.step = 0
            slice.save()

        for bl in blackListDomain:
            contains_incidence = query_kerio.filter(url__contains=bl.domain).order_by('user_name')
            if contains_incidence.count() > 0:
                for obj_s in contains_incidence:
                    list_incidence_kerio.append(obj_s)

    # Paginator Squid User
    # if user_ctrl == 'active':
    paginator = Paginator(list_incidence_kerio_user, 35)

    # Paginator Squid
    if incidence_ctrl == 'active':
        paginator = Paginator(list_incidence_squid, 35)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj_squid = paginator.get_page(page_number)
    # print("----page_obj_squid:" + str(page_obj_squid.next_page_number()))

    # Paginator Kerio
    if incidence_ctrl == 'active':
        paginator = Paginator(list_incidence_kerio, 35)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj_kerio = paginator.get_page(page_number)

    if page_obj_squid.has_next():
        print("--------Paginator next page: " + str(page_obj_squid.next_page_number()))
    else:
        print("There are not next page")
        print("+++ page_obj_squid.has_next() is None: " + str(page_obj_squid.has_next()))

    # 59981255
    result_query = {}

    # redirect to a new URL:
    return render(request, 'analysis_squid_kerio/ask_tables_filterKerio.html', {'form': form,
                                                                           'user_ctrl': user_ctrl,
                                                                           'incidence': userIncidenceForm,
                                                                           'user_cell': user_cell,
                                                                           'date_start': date_start,
                                                                           'date_end': date_end,
                                                                           'incidence_ctrl': incidence_ctrl,
                                                                           'StartDateIncidence': StartDateIncidence,
                                                                           'EndDateIncidence': EndDateIncidence,
                                                                           # 'query': query,
                                                                           'query': page_obj_squid,
                                                                           'query_kerio': page_obj_kerio,
                                                                           'step': slice_get.step,
                                                                           'totalIter': math.floor(
                                                                               allBlackList.count() / slice_get.multiplier) + 1})
