from django.shortcuts import render, HttpResponse, Http404, redirect
from accounts.models import UserProfile
from shop.models import Product, Affiliate
from django.contrib.auth import authenticate, login
from accounts.forms import LoginForm, UserRegistrationForm,CreateUserProfile, EditUserProfile, CreditForm
import xml.etree.ElementTree as ET
from django.core.mail import BadHeaderError, send_mail
from django.core.mail import EmailMultiAlternatives
from shop.models import Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os
import time
import urllib.request
from django.db.models import Q

# Create your views here.

def user_login(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.info(request, 'Ön sikeresen bejelentkezett!')
                    return redirect('accounts:profile')
                else:
                    return redirect('accounts:login')
            else:
                return redirect('accounts:login')
    else:
        messages.warning(request, 'Hibás felhasználónév vagy jelszó! Kérem próbálkozzon újra ...')
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form,'categories':categories})


def register(request):
    categories = Category.objects.all()
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST, prefix="user")
        profile_form = CreateUserProfile(request.POST,request.FILES, prefix="profile")
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            password = (user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            email_to = user.email

            subject, from_email, to = 'premiumDog.hu - Sikeres regisztráció!', 'info@premiumdog.hu', email_to
            text_content = 'This is an important message.'
            html_content = "<p><strong>Kedves Partnerünk!</strong></p><p>Üdvözöljük a premiumDog.hu rendszerében!</p><p>Köszönjük hogy minket választott.</p><p>Személyes információik:</p><p>Felhasználónév: %s</p><p>Email cím: %s</p><p>Jelszó: %s</p><br><a href='#'>Bejelentkezés</a><br><p>Kérdéseiddel, kéréseiddel és észrevételeiddel fordulj ügyfélszolgálatunkhoz az info@premiumdog.hu email címen!</p><p>Üdvözlettel,<br>a premiumDog.hu csapata<br>Email: info@premiumDog.hu</p><small>Értesítés: Minden információt, melyet a premiumDog.hu kap és küld, bizalmasan kezelünk. Soha nem osztjuk meg őket egy harmadik féllel. Ha ezt az emailt véletlenül kapta, kérjük jelezze a feladónak. Ez az üzenet bizalmas információkat tartalmaz és csak a címzettnek szól. Ha nem Ön a szándékolt címzett, ezennel értesítjük, hogy az üzenet tartalmának nyilvánosságra hozatala, másolása, továbbítása vagy az azzal való bármilyen visszaélés szigorúan tilos. Továbbá elfogadjuk kifejezett hozzájárulását a premiumDog.hu oldalon nyújtott szolgáltatásokkal kapcsolatban a visszavonási időszak alatt. Valamint, hogy tudomásul veszi, hogy a visszavonási/megszakítási joga megszűnik, miután a kredit csomagot elkezdte használni.</small>" % (user, password, email_to)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            time.sleep(3)

            subject, from_email, to = 'Új regisztráció', 'info@premiumdog.hu', 'info@premiumdog.hu'
            text_content = 'This is an important message.'
            html_content = "<p>Jelentkezz be a rendszerbe és ellenőrízd le az adatokat, majd vedd fel a kapcsolatot az új regisztrált taggal.</p><p>Felhasználónév: '%s'</p><p>Jelszó: '%s'</p>" % (user, password)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


            return render(request, 'accounts/register_done.html', {'user': user,'categories':categories})
    else:
        user_form = UserRegistrationForm(prefix="user")
        profile_form = CreateUserProfile(prefix="profile")
    context = {"user_form": user_form, "profile_form": profile_form, "categories":categories}
    return render(request, 'accounts/register.html', context)


@login_required
def check_credit(request):
    user = UserProfile.objects.filter(Q(credit__lte = 200))
    for x in user:
        print(x.user.email)
        print('A felhasználónak elküldve a figyelmeztetés')
        subject, from_email, to = 'Hamarosan lefogy a creditje', 'info@premiumdog.hu', x.user.email
        text_content = 'This is an important message.'
        html_content = '<p>This is an <strong>important</strong> message.</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        time.sleep(10)
    return HttpResponse('A folyamat elkészült, kérem zárja be az ablakot.')

@login_required
def profile(request):
    user = request.user
    profile = UserProfile.objects.get(user = user)
    last_affiliates = Affiliate.objects.filter(affiliate_user = user)[0:10]
    return render(request, 'accounts/profile.html', {'profile':profile, 'last_affiliates':last_affiliates})

@login_required
def profile_product(request):
    user = request.user
    products = Product.objects.filter(user = user)
    return render(request, 'accounts/profile_product.html', {'products':products})

@login_required
def profile_product_details(request, pk, slug):
    product = Product.objects.get(product_id = pk, slug = slug)
    category = product.product_category
    company = product.user
    return render(request, 'accounts/profile_product_details.html', {'product':product,'category':category,'company':company})

@login_required
def profile_credit(request):
    user = request.user
    available_credit = UserProfile.objects.get(user = user)
    if request.method == "POST":
        store_name = request.POST.get('store_name')
        form_of_enterprise = request.POST.get('form_of_enterprise')
        pack = request.POST.get('pack')
        tax_number = request.POST.get('tax_number')
        tax_number_eu = request.POST.get('tax_number_eu')
        store_registration_number = request.POST.get('store_registration_number')
        store_main_location = request.POST.get('store_main_location')
        store_city = request.POST.get('store_city')
        store_zip = request.POST.get('store_zip')
        store_street = request.POST.get('store_street')
        store_contact_email = request.POST.get('store_contact_email')
        store_contact_phone = request.POST.get('store_contact_phone')

        pack = int(pack)

        #add credit
        credit = UserProfile.objects.get(user = user)
        credit_old = credit.credit
        credit_new = credit_old + pack
        credit.credit = credit_new
        credit.save()

        products = Product.objects.filter(user = user)
        for product in products:
            product.active = True
            product.save()

        try:
            subject, from_email, to = 'Sikeres kreditfeltöltés', 'info@premiumdog.hu', store_contact_email
            text_content = 'This is an important message.'
            html_content = '<p><strong>Kedves Partnerünk!</strong></p><p>Köszönjük! Sikeresen feltöltötte egyenlegét!</p><p>Kérdéseiddel, kéréseiddel és észrevételeiddel fordulj ügyfélszolgálatunkhoz az info@premiumdog.hu email címen!</p><p>Üdvözlettel,<br>a premiumDog.hu csapata<br>Email: info@premiumDog.hu</p><small>Értesítés: Minden információt, melyet a premiumDog.hu kap és küld, bizalmasan kezelünk. Soha nem osztjuk meg őket egy harmadik féllel. Ha ezt az emailt véletlenül kapta, kérjük jelezze a feladónak. Ez az üzenet bizalmas információkat tartalmaz és csak a címzettnek szól. Ha nem Ön a szándékolt címzett, ezennel értesítjük, hogy az üzenet tartalmának nyilvánosságra hozatala, másolása, továbbítása vagy az azzal való bármilyen visszaélés szigorúan tilos. Továbbá elfogadjuk kifejezett hozzájárulását a premiumDog.hu oldalon nyújtott szolgáltatásokkal kapcsolatban a visszavonási időszak alatt. Valamint, hogy tudomásul veszi, hogy a visszavonási/megszakítási joga megszűnik, miután a kredit csomagot elkezdte használni.</small>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print('Kreditfeltöltési igény elküldve a felhasználó részére ...')
        except:
            pass


        time.sleep(3)

        try:
            subject, from_email, to = 'Kreditfeltöltési igény - díjbekérő kiállítás', 'info@premiumdog.hu', 'info@premiumdog.hu'
            text_content = 'This is an important message.'
            html_content = "<p><strong>Új kreditfeltöltés történt</strong></p><p>A megrendelés részletei:</p><p>Cég neve:'%s'</p><p>Vállalkozási forma: '%s'</p><p>Csomag: '%s'</p><p>Adoszám/EU-Adószám: '%s', '%s'<p/><p>Cégjegyzékszám: '%s'</p><p>Cím: '%s', '%s', '%s', '%s' </p><p>E-mail cím: '%s'</p><p>Telefonszám: '%s'</p>" % (store_name,form_of_enterprise, pack, tax_number, tax_number_eu, store_registration_number, store_main_location, store_city, store_zip, store_street, store_contact_email, store_contact_phone)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print('Kreditfeltöltési igény elküldve a premiumDog.hu részére...')
        except:
            pass

        messages.success(request, 'A kreditfeltöltés sikeres volt, látogasson el az e-mail fiókjába!')
        return redirect('accounts:profile')
    else:
        credit_form = CreditForm(instance=request.user.userprofile)

        context = {'credit_form':credit_form, 'available_credit':available_credit}
        return render(request, 'accounts/profile_credit.html', context)

@login_required
def profile_affiliate(request):
    user = request.user
    affiliates = Affiliate.objects.filter(affiliate_user = user)[0:5000]
    top_product = Product.objects.filter(user = user).order_by('-product_visitor')[0:8]
    return render(request, 'accounts/profile_affiliate.html', {'affiliates':affiliates, 'top_product':top_product})

@login_required
def edit_user_profile(request):
    if request.method == 'POST':
        profile_form = EditUserProfile(request.POST, request.FILES, instance=request.user.userprofile)  # request.FILES is show the selected image or file

        if profile_form.is_valid():
            custom_form = profile_form.save(False)
            custom_form.save()
            messages.success(request, 'A fiók módosítása sikeresen megtörtént!')
            return redirect('accounts:profile')
    else:
        profile_form = EditUserProfile(instance=request.user.userprofile)
        args = {}
        # args.update(csrf(request))
        args['profile_form'] = profile_form
        return render(request, 'accounts/edit_profile.html', args)


@login_required
def update_product_list(request):

    user_id = request.user
    xml = UserProfile.objects.filter(user = user_id)
    for x in xml:
        url = x.xml_link
        file_name = "%s.xml" % user_id
        file_path = os.path.join('priceking/assets/', file_name)
        print('Beginning file download with urllib2...')

        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, file_path)

        dom = ET.parse(file_path)
        products = dom.findall('product')
        print('Termékek feldolgozása')
        for p in products:
            short_description = p.find("short_description")
            if short_description is not None:
                continue

            product_id = p.find('product_id').text
            product_name = p.find('title').text
            product_price = p.find('price').text
            product_category = p.find('categories').text
            product_image_link = p.find('image_link').text
            product_link = p.find('link').text
            product_description = p.find('description').text
            #product_short_description = p.find('short_description').text
            product_sale_price = p.find('sale_price').text
            product_sku = p.find('sku').text
            product_quantity = p.find('quantity').text
            product_available = p.find('available').text
            '''
            xml_sync, created = Product.objects.update_or_create(
                product_id=product_id,
                user=user_id,
                product_name = product_name,
                product_price = product_price,
                product_image_link = product_image_link,
                product_link = product_link,
                product_description = product_description,
                product_short_description = product_short_description,
                product_sale_price = product_sale_price,
                product_sku = product_sku,
                product_available = product_available,
                product_quantity = product_quantity,
                defaults={
                    "product_id":product_id,
                    'user':user_id,
                    'product_name':product_name,
                    'product_price':product_price,
                    'product_image_link':product_image_link,
                    'product_link':product_link,
                    'product_description':product_description,
                    'product_short_description':product_short_description,
                    'product_sale_price':product_sale_price,
                    'product_sku': product_sku,
                    'product_available':product_available,
                    'product_quantity':product_quantity
                    })

            if created:
                pass
                print('létrehozva')
                # A new product object created
            else:
                pass
                print('létezik')
                # product object already exists
            '''

            if Product.objects.filter(product_id=product_id, user=user_id).exists():
                print("Létezik")
                new_values = Product.objects.get(product_id=product_id, user=user_id)
                new_values.product_name = product_name
                new_values.product_price = product_price
                #new_values.product_category = product_category
                new_values.product_image_link = product_image_link
                new_values.product_link = product_link
                new_values.product_description = product_description
                new_values.product_short_description = short_description
                new_values.product_sale_price = product_sale_price
                new_values.product_sku = product_sku
                new_values.product_available = product_available
                new_values.product_quantity = product_quantity
                new_values.save()

            else:
                print("Nem létezik")
                p = Product.objects.create(
                    product_id=product_id,
                    product_name=product_name,
                    product_price=product_price,
                    product_link=product_link,
                    #product_category = product_category,
                    product_image_link=product_image_link,
                    product_description=product_description,
                    product_short_description=short_description,
                    product_sku=product_sku,
                    product_sale_price=product_sale_price,
                    product_quantity=product_quantity,
                    product_available=product_available,
                    user=user_id)
                p.save()

        os.remove(file_path)

    messages.success(request, 'A termékek sikeresen frissítve lettek!')
    return redirect('accounts:profile')



@login_required
def update_xml(request):
    users = UserProfile.objects.all()
    for user in users:
        user_id = user.user
        print(user_id)
        xml = UserProfile.objects.filter(user = user_id)
        for x in xml:
            url = x.xml_link
            print(url)

            try:
                file_name = "%s.xml" % user_id
                file_path = os.path.join('priceking/assets/', file_name)

                print('Beginning file download with urllib2...')

                opener=urllib.request.build_opener()
                opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                urllib.request.install_opener(opener)

                urllib.request.urlretrieve(url,file_path)
                dom = ET.parse(file_path)
                products = dom.findall('product')

                print('Termékek feldolgozása')


                for p in products:
                    short_description = p.find("short_description")
                    if short_description is None:
                        short_description = p.find("short_description")
                        continue


                    product_id = p.find('product_id').text
                    product_name = p.find('title').text
                    product_price = p.find('price').text
                    product_category = p.find('categories').text
                    product_image_link = p.find('image_link').text
                    product_link = p.find('link').text
                    product_description = p.find('description').text
                    short_description = p.find('short_description').text
                    product_sale_price = p.find('sale_price').text
                    product_sku = p.find('sku').text
                    product_quantity = p.find('quantity').text
                    product_available = p.find('available').text


                    if Product.objects.filter(product_id=product_id, user=user_id).exists():
                        print("Létezik a termék")
                        new_values = Product.objects.get(product_id=product_id, user=user_id)
                        new_values.product_name = product_name
                        new_values.product_price = product_price
                        new_values.product_image_link = product_image_link
                        new_values.product_link = product_link
                        new_values.product_description = product_description
                        new_values.product_short_description = short_description
                        new_values.product_sale_price = product_sale_price
                        new_values.product_sku = product_sku
                        new_values.product_available = product_available
                        new_values.product_quantity = product_quantity
                        new_values.save()

                    else:
                        print("Nem létezik a termék")
                        p = Product.objects.create(
                            product_id=product_id,
                            product_name=product_name,
                            product_price=product_price,
                            product_link=product_link,
                            product_image_link=product_image_link,
                            product_description=product_description,
                            product_short_description=short_description,
                            product_sku=product_sku,
                            product_sale_price=product_sale_price,
                            product_quantity=product_quantity,
                            product_available=product_available,
                            user=user_id)
                        p.save()

                os.remove(file_path)
                time.sleep(3)
            except:
                print('hiba a linkkel')
                pass

    print('Az xml letöltések és importálások készen vannak ...')
    return HttpResponse('siker')


@login_required
def credit_check(request):
    users = UserProfile.objects.all()
    for user in users:
        user_id = user.user
        credit = UserProfile.objects.filter(user = user_id)
        for x in credit:
            piece_of_credit = x.credit
            email = x.user.email

            if piece_of_credit < 250 and piece_of_credit > 0:
                print('250 - 0 közötti érték')
                '''
                try:
                    subject, from_email, to = 'Kredit hamarosan elfogy', 'sikler.sikler@gmail.com', email
                    text_content = 'This is an important message.'
                    html_content = "<p>Kedves Partnerünk!</p><p>Kreditje hamarosan elfogy. Jelenlegi kreditje: <strong>%s</strong><p>Ha ez a szám 0-ra csökken a termékei el fognak tünni a listából.</p> <p>Ahhoz, hogy újra feltöltse a kreditjét, lépjen be a fiókjába az alábbi linken.</p>" % (x.credit)
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    print('Kreditfeltöltési igény elküldve a felhasználó részére ...')
                except:
                    pass
                '''
            elif piece_of_credit <= 0:
                credit_is_null_user_list = UserProfile.objects.filter(credit__lte = piece_of_credit, user = user_id)
                for credit_is_null_user in credit_is_null_user_list:
                        user_email = credit_is_null_user.user.email
                        user_credit = credit_is_null_user.user
                        new_values = Product.objects.filter(user = user_credit)
                        for value in new_values:
                            value.active = False
                            value.save()

                        print('lefogyott a kredit....')
                        '''
                        try:
                            subject, from_email, to = 'Kredit elfogyott', 'sikler.sikler@gmail.com', user_email
                            text_content = 'This is an important message.'
                            html_content = "<p>Kedves Partnerünk!</p><p>Kreditje elfogyott.</p> <p>A termékei inaktívak, azaz nem látszódnak.</p> <p>Ahhoz, hogy újra látszódjanak töltse fel a kreditjét. Lépjen be a fiókjába az alábbi linken.</p>"
                            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                            msg.attach_alternative(html_content, "text/html")
                            msg.send()
                            print('Kreditfeltöltési igény elküldve a felhasználó részére ...')
                        except:
                            pass
                        '''
                        time.sleep(3)

    return redirect('shop:homepage')










