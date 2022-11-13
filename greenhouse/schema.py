from datetime import datetime
import graphene
from greenhouse.models import ESPTransmission


class ESPTransmissionType(graphene.ObjectType):
    timestamp_origin = graphene.Int()
    timestamp_receive = graphene.Int()
    mac_address = graphene.String()
    ldr_sensor = graphene.Float()
    temperature_sensor = graphene.Float()
    pressure = graphene.Float()
    moisture = graphene.Float()
    datetime_origin = graphene.DateTime()
    datetime_receive = graphene.DateTime()

    def resolve_datetime_origin(self, info, **kwargs):
        return datetime.fromtimestamp(self.timestamp_origin)

    def resolve_datetime_receive(self, info, **kwargs):
        return datetime.fromtimestamp(self.timestamp_receive)


class Query(graphene.ObjectType):
    version = graphene.String()

    def resolve_version(self, info, **kwargs):
        return '0.0.1'

    esp_transmissions = graphene.List(
        ESPTransmissionType,
        ldr_sensor__gte=graphene.Float(),
        ldr_sensor__lte=graphene.Float(),
        temperature_sensor__gte=graphene.Float(),
        temperature_sensor__lte=graphene.Float(),
        pressure__gte=graphene.Float(),
        moisture__lte=graphene.Float(),
        mac_address__in=graphene.List(graphene.String),
        mac_address__icontains=graphene.String()
    )

    def resolve_esp_transmissions(self, info, **kwargs):
        return ESPTransmission.objects.filter(**kwargs)
