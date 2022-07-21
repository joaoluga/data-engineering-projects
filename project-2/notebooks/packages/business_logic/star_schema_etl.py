from packages.business_logic.star_schema.bancos_tarifas import BancosTarifas
from packages.etl.etl_base import ETLBase
from packages.etl.etl_workflow_manager import ETLWorkflowManager
from packages.utils.database_manager import DatabaseManager


class StarSchemaETL(ETLBase):
    def __init__(self):
        self.__db_manager = DatabaseManager()
        self.__etl_workflow_manager = ETLWorkflowManager
        self.__fact_workflow = BancosTarifas()
        super().__init__()

    def create_schemas(self):
        self._logger.info("Creating trusted schema")
        self.__db_manager.create_schema("trusted")
        self._logger.info("Creating refined schema")
        self.__db_manager.create_schema("refined")

    def execute(self):
        self.create_schemas()
        self._logger.info("Extracting bancos data")
        for entity_name in ["bancos", "lista_tarifas"]:
            self.__etl_workflow_manager(entity_name=entity_name).execute()
        self.__fact_workflow.execute()
