from .kucoin import KUCOIN_API_PARAMS_MAPPING

def find_api_params_mapping(name: str):
    if name == 'kucoin':
        return KUCOIN_API_PARAMS_MAPPING
    else:
        raise ValueError(
            f"There is no predefined API params mapping for name = '{name}'"
            )

