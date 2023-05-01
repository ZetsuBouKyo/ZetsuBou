from back.settings import Setting


class CmdSetting:
    def export_docker_envs(self):
        setting = Setting()
        env_prefix = setting.Config.env_prefix
        setting = setting.dict()
        keys = list(setting.keys())
        keys.sort()
        for key in keys:
            env_key = env_prefix + key
            env_key = env_key.upper()
            env_value = setting[key]
            if env_value is None:
                env_value = "null"
            env = f"{env_key}: ${{{env_key}:-{env_value}}}"
            print(env)
