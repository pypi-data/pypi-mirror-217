from . import configuration_faster_rcnn
from . import modeling_faster_rcnn
from . import image_processing_faster_rcnn

def register():
    configuration_faster_rcnn.register()
    modeling_faster_rcnn.register()
    image_processing_faster_rcnn.register()
