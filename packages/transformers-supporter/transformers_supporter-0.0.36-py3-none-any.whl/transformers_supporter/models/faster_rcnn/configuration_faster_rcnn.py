from transformers import PretrainedConfig
from transformers import AutoConfig

class FasterRcnnConfig(PretrainedConfig):
    model_type = "faster-rcnn"

    def __init__(self, **kwargs):
        #https://github.com/huggingface/transformers/blob/98d88b23f54e5a23e741833f1e973fdf600cc2c5/src/transformers/configuration_utils.py#L323
        #Keys are always strings in JSON so convert ids to int here.       
        super().__init__(**kwargs)   

def register():
    AutoConfig.register("faster-rcnn", FasterRcnnConfig)
