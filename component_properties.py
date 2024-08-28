#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Component properties for all equations of state currently supported

This file stores all of the empirical and physical properties of the components
commonly associated with hydrates. In general, these properties are all those
properties described in the Colorado School of Mines Gibbs Energy Minimization
documentation. Where ambiguities or discrepancies arose, we used our best
judgement on actual properties. In some places, we note inconsistencies.
"""

import numpy as np

# Constants
R = 8.3144621  # Gas constant in J/mol-K
T_0 = 298.15  # Reference temperature in K
P_0 = 1  # Reference pressure in bar


class Component(object):
    """Class for storing information about each component.

    Attributes
    ----------
    menu : dict
        Dictionary that maps preferred name of component to
        possible aliases of that component. Aliases may be used
        for clarity for specific use cases.

    Methods
    ----------
    gibbs_ideal :
        Gibbs free energy of component in ideal gas state.
    """
    menu = dict(h2o=('h2o', 'h_2o', 'h20', 'h_20', 'water'),
                ch4=('ch4', 'ch_4', 'c1', 'methane'),
                c2h6=('c2h6', 'c_2h_6', 'c2', 'ethane'),
                c3h8=('c3h8', 'c_3h_8', 'c3', 'propane'),
                co2=('co2', 'co_2', 'c02', 'c0_2', 'carbon dioxide','carbondioxide'),
                meoh=('methanol', 'meoh'),
                ic4h10=('i-c4h10', "ic4h10", "i-butane"),
                nc4h10=('n-c4h10', "nc4h10", "n-butane"),
                ic5h12=('i-c5h12', "ic5h12", "i-pentane"),
                nc5h12=('n-c5h12', "nc5h12", "n-pentane"),
                nc6h14=('n-c6h14', "nc6h14", "n-hexane"),
                n2=('n2', 'n_2', 'nitrogen'))

    def __init__(self, name_of_comp):
        """Component properties to be used for each EOS

        Parameters
        ----------
        comps : list
            List of components as 'Component' objects created with
            'component_properties.py'.
        T : float
            Temperature at initialization in Kelvin.
        P : float
            Pressure at initialization in bar.
        * : float
            Various other attributes described below. Some are
            nested dictionaries that refere to a specific EOS.

        Attributes
        ----------
        compname : str
            Name of component such that the name is a key in menu.
        """

        if name_of_comp.lower() in self.menu['h2o']:
            self.compname = 'h2o'
        elif name_of_comp.lower() in self.menu['ch4']:
            self.compname = 'ch4'
        elif name_of_comp.lower() in self.menu['c2h6']:
            self.compname = 'c2h6'
        elif name_of_comp.lower() in self.menu['c3h8']:
            self.compname = 'c3h8'
        elif name_of_comp.lower() in self.menu['co2']:
            self.compname = 'co2'
        elif name_of_comp.lower() in self.menu['meoh']:
            self.compname = 'meoh'
        elif name_of_comp.lower() in self.menu['n2']:
            self.compname = 'n2'
        elif name_of_comp.lower() in self.menu['ic4h10']:
            self.compname = 'ic4h10'
        elif name_of_comp.lower() in self.menu['nc4h10']:
            self.compname = 'nc4h10'
        elif name_of_comp.lower() in self.menu['ic5h12']:
            self.compname = 'ic5h12'
        elif name_of_comp.lower() in self.menu['nc5h12']:
            self.compname = 'nc5h12'
        elif name_of_comp.lower() in self.menu['nc6h14']:
            self.compname = 'nc6h14'
        else:
            raise ValueError("""{0} + is not a supported component!!
                             \nConsult 'Component.menu'
                             attribute for \nvalid components and
                             associated call strings.""".format(name_of_comp))

        """
        Set all relevant properties for each component.
        These properties are as follows:
        Generic:
            Tc - 'critical temperature', units = 'Kelvin'
            Pc - 'critical pressure', units = 'bar'
            Vc - 'critical volume', units = 'cm^3'
            MW - 'molecular weight', units = 'g/mol'
            N_carb - 'number of carbon atoms', units = 'none'
            Diam - 'molecular diamter, units = 'angstrom'
            g_io -
                'ideal gas gibb free energy at standard state', units = 'J/mol'
            g_io_ast -
                'partial molar gibb free energy at standard state',
                units = 'J/mol'
            h_io - 'ideal gas enthalpy at standard state', units = 'J/mol'
            h_io_ast -
                'partial molar enthalpy at standard state', units = 'J/mol'
            cp -
                'ideal gas heat capacity parameters',
                units = 'Kelvin'[to power of constant]
        SRK EOS:
            SRK['omega'] - 'acentricity factor', units = 'none'
            SRK['s2'] - 'SRK factor', units = 'none'
            SRK['kij'] = 'interaction factor', units = 'none'
        Hydrate (van der Waals and Platteeuw-Modifed) EOS:
                Structure 1:
                    HvdWPM['s1']['kappa'] -
                        'compressibility constant', units = 'bar^-1'
                    HvdWPM['s1']['large'] - 'large cage factor', units = ''
                    HvdWPM['s1']['small'] - 'small cage factor', units = ''
                Structure 2:
                    HvdWPM['s2']['kappa'] -
                        'compressibility constant', units = 'bar^-1'
                    HvdWPM['s2']['large'] - 'large cage factor', units = ''
                    HvdWPM['s2']['small'] - 'small cage factor', units = ''
                Kihara potential:
                    HvdWPM['kih']['a'] - 'well-radius, units = 'angstrom'
                    HvdWPM['kih']['sigma'] - 'well-depth', units = 'angstrom'
                    HvdWPM['kih']['epsk'] - 'well paramter, units = 'Kelvin'
        Aqueous Hegelson-Bromley EOS:
                AqHB['omega_born'] - 'Born constant', units = 'J/mol'
                AqHB['cp'] -
                    'partial molar heat capacity factors in aqueous phase',
                    units = 'variable'
                AqHB'[v'] -
                'partial molar volume in aqueous phase', units = 'variable'
        Ideal EOS:
            ideal_Hs1 -
                'hydrate structure 1 factors for ideal case, units = ''
            ideal_Hs2 -
                'hydrate structure 2 factors for ideal case, units = ''
        """

        if self.compname == 'h2o':
            self.Tc = 647.3
            self.Pc = 220.483
            self.Vc = 0.0559
            self.MW = 18.015
            self.diam = 0.0
            self.N_carb = 0
            self.g_io = -228700
            self.h_io = -242000
            self.g_io_ast = np.nan
            self.h_io_ast = np.nan
            self.stdst_fug = 0.0334
            self.cp = {'a0': 3.8747 * R,
                       'a1': 0.0231e-2 * R,
                       'a2': 0.1269e-5 * R,
                       'a3': -0.4321e-9 * R}
            self.AqHB = {'cp': {'c1': np.nan,
                                'c2': np.nan},
                         'v': {'v1': np.nan,
                               'v2': np.nan,
                               'v3': np.nan,
                               'v4': np.nan},
                         'omega_born': np.nan}
            self.SRK = {'omega': 0.344,
                        'S2': -0.2018,
                        'kij': {'h2o': 0.0,
                                'ch4': 0.4965,
                                'co2': -0.07,  # CSMGem says 0.2453, documents say -0.07
                                'n2': 0.5063,
                                'c2h6': 0.5975,
                                'meoh': 0.068998,
                                'c3h8': 0.5612,
                                'ic4h10': 0.518,
                                'nc4h10': 0.518,
                                'ic5h12': 0.500000,
                                'nc5h12': 0.5000000,
                                'nc6h14': 0.510900}}
            self.HvdWPM = {'s1': {'kappa': 0.0,
                                  'rep': {'small': 0.0,
                                          'large': 0.0}},
                           's2': {'kappa': 0.0,
                                  'rep': {'small': 0.0,
                                          'large': 0.0}},
                           'kih': {'a': np.nan,
                                   'sig': np.nan,
                                   'epsk': np.nan}}
            self.ideal = {'Hs1': {'a1': np.nan,
                                  'a2': np.nan,
                                  'a3': np.nan,
                                  'a4': np.nan,
                                  'a5': np.nan,
                                  'a6': np.nan,
                                  'a7': np.nan,
                                  'a8': np.nan,
                                  'a9': np.nan,
                                  'a10': np.nan,
                                  'a11': np.nan,
                                  'a12': np.nan,
                                  'a13': np.nan},
                          'Hs2': {'a1': np.nan,
                                  'a2': np.nan,
                                  'a3': np.nan,
                                  'a4': np.nan,
                                  'a5': np.nan,
                                  'a6': np.nan,
                                  'a7': np.nan,
                                  'a8': np.nan,
                                  'a9': np.nan,
                                  'a10': np.nan,
                                  'a12': np.nan,
                                  'a11': np.nan,
                                  'a13': np.nan,
                                  'a14': np.nan,
                                  'a15': np.nan,
                                  'a16': np.nan,
                                  'a17': np.nan,
                                  'a18': np.nan,
                                  'a19': np.nan}}
        elif self.compname == 'ch4':
            self.Tc = 190.56
            self.Pc = 45.991
            self.Vc = 0.09865
            self.MW = 16.043
            self.diam = 4.247
            self.N_carb = 1
            self.g_io = -50830  # Показатель энтропии
            self.h_io = -74900 # Показатель энтальпии
            self.g_io_ast = -34451 #
            self.h_io_ast = -87906 #
            self.stdst_fug = 0.9983
            self.cp = {'a0': 2.3902 * R,
                       'a1': 0.6039e-2 * R,
                       'a2': 0.1525e-5 * R,
                       'a3': -1.3234e-9 * R}
            self.AqHB = {'cp': {'c1': 176.12,
                                'c2': 6310762},
                         'v': {'v1': 2.829,
                               'v2': 3651.8,
                               'v3': 9.7119,
                               'v4': -131365},
                         'omega_born': -133009}
            self.SRK = {'omega': 0.0115,
                        'S2': -0.012223,
                        'kij': {'h2o': 0.4965,
                                'ch4': 0.0,
                                'co2': 0.0936,  # CSMGem says 0.097, documents say 0.0936
                                'n2': 0.0291,  # CSMGem says 0.04, documents say 0.0291
                                'c2h6': 0.003,  # CSMGem says 0.003, documents say 0.0
                                'meoh': -0.035,
                                'c3h8': 0.01008,
                                'ic4h10': 0.0131134,
                                'nc4h10': 0.0123046,
                                'ic5h12': 0.0176275,
                                'nc5h12': 0.0179254,
                                'nc6h14': 0.0234740}}
            self.HvdWPM = {'s1': {'kappa': 1e-5,
                                  'rep': {'small': 0.017668,
                                          'large': 0.010316}},
                           's2': {'kappa': 5e-5,
                                  'rep': {'small': 0.0020998,
                                          'large': 0.011383}},
                           'kih': {'a': 0.3834,
                                   'sig': 3.14393,
                                   'epsk': 155.593}}
            self.ideal = {'Hs1': {'a1': 27.474169,
                                  'a2': -0.8587468,
                                  'a3': 0.0,
                                  'a4': 6604.6088,
                                  'a5': 50.8806,
                                  'a6': 1.57577,
                                  'a7': -1.4011858,
                                  'a8': 0.0,
                                  'a9': 0.0,
                                  'a10': 0.0,
                                  'a11': 0.0,
                                  'a12': 0.0,
                                  'a13': 0.0},
                          'Hs2': {'a1': -0.45872,
                                  'a2': 0.0,
                                  'a3': 0.0,
                                  'a4': 31.6621,
                                  'a5': -3.4028,
                                  'a6': -7.7e-5,
                                  'a7': 0.0,
                                  'a8': 0.0,
                                  'a9': 1.8641,
                                  'a10': -0.78338,
                                  'a11': 0.0,
                                  'a12': 0.0,
                                  'a13': 0.0,
                                  'a14': -77.6955,
                                  'a15': 0.0,
                                  'a16': -2.3e-7,
                                  'a17': -6.1e-5,
                                  'a18': 0.0,
                                  'a19': 0.0}}
        elif self.compname == 'c2h6':
            self.Tc = 305.32
            self.Pc = 48.721
            self.Vc = 0.1455
            self.MW = 30.07
            self.diam = 5.076
            self.N_carb = 2
            self.g_io = -32900
            self.h_io = -84720
            self.g_io_ast = -17000
            self.h_io_ast = -103136
            self.stdst_fug = 0.9925
            self.cp = {'a0': 0.8293 * R,
                       'a1': 2.0752e-2 * R,
                       'a2': -0.7699e-5 * R,
                       'a3': 0.8756e-9 * R}
            self.AqHB = {'cp': {'c1': 226.67,
                                'c2': 9011737},
                         'v': {'v1': 3.612,
                               'v2': 5565.2,
                               'v3': 2.1778,
                               'v4': -139277},
                         'omega_born': -169870}
            self.SRK = {'omega': 0.0995,
                        'S2': -0.012416,
                        'kij': {'h2o': 0.5975,
                                'ch4': 0.003,  # CSMGem says 0.003, documents say 0.0
                                'co2': 0.132,
                                'n2': 0.02,  # CSMGem says 0.02, documents say 0.0082
                                'c2h6': 0.0,
                                'meoh': 0.045,
                                'c3h8': 0.0,
                                'ic4h10': 0.0045735,
                                'nc4h10': 0.0040964,
                                'ic5h12': 0.0074133,
                                'nc5h12': 0.0076094,
                                'nc6h14': 0.0114138}}
            self.HvdWPM = {'s1': {'kappa': 1e-8,
                                  'rep': {'small': 0.0,
                                          'large': 0.025154}},
                           's2': {'kappa': 1e-7,
                                  'rep': {'small': 0.0025097,
                                          'large': 0.014973}},
                           'kih': {'a': 0.5651,
                                   'sig': 3.24693,
                                   'epsk': 188.181}}
            self.ideal = {'Hs1': {'a1': 14.81962,
                                  'a2': 6.813994,
                                  'a3': 0.0,
                                  'a4': 3463.9937,
                                  'a5': 2215.3,
                                  'a6': 0.0,
                                  'a7': 0.0,
                                  'a8': 0.0,
                                  'a9': 0.0,
                                  'a10': 0.0,
                                  'a11': 0.0,
                                  'a12': 0.0,
                                  'a13': 0.0},
                          'Hs2': {'a1': 3.21799,
                                  'a2': 0.0,
                                  'a3': 0.0,
                                  'a4': -290.283,
                                  'a5': 181.2694,
                                  'a6': 0.0,
                                  'a7': 0.0,
                                  'a8': -1.89e-5,
                                  'a9': 1.882,
                                  'a10': -1.19703,
                                  'a11': -402.166,
                                  'a12': -4.897688,
                                  'a13': 0.0411205,
                                  'a14': -68.8018,
                                  'a15': 25.6306,
                                  'a16': 0.0,
                                  'a17': 0.0,
                                  'a18': 0.0,
                                  'a19': 0.0}}
        elif self.compname == 'c3h8':
            self.Tc = 369.83
            self.Pc = 42.481
            self.Vc = 0.2001
            self.MW = 44.097
            self.diam = 5.745
            self.N_carb = 3
            self.g_io = -23500
            self.h_io = -103900
            self.g_io_ast = -7550
            self.h_io_ast = -131000
            self.stdst_fug = 0.9847
            self.cp = {'a0': -0.4861 * R,
                       'a1': 3.6629e-2 * R,
                       'a2': -1.8895e-5 * R,
                       'a3': 3.8143e-9 * R}
            self.AqHB = {'cp': {'c1': 277.52,
                                'c2': 11749531},
                         'v': {'v1': 4.503,
                               'v2': 7738.2,
                               'v3': -6.3316,
                               'v4': -148260},
                         'omega_born': -211418}
            self.SRK = {'omega': 0.1523,
                        'S2': -0.003791,
                        'kij': {'h2o': 0.5612,
                                'ch4': 0.01008,  # CSMGem says 0.01008, documents say 0.0
                                'co2': 0.13,
                                'n2': 0.086,  # CSMGem says 0.086, documents say 0.0865
                                'c2h6': 0.0,
                                'meoh': 0.059999,
                                'c3h8': 0.0,
                                'ic4h10': 0.0010405,
                                'nc4h10': 0.000819,
                                'ic5h12': 0.0025834,
                                'nc5h12': 0.0027005,
                                'nc6h14': 0.0051420}}
            self.HvdWPM = {'s1': {'kappa': 1e-7,
                                  'rep': {'small': 0.0,
                                          'large': 0.0}},
                           's2': {'kappa': 1e-6,
                                  'rep': {'small': 0.0,
                                          'large': 0.025576}},
                           'kih': {'a': 0.6502,
                                   'sig': 3.41670,
                                   'epsk': 192.855}}
            self.ideal = {'Hs1': {'a1': 1e2,
                                  'a2': 0,
                                  'a3': 0,
                                  'a4': 0,
                                  'a5': 0,
                                  'a6': 0,
                                  'a7': 0,
                                  'a8': 0,
                                  'a9': 0,
                                  'a10': 0,
                                  'a11': 0,
                                  'a12': 0,
                                  'a13': 0},
                          'Hs2': {'a1': -7.51966,
                                  'a2': 0.0,
                                  'a3': 0.0,
                                  'a4': 47.056,
                                  'a5': 0.0,
                                  'a6': -1.697e-5,
                                  'a7': 0.0007145,
                                  'a8': 0.0,
                                  'a9': 0.0,
                                  'a10': 0.12348,
                                  'a11': 79.34,
                                  'a12': 0.0,
                                  'a13': 0.0160778,
                                  'a14': 0.0,
                                  'a15': -14.684,
                                  'a16': 5.5e-6,
                                  'a17': 0.0,
                                  'a18': 0.0,
                                  'a19': 0.0}}
        elif self.compname == 'co2':
            self.Tc = 304.21
            self.Pc = 73.831
            self.Vc = 0.09396
            self.MW = 44.01
            self.diam = 4.603
            self.N_carb = 1
            self.g_io = -394600
            self.h_io = -393800
            self.g_io_ast = -385974
            self.h_io_ast = -413798
            self.stdst_fug = 0.9951
            self.cp = {'a0': 2.6751 * R,
                       'a1': 0.7188e-2 * R,
                       'a2': -0.4208e-5 * R,
                       'a3': 0.8977e-9 * R}
            self.AqHB = {'cp': {'c1': 167.50,
                                'c2': 5304066},
                         'v': {'v1': 2.614,
                               'v2': 3125.9,
                               'v3': 11.7721,
                               'v4': -129198},
                         'omega_born': -8368}
            self.SRK = {'omega': 0.2236,
                        'S2': -0.004474,
                        'kij': {'h2o': -0.07,  # CSMGem says 0.2453, documents say -0.07
                                'ch4': 0.0936,  # CSMGem says 0.097, documents say 0.0936
                                'co2': 0.0,
                                'n2': -0.0462,  # CSMGem says -0.046, documents say -0.0462
                                'c2h6': 0.132,
                                'meoh': -0.09,
                                'c3h8': 0.13,
                                'ic4h10': 0.1368,
                                'nc4h10': 0.1412,
                                'ic5h12': 0.1297,
                                'nc5h12': 0.1347,
                                'nc6h14': 0.14200}}
            self.HvdWPM = {'s1': {'kappa': 1e-6,
                                  'rep': {'small': 0.0,
                                          'large': 0.0058282}},
                           's2': {'kappa': 1e-5,
                                  'rep': {'small': 0.002758,
                                          'large': 0.012242}},
                           'kih': {'a': 0.6805,
                                   'sig': 2.97638,
                                   'epsk': 175.405}}
            self.ideal = {'Hs1': {'a1': 15.8336435,
                                  'a2': 3.119,
                                  'a3': 0.0,
                                  'a4': 3760.6324,
                                  'a5': 1090.27777,
                                  'a6': 0.0,
                                  'a7': 0.0,
                                  'a8': 0.0,
                                  'a9': 0.0,
                                  'a10': 0.0,
                                  'a11': 0.0,
                                  'a12': 0.0,
                                  'a13': 0.0},
                          'Hs2': {'a1': 9.0242,
                                  'a2': 0.0,
                                  'a3': 0.0,
                                  'a4': -207.033,
                                  'a5': 0.0,
                                  'a6': 0.00067588,
                                  'a7': -0.006992,
                                  'a8': -0.0006079,
                                  'a9': -0.09026,
                                  'a10': 0.0,
                                  'a11': 0.0,
                                  'a12': 0.0,
                                  'a13': 0.0186833,
                                  'a14': 0.0,
                                  'a15': 0.0,
                                  'a16': 8.82e-5,
                                  'a17': 0.00778015,
                                  'a18': 0.0,
                                  'a19': 0.0}}
        elif self.compname == 'n2':
            self.Tc = 126.2
            self.Pc = 34.001
            self.Vc = 0.08919
            self.MW = 28.013
            self.diam = 4.177
            self.N_carb = 0.0
            self.g_io = 0.0
            self.h_io = 0.0
            self.g_io_ast = 18188
            self.h_io_ast = -10439
            self.stdst_fug = 0.9999
            self.cp = {'a0': 3.4736 * R,
                       'a1': -0.0189e-2 * R,
                       'a2': 0.0971e-5 * R,
                       'a3': -0.3453e-9 * R}
            self.AqHB = {'cp': {'c1': 149.75,
                                'c2': 5046230},
                         'v': {'v1': 2.596,
                               'v2': 3083.0,
                               'v3': 11.9407,
                               'v4': -129018},
                         'omega_born': -145101}
            self.SRK = {'omega': 0.0377,
                        'S2': -0.011016,
                        'kij': {'h2o': 0.5063,
                                'ch4': 0.0291,  # CSMGEm says 0.04, documents say 0.0291
                                'co2': -0.0462,  # CSMGem says -.046, documents say -0.0462
                                'n2': 0.0,
                                'c2h6': 0.0082,  # CSMGem says 0.02, documents say 0.0082
                                'meoh': 0.017,
                                'c3h8': 0.0862,
                                'ic4h10': 0.1315,
                                'nc4h10': 0.0597,
                                'ic5h12': 0.09300,
                                'nc5h12': 0.093598,
                                'nc6h14': 0.165000}}
            self.HvdWPM = {'s1': {'kappa': 1.1e-5,
                                  'rep': {'small': 0.017377,
                                          'large': 0.0}},
                           's2': {'kappa': 1.1e-5,
                                  'rep': {'small': 0.0020652,
                                          'large': 0.011295}},
                           'kih': {'a': 0.3526,
                                   'sig': 3.13512,
                                   'epsk': 127.426}}
            self.ideal = {'Hs1': {'a1': 173.2164,
                                  'a2': -0.5996,
                                  'a3': 0.0,
                                  'a4': 24751.6667,
                                  'a5': 0.0,
                                  'a6': 0.0,
                                  'a7': 0.0,
                                  'a8': 1.441,
                                  'a9': -37.0696,
                                  'a10': -0.287444,
                                  'a11': -2.07e-5,
                                  'a12': 0.0,
                                  'a13': 0.0},
                          'Hs2': {'a1': 1.78857,
                                  'a2': 0.0,
                                  'a3': -0.019667,
                                  'a4': -6.187,
                                  'a5': 0.0,
                                  'a6': 0.0,
                                  'a7': 0.0,
                                  'a8': 5.259e-5,
                                  'a9': 0.0,
                                  'a10': 0.0,
                                  'a11': 0.0,
                                  'a12': 0.0,
                                  'a13': 0.0,
                                  'a14': 0.0,
                                  'a15': 192.39,
                                  'a16': 0.0,
                                  'a17': 3.05e-5,
                                  'a18': 1.1e-7,
                                  'a19': 0.0}}

        elif self.compname == 'meoh':
            self.Tc = 512.59
            self.Pc = 73.76
            self.Vc = 0.127
            self.MW = 32.04
            self.diam = 4.177
            self.N_carb = 0.0
            self.g_io = -162600
            self.h_io = -201300
            self.g_io_ast = -175937
            self.h_io_ast = -246312
            self.stdst_fug = 0.145
            self.cp = {'a0': 2.2896 * R,
                       'a1': 1.1e-2 * R,
                       'a2': -0.1464e-5 * R,
                       'a3': -0.97e-9 * R}
            self.AqHB = {'cp': {'c1': 165.21,
                                'c2': -903211},
                         'v': {'v1': 2.9,
                               'v2': 2307.3,
                               'v3': 47.71,
                               'v4': -125809},
                         'omega_born': -61756}
            self.SRK = {'omega': 0.557,
                        'S2': 0,
                        'kij': {'h2o': 0.068998,
                                'ch4': -0.035,  # CSMGEm says 0.04, documents say 0.0291
                                'co2': -0.09,  # CSMGem says -.046, documents say -0.0462
                                'n2': 0.017,
                                'c2h6': 0.045,  # CSMGem says 0.02, documents say 0.0082
                                'meoh': 0.0,
                                'c3h8': 0.059999,
                                'ic4h10': 0.068998,
                                'nc4h10': 0.068998,
                                'ic5h12': 0.000000,
                                'nc5h12': 0.0000000,
                                'nc6h14': 0.000000}}
            self.HvdWPM = {'s1': {'kappa': 0.0,
                                  'rep': {'small': 0.0,
                                          'large': 0.0}},
                           's2': {'kappa': 0.0,
                                  'rep': {'small': 0.0,
                                          'large': 0.0}},
                           'kih': {'a': 0.0,
                                   'sig': 0.0,
                                   'epsk': 0.0}}
            self.ideal = {'Hs1': {'a1': 0.0,
                                  'a2': 0.0,
                                  'a3': 0.0,
                                  'a4': 0.0,
                                  'a5': 0.0,
                                  'a6': 0.0,
                                  'a7': 0.0,
                                  'a8': 0.0,
                                  'a9': 0.0,
                                  'a10': 0.0,
                                  'a11': 0.0,
                                  'a12': 0.0,
                                  'a13': 0.0},
                          'Hs2': {'a1': 0.0,
                                  'a2': 0.0,
                                  'a3': 0.0,
                                  'a4': 0.0,
                                  'a5': 0.0,
                                  'a6': 0.0,
                                  'a7': 0.0,
                                  'a8': 0.0,
                                  'a9': 0.0,
                                  'a10': 0.0,
                                  'a11': 0.0,
                                  'a12': 0.0,
                                  'a13': 0.0,
                                  'a14': 0.0,
                                  'a15': 0.0,
                                  'a16': 0.0,
                                  'a17': 0.0,
                                  'a18': 0.0,
                                  'a19': 0.0}}

        elif self.compname == 'ic4h10':
            self.Tc = 408.09601
            self.Pc = 36.476201
            self.Vc = 0.263
            self.MW = 58.124001
            self.diam = 6.306
            self.N_carb = 4.0
            self.g_io = -20900
            self.h_io = -134600
            self.g_io_ast = -2900
            self.h_io_ast = -156000
            self.stdst_fug = 0.95
            self.cp = {'a0': -0.9511 * R,
                       'a1': 4.9999e-2 * R,
                       'a2': -2.7651e-5 * R,
                       'a3': -6.00e-9 * R}
            self.AqHB = {'cp': {'c1': 330.77,
                                'c2': 14610096},
                         'v': {'v1': 5.5,
                               'v2': 11014.40,
                               'v3': -14.93,
                               'v4': -157256},
                         'omega_born': -253592}
            self.SRK = {'omega': 0.1848,
                        'S2': 0,
                        'kij': {'h2o': 0.518,
                                'ch4': -0.0131134,  # CSMGEm says 0.04, documents say 0.0291
                                'co2': -0.1368,  # CSMGem says -.046, documents say -0.0462
                                'n2': 0.1315,
                                'c2h6': 0.0045735,  # CSMGem says 0.02, documents say 0.0082
                                'meoh': 0.0689980,
                                'c3h8': 0.0010405, # CSMGem says 0.086, documents say 0.0862
                                'ic4h10': 0.0,
                                'nc4h10': 0.0000134,
                                'ic5h12': 0.0003462,
                                'nc5h12': 0.0003901,
                                'nc6h14': 0.0015653}}
            self.HvdWPM = {'s1': {'kappa': 0.0,
                                  'rep': {'small': 0.0,
                                          'large': 0.0}},
                           's2': {'kappa': 1.0e-08,
                                  'rep': {'small': 0.0,
                                          'large': 3.60e-02}},
                           'kih': {'a': 0.8706,
                                   'sig': 3.41691,
                                   'epsk': 198.333}}
            self.ideal = {'Hs1': {'a1': 0.0,
                                  'a2': 0.0,
                                  'a3': 0.0,
                                  'a4': 0.0,
                                  'a5': 0.0,
                                  'a6': 0.0,
                                  'a7': 0.0,
                                  'a8': 0.0,
                                  'a9': 0.0,
                                  'a10': 0.0,
                                  'a11': 0.0,
                                  'a12': 0.0,
                                  'a13': 0.0},
                          'Hs2': {'a1': -9.55128,
                                  'a2': 0.0,
                                  'a3': 0.0,
                                  'a4': 0.0,
                                  'a5': 0.0,
                                  'a6': 0.0,
                                  'a7': 0.00125,
                                  'a8': 0.0,
                                  'a9': 2.40904,
                                  'a10': -2.75945,
                                  'a11': 0.0,
                                  'a12': 0.0,
                                  'a13': 0.0,
                                  'a14': 0.0,
                                  'a15': -0.28974,
                                  'a16': 0.0,
                                  'a17': -0.00165,
                                  'a18': 0.0,
                                  'a19': 0.0}}

        elif self.compname == 'nc4h10':
            self.Tc = 425.199005
            self.Pc = 37.9662012
            self.Vc = 0.25499001
            self.MW = 58.1240005
            self.diam = 6.336
            self.N_carb = 4.0
            self.g_io = -17200
            self.h_io = -126200
            self.g_io_ast = -940
            self.h_io_ast = -152000
            self.stdst_fug = 0.95
            self.cp = {'a0': 0.4755 * R,
                       'a1': 4.4650e-2 * R,
                       'a2': -2.2041e-5 * R,
                       'a3': 4.21e-9 * R}
            self.AqHB = {'cp': {'c1': 330.77,
                                'c2': 14610096},
                         'v': {'v1': 5.5,
                               'v2': 11014.40,
                               'v3': -14.93,
                               'v4': -157256},
                         'omega_born': -253592}
            self.SRK = {'omega': 0.2010,
                        'S2': 0,
                        'kij': {'h2o': 0.518,
                                'ch4': 0.0123046,  # CSMGEm says 0.04, documents say 0.0291
                                'co2': 0.1412,  # CSMGem says -.046, documents say -0.0462
                                'n2': 0.0597,
                                'c2h6': 0.0040964,  # CSMGem says 0.02, documents say 0.0082
                                'meoh': 0.0689980,
                                'c3h8': 0.0008190,  # CSMGem says 0.086, documents say 0.0862
                                'ic4h10': 0.0000134,
                                'nc4h10': 0.0,
                                'ic5h12': 0.0004951,
                                'nc5h12': 0.0005472,
                                'nc6h14': 0.0018663}}
            self.HvdWPM = {'s1': {'kappa': 0.0,
                                  'rep': {'small': 0.0,
                                          'large': 0.0}},
                           's2': {'kappa': 1.0e-08,
                                  'rep': {'small': 0.0,
                                          'large': 3.66e-02}},
                           'kih': {'a': 0.9379,
                                   'sig': 3.51726,
                                   'epsk': 197.254}}
            self.ideal = {'Hs1': {'a1': 0.0,
                                  'a2': 0.0,
                                  'a3': 0.0,
                                  'a4': 0.0,
                                  'a5': 0.0,
                                  'a6': 0.0,
                                  'a7': 0.0,
                                  'a8': 0.0,
                                  'a9': 0.0,
                                  'a10': 0.0,
                                  'a11': 0.0,
                                  'a12': 0.0,
                                  'a13': 0.0},
                          'Hs2': {'a1': -37.211,
                                  'a2': 0.86564,
                                  'a3': 0.0,
                                  'a4': 732.2,
                                  'a5': 0.0,
                                  'a6': 0.0,
                                  'a7': 0.0,
                                  'a8': 0.00197,
                                  'a9': -15.6144,
                                  'a10': 0.0,
                                  'a11': 0.0,
                                  'a12': -4.56576,
                                  'a13': 0.0,
                                  'a14': 0.0,
                                  'a15': 300.5535,
                                  'a16': 0.0,
                                  'a17': 0.01519,
                                  'a18': 0.0,
                                  'a19': 0.0}}

        elif self.compname == 'ic5h12':
            self.Tc = 460.39801
            self.Pc = 33.3359009
            self.Vc = 0.30799001
            self.MW = 72.151001
            self.diam = 6.777
            self.N_carb = 5.0
            self.g_io = -15229
            self.h_io = -165976
            self.g_io_ast = 1541
            self.h_io_ast = -193476
            self.stdst_fug = 0.85
            self.cp = {'a0': -1.9942 * R,
                       'a1': 6.6725e-2 * R,
                       'a2': -3.9738e-5 * R,
                       'a3': 9.17e-9 * R}
            self.AqHB = {'cp': {'c1': 373.00,
                                'c2': 16997948.00},
                         'v': {'v1': 6.3,
                               'v2': 12100.0,
                               'v3': -23.4,
                               'v4': -166000.00},
                         'omega_born': -301000.00}
            self.SRK = {'omega': 0.2222,
                        'S2': 0,
                        'kij': {'h2o': 0.500,
                                'ch4': 0.0176275,  # CSMGEm says 0.04, documents say 0.0291
                                'co2': 0.1297,  # CSMGem says -.046, documents say -0.0462
                                'n2': 0.09300,
                                'c2h6': 0.0074133,  # CSMGem says 0.02, documents say 0.0082
                                'meoh': 0.00000,
                                'c3h8': 0.0025834,  # CSMGem says 0.086, documents say 0.0862
                                'ic4h10': 0.0003462,
                                'nc4h10': 0.0004951,
                                'ic5h12': 0.000000,
                                'nc5h12': 0.0000013,
                                'nc6h14': 0.0004399}}
            self.HvdWPM = {'s1': {'kappa': 0.0,
                                  'rep': {'small': 0.0,
                                          'large': 0.0}},
                           's2': {'kappa': 1.0e-08,
                                  'rep': {'small': 0.0,
                                          'large': 4.76e-02}},
                           'kih': {'a': 0.9868,
                                   'sig': 3.5455,
                                   'epsk': 199.56}}
            self.ideal = {'Hs1': {'a1': 0.0,
                                  'a2': 0.0,
                                  'a3': 0.0,
                                  'a4': 0.0,
                                  'a5': 0.0,
                                  'a6': 0.0,
                                  'a7': 0.0,
                                  'a8': 0.0,
                                  'a9': 0.0,
                                  'a10': 0.0,
                                  'a11': 0.0,
                                  'a12': 0.0,
                                  'a13': 0.0},
                          'Hs2': {'a1': 0.0,
                                  'a2': 0.0,
                                  'a3': 0.0,
                                  'a4': 0.0,
                                  'a5': 0.0,
                                  'a6': 0.0,
                                  'a7': 0.0,
                                  'a8': 0.0,
                                  'a9': 0.0,
                                  'a10': 0.0,
                                  'a11': 0.0,
                                  'a12': 0.0,
                                  'a13': 0.0,
                                  'a14': 0.0,
                                  'a15': 0.0,
                                  'a16': 0.0,
                                  'a17': 0.0,
                                  'a18': 0.0,
                                  'a19': 0.0}}
        elif self.compname == 'nc5h12':
            self.Tc = 469.6000061
            self.Pc = 33.75120117
            self.Vc = 0.310990006
            self.MW = 72.15100098
            self.diam = 6.777
            self.N_carb = 5.0
            self.g_io = -8370
            self.h_io = -146500
            self.g_io_ast = 9160
            self.h_io_ast = -173887
            self.stdst_fug = 0.85
            self.cp = {'a0': 0.8142 * R,
                       'a1': 5.4598e-2 * R,
                       'a2': -2.6997e-5 * R,
                       'a3': 5.08e-9 * R}
            self.AqHB = {'cp': {'c1': 373.24,
                                'c2': 16955051.00},
                         'v': {'v1': 6.28,
                               'v2': 12082.20,
                               'v3': -23.41,
                               'v4': -166218.00},
                         'omega_born': -300955.00}
            self.SRK = {'omega': 0.2539,
                        'S2': 0,
                        'kij': {'h2o': 0.500,
                                'ch4': 0.0179254,  # CSMGEm says 0.04, documents say 0.0291
                                'co2': 0.1347,  # CSMGem says -.046, documents say -0.0462
                                'n2': 0.0935980,
                                'c2h6': 0.0076094,  # CSMGem says 0.02, documents say 0.0082
                                'meoh': 0.00000,
                                'c3h8': 0.0027005,  # CSMGem says 0.086, documents say 0.0862
                                'ic4h10': 0.0003901,
                                'nc4h10': 0.0005472,
                                'ic5h12': 0.0000013,
                                'nc5h12': 0.0000000,
                                'nc6h14': 0.0003935}}
            self.HvdWPM = {'s1': {'kappa': 0.0,
                                  'rep': {'small': 0.0,
                                          'large': 0.0}},
                           's2': {'kappa': 0.0,
                                  'rep': {'small': 0.0,
                                          'large': 0.0}},
                           'kih': {'a': 0.0,
                                   'sig': 0.0,
                                   'epsk': 0.0}}
            self.ideal = {'Hs1': {'a1': 0.0,
                                  'a2': 0.0,
                                  'a3': 0.0,
                                  'a4': 0.0,
                                  'a5': 0.0,
                                  'a6': 0.0,
                                  'a7': 0.0,
                                  'a8': 0.0,
                                  'a9': 0.0,
                                  'a10': 0.0,
                                  'a11': 0.0,
                                  'a12': 0.0,
                                  'a13': 0.0},
                          'Hs2': {'a1': 0.0,
                                  'a2': 0.0,
                                  'a3': 0.0,
                                  'a4': 0.0,
                                  'a5': 0.0,
                                  'a6': 0.0,
                                  'a7': 0.0,
                                  'a8': 0.0,
                                  'a9': 0.0,
                                  'a10': 0.0,
                                  'a11': 0.0,
                                  'a12': 0.0,
                                  'a13': 0.0,
                                  'a14': 0.0,
                                  'a15': 0.0,
                                  'a16': 0.0,
                                  'a17': 0.0,
                                  'a18': 0.0,
                                  'a19': 0.0}}
        elif self.compname == 'nc6h14':
            self.Tc = 507.8980103
            self.Pc = 30.31620177
            self.Vc = 0.368000001
            self.MW = 86.17790222
            self.diam = 0.0
            self.N_carb = 6.0
            self.g_io = -290
            self.h_io = -167300
            self.g_io_ast = 18200
            self.h_io_ast = -199200
            self.stdst_fug = 0.75
            self.cp = {'a0': 0.8338 * R,
                       'a1': 6.6373e-2 * R,
                       'a2': -3.444e-5 * R,
                       'a3': 6.93e-9 * R}
            self.AqHB = {'cp': {'c1': 424.53,
                                'c2': 19680558.00},
                         'v': {'v1': 7.18,
                               'v2': 14264.40,
                               'v3': -32.02,
                               'v4': -175238.00},
                         'omega_born': -335180.00}
            self.SRK = {'omega': 0.3007,
                        'S2': 0,
                        'kij': {'h2o': 0.5109,
                                'ch4': 0.023474,  # CSMGEm says 0.04, documents say 0.0291
                                'co2': 0.14200,  # CSMGem says -.046, documents say -0.0462
                                'n2': 0.165000,
                                'c2h6': 0.0114138,  # CSMGem says 0.02, documents say 0.0082
                                'meoh': 0.00000,
                                'c3h8': 0.0051420,  # CSMGem says 0.086, documents say 0.0862
                                'ic4h10': 0.0015653,
                                'nc4h10': 0.0018663,
                                'ic5h12': 0.0004399,
                                'nc5h12': 0.0003935,
                                'nc6h14': 0.000000}}
            self.HvdWPM = {'s1': {'kappa': 0.0,
                                  'rep': {'small': 0.0,
                                          'large': 0.0}},
                           's2': {'kappa': 0.0,
                                  'rep': {'small': 0.0,
                                          'large': 0.0}},
                           'kih': {'a': 0.0,
                                   'sig': 0.0,
                                   'epsk': 0.0}}
            self.ideal = {'Hs1': {'a1': 0.0,
                                  'a2': 0.0,
                                  'a3': 0.0,
                                  'a4': 0.0,
                                  'a5': 0.0,
                                  'a6': 0.0,
                                  'a7': 0.0,
                                  'a8': 0.0,
                                  'a9': 0.0,
                                  'a10': 0.0,
                                  'a11': 0.0,
                                  'a12': 0.0,
                                  'a13': 0.0},
                          'Hs2': {'a1': 0.0,
                                  'a2': 0.0,
                                  'a3': 0.0,
                                  'a4': 0.0,
                                  'a5': 0.0,
                                  'a6': 0.0,
                                  'a7': 0.0,
                                  'a8': 0.0,
                                  'a9': 0.0,
                                  'a10': 0.0,
                                  'a11': 0.0,
                                  'a12': 0.0,
                                  'a13': 0.0,
                                  'a14': 0.0,
                                  'a15': 0.0,
                                  'a16': 0.0,
                                  'a17': 0.0,
                                  'a18': 0.0,
                                  'a19': 0.0}}
        elif self.compname == 'nc7h16':
            self.Tc = 540.15802
            self.Pc = 27.36
            self.Vc = 0.425980002
            self.MW = 100.2050018
            self.diam = 0.0
            self.N_carb = 6.0
            self.g_io = -290
            self.h_io = -167300
            self.g_io_ast = 18200
            self.h_io_ast = -199200
            self.stdst_fug = 0.75
            self.cp = {'a0': 0.8338 * R,
                       'a1': 6.6373e-2 * R,
                       'a2': -3.444e-5 * R,
                       'a3': 6.93e-9 * R}
            self.AqHB = {'cp': {'c1': 424.53,
                                'c2': 19680558.00},
                         'v': {'v1': 7.18,
                               'v2': 14264.40,
                               'v3': -32.02,
                               'v4': -175238.00},
                         'omega_born': -335180.00}
            self.SRK = {'omega': 0.3007,
                        'S2': 0,
                        'kij': {'h2o': 0.5109,
                                'ch4': 0.023474,  # CSMGEm says 0.04, documents say 0.0291
                                'co2': 0.14200,  # CSMGem says -.046, documents say -0.0462
                                'n2': 0.165000,
                                'c2h6': 0.0114138,  # CSMGem says 0.02, documents say 0.0082
                                'meoh': 0.00000,
                                'c3h8': 0.0051420,  # CSMGem says 0.086, documents say 0.0862
                                'ic4h10': 0.0015653,
                                'nc4h10': 0.0018663,
                                'ic5h12': 0.0004399,
                                'nc5h12': 0.0003935,
                                'nc6h14': 0.000000}}
            self.HvdWPM = {'s1': {'kappa': 0.0,
                                  'rep': {'small': 0.0,
                                          'large': 0.0}},
                           's2': {'kappa': 0.0,
                                  'rep': {'small': 0.0,
                                          'large': 0.0}},
                           'kih': {'a': 0.0,
                                   'sig': 0.0,
                                   'epsk': 0.0}}
            self.ideal = {'Hs1': {'a1': 0.0,
                                  'a2': 0.0,
                                  'a3': 0.0,
                                  'a4': 0.0,
                                  'a5': 0.0,
                                  'a6': 0.0,
                                  'a7': 0.0,
                                  'a8': 0.0,
                                  'a9': 0.0,
                                  'a10': 0.0,
                                  'a11': 0.0,
                                  'a12': 0.0,
                                  'a13': 0.0},
                          'Hs2': {'a1': 0.0,
                                  'a2': 0.0,
                                  'a3': 0.0,
                                  'a4': 0.0,
                                  'a5': 0.0,
                                  'a6': 0.0,
                                  'a7': 0.0,
                                  'a8': 0.0,
                                  'a9': 0.0,
                                  'a10': 0.0,
                                  'a11': 0.0,
                                  'a12': 0.0,
                                  'a13': 0.0,
                                  'a14': 0.0,
                                  'a15': 0.0,
                                  'a16': 0.0,
                                  'a17': 0.0,
                                  'a18': 0.0,
                                  'a19': 0.0}}
    def gibbs_ideal(self, T, P):
        """Gibbs free energy in ideal gas state.

         Parameters
         ----------
         T : float
            Temperature in Kelvin.
         P : float
            Pressure in bar.

         Returns
         ----------
         g_io_RT : float
            Gibbs free energy of component in ideal gas state.
        """
        g_io_RT = (
                self.g_io / (R * T_0)
                - (12 * T * self.h_io - 12 * T_0 * self.h_io + 12 * T_0 ** 2 * self.cp['a0']
                   + 6 * T_0 ** 3 * self.cp['a1'] + 4 * T_0 ** 4 * self.cp['a2']
                   + 3 * T_0 ** 5 * self.cp['a3'] - 12 * T * T_0 * self.cp['a0']
                   - 12 * T * T_0 ** 2 * self.cp['a1'] + 6 * T ** 2 * T_0 * self.cp['a1']
                   - 6 * T * T_0 ** 3 * self.cp['a2'] + 2 * T ** 3 * T_0 * self.cp['a2']
                   - 4 * T * T_0 ** 4 * self.cp['a3'] + T ** 4 * T_0 * self.cp['a3']
                   + 12 * T * T_0 * self.cp['a0'] * np.log(T)
                   - 12 * T * T_0 * self.cp['a0'] * np.log(T_0)
                   ) / (12 * R * T * T_0)
        )
        return g_io_RT
