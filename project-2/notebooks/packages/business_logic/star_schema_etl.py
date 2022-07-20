from packages.business_logic.bancos.bancos_extractor import BancosExtractor
from packages.business_logic.bancos.bancos_transformer import BancosTransformer
from packages.business_logic.bancos.bancos_loader import BancosLoader
from packages.business_logic.lista_tarifas.lista_tarifas_extractor import ListaTarifasExtractor
from packages.business_logic.lista_tarifas.lista_tarifas_transformer import ListaTarifasTransformer
from packages.business_logic.lista_tarifas.lista_tarifas_loader import ListaTarifasLoader
from packages.business_logic.star_schema.bancos_tarifas import BancosTarifas
from packages.utils.database_manager import DatabaseManager
from packages.utils.logger import Logger


class StarSchemaETL:

    def __init__(self):
        self.__logger = Logger()
        self.__db_manager = DatabaseManager()

    def create_schemas(self):
        self.__logger.info("Creating trusted schema")
        self.__db_manager.create_schema("trusted")
        self.__logger.info("Creating refined schema")
        self.__db_manager.create_schema("refined")

    def execute(self):
        self.create_schemas()
        self.__logger.info("Extracting bancos data")
        BancosExtractor().execute()
        self.__logger.info("Transforming bancos data")
        BancosTransformer().execute()
        self.__logger.info("Loading bancos data to database")
        BancosLoader().execute()
        self.__logger.info("Extracting Lista Tarifas data")
        ListaTarifasExtractor().execute()
        self.__logger.info("Transforming Lista Tarifas data")
        ListaTarifasTransformer().execute()
        self.__logger.info("Loading Lista Tarifas data to database")
        ListaTarifasLoader().execute()
        self.__logger.info("Creating Star Schema")
        BancosTarifas().execute()


