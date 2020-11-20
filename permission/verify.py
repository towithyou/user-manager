import os

import casbin
from django.conf import settings

from .adapter import DjangoAdapter
from .models import CasBinPermissionRule, RoleBind


def verify_permission(*args):
    # username, path, method
    adapter = DjangoAdapter(CasBinPermissionRule, RoleBind)
    model_conf_file = os.path.join(settings.BASE_DIR, "conf", "rbac_model.conf")
    e = casbin.Enforcer(model_conf_file, adapter=adapter)
    return e.enforce(*args)