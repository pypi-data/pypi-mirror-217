import numpy as np
import pandas as pd
try:
    import openmm as mm
    import openmm.unit as unit
except ImportError:
    import simtk.openmm as mm
    import simtk.unit as unit
from openabc.lib.physical_constants import NA, kB, EC, VEP
import math
import sys
import os

"""
Note addGlobalParameter can automatically convert the values to the correct unit. 
Be careful that addGlobalParameter sets global parameters that is used by all the forces in the system. 
"""

def moff_mrg_contact_term(atom_types, df_exclusions, use_pbc, alpha_map, epsilon_map, eta=0.7/unit.angstrom, 
                          r0=8.0*unit.angstrom, cutoff=2.0*unit.nanometer, force_group=5):
    """
    MOFF+MRG model nonbonded contact term.
    """
    eta_value = eta.value_in_unit(unit.nanometer**-1)
    r0_value = r0.value_in_unit(unit.nanometer)
    cutoff_value = cutoff.value_in_unit(unit.nanometer)
    contacts = mm.CustomNonbondedForce(f'''energy;
               energy=(energy1+energy2-offset1-offset2)*step({cutoff_value}-r);
               energy1=alpha_con/(r^12);
               energy2=-0.5*epsilon_con*(1+tanh({eta_value}*({r0_value}-r)));
               offset1=alpha_con/({cutoff_value}^12);
               offset2=-0.5*epsilon_con*(1+tanh({eta_value}*({r0_value}-{cutoff_value})));
               alpha_con=alpha_con_map(atom_type1, atom_type2);
               epsilon_con=epsilon_con_map(atom_type1, atom_type2);
               ''')
    n_atom_types = alpha_map.shape[0]
    discrete_2d_alpha_map = mm.Discrete2DFunction(n_atom_types, n_atom_types, alpha_map.ravel().tolist())
    discrete_2d_epsilon_map = mm.Discrete2DFunction(n_atom_types, n_atom_types, epsilon_map.ravel().tolist())
    contacts.addTabulatedFunction('alpha_con_map', discrete_2d_alpha_map)
    contacts.addTabulatedFunction('epsilon_con_map', discrete_2d_epsilon_map)
    contacts.addPerParticleParameter('atom_type')
    for each in atom_types:
        contacts.addParticle([each])
    for i, row in df_exclusions.iterrows():
        contacts.addExclusion(int(row['a1']), int(row['a2']))
    if use_pbc:
        contacts.setNonbondedMethod(contacts.CutoffPeriodic)
    else:
        contacts.setNonbondedMethod(contacts.CutoffNonPeriodic)
    contacts.setCutoffDistance(cutoff)
    contacts.setForceGroup(force_group)
    return contacts


def ashbaugh_hatch_term(atom_types, df_exclusions, use_pbc, epsilon, sigma_ah_map, lambda_ah_map, force_group=2):
    """
    Ashbaugh-Hatch potential. 
    The cutoff is 4*sigma_ah. 
    """
    lj_at_cutoff = 4*epsilon*((1/4)**12 - (1/4)**6)
    contacts = mm.CustomNonbondedForce(f'''energy;
               energy=(f1+f2-offset)*step(4*sigma_ah-r);
               offset=lambda_ah*{lj_at_cutoff};
               f1=(lj+(1-lambda_ah)*{epsilon})*step(2^(1/6)*sigma_ah-r);
               f2=lambda_ah*lj*step(r-2^(1/6)*sigma_ah);
               lj=4*{epsilon}*((sigma_ah/r)^12-(sigma_ah/r)^6);
               sigma_ah=sigma_ah_map(atom_type1, atom_type2);
               lambda_ah=lambda_ah_map(atom_type1, atom_type2);
               ''')
    n_atom_types = sigma_ah_map.shape[0]
    discrete_2d_sigma_ah_map = mm.Discrete2DFunction(n_atom_types, n_atom_types, sigma_ah_map.ravel().tolist())
    discrete_2d_lambda_ah_map = mm.Discrete2DFunction(n_atom_types, n_atom_types, lambda_ah_map.ravel().tolist())
    contacts.addTabulatedFunction('sigma_ah_map', discrete_2d_sigma_ah_map)
    contacts.addTabulatedFunction('lambda_ah_map', discrete_2d_lambda_ah_map)
    contacts.addPerParticleParameter('atom_type')
    for each in atom_types:
        contacts.addParticle([each])
    for i, row in df_exclusions.iterrows():
        contacts.addExclusion(int(row['a1']), int(row['a2']))
    if use_pbc:
        contacts.setNonbondedMethod(contacts.CutoffPeriodic)
    else:
        contacts.setNonbondedMethod(contacts.CutoffNonPeriodic)
    contacts.setCutoffDistance(4*np.amax(sigma_ah_map))
    contacts.setForceGroup(force_group)
    return contacts


def ddd_dh_elec_term(charges, df_exclusions, use_pbc, salt_conc=150.0*unit.millimolar, 
                     temperature=300.0*unit.kelvin, cutoff=4.0*unit.nanometer, force_group=6):
    """
    Debye-Huckel potential with a distance-dependent dielectric.
    """
    alpha = NA*EC**2/(4*np.pi*VEP)
    gamma = VEP*kB*temperature/(2.0*NA*salt_conc*EC**2)
    # use a distance-dependent relative permittivity (dielectric)
    dielectric_water = 78.4
    A = -8.5525
    kappa = 7.7839
    B = dielectric_water - A
    zeta = 0.03627
    cutoff_value = cutoff.value_in_unit(unit.nanometer)
    alpha_value = alpha.value_in_unit(unit.kilojoule_per_mole*unit.nanometer)
    gamma_value = gamma.value_in_unit(unit.nanometer**2)
    dielectric_at_cutoff = A + B/(1 + kappa*math.exp(-zeta*B*cutoff_value))
    ldby_at_cutoff = (dielectric_at_cutoff*gamma_value)**0.5
    elec = mm.CustomNonbondedForce(f'''energy;
           energy=q1*q2*{alpha_value}*((exp(-r/ldby)/r)-offset)*step({cutoff_value}-r)/dielectric;
           offset={math.exp(-cutoff_value/ldby_at_cutoff)/cutoff_value};
           ldby=(dielectric*{gamma_value})^0.5;
           dielectric={A}+{B}/(1+{kappa}*exp(-{zeta}*{B}*r));
           ''')
    elec.addPerParticleParameter('q')
    for q in charges:
        elec.addParticle([q])
    for i, row in df_exclusions.iterrows():
        elec.addExclusion(int(row['a1']), int(row['a2']))
    if use_pbc:
        elec.setNonbondedMethod(elec.CutoffPeriodic)
    else:
        elec.setNonbondedMethod(elec.CutoffNonPeriodic)
    elec.setCutoffDistance(cutoff)
    elec.setForceGroup(force_group)
    return elec
    

def ddd_dh_elec_switch_term(charges, df_exclusions, use_pbc, salt_conc=150.0*unit.millimolar, 
                            temperature=300.0*unit.kelvin, cutoff1=1.2*unit.nanometer, cutoff2=1.5*unit.nanometer, 
                            switch_coeff=[1, 0, 0, -10, 15, -6], force_group=6):
    """
    Debye-Huckel potential with a distance-dependent dielectric and a switch function. 
    The switch function value changes from 1 to 0 smoothly as distance r changes from cutoff1 to cutoff2. 
    To make sure the switch function works properly, the zeroth order coefficient has to be 1, and the sum of all the coefficients in switch_coeff has to be 0. 
    """
    alpha = NA*EC**2/(4*np.pi*VEP)
    gamma = VEP*kB*temperature/(2.0*NA*salt_conc*EC**2)
    # use a distance-dependent relative permittivity (dielectric)
    dielectric_water = 78.4
    A = -8.5525
    kappa = 7.7839
    B = dielectric_water - A
    zeta = 0.03627
    alpha_value = alpha.value_in_unit(unit.kilojoule_per_mole*unit.nanometer)
    cutoff1_value = cutoff1.value_in_unit(unit.nanometer)
    cutoff2_value = cutoff2.value_in_unit(unit.nanometer)
    gamma_value = gamma.value_in_unit(unit.nanometer**2)
    assert switch_coeff[0] == 1
    assert np.sum(np.array(switch_coeff)) == 0
    switch_term_list = []
    for i in range(len(switch_coeff)):
        if i == 0:
            switch_term_list.append(f'{switch_coeff[i]}')
        else:
            switch_term_list.append(f'({switch_coeff[i]}*((r-{cutoff1_value})/({cutoff2_value}-{cutoff1_value}))^{i})')
    switch_term_string = '+'.join(switch_term_list)
    elec = mm.CustomNonbondedForce(f'''energy;
           energy=q1*q2*{alpha_value}*exp(-r/ldby)*switch/(dielectric*r);
           switch=({switch_term_string})*step(r-{cutoff1_value})*step({cutoff2_value}-r)+step({cutoff1_value}-r);
           ldby=(dielectric*{gamma_value})^0.5;
           dielectric={A}+{B}/(1+{kappa}*exp(-{zeta}*{B}*r));
           ''')
    elec.addPerParticleParameter('q')
    for q in charges:
        elec.addParticle([q])
    for i, row in df_exclusions.iterrows():
        elec.addExclusion(int(row['a1']), int(row['a2']))
    if use_pbc:
        elec.setNonbondedMethod(elec.CutoffPeriodic)
    else:
        elec.setNonbondedMethod(elec.CutoffNonPeriodic)
    elec.setCutoffDistance(cutoff2)
    elec.setForceGroup(force_group)
    return elec


def dh_elec_term(charges, df_exclusions, use_pbc, ldby=1*unit.nanometer, dielectric_water=80.0, 
                 cutoff=3.5*unit.nanometer, force_group=3):
    """
    Debye-Huckel potential with a constant dielectric. 
    
    Parameters
    ----------
    charges : sequence-like
        Atom charges. 
    
    df_exclusions : pd.DataFrame
        Nonbonded exclusions. 
    
    use_pbc : bool
        Whether to use PBC. 
    
    ldby : Quantity
        Debye length. 
    
    dielectric_water : float or int
        Water dielectric constant. 
    
    cutoff : Quantity
        Cutoff distance. 
    
    force_group : int
        Force group. 
    
    returns
    -------
    elec : Force
        Electrostatic interaction force. 
    
    """
    alpha = NA*EC**2/(4*np.pi*VEP)
    ldby_value = ldby.value_in_unit(unit.nanometer)
    alpha_value = alpha.value_in_unit(unit.kilojoule_per_mole*unit.nanometer)
    cutoff_value = cutoff.value_in_unit(unit.nanometer)
    elec = mm.CustomNonbondedForce(f'''energy;
           energy=q1*q2*{alpha_value}*((exp(-r/{ldby_value})/r)-offset)*step({cutoff_value}-r)/{dielectric_water};
           offset={math.exp(-cutoff_value/ldby_value)/cutoff_value};
           ''')
    elec.addPerParticleParameter('q')
    for q in charges:
        elec.addParticle([q])
    for i, row in df_exclusions.iterrows():
        elec.addExclusion(int(row['a1']), int(row['a2']))
    if use_pbc:
        elec.setNonbondedMethod(elec.CutoffPeriodic)
    else:
        elec.setNonbondedMethod(elec.CutoffNonPeriodic)
    elec.setCutoffDistance(cutoff)
    elec.setForceGroup(force_group)
    return elec


def wang_frenkel_term(atom_types, df_exclusions, use_pbc, epsilon_wf_map, sigma_wf_map, mu_wf_map, nu_wf_map=1, 
                      cutoff_to_sigma_ratio=3, force_group=3):
    """
    Wang-Fenkel potential term. 
    
    Parameters
    ----------
    atom_types : sequence-like
        Atom types. 
    
    df_exclusions : pd.DataFrame
        Nonbonded exclusions. 
    
    use_pbc : bool
        Whether to use PBC. 
    
    epsilon_wf_map : 2d sequence-like
        Matrix of epsilon parameter. 
    
    sigma_wf_map : 2d sequence-like
        Matrix of sigma parameter. 
    
    mu_wf_map : 2d sequence-like
        Matrix of mu parameter. 
    
    nu_wf_map : float or int or 2d sequence-like
        Matrix of nu parameter. 
        If this variable is float or int, then it means all the pairs have the same nu value. 
    
    cutoff_to_sigma_ratio : float or int
        The ratio of cutoff to sigma. 
    
    """
    contacts = mm.CustomNonbondedForce(f'''energy;
               energy=epsilon_wf*alpha_wf*g1*g2*step({cutoff_to_sigma_ratio}*sigma_wf-r);
               g1=(sigma_wf/r)^(2*mu_wf)-1;
               g2=(({cutoff_to_sigma_ratio}*sigma_wf/r)^(2*mu_wf)-1)^(2*nu_wf);
               alpha_wf=2*nu_wf*f1*((f2/(2*nu_wf*(f1-1)))^f2);
               f1={cutoff_to_sigma_ratio}^(2*mu_wf);
               f2=2*nu_wf+1;
               epsilon_wf=epsilon_wf_map(atom_type1, atom_type2);
               sigma_wf=sigma_wf_map(atom_type1, atom_type2);
               mu_wf=mu_wf_map(atom_type1, atom_type2);
               nu_wf=nu_wf_map(atom_type1, atom_type2);
               ''')
    n_atom_types = epsilon_wf_map.shape[0]
    discrete_2d_epsilon_wf_map = mm.Discrete2DFunction(n_atom_types, n_atom_types, epsilon_wf_map.ravel().tolist())
    discrete_2d_sigma_wf_map = mm.Discrete2DFunction(n_atom_types, n_atom_types, sigma_wf_map.ravel().tolist())
    discrete_2d_mu_wf_map = mm.Discrete2DFunction(n_atom_types, n_atom_types, mu_wf_map.ravel().tolist())
    if (isinstance(nu_wf_map, int)) or (isinstance(nu_wf_map, float)):
        nu_wf_map = np.full((n_atom_types, n_atom_types), nu_wf_map)
    discrete_2d_nu_wf_map = mm.Discrete2DFunction(n_atom_types, n_atom_types, nu_wf_map.ravel().tolist())
    contacts.addTabulatedFunction('epsilon_wf_map', discrete_2d_epsilon_wf_map)
    contacts.addTabulatedFunction('sigma_wf_map', discrete_2d_sigma_wf_map)
    contacts.addTabulatedFunction('mu_wf_map', discrete_2d_mu_wf_map)
    contacts.addTabulatedFunction('nu_wf_map', discrete_2d_nu_wf_map)
    contacts.addPerParticleParameter('atom_type')
    for each in atom_types:
        contacts.addParticle([each])
    for i, row in df_exclusions.iterrows():
        contacts.addExclusion(int(row['a1']), int(row['a2']))
    if use_pbc:
        contacts.setNonbondedMethod(contacts.CutoffPeriodic)
    else:
        contacts.setNonbondedMethod(contacts.CutoffNonPeriodic)
    contacts.setCutoffDistance(cutoff_to_sigma_ratio*np.amax(sigma_wf_map))
    contacts.setForceGroup(force_group)
    return contacts
    


