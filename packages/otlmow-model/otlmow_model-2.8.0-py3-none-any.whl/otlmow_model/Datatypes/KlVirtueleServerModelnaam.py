# coding=utf-8
import random
from otlmow_model.BaseClasses.KeuzelijstField import KeuzelijstField
from otlmow_model.BaseClasses.KeuzelijstWaarde import KeuzelijstWaarde


# Generated with OTLEnumerationCreator. To modify: extend, do not edit
class KlVirtueleServerModelnaam(KeuzelijstField):
    """De modelnaam van de virtuele server."""
    naam = 'KlVirtueleServerModelnaam'
    label = 'Virtuele server modelnaam'
    objectUri = 'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#KlVirtueleServerModelnaam'
    definition = 'De modelnaam van de virtuele server.'
    status = 'ingebruik'
    codelist = 'https://wegenenverkeer.data.vlaanderen.be/id/conceptscheme/KlVirtueleServerModelnaam'
    options = {
        'boxedacu': KeuzelijstWaarde(invulwaarde='boxedacu',
                                     label='BoxedACU',
                                     status='ingebruik',
                                     definitie='BoxedACU.',
                                     objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlVirtueleServerModelnaam/boxedacu'),
        'ram': KeuzelijstWaarde(invulwaarde='ram',
                                label='RAM',
                                status='ingebruik',
                                definitie='RAM',
                                objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlVirtueleServerModelnaam/ram')
    }

    @classmethod
    def create_dummy_data(cls):
        return cls.create_dummy_data_keuzelijst(cls.options)

