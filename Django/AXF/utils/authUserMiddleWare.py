from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from HomePage.models import UserModel


class AuthUserMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        if request.path == '/axf/home/' or request.path == '/axf/mine/'\
                or request.path == '/axf/login/' or request.path == '/axf/regist/'\
                or request.path == '/axf/market/' or request.path == '/axf/allgoods/'\
                or request.path == '/axf/my/':
            return None

        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return HttpResponseRedirect('/axf/home/')

        users = UserModel.objects.filter(ticket=ticket)
        if not users:
            return HttpResponseRedirect('/axf/regist/')

        request.user = users[0]
