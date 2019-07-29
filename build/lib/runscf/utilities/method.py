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
        self.mix_history_length = kwargs.pop('mix_history_length',30)
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