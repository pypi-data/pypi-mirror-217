import os
from datetime import date

from . import utils
from .rof import ROF
from .mapping import Mapping

cwd = os.path.dirname(__file__)

class PaleoCase:
    def __init__(self, casename=None, work_dirpath=None, esmfbin_path=None, netcdf_lib_path=None, netcdf_inc_path=None, account=None):
        self.casename = casename
        self.account = account
        self.work_dirpath = work_dirpath
        self.esmfbin_path = '/glade/u/apps/derecho/23.06/spack/opt/spack/esmf/8.4.2/cray-mpich/8.1.25/oneapi/2023.0.0/fslf/bin' if esmfbin_path is None else esmfbin_path
        self.netcdf_lib_path = '/glade/u/apps/derecho/23.06/spack/opt/spack/netcdf/4.9.2/oneapi/2023.0.0/iijr/lib' if netcdf_lib_path is None else netcdf_lib_path
        self.netcdf_inc_path = '/glade/u/apps/derecho/23.06/spack/opt/spack/netcdf/4.9.2/oneapi/2023.0.0/iijr/include' if netcdf_inc_path is None else netcdf_inc_path
        if not os.path.exists(work_dirpath):
            os.makedirs(work_dirpath, exist_ok=True)
            utils.p_success(f'>>> {work_dirpath} created')
        os.chdir(work_dirpath)
        utils.p_success(f'>>> Current directory switched to: {work_dirpath}')

    def mapping(self):
        return Mapping(**self.__dict__)

    def setup_runoff(self):
        return ROF(**self.__dict__)
        