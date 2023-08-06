from typing import Union, Dict, List
from .base import BaseService
from ..model.callback import Callback
from ..model.param import TextParam, BatchParam


def _params_convert(task_params: Union[str, Dict, TextParam]):
    # 单个
    if isinstance(task_params, TextParam):
        return task_params.dict()
    elif isinstance(task_params, str):
        return {'text': task_params}

    return task_params


def _params_batch_convert(task_params: Union[str, List[str], BatchParam]):
    if isinstance(task_params, str):
        return [task_params]
    if isinstance(task_params, list):
        return task_params
    if isinstance(task_params, BatchParam):
        return task_params.texts

    return task_params


class InfoExtractService(BaseService):
    """品牌、型号、通用名"""

    def extract_sku(self, task_params: Union[str, Dict, TextParam] = None, callback: Callback = None, **kwargs):
        return self.get_client().apply(task_name='info_extract.sku', task_params=_params_convert(task_params), callback=callback, **kwargs)

    def extract_sku_batch(self, task_params: List[str], callback: Callback = None, **kwargs):
        return self.get_client().apply(task_name="info_extract.sku_batch", task_params=task_params, callback=callback, **kwargs)

