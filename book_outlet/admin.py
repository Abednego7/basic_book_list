from django.contrib import admin
from .models import Book, Author, Address, Country

# Register your models here.


class BookAdmin(admin.ModelAdmin):
    # Aqui vamos a cargar las propiedades (no variables)
    # ese slug es el nombre sacado del model
    # readonly_fields = ("slug",)
    # Nota: se comento esa propiedad para que pueda funcionar correctamente (prepopulated_fields).

    # Pre-visualizar los valores en tiempo real (del form)
    # usamos "title" porque en eso se basa la creacion del slug
    prepopulated_fields = {"slug": ("title",)}
    list_filter = (
        "author",
        "rating",
    )
    # Esta propiedad permite visualizar mas columnas.
    list_display = ("title", "author")


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Address)
admin.site.register(Country)
