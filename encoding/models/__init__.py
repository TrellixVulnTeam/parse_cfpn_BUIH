from .model_zoo import get_model
from .model_store import get_model_file
from .base import *
from .fcn import *
from .psp import *
from .encnet import *
from .deeplabv3 import *
from .abrnet import *

from .cfpn import *
from .cfpn2 import *
from .cfpn_gsf import *
from .dfpn8_gsf import *
from .dfpn82_gsf import *
from .dfpn83_gsf import *
from .dfpn84_gsf import *
from .dfpn85_gsf import *
from .dfpn86_gsf import *
from .dfpn87_gsf import *
from .dfpn_gsf import *
from .pam import *
from .fpn import *
from .fpn_pam import *
from .fpn_aspp import *
from .fpn_psp import *
from .object_gsnet import *
from .object_center_gsnet import *
from .object_center_cut_gsnet import *

from .vggnet import *
from .vgg_spool import *
from .vgg_sa import *
from .vgg_sa_spool import *
from .vgg_full import *
from .vgg_full_dilated import *
from .vgg1x1 import *
from .vgg1x1_pool import *

from .vgg1x1_spool import *
from .vgg1x1_spool2 import *
from .vgg1x1_spoolbnrelu import *
from .vgg1x1_spool2bnrelu import *
from .vgg1x1_spool_iter import *
from .vgg1x1_spool_full import *
from .fatnet import *
from .fatnet1 import *
def get_segmentation_model(name, **kwargs):
    from .fcn import get_fcn
    models = {
        'fcn': get_fcn,
        'psp': get_psp,
        'encnet': get_encnet,
        'deeplab': get_deeplab,
        'abrnet': get_abrnet,

        'cfpn': get_cfpn,
        'cfpn2': get_cfpn2,
        'cfpn_gsf': get_cfpn_gsf,
        'dfpn_gsf': get_dfpn_gsf,
        'dfpn8_gsf': get_dfpn8_gsf,
        'dfpn82_gsf': get_dfpn82_gsf,
        'dfpn83_gsf': get_dfpn83_gsf,
        'dfpn84_gsf': get_dfpn84_gsf,
        'dfpn85_gsf': get_dfpn85_gsf,
        'dfpn86_gsf': get_dfpn86_gsf,
        'dfpn87_gsf': get_dfpn87_gsf,
        
        'pam': get_pam,
        'fpn': get_fpn,
        'fpn_pam': get_fpn_pam,
        'fpn_aspp': get_fpn_aspp,
        'fpn_psp': get_fpn_psp,
        
        'object_gsnet': get_object_gsnet,
        'object_center_gsnet': get_object_center_gsnet,
        'object_center_cut_gsnet': get_object_center_cut_gsnet,
        
        
        'vggnet': get_vggnet,
        'vgg_spool': get_vgg_spool,
        'vgg_sa': get_vgg_sa,
        'vgg_sa_spool': get_vgg_sa_spool,
        'vgg_full': get_vgg_full,
        'vgg_full_dilated': get_vgg_full_dilated,
        'vgg1x1': get_vgg1x1,
        'vgg1x1_pool': get_vgg1x1_pool,
        'vgg1x1_spool': get_vgg1x1_spool,
        'vgg1x1_spool2': get_vgg1x1_spool2,
        'vgg1x1_spoolbnrelu': get_vgg1x1_spoolbnrelu,
        'vgg1x1_spool2bnrelu': get_vgg1x1_spool2bnrelu,
        'vgg1x1_spool_iter': get_vgg1x1_spool_iter,
        'vgg1x1_spool_full': get_vgg1x1_spool_full,
        'fatnet': get_fatnet,
        'fatnet1': get_fatnet1,

    }
    return models[name.lower()](**kwargs)
