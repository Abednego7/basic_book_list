from django.shortcuts import get_object_or_404, render
from django.http import Http404

# Average
from django.db.models import Avg

# Import Models
from .models import Book

# Create your views here.


def index(request):
    # Para ordenar de forma descendente se usa un signo de -
    books = Book.objects.all().order_by("-title")
    # Para no repetir la consulta, la optimizamos como sabemos:
    num_books = books.count()
    # usamos el nombre de rating, puesto que ese es el nombre en el models:
    avg_rating = books.aggregate(Avg("rating"))

    return render(
        request,
        "book_outlet/index.html",
        {
            "books": books,
            "total_number_of_books": num_books,
            "average_rating": avg_rating,
        },
    )


def book_detail(request, slug):
    """
    try:
        book = Book.objects.get(pk=id)
    except:
        raise Http404()
    """
    # slug (models): slug (parametro)
    book = get_object_or_404(Book, slug=slug)
    return render(
        request,
        "book_outlet/book_detail.html",
        {
            "title": book.title,
            "author": book.author,
            "rating": book.rating,
            "is_bestseller": book.is_bestselling,
        },
    )
