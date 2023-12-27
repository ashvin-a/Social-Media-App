"""Code snippet for repetitive function"""
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.db.models.query import QuerySet
from django.contrib.auth.models import User


def paginate(request: HttpRequest, x: QuerySet[User]):
    """
    A function used for pagination.
    """
    paginator = Paginator(x, per_page=4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj
