from rest_framework.response import Response
from rest_framework.views import APIView


class HostView(APIView):
    def get(self, request):
        return Response("method <GET>, resources <主机信息>, success")

    def post(self, request):
        return Response("method <POST>, resources <主机信息>, success")

    def put(self, request):
        return Response("method <PUT>, resources <主机信息>, success")

    def delete(self, request):
        return Response("method <DELETE>, resources <主机信息>, success")


class DNSView(APIView):
    def get(self, request):
        return Response("method <GET>, resources <DNS信息>, success")

    def post(self, request):
        return Response("method <POST>, resources <DNS信息>, success")

    def put(self, request):
        return Response("method <PUT>, resources <DNS信息>, success")

    def delete(self, request):
        return Response("method <DELETE>, resources <DNS信息>, success")
