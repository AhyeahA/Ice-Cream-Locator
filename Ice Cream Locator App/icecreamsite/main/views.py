from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse
from .models import User, IceCreamStore, IceCreamFlavors, Favorite_Wantto_Visited_Store, FavoriteIceCreamFlavor, RatingsAndReview, RecentSearch
from datetime import datetime 
# Create your views here.


def LoginView(request):
    errors = []
    userobj = User.objects.none()
    context = {
    'errors': errors,
    'user': userobj,
    }
    if request.method =='POST':
        buttonclicked = request.POST.get('buttonvalue')
        username = request.POST.get('username')
        password = request.POST.get('pass_word')
        if(buttonclicked == "Register a new account"):
            return RegisterView(request)
        else:
            if(User.objects.filter(username=username).exists()):
                userpassword = User.objects.get(username=username)
                if(userpassword.password == password):
                    userobj = userobj.union(User.objects.get(username=username))
                    context2 = {
                        'user': userobj,
                    }
                    print(userobj.username)
                    return render(request, 'main/mapresults.html', context2)
                else:
                    errors.extend(["Incorrect password"])
                    return render(request, 'main/login.html', context)
            elif(not User.objects.filter(username=username).exists() and username != ""):
                errors.extend(["Username incorrect or does not exist"])
                return render(request, 'main/login.html', context)

    return render(request, 'main/login.html', {})
     
def RegisterView(request):
    flavors = IceCreamFlavors.objects.all()
    errors = []
    context = {
    'flavors': flavors,
    'errors': errors,
    }
    if request.method =='POST':
       
        buttonclicked = request.POST.get('buttonclicked')
        print("buttonclicked" + str(buttonclicked))
        if(buttonclicked == "Submit"):
            allusers = User.objects.all()
            username = request.POST.get('username')
            firstname = request.POST.get('your_name')
            password = request.POST.get('pass_word')
            location = request.POST.get('loc')
            flavor_selected = request.POST.getlist('flavor')
            if not (User.objects.filter(username=username).exists()) and firstname != "" and location != "" and password != "" :
                if len(flavor_selected) == 0:
                    errors.extend(["Need to select at least one flavor"])
                    return render(request, 'main/signup.html', context)
                else:
                    User.objects.create(first_name= firstname,username=username,password=password,current_location_lat=location.split(",")[0],current_location_lng=location.split(",")[1])
                    userobject = User.objects.get(username=username)
                    #add flavors related to user
                    for f in flavor_selected:
                        flavorobj = IceCreamFlavors.objects.get(flavor_name = f)
                        FavoriteIceCreamFlavor.objects.create(user = userobject,flavor = flavorobj)
                    errors.extend(["Success!!"])
                    return render(request, 'main/signup.html', context)
            elif(username == ""):
                errors.extend(["Please enter empty Fields"])
                print(errors)
                return render(request, 'main/signup.html', context)
            elif(User.objects.filter(username=username).exists()):
                errors.extend(["Username not available"])
                print(errors)
                return render(request, 'main/signup.html', context)

        elif (buttonclicked == "Go back to login page"):
            return render(request, 'main/login.html', {})
    return render(request, 'main/signup.html', context)

def ProfileView(request):
    if request.method =='GET':
        return render(request, 'main/mapresults.html', context)
    if request.method =='POST':
        search = request.POST.get('search')
        print("search" + search)
        username = request.POST.get('username')
        userobject = User.objects.get(username=username)
        if search != "":
            stores = IceCreamStore.objects.none()
     
            if IceCreamStore.objects.filter(store_name__contains=search).exists():
                stores = IceCreamStore.objects.filter(store_name__contains=search)
                RecentSearch.objects.create(user = userobject,search_content = search )
            if IceCreamFlavors.objects.filter(flavor_name__contains=search).exists():
                allstores = IceCreamStore.objects.all()
                userobject = User.objects.get(username=username)
                    #add search to recent searches model
                RecentSearch.objects.create(user = userobject,search_content = search )
            for store in allstores:
                if IceCreamStore.objects.get(id=store.id).icecreamflavors_set.filter(flavor_name__contains=search).exists():
                    stores = stores.union(IceCreamStore.objects.filter(id=store.id))
                    print(stores)       
                context = {
                    'stores': stores,
                    'user' : userobject,
                }
            return render(request, 'main/mapresults.html', context)
        if request.POST.get('buttonclicked') != None:
            if request.POST.get('buttonclicked') == username + "'s Profile":
                username = request.POST.get('username')
                
                favoriteicecreams = FavoriteIceCreamFlavor.objects.filter(user=userobject)
                checkoptions = Favorite_Wantto_Visited_Store.objects.filter(user=userobject)
                context = {
                    'user':userobject,
                    'flavors': favoriteicecreams,
                    'checkoptions': checkoptions,
                }
               
                return render(request, 'main/profile.html', context)
            elif request.POST.get('buttonclicked') == "Map":
                context2 = {
                    'user': userobject,
                }
                return render(request, 'main/mapresults.html', context2)

def MapView(request):
    context = {}
    foundflavors = IceCreamFlavors.objects.none()
    if request.method =='GET':
        return render(request, 'main/mapresults.html', context)
    if request.method =='POST':
        username = request.POST.get('username')
        print("button clicked" + request.POST.get('buttonclicked'))
        if request.POST.get('buttonclicked') != None:
            if request.POST.get('buttonclicked') == username + "'s Profile":
                userobject = User.objects.get(username=username)
                favoriteicecreams = FavoriteIceCreamFlavor.objects.filter(user=userobject)
                checkoptions = Favorite_Wantto_Visited_Store.objects.filter(user=userobject)
                context = {
                    'user':userobject,
                    'flavors': favoriteicecreams,
                    'checkoptions': checkoptions,
                }
             
                return render(request, 'main/profile.html', context)
            else:
                storequery = request.POST.get('buttonclicked')
                print(storequery)
                if storequery != "Map":
                    username1 = request.POST.get('username')
                    userobject1 = User.objects.get(username=username1)
                    storeobject = IceCreamStore.objects.get(store_name__contains=storequery)
                    reviews = RatingsAndReview.objects.filter(store=storeobject)
                    allflavors = IceCreamFlavors.objects.filter(str_fk=storeobject)
                    for f in allflavors:
                        foundflavors = foundflavors.union(IceCreamFlavors.objects.filter(id=f.id))
                        context2 = {
                            'flavors': foundflavors,
                            'storename': storeobject,
                            'user': userobject1,
                            'reviews': reviews,
                        }
                    return render(request, 'main/storepage.html', context2)
        search = request.POST.get('search')
        userobject = User.objects.get(username=username)
        print(username)
        stores = IceCreamStore.objects.none()
     
        if IceCreamStore.objects.filter(store_name__contains=search).exists():
            stores = IceCreamStore.objects.filter(store_name__contains=search)
            RecentSearch.objects.create(user = userobject,search_content = search )
        if IceCreamFlavors.objects.filter(flavor_name__contains=search).exists():
            allstores = IceCreamStore.objects.all()
            userobject = User.objects.get(username=username)
                    #add search to recent searches model
            RecentSearch.objects.create(user = userobject,search_content = search )
            for store in allstores:
                if IceCreamStore.objects.get(id=store.id).icecreamflavors_set.filter(flavor_name__contains=search).exists():
                    stores = stores.union(IceCreamStore.objects.filter(id=store.id))
                    print(stores)       
        context = {
        'stores': stores,
        'user' : userobject,
        }
    return render(request, 'main/mapresults.html', context)


def StatisticsView(request):
    favoriteflavorresults=[]
    flavors = IceCreamFlavors.objects.all()
    allstores = IceCreamStore.objects.all()
    searchoccurences = []
    allsearches = RecentSearch.objects.all()
    users = User.objects.all()
    for s in allsearches:
        if s.search_content != "":
            count1 = RecentSearch.objects.filter(search_content__contains=s.search_content).count()
            if count1 != 0:
                if s.search_content not in searchoccurences:
                    searchoccurences.extend([s.search_content,count1])
    for f in flavors:
        count = FavoriteIceCreamFlavor.objects.filter(flavor=f).count()
        if count != 0:
            favoriteflavorresults.extend([f.flavor_name,count])
    context = {
        'favoriteflavors': favoriteflavorresults,
        'searchcount': searchoccurences,
    }
    return render(request, 'main/statictics.html', context)


def StoreView(request):
    if request.method =='POST':
        foundflavors = IceCreamFlavors.objects.none()
        errors = []
        wanttovisit = False
        beenvisited = False
        Favorite = False
        username = request.POST.get('username')
        storequery = request.POST.get('storename')
        storeobject = IceCreamStore.objects.get(store_name__contains=storequery)
        reviews = RatingsAndReview.objects.filter(store=storeobject)
        allflavors = IceCreamFlavors.objects.filter(str_fk=storeobject)
        for f in allflavors:
            foundflavors = foundflavors.union(IceCreamFlavors.objects.filter(id=f.id))
        setRating = request.POST.get('ratevalue')
        setReview = request.POST.get('setReview')
        option_selected = request.POST.getlist('optioncheckbox')
        userobject = User.objects.get(username=username)
        context = {
        'flavors': foundflavors,
        'storename': storeobject,
        'reviews': reviews,
        'errors': errors,
        'user' : userobject,
        }
        if setRating == None and setReview == None:
            errors.extend(["Please fill in both Rating and Review"])
            return render(request, 'main/storepage.html', context)
        elif int(setRating) > 5 or int(setRating) < 1:
            errors.extend(["Rating should be a positive number or less than or equal to 5"])
            return render(request, 'main/storepage.html', context)
        else:
            #add to rating review model
            RatingsAndReview.objects.create(user = userobject,store = storeobject,rating = int(setRating), reviews = setReview)
            #check which checkboxes have been selected
            for op in option_selected:
                if op == "Want to Visit":
                    wanttovisit = True
                elif op == "Been Visited":
                    beenvisited = True
                elif op == "Favorite":
                    Favorite = True
            if wanttovisit or beenvisited or Favorite:
                Favorite_Wantto_Visited_Store.objects.create(user = userobject, store = storeobject ,favorite_store =Favorite ,want_to_visit = wanttovisit,been_visited = beenvisited )
            errors.extend(["Success!"])   
            return render(request, 'main/storepage.html', context)
    return render(request, 'main/storepage.html', {})

