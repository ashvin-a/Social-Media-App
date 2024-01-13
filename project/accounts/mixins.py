from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.http import HttpRequest


class PaginatorMixin:
    """
    A mixin used for pagination.
    """
    def paginate(self, request: HttpRequest, x: QuerySet[User]):
        """
        A function used for pagination.

        Args:
            request (HttpRequest): The HTTP request object.
            x (QuerySet[User]): The queryset to paginate.

        Returns:
            page_obj (Page): The paginated page object.
        """
        paginator = Paginator(x, per_page=4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj


class LoginMixin(LoginRequiredMixin):
    """
    A mixin used to require login for a view.

    Args:
        login_url (str): The URL to redirect to if the user
        is not authenticated.
    """
    login_url = "login-page"


class AllowedUsersMixin:
    """
    A mixin used to restrict access to a view based on the user's group.

    Args:
        allowed_roles (list): A list of allowed group names.
    """
    allowed_roles = ["admin"]

    def dispatch(self, request, *args, **kwargs):
        """
        A function used to dispatch the request.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response object.
        """
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group in self.allowed_roles:
            return super().dispatch(request, *args, **kwargs)
        else:
            return render(request, "accounts/denied.html")
