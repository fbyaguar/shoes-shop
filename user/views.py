from django.contrib.auth import logout, login
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView
import shoes
from shoes.models import Shoes
from user.forms import Registration_form, User_login_form #Add_to_wishlist_form
from django.contrib import messages
# Create your views here.
from user.models import Wishlist
from cart.models import Cart
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.models import User
from django.template import context, loader
from django.template.loader import render_to_string



def registration(request):
    if request.method=='POST':
        form = Registration_form(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.info(request,'Спасибо за регистрацию')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = Registration_form()
    return render(request,'user/registration.html',{'form':form})

def user_login(request):
    if request.method == 'POST':
        form = User_login_form(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            messages.info(request, 'Успешная авторизация')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка авторизации')

    else:
        form = User_login_form()
    return render(request, 'user/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')


class WishlistView(ListView):
    template_name = 'user/wishlist.html'
    model = Shoes
    context_object_name = 'favorite'


    def get_queryset(self):
        # try:
        user_wishlist = Wishlist.objects.filter(user_id=self.request.user).values_list('shoes_id', flat=True)
        queryset = Shoes.objects.filter(pk__in=user_wishlist)

        print(user_wishlist)
        return queryset
        # except Exception:
        #     raise Http404("Error. Wrong queryset")

    def get(self, request, *args, **kwargs):
        user = request.user
        if request.is_ajax():
            if request.GET.get('action')== 'delete':
                try:
                    wishlist = Wishlist.objects.get(user_id=user, shoes_id=request.GET.get('shoes_id'))
                    wishlist.delete()
                    user_wishlist = Wishlist.objects.filter(user_id=self.request.user).values_list('shoes_id',
                                                                                                   flat=True)
                    context = {'favorite': Shoes.objects.filter(pk__in=user_wishlist)}
                    #return render(request, 'user/wishlist.html', {'favorite':self.queryset})
                    # template = loader.get_template('user/favorites_list.html')
                    # html = template.render(context)
                    html = render_to_string('user/favorites_list.html', context)
                    print('должен быть хтмл')
                    print(html)
                    return JsonResponse({'html':html}, status=200,content_type="application/json")
                    #return render(request, 'user/wishlist.html', context)

                except Exception:
                    messages.info(request, 'Не удалось удалить обьект с избранного')
            if request.GET.get('action') == 'cart':
                try:
                    if Cart.objects.filter(Q(user_id=user) & Q(shoes_id=request.GET.get('shoes_id'))).count() == 0:
                        Cart.objects.create(user_id=user, shoes_id=request.GET.get('shoes_id'), number=1)
                    else:
                        cart = Cart.objects.get(Q(user_id=user) & Q(shoes_id=request.GET.get('shoes_id')))
                        cart.number+=1
                        cart.save()
                except Exception:
                    messages.info(request, 'Не удалось обавить обьект в корзину')


        return super(WishlistView, self).get(request, *args, **kwargs)



    # def post(self,request):
    #     form = Add_to_wishlist_form(request.POST)
    #     if form.is_valid():
    #         wishlist = form.save(commit=False)
