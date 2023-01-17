import pytz

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from django.conf import settings
from datetime import datetime, timedelta

from .models import ValidationToken


def get_query_params(request, parameter):
    ret_val = request.query_params.get(parameter, None)
    if ret_val is None:
        ret_val = request.data.get(parameter, None)
    return ret_val


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def validate_token(request):
    token_id = get_query_params(request, 'token_id')
    token = ValidationToken.objects.get(token=token_id)
    time_window = token.created + timedelta(seconds=settings.EXPIRATION_TIME)
    current_time = datetime.now(pytz.utc)
    if time_window > current_time:
        return Response({'validated': True}, status=status.HTTP_200_OK)
    else:
        return Response({'validated': False}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def clean_tokens(request):
    time_limit = datetime.now(pytz.utc) - timedelta(seconds=settings.TOKEN_CLEAN_TIME)
    ValidationToken.objects.filter(ceated__lt=time_limit).delete()
    return Response({'State': 'Complete'}, status=status.HTTP_200_OK)