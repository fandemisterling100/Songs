import pytest

from app.users.models import User
from app.users.tests.factories import UserFactory
from app.users.views import UserRedirectView, UserUpdateView, user_detail_view
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http.response import Http404
from django.test import RequestFactory

pytestmark = pytest.mark.django_db


class TestUserUpdateView:
    """
    TODO:
        extracting view initialization code as class-scoped fixture
        would be great if only pytest-django supported non-function-scoped
        fixture db access -- this is a work-in-progress for now:
        https://github.com/pytest-dev/pytest-django/pull/258
    """

    def test_get_success_url(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_success_url() == f"/users/{user.username}/"

    def test_get_object(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == user

    def test_update_object(self, user: User, rf: RequestFactory):
        request = rf.post({"name": "Other name"})  # type: ignore
        from django.contrib.messages.storage.fallback import FallbackStorage

        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = user
        response = UserUpdateView.as_view()(request)
        assert response.status_code == 302


class TestUserRedirectView:
    def test_get_redirect_url(self, user: User, rf: RequestFactory):
        view = UserRedirectView()
        request = rf.get("/fake-url")
        request.user = user

        view.request = request

        assert view.get_redirect_url() == f"/users/{user.username}/"


class TestUserDetailView:
    def test_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = UserFactory()

        response = user_detail_view(request, username=user.username)

        assert response.status_code == 200

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()  # type: ignore

        response = user_detail_view(request, username=user.username)

        assert response.status_code == 302
        assert response.url == "/accounts/login/?next=/fake-url/"

    def test_case_sensitivity(self, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = UserFactory(username="UserName")

        with pytest.raises(Http404):
            user_detail_view(request, username="username")
