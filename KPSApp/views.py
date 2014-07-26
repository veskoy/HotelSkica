# -*- coding: utf-8 -*-
from django.shortcuts import render

from KPSApp.forms import LoginForm, CheckForm

import string
import time

from django.http import HttpResponse, HttpResponseRedirect

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle

# Create your views here.
def index(request):
    context_dictionary = {
        'page': 'index'
    }

    is_logged = request.session.get('is_logged', False)
    
    if request.method == 'POST' and not is_logged:
        form = LoginForm(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            if username=='kps' and password=='kps':
                request.session['is_logged'] = True
                request.session['username'] = 'kps'
                if 'remember_me' in request.POST:
                    day_seconds = 24 * 60 * 60
                    request.session.set_expiry(day_seconds)
                    request.session['session_expiry'] = int(time.time())+day_seconds
                else:
                    request.session.set_expiry(0)
                    request.session['session_expiry'] = 0
                context_dictionary['login_message'] = 'Успешно влязохте в акаунта на х-л "Компас"!'
            else:
                context_dictionary['login_message'] = 'Грешно потребителско име или парола!'

        context_dictionary['form'] = form

    return render(request, 'KPSApp/index.html', context_dictionary)

def about(request):
    context_dictionary = {
        'page': 'about'
    }
    return render(request, 'KPSApp/about.html', context_dictionary)

def check(request):
    if 'is_logged' not in request.session:
        return HttpResponseRedirect('/kps')


    print request.session['session_expiry']

    context_dictionary = {
        'page': 'check'
    }
    if request.method == 'POST':
        form = CheckForm(request.POST)

        if form.is_valid():
            rooms = request.POST['rooms_field'].split(',')
            if len(rooms) > 0:
                rooms_up = [366,266,
                            364,264,
                            362,262,
                            360,260,
                            358,258,
                            356,256,
                            354,254,
                            352,252,
                            350,250,
                            348,248,

                            346,344,
                            246,244,
                            146,144,

                            342,242,142,
                            340,240,140,
                            338,238,138,
                            336,236,136,

                            323,321,
                            223,221,
                            123,121,

                            125,225,325,
                            127,227,327,
                            129,229,329,
                            131,231,331,

                            101,201,301,
                            103,203,303,
                            105,205,305,
                            107,207,307,
                            109,209,309,
                            111,211,311,
                            113,213,313,
                            115,215,315,
                            117,217,317,
                            119,219,319]

                rooms_right = [302,304,306,308,310,312,314,316,318,
                                202,204,206,208,210,212,214,216,218,
                                102,104,106,108,110,112,114,116,118,

                                132,134,130,128,126,124,122,120,
                                234,232,230,228,226,224,222,220,
                                334,332,330,328,326,324,322,320,

                                1,3,5,7,9,11,13,15,17,19,
                                20,18,16,14,12,10,8,6,4,2,

                                133,233,333,
                                135,235,335,
                                137,
                                139,237,337,
                                141,
                                143,239,
                                145,
                                147,241,
                                149,
                                151,243,
                                153,
                                155,
                                157,
                                159,
                                161,
                                163]
                rooms_order = []                
                rooms_dict = {}
                for room in rooms:

                    room.strip()
                    try:
                        if int(room) in rooms_up:
                            rooms_dict.update({room: 'Стаята се намира направо. ^'})
                        elif int(room) in rooms_right:
                            rooms_dict.update({room: 'Стаята се намира надясно. >'})
                        else:
                            rooms_dict.update({room: 'Няма такава стая.'})

                        rooms_order.append(room)
                    except ValueError:
                        continue
                context_dictionary['rooms_order'] = rooms_order
                context_dictionary['rooms'] = rooms_dict
            else:
                context_dictionary['error'] = 'Няма посочена стая.'
    else:
        form = CheckForm()

    context_dictionary['form'] = form
    return render(request, 'KPSApp/check.html', context_dictionary)

def logout(request):
    if request.session.get('is_logged', False):
        request.session.flush()
    return HttpResponseRedirect('/kps')

def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="RoomsDirections.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)

    data = [
        ['Стая', 'Посока'],
        ['101', '>>>'],
        ['102', "^^^"],
        ['103', ">>>"],
    ]

    parts = []
    #table = Table(data, [3 * inch, 1.5 * inch, inch])
    table_with_style = Table(data, [1.5 * inch, 3 * inch])

    table_with_style.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Courier'),
        ('FONT', (0, 0), (-1, 0), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, 0), 0.25, colors.green),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ]))

    #parts.append(table)
    #parts.append(Spacer(1, 0.5 * inch))
    parts.append(table_with_style)
    doc.build(parts)

    return response