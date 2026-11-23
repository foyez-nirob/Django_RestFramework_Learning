from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from student.models import student

from .serializers import studentserializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from Employee.models import Employee
from rest_framework.views import APIView
from .serializers import EmployeeSerializer
from django.http import Http404

from rest_framework import mixins, generics

from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from blogs.models import Blog, Comment
from blogs.serializers import BlogSerializer, CommentSerializer

from .paginations import CustomPagination
from Employee.filters import EmployeeFilter
from rest_framework.filters import SearchFilter, OrderingFilter



# def student_views(request):
#     ## manual way of serializing the data ==>
#     students = student.objects.all()
#     students_list = list(students.values())
#     print(students)
#     return JsonResponse(students_list, safe=False)

# for all student data 
@api_view(['GET','POST'])
def student_views(request):
    if request.method == 'GET':
        students = student.objects.all()
        serializer = studentserializer(students, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = studentserializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#for one student data =>

@api_view(['GET','PUT','DELETE'])
def student_one_view(request, pk):
    try:
        student_one = student.objects.get(pk = pk)
    except student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = studentserializer(student_one)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = studentserializer(student_one, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student_one.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ---- Class Based Views -----

# class Employees(APIView):

#     def get(self, request):
#         employees = Employee.objects.all()
#         serializer = EmployeeSerializer(employees, many = True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     def post(self, request):
#         serializer = studentserializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class Employee_one(APIView):
#     def get_object(self, pk):
#         try :
#             return Employee.objects.get(pk = pk)
#         except Employee.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         data = self.get_object(pk)
#         serializer = EmployeeSerializer(data)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, pk):
#         employee = self.get_object(pk)
#         serializer = EmployeeSerializer(employee, data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else :
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         employee = self.get_object(pk)
#         employee.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

"""
# --- CRUD OPERATION USING MIXINS ----

class Employees(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)

class Employee_one(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)
    
    def put(self, request, pk):
        return self.update(request, pk)
    
    def delete(self, request, pk):
        return self.destroy(request, pk)

"""

"""
# ---- CRUD USING GENERICS ---
class Employees(generics.ListCreateAPIView):                    #generics.ListAPIView + generics.CreateAPIView = listcreate
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class Employee_one(generics.RetrieveAPIView, generics.RetrieveUpdateDestroyAPIView):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk'

"""


#--- CRUD USING VIEWSETS -> (viewset) ----
"""
class EmployeeViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Employee.objects.all()
        serializer = EmployeeSerializer(queryset, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = EmployeeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(Employee, pk = pk)   # get data or sent error msg
        serializer = EmployeeSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        queryset = get_object_or_404(Employee, pk = pk)
        serializer = EmployeeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk = None):
        employee = get_object_or_404(Employee, pk = pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""

#--- CRUD USING VIEWSETS -> (Modelset) ----

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination
    # filterset_class = EmployeeFilter             # for custom filter
    filter_backends = [SearchFilter, OrderingFilter]              # for search filter
    search_fields = ['name']              # for search filter
    ordering_fields = ['name', 'dept']              # for ordering filter
    ordering_fields = ['id']              # default ordering


# --- crud for blog app ----

class BlogViews(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class CommentViews(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class BlogOneViews(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'

class CommentOneViews(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'

