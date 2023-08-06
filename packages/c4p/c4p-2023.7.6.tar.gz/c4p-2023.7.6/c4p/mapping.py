import os
from datetime import date

from . import utils

cwd = os.path.dirname(__file__)

class Mapping:
    '''Generate mapping and domain files'''
    def __init__(self, atm_scrip=None, ocn_scrip=None, rof_scrip=None, atm_grid_name=None, ocn_grid_name=None, rof_grid_name=None,
                 gen_cesm_maps_script=None, gen_esmf_map_script=None, gen_domain_exe=None, job_name=None, **kwargs):

        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.job_name = 'mapping' if job_name is None else job_name

        # a set of default scrip files and grid names for ne16_g16
        scripgrids_dir = '/glade/p/cesmdata/inputdata/share/scripgrids'
        self.atm_scrip = os.path.join(scripgrids_dir, 'ne16np4_scrip_171002.nc') if atm_scrip is None else atm_scrip
        self.ocn_scrip = os.path.join(scripgrids_dir, 'gx1v6_090205.nc') if ocn_scrip is None else ocn_scrip
        self.rof_scrip = os.path.join(scripgrids_dir, '1x1d.nc') if rof_scrip is None else rof_scrip
        self.atm_grid_name = 'ne16np4' if atm_grid_name is None else atm_grid_name
        self.ocn_grid_name = 'gx1v6' if ocn_grid_name is None else ocn_grid_name
        self.rof_grid_name = 'r1_nomask' if rof_grid_name is None else rof_grid_name

        # paths for mapping and domain generation scripts
        self.gen_cesm_maps_script = os.path.join(cwd, './src/cime_mapping/gen_cesm_maps.ncpu36.sh') if gen_cesm_maps_script is None else gen_cesm_maps_script
        self.gen_esmf_map_script = os.path.join(cwd, './src/cime_mapping/create_ESMF_map.sh') if gen_esmf_map_script is None else gen_esmf_map_script
        self.gen_domain_exe = os.path.join(cwd, './src/cime_mapping/gen_domain') if gen_domain_exe is None else gen_domain_exe

        for k, v in self.__dict__.items():
            utils.p_success(f'>>> Mapping.{k}: {v}')

    def ocn2atm(self):
        utils.p_header(f'>>> Creating ocean<->atmosphere mapping files')
        utils.qsub_script(
            self.gen_cesm_maps_script,
            args=f'-fatm {self.atm_scrip} -natm {self.atm_grid_name} -focn {self.ocn_scrip} -nocn {self.ocn_grid_name} --nogridcheck',
            name=self.job_name, account=self.account,
        )

    def rof2atm(self):
        utils.p_header(f'>>> Creating river->atmosphere(land) mapping files')
        utils.qsub_script(
            self.gen_esmf_map_script,
            args=f'-fsrc {self.rof_scrip} -nsrc {self.rof_grid_name} -fdst {self.atm_scrip} -ndst {self.atm_grid_name} -map aave',
            name=self.job_name, account=self.account,
        )
    
    def atm2rof(self):
        utils.p_header(f'>>> Creating atmosphere(land)->river mapping files')
        utils.qsub_script(
            self.gen_esmf_map_script,
            args=f'-fsrc {self.atm_scrip} -nsrc {self.atm_grid_name} -fdst {self.rof_scrip} -ndst {self.rof_grid_name} -map aave',
            name=self.job_name, account=self.account,
        )
        
    def rof2ocn(self):
        utils.p_header(f'>>> Creating river->ocean mapping files')
        utils.qsub_script(
            self.gen_esmf_map_script,
            args=f'-fsrc {self.rof_scrip} -nsrc {self.rof_grid_name} -fdst {self.ocn_scrip} -ndst {self.ocn_grid_name} -map aave',
            name=self.job_name, account=self.account,
        )

    def gen_domain(self):
        utils.p_header(f'>>> Creating ocean<->atmosphere domain files')
        date_today = date.today().strftime('%y%m%d')
        utils.qsub_script(
            self.gen_domain_exe,
            args=f'-m map_{self.ocn_grid_name}_TO_{self.atm_grid_name}_aave.{date_today}.nc -o {self.ocn_grid_name} -l {self.atm_grid_name}',
            name=self.job_name, account=self.account,
        )

    def clean(self):
        utils.run_shell(f'rm -rf {self.job_name}.* PET*')