from django.conf                                  import settings
from rest_framework                               import generics, status
from rest_framework.permissions                   import IsAuthenticated
from rest_framework.response                      import Response
from rest_framework_simplejwt.backends            import TokenBackend


from authApp.models.pruebas                import Pruebas
from authApp.models.dep_ips                import Dep_ips
from authApp.serializers.pruebasSerializer import PruebasSerializer



class PruebasCreateView(generics.CreateAPIView):
    serializer_class   = PruebasSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        token        = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != request.data['user_id']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        request.data['prueba_data']['dep_ips'] = request.data['user_id']

        totalTests = request.data['prueba_data']['positiveTests'] + request.data['prueba_data']['negativeTests'] + request.data['prueba_data']['indeterminateTests']
        request.data['prueba_data']['totalTests'] = totalTests

        serializer = PruebasSerializer(data=request.data['prueba_data'])
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response("Prueba registrada", status=status.HTTP_201_CREATED)

class PruebasDep_ipsView(generics.ListAPIView):
    serializer_class   = PruebasSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        token        = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        
        queryset = Pruebas.objects.filter(dep_ips_id=self.kwargs['user'])
        return queryset

class PruebasDepartamentoView(generics.ListAPIView):
    serializer_class = PruebasSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        token        = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        queryset = Pruebas.objects.select_related().filter(dep_ips__departamento__id = 1)
        print('*'*100)
        print(str(queryset.query))
        print('*'*100)

        return queryset
