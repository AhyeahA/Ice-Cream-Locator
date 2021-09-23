from django.contrib import admin

# Register your models here.
from .models import User, IceCreamStore, IceCreamFlavors, Favorite_Wantto_Visited_Store, FavoriteIceCreamFlavor, RatingsAndReview, RecentSearch



class FavoriteIceCreamFlavorInline(admin.TabularInline):
    model = FavoriteIceCreamFlavor
    extra = 1

class Favorite_Wantto_Visited_StoreInline(admin.TabularInline):
    model = Favorite_Wantto_Visited_Store
    extra = 1

class IceCreamStoreDisplay(admin.ModelAdmin):
    list_display = ('store_name', 'current_location_lat', 'current_location_lon' )

class RecentSearchDisplay(admin.ModelAdmin):
    verbose_name_plural = "RecentSearches"
    list_display = ('user', 'search_content', 'time_stamp' )

class RatingsAndReviewDisplay(admin.ModelAdmin):
    list_display = ('user', 'store', 'rating','reviews')

class IceCreamFlavorStoreDisp(admin.ModelAdmin):
    filter_horizontal = ('str_fk',)
    list_display = ('flavor_name', )

class UserAdmin(admin.ModelAdmin):
    inlines = [FavoriteIceCreamFlavorInline,Favorite_Wantto_Visited_StoreInline]
# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(IceCreamStore, IceCreamStoreDisplay)
admin.site.register(IceCreamFlavors,IceCreamFlavorStoreDisp)
admin.site.register(Favorite_Wantto_Visited_Store)
admin.site.register(FavoriteIceCreamFlavor)
admin.site.register(RecentSearch,RecentSearchDisplay)
admin.site.register(RatingsAndReview,RatingsAndReviewDisplay)