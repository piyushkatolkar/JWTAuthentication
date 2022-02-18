from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView #APIView is parent class and student_api is a child class.

from .models import Student
from .serializers import StudentSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# pep8

# Create your views here.
class Student_Api(APIView):
    query = Student.objects.all()
    serializer = StudentSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

    # GET - show all records from the database with the help of postman
    def get(self, request, format=None):
        query = Student.objects.all()
        # query = Student.objects.filter(name ="johny").all()
        # print(query, type(query))
        serializer = StudentSerializer(query, many=True)
        # print("-"*100)
        # print(serializer.data, type(serializer.data))
        return Response(serializer.data)

    # POST - 1 by 1 records in the database with the help of postman normal vaildation
    # def post(self, request, format=None):
    #     serializer = StudentSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)

        # if request.data['roll'] > 50:
        #     return Response({'status' : 403, 'message' : 'roll no less than or equal to 50'})

        if not serializer.is_valid():
            print(serializer.errors)
        return Response({'status' : 403, 'errors' : serializer.errors , 'message' : 'something went wrong'})
        serializer.save()
            
        return Response({'status' : 200, 'payload' : serializer.data , 'message' : 'your data has been created'})

class Student_Detail(APIView):
    query = Student.objects.all()
    serializer = StudentSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]
    
    def get_object(self, id):
        try:
            return Student.objects.get(id=id)
        except Student.DoesNotExist as e:
            return Response({"error": "object not found"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serializer = StudentSerializer(instance)
        return Response(serializer.data)

    # PUT - update 1 by 1 records in the database with the help of postman - all fields are required
    def put(self, request, id=None):
        query = self.get_object(id)
        serializer = StudentSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH - partially update data in the database with the help of postman - minimum 1 field are required which we can update
    def patch(self, request, id=None):
        query = self.get_object(id)
        serializer = StudentSerializer(query, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE - record in the database with the help of postman
    def delete(self, request, id=None):
        query = self.get_object(id)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
