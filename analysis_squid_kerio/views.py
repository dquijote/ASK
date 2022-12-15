from builtins import type, str
from datetime import datetime
# import datetime
import math
from itertools import count

from django.core import paginator
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from analysis_squid_kerio.form import RangeDateUserForm, RangeDateForm
from analysis_squid_kerio.models import CategoryBlackListDomain, User, LogsSquidPartitioned
from .models import LogsKerio, LogsSquid, BlackListDomain, SliceTmp, LogsSquidTmp,SearchParameterSquid

from .form import filter_userForm, FilterIncidenceForm

# Create your views here.


def index(request):

    #return render(request, 'index.html')
    return render(request, 'analysis_squid_kerio/ask-index.html')


def user_profile(request):
    return render(request, 'analysis_squid_kerio/ask_user_profile.html')


def list_user(request):
    query_user = User.objects.all().order_by('name')

    number_of_line = 50
    paginator_user = Paginator(query_user, number_of_line)

    page_number = request.GET.get('page')
    page_paginator_user = paginator_user.get_page(page_number)  # Return a list with the element the page specified

    context = {'user': page_paginator_user,
               'page': page_number,
    }
    return render(request, 'analysis_squid_kerio/ask_user_list.html', context)

# Convert date to python format
# def convert_date(date):
#     # 'Sept. 1, 2021'
#     month = date[0:3]
#     day = date[5:7]
#     year = date[8:]
#     print("day:" + day)
#     print((int(day)))
#     # print((int(month)))
#     print((int(year)))
#
#     print("day: " + day + "month: " + month + "year: " + year)
#     python_date = datetime.date(int(year), month, int(day))
#     return python_date


def report_withoutuser(request):
    form = RangeDateForm()

    hidden_button_squid = request.GET.get('squid')
    hidden_button_kerio = request.GET.get('kerio')

    query = []
    query_kerio = []

    if hidden_button_squid == 'squid':
        param_form_squid_first = request.GET.get('StarDate')
        param_form_squid_end = request.GET.get('EndDate')
        date_first_squid = datetime.strptime(param_form_squid_first, '%m/%d/%Y')
        date_end_squid = datetime.strptime(param_form_squid_end, '%m/%d/%Y')

        print("param_form_squid_end:" + param_form_squid_end)
        print("param_form_squid_first: " + param_form_squid_first)
        print("hidden_button_squid: " + hidden_button_squid)

        print(date_first_squid)
        print(date_end_squid)

        query = LogsSquid.objects.filter(date_time__range=(date_first_squid, date_end_squid))
    if hidden_button_kerio == 'kerio':
        param_form_squid_first = request.GET.get('StarDate')
        param_form_squid_end = request.GET.get('EndDate')
        date_first_squid = datetime.strptime(param_form_squid_first, '%m/%d/%Y')
        date_end_squid = datetime.strptime(param_form_squid_end, '%m/%d/%Y')

        query_kerio = LogsKerio.objects.filter(date_time__range=(date_first_squid, date_end_squid))

    paginator_squid = Paginator(query, 50)
    paginator_kerio = Paginator(query_kerio, 50)

    page_number = request.GET.get('page')
    page_query_squid = paginator_squid.get_page(page_number)
    page_query_kerio = paginator_kerio.get_page(page_number)

    context = {'query': page_query_squid,
               'query_kerio': page_query_kerio,
               'form': form,

               'param_form_squid_first': request.GET.get('StarDate'),
               'param_form_squid_end': request.GET.get('EndDate'),

               'param_form_squid_first': request.GET.get('StarDate'),
               'param_form_squid_end': request.GET.get('EndDate')

               }

    return render(request, 'analysis_squid_kerio/ask_tables_withoutuser.html', context)


def report(request):
    form = RangeDateUserForm(request.GET)
    hidden_button_squid = request.GET.get('squid')
    hidden_button_kerio = request.GET.get('kerio')

    query = []
    query_kerio = []

    param_form_StartDate = request.GET.get('StarDate')
    param_form_EndDate = request.GET.get('EndDate')
    user_name = request.GET.get('user')
    if hidden_button_squid == 'squid':

        date_first_squid = datetime.strptime(param_form_StartDate, '%m/%d/%Y')
        date_end_squid = datetime.strptime(param_form_EndDate, '%m/%d/%Y')
        print('date_first_squid: ' + str(date_first_squid))
        print('date_end_squid: ' + str(date_end_squid))
        print('user_name: ' + str(user_name))

        query = LogsSquid.objects.filter(date_time__range=(date_first_squid, date_end_squid)).filter(ip_client__contains=user_name)
    if hidden_button_kerio == 'kerio':
        # param_form_StartDate = request.GET.get('StarDate')
        # param_form_EndDate = request.GET.get('EndDate')
        date_first_squid = datetime.strptime(param_form_StartDate, '%m/%d/%Y')
        date_end_squid = datetime.strptime(param_form_EndDate, '%m/%d/%Y')

        query_kerio = LogsKerio.objects.filter(date_time__range=(date_first_squid, date_end_squid)).filter(
            user_name__contains=user_name)

    paginator_squid = Paginator(query, 50)
    paginator_kerio = Paginator(query_kerio, 50)
    page_number = request.GET.get('page')
    page_query_squid = paginator_squid.get_page(page_number)
    page_query_kerio = paginator_kerio.get_page(page_number)


    context = {'query': page_query_squid,
               'query_kerio': page_query_kerio,
               'form': form,

               'param_form_StartDate': param_form_StartDate,
               'param_form_EndDate': param_form_EndDate,
               'user_name': user_name

               }

    return render(request, 'analysis_squid_kerio/ask_tables.html', context)


def sortListLogSquidObj(e):
    return e.ip_client


# Show the diferent filter (SQUID)
def report_filter(request):

    # Control to look for incidence, with out user, just interval of date
    incidence_ctrl = request.GET.get('incidence_ctrl')
    # Control to look for individual user incidence
    user_ctrl = request.GET.get('user_ctrl')

    # Category black list
    category = request.GET.get('category')
    category_black_list = []
    count_category_black_list = 0
    category_black_list_domain = []
    if category is not None and category != "":
        category_black_list = CategoryBlackListDomain.objects.get(pk=category)
        category_black_list_domain = BlackListDomain.objects.filter(category=category)
        count_category_black_list = category_black_list_domain.count()
        print("category black list : " + str(category_black_list))

    # if request.method == 'POST':        #create a form instance and populate it with data from the request:
    form = filter_userForm()

    form = filter_userForm(request.GET)
    userIncidenceForm = FilterIncidenceForm(request.GET)

    #Take the send value
    StartDateIncidence = request.GET.get('StarIncidence')
    EndDateIncidence = request.GET.get('EndIncidence')
    print("EndDateIncidence: " + str(EndDateIncidence) + " and type:" + str(type(EndDateIncidence)))
    print("StartDateIncidence: " + str(StartDateIncidence) + " and type:" + str(type(StartDateIncidence)))
    if StartDateIncidence != "None" and StartDateIncidence is not None:
        StartDateIncidence = datetime.strptime(request.GET.get('StarIncidence'), '%m/%d/%Y')
        StartDateIncidence = StartDateIncidence.date()
        print("converted datime: " + str(StartDateIncidence))
        # StartDateIncidence = request.GET.get('StarIncidence')
    if EndDateIncidence != "None" and EndDateIncidence is not None:
        # EndDateIncidence = convert_date(request.GET.get('EndIncidence'))
        EndDateIncidence = datetime.strptime(request.GET.get('EndIncidence'), '%m/%d/%Y')
        EndDateIncidence = EndDateIncidence.date()
        # EndDateIncidence = datetime.date(EndDateIncidence.year, EndDateIncidence.month, EndDateIncidence.day)

    user_cell = request.GET.get('user_cell')
    date_start = request.GET.get('date_start')
    date_end = request.GET.get('date_end')
    print("type of date_end" + str(type(date_end)))
    print("type of date_end" + str(date_start))

    #Convert the data in a datetime objet
    if date_start is not None and date_start != "None" and date_start != "":
        date_start = datetime.strptime(date_start, '%m/%d/%Y')
        print("date start: " + str(date_start))
    if date_end is not None and date_end != "None" and date_end != "":
        date_end = datetime.strptime(date_end, '%m/%d/%Y')
        print("date end: " + str(date_end))

    page = request.GET.get('page')
    up_bl = request.GET.get('up_bl')  # black list up
    down_bl = request.GET.get('down_bl')  # black list down


    # Next iteration in the black list
    slice_get = SliceTmp.objects.get(pk=1)
    if up_bl is not None:
        black_list_slice = BlackListDomain.objects.all()
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

    list_incidence_squid_user = []
# user_cell is not None and date_start is not None and
    search_made = []

    print("user_ctrol: " + str(user_ctrl))

    # Search with user, part of a parameter
    if user_ctrl == 'active':
        print("----user control is active inside of if user_ctrl")
        query_user = LogsSquidPartitioned.objects.filter(ip_client__contains=user_cell).filter(
            date_time__range=(date_start, date_end))

        black_list_to_user = BlackListDomain.objects.all()[
                             SliceTmp.objects.get(pk=1).start:SliceTmp.objects.get(pk=1).end]

        # Make interception between date interval
        param_with_user = SearchParameterSquid.objects.exclude(user__contains="False"). \
            filter(category_black_list__id__contains=category_black_list.pk).order_by("date_start")
        # for a in param_with_user:
        #     print("param_with_user date start: " + str(a.date_start))

        #
        param_with_user_all = SearchParameterSquid.objects.all()
        print("144, param_with_user_all: " + str(param_with_user_all.count()))

        search_for_do = {}
        print("145, param_with_user: " + str(param_with_user.count()))
        #
        if param_with_user_all.count() > 0:

            date_made_first = ""
            date_made_end = ""
            # Interception above, the second part of interval is out (for do)
            for iter0 in param_with_user:
                if date_start.date() < iter0.date_end < date_end.date() and \
                        iter0.date_start < date_start.date() < iter0.date_end:
                    date_made_end = iter0
                    print("Line 154, date_made_end assignment value: " + str(date_made_end))
                    break

            # Interception bottom, the  first part of interval is out (for do)
            for iter1 in param_with_user:
                if date_start.date() < iter1.date_start < date_end.date() and \
                     iter1.date_start < date_end.date() < iter1.date_end:
                    date_made_first = iter1



                    print("Line 160, date_made_first assignment value: " + str(date_made_first))
                    break

            # print("Line 162, date_made_first inicio: " + str(date_made_first.date_start))
            # print("Line 162, date_made_first fin: " + str(date_made_first.date_end))
            # print("Line 163, date_made_end: " + str(date_made_end))

            print("Line 167, date_made_end is not None" + str(date_made_end is not None))
            print("Line 168, range(0, len(param_with_user) - 1" + str(range(0, len(param_with_user))))

            no_search_made = True  #
            search_done = False  # The Search is done

            if date_made_end is not None and date_made_end != "":
                cont = 0
                for iter in range(0, len(param_with_user)):
                    if param_with_user.count() == 1:
                        search_for_do[param_with_user[iter].date_end] = date_end.date()
                for iter in range(0, len(param_with_user)):
                    # Interception above, the second part of interval is out
                    if date_made_end.date_end <= param_with_user[iter].date_start <= date_end.date() and \
                            date_made_end.date_end <= param_with_user[iter].date_end <= date_end.date():
                        # If 1st searches done don't start like the interval
                        cont += 1
                        print("188 cont: " + str(cont))
                        if cont == 1 and date_made_end.date_end < param_with_user[iter].date_start:
                            search_for_do[date_made_end.date_end] = param_with_user[iter].date_start
                            no_search_made = False
                        if iter + 1 < len(param_with_user):
                            if param_with_user[iter].date_end < param_with_user[iter + 1].date_start:
                                search_for_do[param_with_user[iter].date_end] = param_with_user[
                                    iter + 1].date_start
                                no_search_made = False
                                # If last searches done don't end like the end  of the interval
                            if iter == len(param_with_user) and date_end.date() > param_with_user[iter].date_end:
                                search_for_do[param_with_user[iter].date_end] = date_end.date()
                                no_search_made = False
                    else:
                        search_for_do[date_made_end.date_end] = date_end.date()
                        no_search_made = False
                        print("Line 200")

            elif date_made_first is not None and date_made_first != "":
                cont = 0

                for iter in range(0, len(param_with_user)):
                    print("param_with_user[iter].date_start: " + str(param_with_user[iter].date_start))
                    print("param_with_user[iter].date_end: " + str(param_with_user[iter].date_end))
                    # Interception bottom, the first part of interval is out
                    if date_start.date() <= param_with_user[iter].date_start <= date_made_first.date_start and \
                            date_start.date() <= param_with_user[iter].date_end <= date_made_first.date_start:
                        cont += 1
                        print("205")
                        print("cont: " + str(cont))
                        # If 1st searches done don't start like the interval
                        if cont == 1 and date_start.date() < param_with_user[iter].date_start:
                            search_for_do[date_start.date()] = param_with_user[iter].date_start
                            no_search_made = False
                            print("210")
                            print("date_start.date()" + str(date_start.date()))
                            print("param_with_user[iter].date_start" + str(param_with_user[iter].date_start))
                        if iter + 1 < len(param_with_user):
                            if param_with_user[iter].date_end < param_with_user[iter + 1].date_start:
                                search_for_do[param_with_user[iter].date_end] = param_with_user[iter + 1].date_start
                                no_search_made = False
                                print("214")
                                print("param_with_user[iter].date_end" + str(param_with_user[iter].date_end))
                                print("param_with_user[iter + 1].date_start" + str(param_with_user[iter + 1].date_start))
                            # If last searches done don't end like the end  of the interval
                        if iter == len(param_with_user) and date_end.date() > param_with_user[iter].date_end:
                            search_for_do[param_with_user[iter].date_end] = date_end.date()
                            no_search_made = False
                            print("218")
                            print("param_with_user[iter].date_end" + str(param_with_user[iter].date_end))
                            print("date_end.date()" + str(date_end.date()))
                    else:
                        search_for_do[date_start.date()] = date_made_first.date_start
                        no_search_made = False
                        print("221")
                        print("date_start.date()" + str(date_start.date()))
                        print("date_made_first.date_start" + str(date_made_first.date_start))

            # Interception for both side, above and below
            elif date_made_first is not None and date_made_first != "" and \
                    date_made_end is not None and date_made_end != "":
                for iter in range(0, len(param_with_user) - 1):
                    # Interception for both side, above and below
                    if date_made_first.date_end.date() <= param_with_user[iter].date_start <= date_made_first.date_start.date() and \
                            date_made_first.date_end.date() <= param_with_user[iter].date_end <= date_made_first.date_start.date():
                        # If 1st searches done don't start like the interval
                        if iter == 0 and date_start.date() < param_with_user[iter].date_start:
                            search_for_do[date_start.date()] = param_with_user[iter].date_start
                            no_search_made = False
                        if iter + 1 <= len(param_with_user):
                            if param_with_user[iter].date_end < param_with_user[iter + 1].date_start:
                                search_for_do[param_with_user[iter].date_end] = param_with_user[iter + 1].date_start
                                no_search_made = False
                        # If last searches done don't end like the end  of the interval
                        if iter == len(param_with_user) - 1 and date_end.date() > param_with_user[iter].date_end:
                            search_for_do[param_with_user[iter].date_end] = date_end.date()
                            no_search_made = False

            # All interseption are inside
            else:

                for iter in range(0, len(param_with_user)):
                    # The made is done
                    if param_with_user[iter].date_start <= date_start.date() < param_with_user[iter].date_end and \
                            param_with_user[iter].date_start < date_end.date() <= param_with_user[iter].date_end:
                        date_start_done = param_with_user[iter].date_start
                        date_end_done = param_with_user[iter].date_end
                        no_search_made = False
                        search_done = True
                        print("278, the search is done")
                        break
                    if date_start.date() <= param_with_user[iter].date_start <= date_end.date() and \
                    date_start.date() <= param_with_user[iter].date_end <= date_end.date():
                        # If 1st searches done don't start like the interval
                        print("283, ")
                        if iter == 0 and date_start.date() < param_with_user[iter].date_start:
                            search_for_do[date_start.date()] = param_with_user[iter].date_start
                            no_search_made = False
                        if iter + 1 < len(param_with_user):
                            if param_with_user[iter].date_end < param_with_user[iter + 1].date_start:
                                search_for_do[param_with_user[iter].date_end] = param_with_user[iter + 1].date_start
                                no_search_made = False
                                # If last searches done don't end like the end  of the interval
                        if iter == len(param_with_user) - 1 and date_end.date() > param_with_user[iter].date_end:
                            search_for_do[param_with_user[iter].date_end] = date_end.date()
                            no_search_made = False

            # No search made
            if no_search_made:
                print("292, no_search_made")
                for iter in range(0, len(param_with_user)):
                    print("294, param_with_user[0].date_start: " + str(param_with_user[0].date_start))
                    print("295, date_end.date(): " + str(date_end.date()))
                    if param_with_user[0].date_start > date_end.date():
                        search_for_do[date_start.date()] = date_end.date()
                        print("300, ")
                    if iter < len(param_with_user) - 1 and param_with_user[iter].date_end < date_start.date() and date_end.date() < param_with_user[iter+1].date_start:
                        search_for_do[date_start.date()] = date_end.date()
                        print("303, ")
                    if iter == len(param_with_user) - 1 and param_with_user[iter].date_end < date_end.date():
                        search_for_do[date_start.date()] = date_end.date()
                        print("306, ")


            print("428, search_for_do, dictonary" + str(search_for_do))

            # Subtracting the searches done that are out on the bottom side

            for date_start_dictionary, date_end_dictionary in search_for_do.items():
                print("Making the search and saving in param user, Line 308")
                for bl in black_list_to_user:
                    contains_incidence_user = query_user.filter(url__contains=bl.domain).filter(
                        date_time__range=(date_start_dictionary, date_end_dictionary)).order_by('date_time')
                    if contains_incidence_user.count() > 0:
                        for obj_s in contains_incidence_user:
                            search_parameter = SearchParameterSquid()
                            search_parameter.date_start = date_start_dictionary
                            search_parameter.date_end = date_end_dictionary
                            search_parameter.start_slice = SliceTmp.objects.get(pk=1).start
                            search_parameter.end_slice = SliceTmp.objects.get(pk=1).end
                            search_parameter.step_slice = SliceTmp.objects.get(pk=1).step
                            search_parameter.user = user_cell
                            search_parameter.multiplier_slice = SliceTmp.objects.get(pk=1).multiplier
                            search_parameter.category_black_list = category_black_list
                            search_parameter.save()

                            log_squid_tmp_obj = LogsSquidTmp()
                            log_squid_tmp_obj.log_squid = obj_s
                            log_squid_tmp_obj.parameter_search = search_parameter
                            log_squid_tmp_obj.save()

                            print("Line 331, search_parameter: " + str(search_parameter))

            if search_done:
                search_made = param_with_user.filter(user__contains=user_cell).exclude(date_start__lt=date_start_done).\
                    exclude(date_end__gt=date_end_done)
            else:
                search_made = param_with_user.filter(user__contains=user_cell).exclude(date_start__lt=date_start.date()).\
                    exclude(date_end__gt=date_end.date())

            print("Line 335, search_made, exlude")

        else:
            search_for_do[date_start.date()] = date_end.date()
            print("339, search_for_do" + str(search_for_do))
            for date_start_dictionary, date_end_dictionary in search_for_do.items():
                for bl in black_list_to_user:
                    contains_incidence_user = query_user.filter(url__contains=bl.domain).filter(
                        date_time__range=(date_start_dictionary, date_end_dictionary)).order_by('date_time')
                    if contains_incidence_user.count() > 0:
                        print("345, contains_incidence_user" + str(contains_incidence_user.count()))
                        for obj_s in contains_incidence_user:
                            search_parameter = SearchParameterSquid()
                            search_parameter.date_start = date_start
                            search_parameter.date_end = date_end
                            search_parameter.start_slice = SliceTmp.objects.get(pk=1).start
                            search_parameter.end_slice = SliceTmp.objects.get(pk=1).end
                            search_parameter.step_slice = SliceTmp.objects.get(pk=1).step
                            search_parameter.user = user_cell
                            search_parameter.multiplier_slice = SliceTmp.objects.get(pk=1).multiplier
                            search_parameter.category_black_list = category_black_list
                            search_parameter.save()

                            log_squid_tmp_obj = LogsSquidTmp()
                            log_squid_tmp_obj.log_squid = obj_s
                            log_squid_tmp_obj.parameter_search = search_parameter
                            log_squid_tmp_obj.save()

            search_made = param_with_user.filter(user__contains=user_cell).exclude(date_start__lt=date_start.date(),
                                                                                   date_end__gt=date_end.date())
            #

            print("None part of the search is made, search parameter table is empty")

        print("Line 368, search_for_do" + str(search_for_do))
        print("search made count: " + str(search_made.count()))

        # Make the search in logssquidtmp. The search is made, just take a parameter and ask what is the log that
        # belong it
        for a in search_made:
            parameter_search = LogsSquidTmp.objects.filter(parameter_search=a.id)
            list_incidence_squid_user.append(LogsSquidPartitioned.objects.filter(pk=parameter_search.get().log_squid.pk).get())

        # for bl in black_list_to_user:
        #     print("-------black objet in user:" + str(bl.domain))
        #     contains_incidence_user = query_user.filter(url__contains=bl.domain).order_by('date_time')
        #     if contains_incidence_user.count() > 0:
        #         for obj_s in contains_incidence_user:
        #             log_squid_tmp = obj_s
        #             log_squid_tmp.save()
        #             #list_incidence_squid_user.append(obj_s)
        #             print("--------obj_s:" + str(obj_s))

    # Look for incidence into the logs squid
    queryIncidenceSquid = []

    # Reset first time load
    if StartDateIncidence is None and page is None and user_cell is None and date_start is None:
        sliceResetFirstLoad = SliceTmp.objects.get(pk=1)
        sliceResetFirstLoad.start = 0
        sliceResetFirstLoad.end = sliceResetFirstLoad.multiplier
        sliceResetFirstLoad.step = 1
        sliceResetFirstLoad.save()

    list_incidence_squid = []
    list_incidence_kerio = []
    print("request: " + str(request))
    print("-------incidence ctrl: " + str(incidence_ctrl))
    print("-------StartDateIncidence: " + str(StartDateIncidence))

    b_list = BlackListDomain.objects.filter(category=category)[
             SliceTmp.objects.get(pk=1).start:SliceTmp.objects.get(pk=1).end]

    # Paginator Squid User
    #if user_ctrl == 'active':
    paginator = Paginator(list_incidence_squid_user, 35)
    print("-----------list_incidence_squid_user count: " + str(list_incidence_squid_user.__len__()))

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

    if page_obj_squid.has_next():
        print("--------Paginator next page: " + str(page_obj_squid.next_page_number()))
    else:
        print("There are not next page")
        print("+++ page_obj_squid.has_next() is None: " + str(page_obj_squid.has_next()))


    # 59981255
    result_query = {}

    # Converting the parameter "interval of date" to format's template
    if StartDateIncidence != "None" and StartDateIncidence is not None:
        StartDateIncidence = str(StartDateIncidence.month) + "/" + str(StartDateIncidence.day) + "/" + str(StartDateIncidence.year)
    if EndDateIncidence != "None" and EndDateIncidence is not None:
        EndDateIncidence = str(EndDateIncidence.month) + "/" + str(EndDateIncidence.day) + "/" + str(EndDateIncidence.year)

    # Converting the parameter "interval of date" to format's template
    if date_start != "None" and date_start is not None:
        date_start = str(date_start.month) + "/" + str(date_start.day) + "/" + str(date_start.year)
    if date_end != "None" and date_end is not None:
        date_end = str(date_end.month) + "/" + str(date_end.day) + "/" + str(date_end.year)

    # render to a URL:
    return render(request, 'analysis_squid_kerio/ask_tables_filter.html', {'form': form,
                                                                           'user_ctrl': user_ctrl,
                                                                           'incidence': userIncidenceForm,
                                                                           'user_cell': user_cell,
                                                                           'date_start': date_start,
                                                                           'date_end': date_end,
                                                                           'incidence_ctrl': incidence_ctrl,
                                                                           'StartDateIncidence': str(StartDateIncidence),
                                                                           'EndDateIncidence': str(EndDateIncidence),
                                                                           'category': category,
                                                                           #'query': query,
                                                                           'query': page_obj_squid,
                                                                           'query_kerio': page_obj_kerio,
                                                                           'step': slice_get.step,
                                                                           'totalIter': math.floor(count_category_black_list/slice_get.multiplier) + 1})


# Filter log looking for incidence without user parameter
def reportFilterSquidDate(request):
    # Control to look for incidence, with out user, just interval of date
    incidence_ctrl = request.GET.get('incidence_ctrl')
    # Control to look for individual user incidence
    user_ctrl = request.GET.get('user_ctrl')
    # Category black list
    category = request.GET.get('category')

    user_cell = request.GET.get('user_cell')
    date_start = request.GET.get('date_start')
    date_end = request.GET.get('date_end')

    slice_get = SliceTmp.objects.get(pk=1)

    page = request.GET.get('page')
    up_bl = request.GET.get('up_bl')  # black list up
    down_bl = request.GET.get('down_bl')  # black list down

    # Taking just the category selected (Black list)
    category_black_list = []
    count_category_black_list = 0
    category_black_list_domain = []
    if category is not None and category != "":
        category_black_list = CategoryBlackListDomain.objects.get(pk=category)
        category_black_list_domain = BlackListDomain.objects.filter(category=category)
        count_category_black_list = category_black_list_domain.count()
        print("category black list : " + str(category_black_list))

    form = filter_userForm(request.GET)
    userIncidenceForm = FilterIncidenceForm(request.GET)



    # Take the send value
    StartDateIncidence = request.GET.get('StarIncidence')
    EndDateIncidence = request.GET.get('EndIncidence')
    print("EndDateIncidence: " + str(EndDateIncidence) + " and type:" + str(type(EndDateIncidence)))
    print("StartDateIncidence: " + str(StartDateIncidence) + " and type:" + str(type(StartDateIncidence)))

    print("page: " + str(page))
    #  Formating date From the form
    if StartDateIncidence != "None" and StartDateIncidence is not None:
        StartDateIncidence = datetime.strptime(request.GET.get('StarIncidence'), '%m/%d/%Y')
        StartDateIncidence = StartDateIncidence.date()
        print("converted datime: " + str(StartDateIncidence))
        # StartDateIncidence = request.GET.get('StarIncidence')
    if EndDateIncidence != "None" and EndDateIncidence is not None:
        # EndDateIncidence = convert_date(request.GET.get('EndIncidence'))
        EndDateIncidence = datetime.strptime(request.GET.get('EndIncidence'), '%m/%d/%Y')
        EndDateIncidence = EndDateIncidence.date()
        # EndDateIncidence = datetime.date(EndDateIncidence.year, EndDateIncidence.month, EndDateIncidence.day)


    # Process the form without user
    if StartDateIncidence is not None:
        query_squid = LogsSquidPartitioned.objects.filter(date_time__range=(StartDateIncidence, EndDateIncidence))
        query_kerio = LogsKerio.objects.filter(date_time__range=(StartDateIncidence, EndDateIncidence))
        # [:SliceTmp.objects.get().end]
        # [:SliceTmp.objects.get().end]

        # b_list = BlackListDomain.objects.filter(category=category)SliceTmp.objects.get(pk=1).start:SliceTmp.objects.get(pk=1).end]
        slice = SliceTmp.objects.get(pk=1)

        # print("b_list count: " + str(b_list.count()))

        # blackListDomainCategory = BlackListDomain.objects.filter(category=category)

        print("------slice inicio:" + str(SliceTmp.objects.get(pk=1).start))
        print("------slice fin:" + str(SliceTmp.objects.get(pk=1).end))

        # Reset entity slice
        if category_black_list_domain.count() / slice.multiplier < slice.step:
            slice.start = 0
            slice.end = slice.multiplier
            slice.step = 1
            slice.save()

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
                print('slice_get.start' + str(slice_get.start))
                print('slice_get.end' + str(slice_get.end))
                print(' slice_get.step' + str( slice_get.step))

        b_list = BlackListDomain.objects.filter(category=category)[
                 SliceTmp.objects.get(pk=1).start:SliceTmp.objects.get(pk=1).end]

        list_tmp_incidence = []

        # List incidence to show in template
        list_incidence_squid = []

        # print("-------many of query_squid:" + str(query_squid.count()))
        # print("-------many of query_kerio:" + str(query_kerio.count()))

        for bl in b_list:
            # print("query_squid: " + str(query_squid.count()))
            print(" for bl in b_list:")
            print("query_squid.count: " + str(query_squid.count()))
            contains_incidence = query_squid.filter(url__contains=bl.domain)  # .order_by('ip_client')
            print(" paso:" + str(contains_incidence.first()))
            print("contains_incidence.count(): " + str(contains_incidence.__len__()))
            print("contains_incidence.count(): " + str(contains_incidence.count()))
            if contains_incidence.count() > 0:
                print("-------black objet:" + str(bl.domain))

                for obj_s in contains_incidence:
                    print("-------black objet:" + str(bl.domain))
                    print("entro")
                    list_incidence_squid.append(obj_s)

        list_incidence_squid.sort(key=sortListLogSquidObj)

        # Increase the value in temp slice
        print("b_list count: " + str(b_list.count()))
        # if up_bl == 1 and category_black_list_domain.count() / slice.step <= slice.step + 1:
        #     print("entro up_bl")
        #     slice1 = SliceTmp.objects.get(pk=1)
        #     slice1.start = slice1.start + slice1.multiplier
        #     slice1.end = slice1.end + slice1.multiplier
        #     slice1.step += 1
        #     slice1.save()
        #
        # # Decrease the value in temp slice
        # if down_bl == -1 and slice.step > 1:
        #     print("entro down_bl")
        #     slice1 = SliceTmp.objects.get(pk=1)
        #     slice1.start = slice1.start - slice1.multiplier
        #     slice1.end = slice1.end - slice1.multiplier
        #     slice1.step -= 1
        #     slice1.save()

        # Paginator Squid
        paginator = Paginator(list_incidence_squid, 35)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj_squid = paginator.get_page(page_number)

        # Format to jquery format
        StartDateIncidence = str(StartDateIncidence.month) + '/' + str(StartDateIncidence.day) + '/' + str(StartDateIncidence.year)
        EndDateIncidence = str(EndDateIncidence.month) + '/' + str(EndDateIncidence.day) + '/' + str(EndDateIncidence.year)

        # render to a URL:
        return render(request, 'analysis_squid_kerio/ask_tables_filter.html', {'form': form,
                                                                               'user_ctrl': user_ctrl,
                                                                               'incidence': userIncidenceForm,
                                                                               # 'user_cell': user_cell,
                                                                               'date_start': date_start,
                                                                               'date_end': date_end,
                                                                               'incidence_ctrl': incidence_ctrl,
                                                                               'StartDateIncidence': str(
                                                                                   StartDateIncidence),
                                                                               'EndDateIncidence': str(
                                                                                   EndDateIncidence),
                                                                               'category': category,
                                                                               # 'query': query,
                                                                               'query': page_obj_squid,
                                                                               # 'query_kerio': page_obj_kerio,
                                                                               'step': slice_get.step,
                                                                               'totalIter': math.floor(
                                                                                   count_category_black_list / slice_get.multiplier) + 1})


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
