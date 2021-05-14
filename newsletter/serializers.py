from rest_framework import serializers

from newsletter.models import Newsletter, Subscriber


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'
        read_only_fields = ('slug',)


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ('email', 'code')
