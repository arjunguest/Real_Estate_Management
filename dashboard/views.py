from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from django.utils import timezone
from django.urls import reverse_lazy
from django.db import models
from rest_framework.filters import SearchFilter
from django.db.models import Q
from rest_framework import generics

from django.contrib.auth import get_user_model

from dashboard.models import AiUser, Unit, Tenant, Lease
from dashboard.serializers import RegisterSerializer, LoginSerializer, TenantSerializer, UnitSerializer

# Create your views here.
class RegisterApi(APIView):
    api_view = ['POST']
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/signuppage.html'

    def post(self, request):
            try:
                if AiUser.objects.filter(email=request.data.get('email')).exists():
                    return render(request, 'user/signuppage.html', {'serializer': RegisterSerializer(), 'error': 'User with this email already exists.'})
                else:
                    serializer = RegisterSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return redirect('dashboard:login_user')
                    else:
                        return Response(request, 'user/signuppage.html',{'error': serializer.errors})
            except Exception as e:
                print("Error--------:",str(e))
                return Response({ 'error': 'Error registering user'})
    
    def get(self, request):
        serializer = RegisterSerializer()
        return Response({'serializer':serializer,'message':"login page"}, status = status.HTTP_200_OK)

class LoginView(APIView):
    api_view = ['POST']
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/loginpage.html'

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    # return Response({'payload':serializer.data,'message':"Login successfully"}, status = status.HTTP_200_OK)
                    return redirect('dashboard:dashboard')
                    
                else:
                    # return Response({'message': 'Invalid credentials.'}, status = status.HTTP_400_BAD_REQUEST)
                    return render(request, 'user/signuppage.html', {'serializer': serializer, 'error': 'Invalid credentials'})
            else:
                return Response({'message': ' Please fill vaild data'}, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Error--------:",str(e))
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        serializer = LoginSerializer()
        return Response({'serializer':serializer,'message':"login page"}, status = status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        logout(request)
        return redirect('dashboard:login_user')
        # return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)

class DashboardView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'dashboard/homepage.html'

    def get(self, request):
        try:
            user = request.user
            serializer = RegisterSerializer(user)
            properties_obj = Unit.objects.all()
            return Response({'serializer_data':serializer.data, 'content': properties_obj, 'message':"successfully"}, status = status.HTTP_200_OK)
        except Exception as e:
            print("Error--------:",str(e))
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)

class TenantView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'dashboard/tenantprofile.html'
    

    def get(self, request,pk):
        try:
            user_obj = AiUser.objects.get(id = pk)
            tenant_obj = Tenant.objects.get(user = user_obj)
            if tenant_obj:
                Lease_obj = Lease.objects.get(tenant = tenant_obj)
                return Response({'serializer_data':Lease_obj, 'message':"successfully"}, status = status.HTTP_200_OK)
            else:
                return Response({ 'error':"User not found"}, status = status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Error--------:",str(e))
            return Response({ 'error':"User not found"}, status = status.HTTP_404_NOT_FOUND)
    

class SearchView(APIView):
    serializer_class = UnitSerializer
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'dashboard/tenantprofile.html'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return Unit.objects.filter(Q(unit_type__icontains=query) | Q(rent_cost__icontains=query) )

    def get(self, request, pk):
        user_obj = AiUser.objects.get(id = pk)
        tenant_obj = Tenant.objects.get(user = user_obj)
        query = request.GET.get('query', '')
        queryset = Unit.objects.filter(unit_type__icontains=query)
        if tenant_obj:
            Lease_obj = Lease.objects.get(tenant = tenant_obj)
        query = request.GET.get('query', '')
        queryset = Unit.objects.filter(unit_type__icontains=query)
        return Response({'serializer_data':Lease_obj,'data': queryset, 'query': query})