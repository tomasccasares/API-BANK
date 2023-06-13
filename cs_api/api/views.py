from django.shortcuts import render
from django.contrib.auth.models import Group
from django.db import transaction, IntegrityError
from django.core.paginator import Paginator, EmptyPage

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from api import forms, models, serializers, constants, pagination, extractor
from api.permissions import IsAdmin, IsUser


@api_view(["POST", "GET"])
@permission_classes([AllowAny])
def accounts_view(request):
    if request.method == "GET":
        return get_accounts(request)
    else:
        return create_account(request)


def create_account(request):
    form = forms.CreateUserForm(request.POST)

    if form.is_valid():
        user = form.save()
        user.groups.add(Group.objects.get(name=constants.GROUP_USER))
        
        models.Account.objects.create(user=user)

        return Response(serializers.UserSerializer(user, many=False).data, status=status.HTTP_201_CREATED)
    
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


def get_accounts(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    query = request.GET.get("q", None)

    page, page_size, err = extractor.extract_paging_from_request(request=request)

    if err != None:
        return err
    
    if query != None:
        queryset = models.User.objects.filter(username__icontains=query).order_by("-id")
    else:
        queryset = models.User.objects.all().order_by("-id")

    try:
        query_paginator = Paginator(queryset, page_size)

        query_data = query_paginator.page(page)

        serializer = serializers.UserSerializer(query_data, many=True)

        res = Response(serializer.data)

        res = pagination.add_paging_to_response(request, res, query_data, page, query_paginator.num_pages)

        return res
    except EmptyPage:
        return Response(status=status.HTTP_404_NOT_FOUND)
        

@api_view(["DELETE"])
@permission_classes([IsAdmin])
def user_delete(request, id):
    if request.user.id == id:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        user = models.User.objects.get(pk=id)
        
        user.is_active = False
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    except models.User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([IsUser])
def create_transaction(request):
    form = forms.CreateTransactionForm(request.POST)

    if form.is_valid():
        destination = models.User.objects.get(id=form.cleaned_data["destination"])
        quantity = form.cleaned_data["quantity"]

        try:
            with transaction.atomic():
                if quantity > request.user.account.balance:
                    return Response({"Error": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)
                
                new_transaction = models.Transaction(origin=request.user, destination=destination, quantity=quantity)

                request.user.account.balance -= quantity
                destination.account.balance += quantity

                new_transaction.save()
                request.user.account.save()
                destination.account.save()

                return Response(serializers.TransactionSerializer(new_transaction, many=False).data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"Error": "Error transferring funds"}, status=status.HTTP_400_BAD_REQUEST)    
        
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
