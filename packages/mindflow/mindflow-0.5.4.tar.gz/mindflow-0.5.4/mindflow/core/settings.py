from mindflow.core.types.mindflow_model import ConfiguredMindFlowModels
from mindflow.core.types.service import ConfiguredServices


class Settings:
    services: ConfiguredServices
    mindflow_models: ConfiguredMindFlowModels

    def __init__(self):
        self.services = ConfiguredServices()
        self.mindflow_models = ConfiguredMindFlowModels(self.services)
