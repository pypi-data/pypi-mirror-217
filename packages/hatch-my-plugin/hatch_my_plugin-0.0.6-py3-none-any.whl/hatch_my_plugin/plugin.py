from hatch.env.collectors.plugin.interface import EnvironmentCollectorInterface
from hatch.env.utils import ensure_valid_environment

class SpecialEnvironmentCollector(EnvironmentCollectorInterface):
    PLUGIN_NAME = 'myplug'
    print('-------------------------------------------マイプラグ')
    print('更新')
    def get_initial_config(self):
        config = {}
        ensure_valid_environment(config)

        return {'myplug': config}
