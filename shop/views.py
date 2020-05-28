from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import AffiliateLinkForm
from .models import Product, Affiliate, Category
from accounts.models import UserProfile
from django.db.models import Q
from django.db.models import Max
from datetime import date, time, datetime
from django.core.paginator import Paginator


def homepage(request):

    #update_product_list()
    companies = UserProfile.objects.all()[0:8]
    categories = Category.objects.all().order_by('category_order')

    products_last = Product.objects.filter(active = True).order_by('-created_at')[0:8]
    products_most = Product.objects.filter(active = True).order_by('-product_visitor')[0:8]
    products_offer = Product.objects.filter(is_offer = True, active = True).order_by('?')[0:8]
    products_discount = Product.objects.filter(product_sale_price__isnull=False, active = True).order_by('?')[0:8]

    return render(request, 'product/homepage.html', {'companies':companies,'categories':categories, 'products_last':products_last,'products_most':products_most,'products_offer':products_offer,'products_discount':products_discount})


def product_last(request):
    products = Product.objects.filter(active = True).order_by('-created_at')
    paginator = Paginator(products, 32)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    category_list = Category.objects.all().order_by('category_order')

    return render(request, 'product/product_latest.html', {'products': products, 'category_list':category_list, 'page_obj':page_obj})


def product_list_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    categories = Category.objects.all().order_by('category_order')
    product_list = Product.objects.filter(product_category=category, active = True)
    paginator = Paginator(product_list, 32)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    return render(request, 'product/product_list_by_category.html', {'products':products, 'categories':categories, 'category':category})


def product_filter(request):
    category_list = Category.objects.all().order_by('category_order')
    companies = UserProfile.objects.all()

    if request.method == 'GET':

        price1 = request.GET.get('min_price', 0)
        price2 = request.GET.get('max_price', 0)
        category = request.GET.getlist('category')
        company = request.GET.getlist('company')

        if not price2:
            price2 = Product.objects.aggregate(Max('product_price'))['product_price__max']

        if company and price1 and category:
            products = Product.objects.filter(Q(product_category__slug__in = category) & Q(user__username__in = company) & Q(product_price__range=(price1, price2)) & Q(active = True))

        elif company and category:
            products = Product.objects.filter(Q(product_category__slug__in = category) & Q(user__username__in = company) & Q(active = True))

        elif company:
            products = Product.objects.filter(Q(user__username__in = company) & Q(active = True))

        elif price1 and category:
            products = Product.objects.filter(Q(product_price__range=(price1, price2)) & Q(product_category__slug__in = category) & Q(active = True))

        elif price1:
            products = Product.objects.filter(Q(product_price__range=(price1, price2)) & Q(active = True))

        elif category:
            products = Product.objects.filter(Q(product_category__slug__in = category) & Q(active = True))

        else:
            print('----')
            products = Product.objects.filter(active=True)

    context = {'products':products, 'category_list':category_list, 'companies':companies, 'price1':price1, 'price2':price2, 'category':category, 'company':company}
    #return HttpResponse('siker')
    return render(request, 'product/product_filter.html', context)


def product_most_viewed(request):
    products = Product.objects.filter(active = True).order_by('-product_visitor')
    paginator = Paginator(products, 32)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    category_list = Category.objects.all().order_by('category_order')
    return render(request, 'product/product_most_viewed.html',{'products':products, 'category_list':category_list, 'page_obj':page_obj})


def product_offer(request):
    products = Product.objects.filter(is_offer = True, active = True).order_by('-product_visitor')
    paginator = Paginator(products, 32)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    category_list = Category.objects.all().order_by('category_order')
    return render(request, 'product/product_offer.html',{'products':products, 'category_list':category_list, 'page_obj':page_obj})


def product_discount(request):
    products = Product.objects.filter(product_sale_price__isnull=False, active = True)
    paginator = Paginator(products, 32)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    category_list = Category.objects.all().order_by('category_order')
    print(products)
    return render(request, 'product/product_discount.html',{'products':products, 'category_list':category_list, 'page_obj':page_obj})


def product_details(request, pk, slug):
    categories = Category.objects.all().order_by('category_order')
    '''
    from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
    from django.http import HttpResponse
    '''
    product = get_object_or_404(Product, product_id = pk, slug = slug)
    '''
    try:
        product = get_object_or_404(Product, product_id = pk, slug = slug)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        product = Product.objects.filter(product_id = pk, slug = slug).first()
        #return HttpResponse('ger')
    '''
    category = product.product_category
    company = product.user
    company_name = UserProfile.objects.get(user = company)
    related_product_from_company = Product.objects.filter(product_category = category, user = company, active=True).order_by('?')[0:3]
    related_product_by_category = Product.objects.filter(product_category = category, active=True).order_by('?')[0:3]


    if request.method == 'POST':
        formset = AffiliateLinkForm(request.POST, instance=product)
        if formset.is_valid():
            product_id = formset.cleaned_data.get('product_id')
            user = formset.cleaned_data.get('user')
            name = formset.cleaned_data.get('product_name')
            price = formset.cleaned_data.get('product_price')
            link = formset.cleaned_data.get('product_link')
            ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
            price = int(price)

            d = date.today()
            min_time = time.min
            max_time = time.max
            today_start = datetime.combine(d, min_time)
            today_end = datetime.combine(d, max_time)

            print(today_start)
            print('-------------------')


            affiliate_user_protect = Affiliate.objects.filter(affiliate_user = user, affiliate_product_id = product_id, affiliate_ip_address = ip_address, created_at__gte = today_start, created_at__lte = today_end)
            redirect_counter = len(affiliate_user_protect)
            print(redirect_counter)
            for x in affiliate_user_protect:
                print(x.created_at)


            if redirect_counter > 3:
                print('tiltas')
                return redirect(link)
            else:
                print('mehet tovabb')

                if price >= 199 and price < 0:
                    affiliate_user_obj = UserProfile.objects.get(user = user)
                    affiliate_new_creadit = affiliate_user_obj.credit - 0
                    affiliate_user_obj.credit = affiliate_new_creadit  # change field

                    Affiliate.objects.create(
                    affiliate_product_id=product_id,
                    affiliate_product_name = name,
                    affiliate_link = link,
                    affiliate_user = user,
                    affiliate_ip_address = ip_address
                    )
                    form_field = formset.save(commit=False)
                    form_field.save()

                    product_visitor_now = Product.objects.filter(product_id = product_id)
                    product_visitor_increase = Product.objects.get(product_id = product_id)

                    for x in product_visitor_now:
                        now = x.product_visitor
                        increased = now + 1

                    product_visitor_increase.product_visitor = increased
                    product_visitor_increase.save()

                    user_credit_now = UserProfile.objects.get(user = user)
                    print(user_credit_now.credit)
                    if user_credit_now.credit > 9900:
                        print('nagyonn mint 9900')
                    else:
                        print('Kisebb mint 9900')

                    return redirect(link)

                elif price >= 200 and price < 1999:
                    affiliate_user_obj = UserProfile.objects.get(user = user)
                    affiliate_new_creadit = affiliate_user_obj.credit - 14
                    affiliate_user_obj.credit = affiliate_new_creadit  # change field
                    affiliate_user_obj.save() # this will update only
                    print('price < 200 and price > 1999')

                    Affiliate.objects.create(
                    affiliate_product_id=product_id,
                    affiliate_product_name = name,
                    affiliate_link = link,
                    affiliate_user = user,
                    affiliate_ip_address = ip_address
                    )
                    form_field = formset.save(commit=False)
                    form_field.save()

                    product_visitor_now = Product.objects.filter(product_id = product_id)
                    product_visitor_increase = Product.objects.get(product_id = product_id)

                    for x in product_visitor_now:
                        now = x.product_visitor
                        increased = now + 1

                    product_visitor_increase.product_visitor = increased
                    product_visitor_increase.save()

                    user_credit_now = UserProfile.objects.get(user = user)
                    print(user_credit_now.credit)
                    if user_credit_now.credit > 9900:
                        print('nagyonn mint 9900')
                    else:
                        print('Kisebb mint 9900')

                    return redirect(link)

                elif price >= 2000 and price < 9999:
                    affiliate_user_obj = UserProfile.objects.get(user = user)
                    affiliate_new_creadit = affiliate_user_obj.credit - 19
                    affiliate_user_obj.credit = affiliate_new_creadit  # change field
                    affiliate_user_obj.save() # this will update only
                    print('price < 2000 and price > 9999')

                    Affiliate.objects.create(
                    affiliate_product_id=product_id,
                    affiliate_product_name = name,
                    affiliate_link = link,
                    affiliate_user = user,
                    affiliate_ip_address = ip_address
                    )
                    form_field = formset.save(commit=False)
                    form_field.save()

                    product_visitor_now = Product.objects.filter(product_id = product_id)
                    product_visitor_increase = Product.objects.get(product_id = product_id)

                    for x in product_visitor_now:
                        now = x.product_visitor
                        increased = now + 1

                    product_visitor_increase.product_visitor = increased
                    product_visitor_increase.save()

                    user_credit_now = UserProfile.objects.get(user = user)
                    print(user_credit_now.credit)
                    if user_credit_now.credit > 9900:
                        print('nagyonn mint 9900')
                    else:
                        print('Kisebb mint 9900')

                    return redirect(link)

                elif price >= 10000 and price < 24999:
                    affiliate_user_obj = UserProfile.objects.get(user = user)
                    affiliate_new_creadit = affiliate_user_obj.credit - 21
                    affiliate_user_obj.credit = affiliate_new_creadit  # change field
                    affiliate_user_obj.save() # this will update only
                    print('price < 10000 and price > 24999')

                    Affiliate.objects.create(
                    affiliate_product_id=product_id,
                    affiliate_product_name = name,
                    affiliate_link = link,
                    affiliate_user = user,
                    affiliate_ip_address = ip_address
                    )
                    form_field = formset.save(commit=False)
                    form_field.save()

                    product_visitor_now = Product.objects.filter(product_id = product_id)
                    product_visitor_increase = Product.objects.get(product_id = product_id)

                    for x in product_visitor_now:
                        now = x.product_visitor
                        increased = now + 1

                    product_visitor_increase.product_visitor = increased
                    product_visitor_increase.save()

                    user_credit_now = UserProfile.objects.get(user = user)
                    print(user_credit_now.credit)
                    if user_credit_now.credit > 9900:
                        print('nagyonn mint 9900')
                    else:
                        print('Kisebb mint 9900')

                    return redirect(link)

                elif price >= 25000 and price < 54990:
                    affiliate_user_obj = UserProfile.objects.get(user = user)
                    affiliate_new_creadit = affiliate_user_obj.credit - 25
                    affiliate_user_obj.credit = affiliate_new_creadit  # change field
                    affiliate_user_obj.save() # this will update only
                    print('price < 25000 and price > 54990')

                    Affiliate.objects.create(
                    affiliate_product_id=product_id,
                    affiliate_product_name = name,
                    affiliate_link = link,
                    affiliate_user = user,
                    affiliate_ip_address = ip_address
                    )
                    form_field = formset.save(commit=False)
                    form_field.save()

                    product_visitor_now = Product.objects.filter(product_id = product_id)
                    product_visitor_increase = Product.objects.get(product_id = product_id)

                    for x in product_visitor_now:
                        now = x.product_visitor
                        increased = now + 1

                    product_visitor_increase.product_visitor = increased
                    product_visitor_increase.save()

                    user_credit_now = UserProfile.objects.get(user = user)
                    print(user_credit_now.credit)
                    if user_credit_now.credit > 9900:
                        print('nagyonn mint 9900')
                    else:
                        print('Kisebb mint 9900')

                    return redirect(link)

                elif price >= 55000 and price < 99999:
                    affiliate_user_obj = UserProfile.objects.get(user = user)
                    affiliate_new_creadit = affiliate_user_obj.credit - 28
                    affiliate_user_obj.credit = affiliate_new_creadit  # change field
                    affiliate_user_obj.save() # this will update only
                    print('price < 55000 and price > 99999')

                    Affiliate.objects.create(
                    affiliate_product_id=product_id,
                    affiliate_product_name = name,
                    affiliate_link = link,
                    affiliate_user = user,
                    affiliate_ip_address = ip_address
                    )
                    form_field = formset.save(commit=False)
                    form_field.save()

                    product_visitor_now = Product.objects.filter(product_id = product_id)
                    product_visitor_increase = Product.objects.get(product_id = product_id)

                    for x in product_visitor_now:
                        now = x.product_visitor
                        increased = now + 1

                    product_visitor_increase.product_visitor = increased
                    product_visitor_increase.save()

                    user_credit_now = UserProfile.objects.get(user = user)
                    print(user_credit_now.credit)
                    if user_credit_now.credit > 9900:
                        print('nagyonn mint 9900')
                    else:
                        print('Kisebb mint 9900')

                    return redirect(link)

                elif price >= 100000:
                    affiliate_user_obj = UserProfile.objects.get(user = user)
                    affiliate_new_creadit = affiliate_user_obj.credit - 34
                    affiliate_user_obj.credit = affiliate_new_creadit  # change field
                    affiliate_user_obj.save() # this will update only

                    Affiliate.objects.create(
                    affiliate_product_id=product_id,
                    affiliate_product_name = name,
                    affiliate_link = link,
                    affiliate_user = user,
                    affiliate_ip_address = ip_address
                    )
                    form_field = formset.save(commit=False)
                    form_field.save()

                    product_visitor_now = Product.objects.filter(product_id = product_id)
                    product_visitor_increase = Product.objects.get(product_id = product_id)

                    for x in product_visitor_now:
                        now = x.product_visitor
                        increased = now + 1

                    product_visitor_increase.product_visitor = increased
                    product_visitor_increase.save()

                    user_credit_now = UserProfile.objects.get(user = user)
                    print(user_credit_now.credit)
                    if user_credit_now.credit > 9900:
                        print('nagyonn mint 9900')
                    else:
                        print('Kisebb mint 9900')

                    return redirect(link)

                else:
                    return HttpResponse('Valami hiba történt - Kérem lépjen a kezdőoldalra - premiumdog.hu')

    else:
        formset = AffiliateLinkForm(instance=product)
    return render(request, 'product/details.html', {'product':product,'categories':categories,'company_name':company_name,'related_product_from_company':related_product_from_company,'related_product_by_category':related_product_by_category,'formset': formset})


def store_list(request):
    store_list = UserProfile.objects.all()
    category_list = Category.objects.all().order_by('category_order')
    return render(request, 'product/store_list.html', {'store_list':store_list, 'category_list':category_list})


def store_details(request, store_slug):
    categories = Category.objects.all().order_by('category_order')
    store = UserProfile.objects.get(user = store_slug)
    products = Product.objects.filter(user = store_slug, active=True)
    paginator = Paginator(products, 32)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product/store_details.html', {'store':store,'categories':categories, 'products':products, 'page_obj':page_obj})


def category_list(request):
    category_list = Category.objects.all().order_by('category_order')
    return render(request, 'product/list_of_category.html', {'category_list':category_list})


def search_result(request):
    category_list = Category.objects.all().order_by('category_order')
    q = request.GET['q']
    kifejezesek = str(q).split(" ")
    query = Q()

    for kifejezes in kifejezesek:
        query = query | Q(product_name__contains=kifejezes)

        result = Product.objects.filter(query).distinct().exclude(active=False)

    context = {}
    if result.count() != 0:
        print('van találat')
        context = {"result": result, 'q':q, 'category_list':category_list}

    return render(request, 'product/search_result.html', context)


def for_company(request):
    return render(request, 'product/landing.html')


def page_gdpr(request):
    return render(request, 'product/page_gdpr.html')

def page_banner(request):
    return render(request, 'product/page_banner.html')

def page_aszf(request):
    return render(request, 'product/page_aszf.html')

