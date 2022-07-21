from packages.business_logic.bancos.bancos_extractor import BancosExtractor
from packages.business_logic.bancos.bancos_transformer import BancosTransformer
from packages.business_logic.bancos.bancos_loader import BancosLoader
from packages.business_logic.lista_tarifas.lista_tarifas_extractor import (
    ListaTarifasExtractor,
)
from packages.business_logic.lista_tarifas.lista_tarifas_transformer import (
    ListaTarifasTransformer,
)
from packages.business_logic.lista_tarifas.lista_tarifas_loader import (
    ListaTarifasLoader,
)


class ETLFactory:
    def __init__(self, entity_name):
        self.entity_name = entity_name

    def entity_name_normalizer(self):
        return "".join(
            [part_entity.capitalize() for part_entity in self.entity_name.split("_")]
        )

    def get_etl_classes(self):
        entity_cap = self.entity_name_normalizer()
        extractor = f"{entity_cap}Extractor"
        transformer = f"{entity_cap}Transformer"
        loader = f"{entity_cap}Loader"
        return globals()[extractor], globals()[transformer], globals()[loader]
