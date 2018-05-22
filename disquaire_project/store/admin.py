from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

from .models import Booking, Contact, Album, Artist

# admin.site.register(Booking)

class AdminURLMixin(object):
    """docstring for AdminURLMixin."""
    def get_admin_url(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        return reverse("admin:store_%s_change" % (content_type.model), args=(obj.id, ))


class BookingInline(admin.TabularInline, AdminURLMixin):
    model = Booking
    readonly_fields = ['created_at', 'album_link', 'contacted']
    fieldsets = [
        (None, {'fields': ['created_at', 'album_link', 'contacted']})
        ] # list columns
    extra = 0
    verbose_name = "Réservation"
    verbose_name_plural = "Réservations"

    def has_add_permission(sel, request):
        return False

    def album_link(self, booking):
        url = self.get_admin_url(booking.album)
        return mark_safe("<a href='{}'</a>".format(url, booking.album.title))

    album_link.short_description = "Album"


class AlbumArtistInline(admin.TabularInline):
    model = Album.artists.through
    extra = 1
    verbose_name = "Disque"
    verbose_name_plural = "Disques"

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    inlines = [BookingInline, ]

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    inlines = [AlbumArtistInline, ]

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    search_fields = ['reference', 'title']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin, AdminURLMixin):
    readonly_fields = ['created_at', 'contact_link', 'album_link', 'contacted']
    fields = ['created_at', 'contact_link', 'album_link', 'contacted']
    list_filter = ['created_at', 'contacted']

    def has_add_permission(self, request):
        return False

    def contact_link(self, booking):
        url = self.get_admin_url(booking.contact)
        return mark_safe("<a href='{}'>{}</a>".format(url, booking.contact.name))

    def album_link(self, booking):
        url = self.get_admin_url(booking.album)
        return mark_safe("<a href='{}'>{}</a>".format(url, booking.album.title))