from typing import Iterable
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Importar funcion reverse
from django.urls import reverse

# Importamos funcion de transformacion de texto a slug
from django.utils.text import slugify


# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=80)
    code = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.name} {self.code}"

    class Meta:
        verbose_name_plural = "Countries"


# Notas:
# * La propiedad de models.ForeignKey, genera una relacion -> 'Muchos a uno'
# * La propiedad de models.OneToOneField, hace lo que su nombre indica -> 'Uno a uno'
# * Al crear una relacion 'Uno a uno', no hace falta configurar el nombre de la relacion,
# ya que no retorna un conjunto o set, puesto que es una relacion Uno a uno y el resultado siempre sera uno;
# ademas el nombre de la relacion al consultar desde Address sera: 'author'
class Address(models.Model):
    street = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=5)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.street}, {self.postal_code}, {self.city}"

    # Clase anidada
    class Meta:
        # propiedad:
        # Esta propiedad nos sirve de forma estetica unicamente:
        # Al estar en la pagina de admin, todos los nombres de tablas se muestran en 'PLURAL',
        # es decir, Django les agrega una 's' al final del nombre...
        # Ejem: Addresss
        # Con la propiedad de 'verbose_name_plural', podemos definir el nombre de la tabla en la pagina de admin...
        # Ojo, esto es solo con fines esteticos, en realidad no cambia el nombre original de la tabla.
        verbose_name_plural = "Address Entries"


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True)

    # Funcion para ser llamada en cualquier parte:
    # plantillas, etc.
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()


class Book(models.Model):
    # Google: django model fields reference
    # Migraciones: Crearlas y Ejecutarlas, para el uso de nuestros modelos
    # 1.Crear modelo de base de datos (las class)
    # 2.Crear migraciones:      py manage.py makemigrations
    # 3.Ejecutar migraciones:   py manage.py migrate
    title = models.CharField(max_length=50)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    # Para estos dos valores nuevos, podemos hacer dos cosas:
    # 1.Podemos usar la palabra clave ( default= ) para poder proporcionar algun valore por defecto.
    # 2.Podemos usar la palabra clave de ( null= ) y dejarlo en True
    # 3.Usar el valor de blank=True

    # Relacion: 1 - M
    # Author ahora sera una foreing key y se conecta con Author
    # CASCADE = Si se elimina un author, tambien los libros relacionados.
    # null para evitar errores al hacer migraciones, puesto que esa columna se modifico y contenia valores.
    # y tambien si hay libros de los cuales se desconoce su author.

    # Para agregar un nombre para la 'relacion de la foreing key', se utiliza la propiedad de 'related_name'.
    # para que surja efecto, se debe guardar el cambio.
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, null=True, related_name="books"
    )

    is_bestselling = models.BooleanField(default=False)
    # Slug -> Example: Harry Potter 1 -> harry-potter-1
    # db_index=True: optimizacion de consultas, para busquedas repetitivas.
    # Para evitar campos requeridos en admin page, se deja en blank=True
    # La propiedad editable=True, quita el campo del form en admin page.
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)

    # Crear relacion Muchos a Muchos:
    # nota: no se puede agregar la propiedad: on_delete
    # esto se debe al tipo de relacion, Django crea una tercera tabla intermedia,
    # donde se agregan filas dependiendo de las iteraciones y cuando se elimina un registro,
    # Django va a esa tabla intermedia y elimina esas conexiones.
    published_countries = models.ManyToManyField(Country, null=True)

    # Al guardar los datos, se llama a nuestro metodo sobreescrito,
    # el cual crea el slug automaticamente para ese registro que se guardara en la BD.
    # Nota: se elimina esta funcion debido a que el slug se esta generando automaticamente tambien en el admin.
    """
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        # super().save() -> Guarda los datos en la BD
        super().save(*args, **kwargs)
    """

    def get_absolute_url(self):
        return reverse("book-detail", args=[self.slug])

    # Esta edicion tambien afecta como se presentaran los nombres de los libros en la interfaz de admin.
    def __str__(self):
        return f"{self.title} ({self.rating})"
