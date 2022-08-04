from packages.business_logic.bancos.bancos_extractor import BancosExtractor
from packages.business_logic.bancos.bancos_transformer import BancosTransformer
from packages.business_logic.lista_tarifas.lista_tarifas_extractor import (
    ListaTarifasExtractor,
)
from packages.business_logic.lista_tarifas.lista_tarifas_transformer import (
    ListaTarifasTransformer,
)
from packages.business_logic.star_schema.star_schema_transformer import (
    StarSchemaTransformer,
)


class ETLFactory:

    etl_class = {
        'bancos': {
            'extract': BancosExtractor,
            'transform': BancosTransformer
        },
        'lista_tarifas': {
            'extract': ListaTarifasExtractor,
            'transform': ListaTarifasTransformer
        },
        'star_schema': {
            'transform': StarSchemaTransformer
        }
    }

    def __init__(self, entity_name, process):
        self.entity_name = entity_name
        self.process = process

    def get_etl_class(self):
        return self.etl_class[self.entity_name][self.process]
