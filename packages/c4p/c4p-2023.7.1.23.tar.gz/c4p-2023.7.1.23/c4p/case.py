import os

from . import utils
from .runoff import Runoff


class PaleoCase:
    def __init__(self, casename=None, work_dirpath=None, esmfbin_path=None, lib_netcdf=None, inc_netcdf=None):
        self.casename = casename
        self.work_dirpath = work_dirpath
        self.esmfbin_path = '/glade/u/apps/derecho/23.06/spack/opt/spack/esmf/8.4.2/cray-mpich/8.1.25/oneapi/2023.0.0/fslf/bin' if esmfbin_path is None else esmfbin_path
        self.lib_netcdf = '/glade/u/apps/derecho/23.06/spack/opt/spack/netcdf/4.9.2/oneapi/2023.0.0/iijr/lib' if lib_netcdf is None else lib_netcdf
        self.inc_netcdf = '/glade/u/apps/derecho/23.06/spack/opt/spack/netcdf/4.9.2/oneapi/2023.0.0/iijr/include' if inc_netcdf is None else inc_netcdf
        if not os.path.exists(work_dirpath):
            os.makedirs(work_dirpath, exist_ok=True)
            utils.p_success(f'>>> {work_dirpath} created')
        os.chdir(work_dirpath)
        utils.p_success(f'>>> Current directory switched to: {work_dirpath}')

    def setup_runoff(self):
        return Runoff(**self.__dict__)
        