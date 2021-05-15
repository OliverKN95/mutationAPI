import requests
from django.shortcuts import render
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from datetime import datetime
from .models import logs
from .serializers import logsSerializer, hasMutationSerializer
from .filters import logsFilter
from django.db.models import Q
import numpy as np
import urllib.request
import json
import re



# Create your views here.

class hasMutationViewset(GenericAPIView):
    """
    API para traer info de la mutacion de una cadena de ADN.
    """
    queryset = logs.objects.all()
    serializer_class = hasMutationSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request):

        dna = request.data.get('dna', '')
        dna_matrix = []

        if dna != '':
            try:
                match = False

                for a in dna:
                    # Validacion de integridad de datos
                    match = bool(re.compile(r'[^ATCG]').search(a.upper()))
                    if match:
                        log = logs.objects.create(
                                has_mutation=False,
                                success=False,
                                dna_provided=dna
                            )
                        log.save()
                        return Response(_('Hubo un error al procesar los datos. La cadena proporcionada no tiene el formato correcto, solo se aceptan los caracteres "A,T,C o G".'), status=status.HTTP_403_FORBIDDEN)
                
                # Validacion de horizontales
                    if 'AAAA' in a.upper() or 'TTTT' in a.upper() or 'CCCC' in a.upper() or 'GGGG' in a.upper():
                        log = logs.objects.create(
                                has_mutation=True,
                                success=True,
                                dna_provided=dna
                            )
                        log.save()
                        return Response(data = {"has_mutation": True}, status=status.HTTP_200_OK)
                    dna_matrix.append(list(a.upper()))

                # Validacion de verticales
                for idx, d in enumerate(dna_matrix):
                    vertical_val = ''.join([row[idx] for row in dna_matrix])
                    if 'AAAA' in vertical_val or 'TTTT' in vertical_val or 'CCCC' in vertical_val or 'GGGG' in vertical_val:
                        log = logs.objects.create(
                                has_mutation=True,
                                success=True,
                                dna_provided=dna
                            )
                        log.save()
                        return Response(data = {"has_mutation": True}, status=status.HTTP_200_OK)

                # Validacion de diagonales
                diags = [np.array(dna_matrix)[::-1,:].diagonal(i) for i in range(-2,4)]
                diags.extend(np.array(dna_matrix).diagonal(i) for i in range(2,-4,-1))
                for n in diags:
                    print(n.tolist())
                    if 'AAAA' in ''.join(n) or 'TTTT' in ''.join(n) or 'CCCC' in ''.join(n) or 'GGGG' in ''.join(n):
                        log = logs.objects.create(
                                has_mutation=True,
                                success=True,
                                dna_provided=dna
                            )
                        log.save()
                        return Response(data = {"has_mutation": True}, status=status.HTTP_200_OK)

                log = logs.objects.create(
                        has_mutation=False,
                        success=True,
                        dna_provided=dna
                    )
                log.save()
                data = {
                    "has_mutation": False,
                }
                return Response(data, status=status.HTTP_200_OK)
            except Exception as e:
                log = logs.objects.create(
                        has_mutation=False,
                        success=False,
                        dna_provided=dna
                    )
                log.save()
                return Response(_('Hubo un error al procesar los datos.'), status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(data={'detail': _("Se esperaba parámetro 'dna'.")}, status=status.HTTP_400_BAD_REQUEST)


class getStadisticsViewset(GenericAPIView):
    """
    API para traer info publica del Cliente.
    """
    queryset = logs.objects.all()
    serializer_class = logsSerializer
    authentication_classes = []
    permission_classes = []

    def get(self, request):

        try:
            ratio = (self.queryset.filter(has_mutation=True, success=True).count()/self.queryset.filter(success=True).count())
            data = {
                "total": self.queryset.filter(success=True).count(),
                "count_mutations": self.queryset.filter(has_mutation=True, success=True).count(),
                "count_no_mutations": self.queryset.filter(has_mutation=False, success=True).count(),
                "ratio": ratio
            }

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:

            return Response(_('Hubo un error al obtener datos de estadisticas.'), status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

