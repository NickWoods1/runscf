"""
Defines the algorithm class, the attributes of which are
the parameters used. I.e., which method is used in the calculation,
and what should its parameters be.
"""

class algorithm(object):
    def __init__(self,method,*args,**kwargs):

        # Optionally set parameters. If specified, the parameter takes the specified value.
        # If not specified, the parameter takes the default value.
        self.mixing_scheme = method
        self.mix_history_length = kwargs.pop('mix_history_length',20)
        #self.smearing_width = kwargs.pop('smearing_width',"300 K")
        self.mix_charge_amp = kwargs.pop('mix_charge_amp',0.8)
        self.mix_charge_gmax = kwargs.pop('mix_charge_gmax',1.5)
        #self.mix_spin_amp = kwargs.pop('mix_spin_amp',2.0)
        self.mix_spin_amp = 2.0 * self.mix_charge_amp
        #self.mix_spin_gmax = kwargs.pop('mix_spin_gmax',1.5)
        self.mix_spin_gmax = self.mix_charge_gmax
        self.mix_metric_q = kwargs.pop('mix_metric_q',0)
        #self.mix_cutoff_energy = kwargs.pop('mix_cutoff_energy',"!castep_default")
        self.metals_method = kwargs.pop('metals_method','dm')
        self.rand_seed = kwargs.pop('rand_seed',654321)
        self.max_scf_cycles = kwargs.pop('max_scf_cycles',2000)
        self.alpha = kwargs.pop('alpha',0.0001)
        self.sigma = kwargs.pop('sigma',0.5)
        #self.PP_n = kwargs.pop('PP_n',2)
        self.PP_scaling = kwargs.pop('PP_scaling',0.4)
 
