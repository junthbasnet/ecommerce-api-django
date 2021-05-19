from django.http import HttpResponse
from django.db import IntegrityError
from django.template.loader import render_to_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView


from common.permissions import IsAdminUserOrReadOnly
from common.tasks import send_email
from .models import (
    SiteSetting,
    SEOSetting,
    SocialLinkSetting,
    Slideshow,
    FAQ,
    FAQCategory,
    PaymentMethod,
    Testimonial,
    Province,
    City,
    Area,
)
from .serializers import (
    SiteSettingSerializer,
    SEOSettingSerializer,
    SocialLinkSettingSerializer,
    SlideshowSerializer,
    FAQSerializer,
    FAQCategorySerializer,
    PaymentMethodSerializer,
    TestimonialSerializer,
    ProvinceSerializer,
    CitySerializer,
    AreaSerializer,
)


def home_view(request):
    return HttpResponse("You are not authorized to view this page.")


class SiteSettingsAPI(APIView):
    serializer_class = SiteSettingSerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    def get(self, request):
        site_settings = SiteSetting.objects.all()
        if site_settings.exists():
            return Response(SiteSettingSerializer(site_settings[0]).data, status.HTTP_200_OK)
        return Response(
            {
                'message': "No Settings"
            },
            status.HTTP_400_BAD_REQUEST
        )

    def post(self, request):
        site_settings = SiteSetting.objects.all()
        if site_settings.exists():
            serializer = SiteSettingSerializer(data=request.data, instance=site_settings[0])
            if serializer.is_valid():
                p = serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            return Response(
                {
                    'message': "Invalid Data"
                }, status.HTTP_201_CREATED
            )

        else:
            serializer = SiteSettingSerializer(data=request.data)
            if serializer.is_valid():
                p = serializer.save()
                return Response(SiteSettingSerializer(p).data, status.HTTP_200_OK)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class SEOSettingsAPI(APIView):
    serializer_class = SEOSettingSerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    def get(self, request):
        seo_settings = SEOSetting.objects.all()
        if seo_settings.exists():
            return Response(SEOSettingSerializer(seo_settings[0]).data, status.HTTP_200_OK)
        return Response(
            {
                'message': "No Settings"
            }, status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        seo_settings = SEOSetting.objects.all()
        if seo_settings.exists():
            serializer = SEOSettingSerializer(data=request.data, instance=seo_settings[0])
            if serializer.is_valid():
                p = serializer.save()
                subject = f'SEO Settings Changed'
                message = f'SEO Settings in Nebuyo has changed'
                html_content = render_to_string('seo_setting_change.html', {'settings': p})
                to_mail = ['avimshra@gmail.com', 'ajaykarki333@gmail.com']
                send_email.delay(subject, message, html_content, to_mail, from_mail="system@mail.akku.gg")
                return Response(serializer.data, status.HTTP_200_OK)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            serializer = SEOSettingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            return Response(seo_set.errors, status.errors)


class SocialLinkViewSet(viewsets.ModelViewSet):
    """ Manage SocialLInks  
    ## Fields:
        id,icon,link,platform
    """

    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = SocialLinkSetting.objects.all()
    serializer_class = SocialLinkSettingSerializer


class SlideShowViewSet(viewsets.ModelViewSet):
    queryset = Slideshow.objects.all()
    serializer_class = SlideshowSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['is_active', ]
    search_fields = ['caption', ]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Success',
                    'data': serializer.data
                }, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, instance=self.get_object())
        if serializer.is_valid():
            return Response(
                {
                    'message': 'Success',
                    'data': serializer.data
                }, status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        caption = instance.caption
        self.perform_destroy(instance)
        return Response(
            {
                'message': f'{caption} Deleted Successfully'
            },
            status.HTTP_204_NO_CONTENT
        )


class PaymentMethodViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.all()

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'message': 'Successfully Added Payment Method',
                'data': serializer.data
            }, status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Update a model instance.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'request':request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                'message': 'Successfully Edited.',
                'data': serializer.data
            },
            status.HTTP_202_ACCEPTED
        )

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        name = instance.name
        self.perform_destroy(instance)
        return Response(
            {
                'message': f'{name} Deleted Successfully'
            }, status.HTTP_204_NO_CONTENT
        )


class FAQCategoryViewSet(viewsets.ModelViewSet):
    '''
    FAQ Category
    '''
    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = FAQCategory.objects.all()
    serializer_class = FAQCategorySerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                {
                    'message': 'Successfully Added Category',
                    'data': serializer.data
                }, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        faq = self.get_object()
        serializer = self.serializer_class(faq, data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                {
                    'message': 'Successfully Edited Category',
                    'data': serializer.data
                }, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        name = instance.title
        self.perform_destroy(instance)
        return Response(
            {
                'message': f'{name} Deleted Successfully'
            }, status.HTTP_204_NO_CONTENT)


class FAQViewSet(viewsets.ModelViewSet):
    '''
    Answering the frequently asked questions by users.
    Filtering option is_active
    '''
    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active', 'category']

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                {
                    'message': 'Successfully Added FAQ',
                    'data': serializer.data
                }, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        faq = self.get_object()
        serializer = self.serializer_class(faq, data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                {
                    'message': 'Successfully Edited FAQ',
                    'data': serializer.data
                }, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        name = instance.question
        self.perform_destroy(instance)
        return Response(
            {
                'message': f'{name} Deleted Successfully'
            }, status.HTTP_204_NO_CONTENT)


class TestimonialViewSet(viewsets.ModelViewSet):
    '''
    Testimonial API
    '''
    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                {
                    'message': 'Successfully Added Testimonial',
                    'data': serializer.data
                }, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                {
                    'message': 'Successfully Edited Testimonial',
                    'data': serializer.data
                }, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        name = instance.question
        self.perform_destroy(instance)
        return Response(
            {
                'message': 'Deleted Successfully'
            }, status.HTTP_204_NO_CONTENT)


class ProvinceAPIViewSet(viewsets.ModelViewSet):
    '''
    APIViewSet that manages province (region).
    '''
    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name', ]
    search_fields = ['name', ]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                {
                    'message': 'Successfully Added Province',
                    'data': serializer.data
                }, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        faq = self.get_object()
        serializer = self.serializer_class(faq, data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                {
                    'message': 'Successfully Edited Province',
                    'data': serializer.data
                }, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        name = instance.name
        self.perform_destroy(instance)
        return Response(
            {
                'message': f'{name} Deleted Successfully'
            }, status.HTTP_204_NO_CONTENT)


class CityAPIViewSet(viewsets.ModelViewSet):
    '''
    APIViewSet that manages city.
    '''
    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['name', ]
    filterset_fields = ('province',)
    search_fields = ['name', ]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                {
                    'message': 'Successfully Added City',
                    'data': serializer.data
                }, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        faq = self.get_object()
        serializer = self.serializer_class(faq, data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                {
                    'message': 'Successfully Edited City',
                    'data': serializer.data
                }, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        name = instance.name
        self.perform_destroy(instance)
        return Response(
            {
                'message': f'{name} Deleted Successfully'
            }, status.HTTP_204_NO_CONTENT)


class AreaAPIViewSet(viewsets.ModelViewSet):
    '''
    APIViewSet that manages area.
    '''
    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['name', ]
    filterset_fields = ('city__province', 'city')
    search_fields = ['name', ]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                {
                    'message': 'Successfully Added Area',
                    'data': serializer.data
                }, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        faq = self.get_object()
        serializer = self.serializer_class(faq, data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                {
                    'message': 'Successfully Edited Area',
                    'data': serializer.data
                }, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        name = instance.name
        self.perform_destroy(instance)
        return Response(
            {
                'message': f'{name} Deleted Successfully'
            }, status.HTTP_204_NO_CONTENT)