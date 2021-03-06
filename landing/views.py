from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from .forms import *
from products.models import *
from landing.models import *
from blogs.models import *
from cosmetologs.models import *
from addresses.models import *
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse
import datetime
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import json
from django.http import JsonResponse
import random
import googlemaps


def landing(request):
    # logo_images = LogoImage.objects.filter(is_active=True, is_main=True)
    name = "DimaKostyuk"
    current_day = "31.05.2017"
    form = SubscriberForm(request.POST or None)
    # username = auth.get_user(request).username

    if request.method == "POST" and form.is_valid():
        # print (request.POST)
        # print (form.cleaned_data)
        data = form.cleaned_data
        # print (data["name"])
        new_form = form.save()

    return render(request, 'landing/landing.html', locals())


def validate_save_user_send_email(request, newuser_form, email_1, username_original, cosmetolog_name, cosmetolog_type):
    args_1 = {}
    newuser = newuser_form.save(commit=False)
    newuser.is_active = False
    newuser.save()
    subscriber_current = Subscriber.objects.get(user__username=email_1)
    subscriber_current.email = email_1
    subscriber_current.name = username_original
    subscriber_current.save()
    new_cosmetolog_type = CosmetologType.objects.get(name=cosmetolog_type)
    new_cosmetolog = Cosmetolog(name=cosmetolog_name, type=new_cosmetolog_type,
                                registration_time=timezone.now(), order_email=email_1)
    new_cosmetolog.save()


    new_subscriber_cosmetolog = SubscriberCosmetolog(cosmetolog_name=new_cosmetolog, cosmetolog_id=new_cosmetolog.id,
                                                     subscriber_name=subscriber_current,
                                                     subscriber_id=subscriber_current.id)
    new_subscriber_cosmetolog.save()

    # Email sending code:
    current_site = get_current_site(request)
    mail_subject = 'Activate your blog account on Site RENEW for example.'
    message = render_to_string('landing/acc_confirmation_email.html', {
        'user': newuser,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(newuser.pk)).decode(),
        'token': account_activation_token.make_token(newuser),
    })
    to_email = newuser_form.cleaned_data.get('email')
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
    args_1['registration_success'] = \
        '999999999 Please confirm your email address to complete the registration'
    return args_1


def registration(request):
    args = {}
    form = UserRegistrationForm()
    cosmetolog_types = CosmetologType.objects.filter(is_active=True)
    if request.POST:
        username_original = request.POST.get('username', '')
        email_1 = request.POST.get('email', '')
        password_11 = request.POST.get('password1', '')
        request.POST = request.POST.copy()
        request.POST['username'] = email_1
        request.POST['password2'] = password_11
        newuser_form = UserRegistrationForm(request.POST)
        cosmetolog_name = request.POST.get('cosmetolog_name', '')
        cosmetolog_type = request.POST.get('cosmetolog_type', '')

        # Check email is the same or not
        user_old = User.objects.filter(username=email_1).first()
        if user_old:
            if user_old.is_active:
                args['registration_error'] =\
                    'THE SAME E-MAIL and Account is active Please, use option FORGET THE PASSWORD'
                return render(request, 'landing/registration.html', args)
            else:
                now_again = '_AGAIN_'+'-'.join(('_'.join(str(datetime.datetime.now()).split(sep=' '))).split(sep=':'))
                user_old.username = str(user_old.username)+now_again
                user_old.email = str(user_old.email)+now_again
                # we have to change also emial in MySubscriber table - everywhere Uniq enail must be (one time)
                subs_old = Subscriber.objects.filter(email=email_1).first()
                subs_old.email = str(subs_old.email) + now_again
                user_old.save()
                subs_old.save()
                cosmetolog_old = Cosmetolog.objects.filter(name=cosmetolog_name).first()
                if cosmetolog_old:
                    cosmetolog_old.name = str(cosmetolog_name)+now_again
                    cosmetolog_old.order_email = str(email_1)+now_again
                    cosmetolog_old.save()
                validate_save_user_send_email(request, newuser_form, email_1,
                                              username_original, cosmetolog_name, cosmetolog_type)
                return redirect('registration_profile')
        else:
            if newuser_form.is_valid():
                validate_save_user_send_email(request, newuser_form, email_1,
                                              username_original, cosmetolog_name, cosmetolog_type)
                return redirect('registration_profile')
            else:
                form = newuser_form
                print(form.error_messages)
    return render(request, 'landing/registration.html', locals())


def registration_profile(request):
    aswer = "wefewrfergrtgrtgersd"
    return render(request, 'landing/registration_profile.html', locals())


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        profile = Subscriber.objects.get(email=user.email)
        profile.email_confirm = True
        profile.save()
        # return render(request, 'landing/profile.html', locals())
        return redirect('profile')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def profile(request):
    username_now = auth.get_user(request).username
    form = CosmetologForm(request.POST or None)
    if username_now:
        subscriber_current = Subscriber.objects.filter(email=username_now).first()

        cosmetolog_first_id = SubscriberCosmetolog.objects.filter(
            subscriber_id=subscriber_current.id).first().cosmetolog_id
        cosmetolog_url = Cosmetolog.objects.get(pk=cosmetolog_first_id).slug
        return HttpResponseRedirect('/profile/' + cosmetolog_url, locals())
    else:
        authorization_error = "Просмотр профиля только для зарегистрированного менеджера."\
                              + '\n' + "Ввойдите в систему, пожалуйста."
        print(authorization_error)
        return render(request, 'landing/login.html', locals())


def do_save_profile(request, cosmetolog_url):
    user_profile = Cosmetolog.objects.filter(pk=request.POST.get('cosmetolog_id', '')).first()
    form = CosmetologForm(request.POST, request.FILES, instance=user_profile)
    if form.is_valid():
        form_save = form.save(commit=False)
        form_save.city_cosmetolog = Address.objects.get(pk=request.POST.get('city_cosmetolog',''))
        # form1_save.category = service_category
        form_save.save()
        profile_success = "success"
        print(profile_success)
        return locals()
    else:
        form = CosmetologForm()
    return locals()
    # return render(request, 'landing/profile.html', locals())


def do_add_service(request, cosmetolog_url):
    user_profile = Cosmetolog.objects.filter(pk=request.POST.get('cosmetolog_id', '')).first()
    service_category = CategoryForCosmetolog.objects.filter(name=request.POST.get('category_name', '')).first()
    service_subcategory = SubCategoryForCosmetolog.objects.filter(name=request.POST.get('subcategory_name', '')).first()
    form1 = AddServiceForm(request.POST or None)
    form2 = AddServiceImageForm(request.POST, request.FILES or None)
    if form1.is_valid() and form2.is_valid():
        form1_save = form1.save(commit=False)
        form1_save.cosmetolog = user_profile
        form1_save.category = service_category
        form1_save.subcategory = service_subcategory
        form1_save.save()
        form2_save = form2.save(commit=False)
        form2_save.is_main = True
        form2_save.is_active = True
        form2_save.service_product = form1_save
        form2_save.save()
        profile_success = "success"
        return HttpResponseRedirect('/profile/' + cosmetolog_url, locals())
    else:
        print(form1.errors)
        form1 = AddServiceForm()
    return render(request, 'landing/profile.html', locals())

def test_ajax(request):
    return_dict = dict()
    session_key = request.session.session_key
    data = request.POST
    service_category = data.get("category_name")
    service_category_object = CategoryForCosmetolog.objects.get(name=service_category, is_active=True)
    service_subcategory_set = SubCategoryForCosmetolog.objects.filter(category=service_category_object, is_active=True)
    i = 1
    for item in service_subcategory_set:
        return_dict[i] = item.name
        i +=1
    return JsonResponse(return_dict)


def profile_cosmetolog(request, cosmetolog_url=None):
    cosmetolog_object = Cosmetolog.objects.get(slug=cosmetolog_url)
    form = CosmetologForm(request.POST or None, instance=cosmetolog_object)
    form1 = AddServiceForm()
    form2 = AddServiceImageForm()
    service_types = CategoryForCosmetolog.objects.filter(is_active=True)
    subservice_types = SubCategoryForCosmetolog.objects.filter(is_active=True)
    service_set = ServiceProduct.objects.filter(cosmetolog = cosmetolog_object)
    # @property
    # def logo_image(self):
    #     if self.image and hasattr(self.image, 'url'):
    #         return self.image.url
    if request.POST:
        if '_save_profile' in request.POST:
            do_save_profile(request, cosmetolog_url)
            return HttpResponseRedirect('/profile/' + cosmetolog_url, locals())
        elif '_add_service' in request.POST:
            do_add_service(request, cosmetolog_url)
    return render(request, 'landing/profile.html', locals())


def profile_cosmetolog_edit_service(request, cosmetolog_url, service_slug):
    return render(request, 'landing/profile.html', locals())

def login(request):
    args = {}
    # args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            # print("user_login", user)
            return HttpResponseRedirect(reverse(profile))
            # return HttpResponseRedirect('/profile' + url_full)
        else:
            login_error = "NO NO NO NO NO NO NO"
            return render(request, 'landing/login.html')
            # return render_to_response('login.html', args)
    else:
        return render(request, 'landing/login.html', locals())
        # return render_to_response('login.html', args)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse(home))
    # return redirect("/")


def home(request):
    # username = auth.get_user(request).username

    address_cosmetologs = Cosmetolog.objects.filter(is_active=True)
    cosmetolog_addresses = CosmetologAddress.objects.filter(is_active=True)
    search_active_addresses = Address.objects.filter(is_active=True)
    active_addresses = search_active_addresses.filter(
        Q(type_id=5) |
        Q(type_id=4)
    ).order_by('type_id')
    service_categories = CategoryForCosmetolog.objects.filter(is_active=True)
    subservice_categories = SubCategoryForCosmetolog.objects.filter(is_active=True)
    service_products = ServiceProduct.objects.filter(is_active=True, is_visible=True)
    service_products_images_all = ServiceProductImage.objects.filter(is_active=True, is_main=True,
                                                                     service_product__is_active=True,
                                                                     service_product__is_visible=True)
    service_products_images = service_products_images_all[:4]
    cosmetologs_all = Cosmetolog.objects.filter(is_active=True, is_visible=True)
    cosmetologs = cosmetologs_all[:4]
    slider_mains = SliderMain.objects.filter(is_active=True, is_main=True)
    slider_mains_counts = range(slider_mains.count() - 1)
    advert_all = SliderMain.objects.filter(is_active=True, is_main=False)
    advert_left = advert_all.get(position=1)
    advert_right = advert_all.get(position=2)
    advert_right_up = advert_all.get(position=3)
    advert_right_down = advert_all.get(position=4)
    blogs_images_all = BlogImage.objects.filter(is_active=True, is_main=True)
    blogs_images = blogs_images_all[:4]
    products_images_all = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True)
    products_images = products_images_all[:4]
    products_images_new = products_images_all.filter(product__category__id=1)
    products_images_popular = products_images_all.filter(product__category__id=2)

    return render(request, 'landing/home.html', locals())


def search_ajax(request):
    if request.is_ajax:
        q_address = request.GET.get('term','').capitalize()
        q_99 = q_address.replace(',','').split()

        q_address_set = Address.objects.filter(full_address__icontains=q_99[0])

        if len(q_99) > 1:
            i = 1
            for i in range(1,len(q_99)):
                q_100 = q_99[i].capitalize()
                q_address_set = q_address_set.filter(full_address__icontains=q_100)
                i += 1

        # q_address_set = Address.objects.filter(full_address__icontains=q_address)

        q_results = []

        for i in q_address_set:
            i_json = {}
            i_json['label'] = i.display_address
            i_json['value'] = i.display_address
            i_json['id'] = i.id
            q_results.append(i_json)

        # print('q_results', q_results)
        q_data_json = json.dumps(q_results)

    else:
        q_data_json = 'fail'

    mimetype = 'application/json'
    return HttpResponse(q_data_json, mimetype)


def search_ajax_service(request):
    if request.is_ajax:
        q_service = request.GET.get('term','').capitalize()
        q_99 = q_service.replace(',','').split()

        q_service_set = SubCategoryForCosmetolog.objects.filter(subcategory_category__icontains=q_99[0])

        if len(q_99) > 1:
            i = 1
            for i in range(1,len(q_99)):
                q_100 = q_99[i].capitalize()
                q_service_set = q_service_set.filter(subcategory_category__icontains=q_100)
                i += 1

        q_results = []

        for i in q_service_set:
            i_json = {}
            i_json['label'] = i.subcategory_category
            i_json['value'] = i.subcategory_category
            i_json['id'] = i.id
            q_results.append(i_json)

        q_data_json = json.dumps(q_results)

    else:
        q_data_json = 'fail'

    mimetype = 'application/json'
    return HttpResponse(q_data_json, mimetype)


def search_ajax_city(request):
    if request.is_ajax:
        # print()
        q_city = request.GET.get('term','').capitalize()
        q_99 = q_city.replace(',','').split()

        q_address_set = Address.objects.filter(full_address__icontains=q_99[0], type_id=4)

        if len(q_99) > 1:
            i = 1
            for i in range(1,len(q_99)):
                q_100 = q_99[i].capitalize()
                q_address_set = q_address_set.filter(full_address__icontains=q_100)
                i += 1

        q_results = []

        for i in q_address_set:
            i_json = {}
            i_json['label'] = i.display_address
            i_json['value'] = i.display_address
            i_json['id'] = i.id
            q_results.append(i_json)

        # print('q_results', q_results)
        q_data_json = json.dumps(q_results)

    else:
        q_data_json = 'fail'

    mimetype = 'application/json'
    return HttpResponse(q_data_json, mimetype)


def search_ajax_street(request):
    data = request.POST
    city_id = data.get("city_id")
    city_street_set = Address.objects.filter(type_id=10, parent_id__parent_id=city_id)

    q_results = []

    for i in city_street_set:
        i_json = {}
        i_json['label'] = i.display_address
        i_json['value'] = i.display_address
        i_json['id'] = i.id
        q_results.append(i_json)

    q_data_json = json.dumps(q_results)

    mimetype = 'application/json'
    return HttpResponse(q_data_json, mimetype)


def get_address_url(q_address_id):
    address_object = Address.objects.get(pk=q_address_id)
    print('address_object', address_object)
    address_url = address_object.url
    if address_object.type_id == 4:
        print('city')
        address_url = address_url + '/' + 'vse-rajony/' + 'vse-ulicy/' + 'vse-doma'
        print('address_url', address_url)
    elif address_object.type_id == 5:
        print('rajon')
        address_url = address_url + '/' + 'vse-ulicy/' + 'vse-doma'
        print('address_url', address_url)
    else:
        print('ulica')
        house = random.randrange( 1, 100, 1)
        address_url = address_url + '/' + str(house)
        print('address_url', address_url)
    return address_url


def get_service_url(q_service_id):
    service_object = SubCategoryForCosmetolog.objects.get(pk=q_service_id)
    service_url = service_object.url
    return service_url


def salon(request):
    q_address_id = request.GET.get('q_48')
    q_service_id = request.GET.get('q_148')
    if q_address_id != '' and q_service_id != '':
        print('both')
        address_url = get_address_url(q_address_id)
        service_url = get_service_url(q_service_id)
        url_full = service_url + address_url +  '/'
        return HttpResponseRedirect(url_full)
    elif q_address_id != '' and q_service_id == '':
        print('address')
        address_url = get_address_url(q_address_id)
        url_full = 'vse/uslugi' + address_url + '/'
        print('address', address_url)
        return HttpResponseRedirect(url_full)
    elif q_address_id == '' and q_service_id != '':
        print('service')
        service_url = get_service_url(q_service_id)
        url_full = service_url + '/vse-goroga/vse-rajony/vse-ulicy/vse-doma' + '/'
        return HttpResponseRedirect(url_full)
    else:
        print('NO NO NO NO')
        error = True
        return HttpResponseRedirect(reverse(home), {'error': error})


def get_city_district_street_id(q_city, q_district, q_street):
    if q_street != 'vse-ulicy':
        q_address_url = '/' + q_city + '/' + q_district + '/' + q_street
        search_city_active_addresses = Address.objects.get(is_active=True, url__exact=q_address_url)
        street_id = search_city_active_addresses.id
        district_id = search_city_active_addresses.parent_id.id
        city_id = search_city_active_addresses.parent_id.parent_id.id
        type_id = search_city_active_addresses.type_id
        print(987654321, street_id, district_id, city_id, type_id)
    elif q_district !='vse-rajony':
        q_address_url = '/' + q_city + '/' + q_district
        search_city_active_addresses = Address.objects.get(is_active=True, url__exact=q_address_url)
        district_id = search_city_active_addresses.id
        city_id = search_city_active_addresses.parent_id.id
        type_id = search_city_active_addresses.type_id
        street_id = 0
        print(987654321, street_id, district_id, city_id, type_id)
    else:
        q_address_url = '/' + q_city
        search_city_active_addresses = Address.objects.get(is_active=True, url__exact=q_address_url)
        city_id = search_city_active_addresses.id
        type_id = search_city_active_addresses.type_id
        street_id = 0
        district_id = 0
        print(987654321, street_id, district_id, city_id, type_id)
    display_address = search_city_active_addresses.display_address
    city_name = Address.objects.get(pk=city_id).name
    if district_id:
        district_name = str(Address.objects.get(pk=district_id).name) + ' ' + str(Address.objects.get(pk=district_id).type_level)
    else:
        district_name = None
    if street_id:
        street_name = str(Address.objects.get(pk=street_id).name) + ' ' + str(Address.objects.get(pk=street_id).type_level)
    else:
        street_name = None
    return street_name, district_name, city_name, display_address, street_id, district_id, city_id, type_id


def get_subservice_id(q_service, q_subservice):
    q_subservice_url = q_service + '/' + q_subservice
    search_active_subservice = SubCategoryForCosmetolog.objects.get(is_active=True, url__exact=q_subservice_url)
    subservice_id = search_active_subservice.id
    # print('subservice_id', subservice_id, type(subservice_id))
    return search_active_subservice, subservice_id


def get_cosmetolog_address_set(address_id, type_id, subservice_id=None):
    cosmetolog_address_set = set()
    # print(9876543321, type(subservice_id), 9999999)
    if subservice_id:
        if type_id == 10:
            cosmetolog_address_object_set = CosmetologAddress.objects.filter(is_active=True, street_id=address_id,
                                                                             service_name__subcategory_id = subservice_id)
        elif type_id == 5:
            cosmetolog_address_object_set = CosmetologAddress.objects.filter(is_active=True, district_id=address_id,
                                                                             service_name__subcategory_id = subservice_id)
        elif type_id == 4:
            cosmetolog_address_object_set = CosmetologAddress.objects.filter(is_active=True, city_id=address_id,
                                                                             service_name__subcategory_id = subservice_id)
    else:
        if type_id == 10:
            cosmetolog_address_object_set = CosmetologAddress.objects.filter(is_active=True, street_id=address_id)
        elif type_id == 5:
            cosmetolog_address_object_set = CosmetologAddress.objects.filter(is_active=True, district_id=address_id)
        elif type_id == 4:
            cosmetolog_address_object_set = CosmetologAddress.objects.filter(is_active=True, city_id=address_id)
    if cosmetolog_address_object_set:
        for j in cosmetolog_address_object_set:
            cosmetolog_address_set.add(j.cosmetolog_id)
    return cosmetolog_address_set


def get_service_images_address(cosmetolog_street_set, cosmetolog_district_set, cosmetolog_city_set):
    service_street_images = ServiceProductImage.objects.filter(
        is_active=True, is_main=True, service_product__is_active=True,
        service_product__is_visible=True, service_product__cosmetolog__id__in=cosmetolog_street_set)
    service_district_images = ServiceProductImage.objects.filter(
        is_active=True, is_main=True, service_product__is_active=True, service_product__is_visible=True,
        service_product__cosmetolog__id__in=cosmetolog_district_set).exclude(service_product__cosmetolog__id__in=cosmetolog_street_set)
    service_city_images = ServiceProductImage.objects.filter(
        is_active=True, is_main=True, service_product__is_active=True, service_product__is_visible=True,
        service_product__cosmetolog__id__in=cosmetolog_city_set).exclude(service_product__cosmetolog__id__in=cosmetolog_street_set).exclude(service_product__cosmetolog__id__in=cosmetolog_district_set)
    return service_street_images, service_district_images, service_city_images


def search_service_address(request, q_1, q_2, q_3, q_4, q_5, q_6):
    print('search - q1:', q_1) #категория услуги - проверка на vse
    print('search - q2', q_2) #субкатегория услуги
    print('search - q3', q_3) #город - проверка на vse-goroga
    print('search - q4', q_4) #район
    print('search - q5', q_5) #улица
    print('search - q6', q_6) #дом (рандомный), вне анализа
    logo_images = LogoImage.objects.filter(is_active=True, is_main=True)

    if q_1 == 'vse':          #сервис-нет и город-да, надо показать все активные сервисы на Этом адрессе и Уточните Сервис
        print("service-NO and city-YES")
        street_name, district_name, city_name, display_address, street_id, district_id, city_id, type_id = \
            get_city_district_street_id(q_3, q_4, q_5)
        # получаем сэт ид косметологов у кого есть любые услуги по этой улице
        cosmetolog_street_set = get_cosmetolog_address_set(street_id, 10)
        # получаем сэт ид косметологов у кого есть любые услуги по этому району
        cosmetolog_district_set = get_cosmetolog_address_set(district_id, 5)
        # получаем сэт ид косметологов у кого есть любые услуги по этому городу
        cosmetolog_city_set = get_cosmetolog_address_set(city_id, 4)
        service_street_images, service_district_images, service_city_images =\
            get_service_images_address(cosmetolog_street_set, cosmetolog_district_set, cosmetolog_city_set)
        subservice_categories = SubCategoryForCosmetolog.objects.filter(is_active=True)
        print('set for street', cosmetolog_street_set)
        print('service images for street', service_street_images)
        print('set for district', cosmetolog_district_set)
        print('service images for district', service_district_images)
        print('set for city', cosmetolog_city_set)
        print('service images for city', service_city_images)
    elif q_3 == 'vse-goroga': #сервис-да и город-нет, надо показать Этот сервис для всех активных косметологов во всех городах
        print("service-YES and city-NO")
        service_street_images = None
        service_district_images = None
        search_active_subservice, subservice_id = get_subservice_id(q_1, q_2)
        service_city_images = ServiceProductImage.objects.filter(
            is_active=True, is_main=True, service_product__is_active=True,
            service_product__is_visible=True, service_product__subcategory__category_id=subservice_id)
        active_addresses_towns = Address.objects.filter(is_active=True, type_id=4)
        # city_list = set()
        for i in active_addresses_towns:
            oldstr = i.url
            i.slug = oldstr.replace("/", "")
            # city_list.add(newstr)
            # i.slug = slugify(i.name)
    else:                     # сервис-да и город-да, надо показать Этот сервис по Этому адресу
        print('service-YES and city-YES')
        street_name, district_name, city_name, display_address, street_id, district_id, city_id, type_id = \
            get_city_district_street_id(q_3, q_4, q_5)
        search_active_subservice, subservice_id = get_subservice_id(q_1, q_2)
        # получаем сэт ид косметологов у кого есть Эта услуги по Этой улице
        cosmetolog_street_set = get_cosmetolog_address_set(street_id, 10, subservice_id)
        # получаем сэт ид косметологов у кого есть Эта услуга по Этому району
        cosmetolog_district_set = get_cosmetolog_address_set(district_id, 5, subservice_id)
        # получаем сэт ид косметологов у кого есть Эта услуга по Этому городу
        cosmetolog_city_set = get_cosmetolog_address_set(city_id, 4, subservice_id)
        service_street_images, service_district_images, service_city_images = \
            get_service_images_address(cosmetolog_street_set, cosmetolog_district_set, cosmetolog_city_set)
        if city_id:
            active_addresses_town_districts = Address.objects.filter(parent_id=city_id)
            for i in active_addresses_town_districts:
                oldstr = i.url
                search_index = oldstr.rfind('/')
                i.slug = oldstr[search_index+1:]
        if district_id:
            active_addresses_town_district_streets = Address.objects.filter(parent_id=district_id)
            for i in active_addresses_town_district_streets:
                oldstr = i.url
                search_index = oldstr.rfind('/')
                i.slug = oldstr[search_index+1:]
    if service_street_images or service_district_images or service_city_images:
        print('yes_yesy_yesy 2019 2019 2019')
        return render(request, 'landing/search_results.html', locals())
    else:
        print('NO NO NO No NO 2019 2019 2019')
        return render(request, 'landing/no_search_results.html', locals())


def contact(request):
    session_key = request.session.session_key
    args = {}
    form = LetterForm()

    if request.POST:
        new_letter_form = LetterForm(request.POST)
        if new_letter_form.is_valid():
            username = auth.get_user(request).username
            if username:
                user_current = Subscriber.objects.filter(email=username).first()
                new_letter = new_letter_form.save(commit=False)
                new_letter.user_name = user_current.name
                new_letter.user_email = user_current.email
                data = new_letter_form.cleaned_data
                new_letter.save()
            else:
                data = new_letter_form.cleaned_data
                new_letter = new_letter_form.save()

            subject = 'message from site renew-polska.pl/contact' + request.POST.get('subject', '')
            message = request.POST.get('message', '')
            from_email = settings.EMAIL_HOST_USER
            to_list = ['biuro@renew-polska.pl', settings.EMAIL_HOST_USER]
            send_mail(subject, message, from_email, to_list, fail_silently=True)

            letter_success = "success"
        else:
            form = new_letter_form
            # print(form.error_messages)

    return render(request, 'landing/contact.html', locals())


def about(request):
    session_key = request.session.session_key
    args = {}
    about_text_object = Page.objects.get(is_active=True, page_name="About")
    print(about_text_object)
    # about_text = about_text_object.page_text

    return render(request, 'landing/about.html', locals())


def training(request):
    session_key = request.session.session_key
    args = {}
    trainings_all = Training.objects.filter(is_active=True)

    return render(request, 'landing/warsztaty.html', locals())


def validate_training_send_email(request, trainee_name, trainee_email, email_message):
    # Email sending code:
    new_trainee = TrainingUser.objects.filter(trainee_email=trainee_email).first()
    current_site = get_current_site(request)
    mail_subject = 'Confirm Your Registration for' + trainee_name + 'at Renew-Polska.pl'
    message = render_to_string(email_message, {
        'user': trainee_name,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(new_trainee.pk)),
        'token': account_activation_token.make_token(new_trainee),
    })
    to_email = trainee_email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
    print(999999999999999999999999)
    return 999


def training_item(request, slug):
    # registration_success = 1
    # product = Product.objects.get(slug=slug)

    training = Training.objects.get(slug=slug, is_active=True)
    date_now = datetime.datetime.now(datetime.timezone.utc)
    day_left = (training.start_date - date_now).days
    if day_left >= 7:
        left_place_shown = training.total_place * 0.5
    else:
        left_place_shown = int(training.total_place * 0.5)
    print(day_left)
    left_place = training.left_place
    print('left place', left_place)
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    form = TrainingUserForm()
    username = auth.get_user(request).username  # This is EMAIL in fact
    if username:
        user_current = Subscriber.objects.filter(email=username).first()
        username = user_current.name # this is NAME in fact (not EMAIL)
        registered_user = TrainingUser.objects.filter(trainee_email=user_current.email).first()
        if registered_user:
            registered_message = "already"
    if request.POST:
        print(form.errors)
        new_registration_form = TrainingUserForm(request.POST)
        print(new_registration_form.errors)
        if new_registration_form.is_valid():
            trainee_email = request.POST.get('trainee_email', '')
            training_id = request.POST.get('training', '')
            print(training_id)
            training_users = TrainingUser.objects.filter(training=training_id)
            print(training_users)
            if training_users:
                training_user_set = set()
                for i in training_users:
                    training_user_set.add(i.trainee_email)
                if trainee_email in training_user_set:
                    registered_message = "already"
                    return render(request, 'landing/training_item_full.html', locals())
                print('training_user_set', training_user_set)
                print('trainee_email', trainee_email)
            if username:
                new_registration = new_registration_form.save(commit=False)
                new_registration.user_name = user_current.name
                new_registration.user_email = user_current.email
                data = new_registration_form.cleaned_data
                new_registration.save()
                email_message = 'landing/training_confirmation_email_acc.html'
                validate_training_send_email(request, request.POST.get('trainee_name', ''),
                                             trainee_email, email_message)
            else:
                user_yes = Subscriber.objects.filter(email=trainee_email).first()
                if user_yes:
                    login_message = 'please_register'
                    return render(request, 'landing/login.html', locals())
                else:
                    data = new_registration_form.cleaned_data
                    new_letter = new_registration_form.save()
                    email_message = 'landing/training_confirmation_email_not_user.html'
                    validate_training_send_email(request, request.POST.get('trainee_name', ''),
                                                 trainee_email, email_message)
            registration_success = "success"
            training.registered_place += 1
            training.save()

            # subject = 'Somebody has registered on your training' + training.name
            # message = username + '\n' + trainee_email + '\n' + request.POST.get('trainee_tel_number', '') + '\n'\
            #           + training.name + '\n' + request.POST.get('comments', '')
            # from_email = settings.EMAIL_HOST_USER
            # to_list = ['biuro@renew-polska.pl', settings.EMAIL_HOST_USER]
            # send_mail(subject, message, from_email, to_list, fail_silently=True)

        else:
            form = new_registration_form
            registration_error = "error"
    registered_user = TrainingUser.objects.filter(user_name=username, id=training.id).first()
    if registered_user:
        registered_message = "already"

    return render(request, 'landing/training_item_full.html', locals())


def activate_training(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = TrainingUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, TrainingUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('training')
    else:
        return HttpResponse('Activation link is invalid!')
