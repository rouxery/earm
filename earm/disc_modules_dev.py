""" Docstring for disc_modules_dev...
"""

from pysb import *
from pysb.util import alias_model_components
from earm.shared import *
from pysb.macros import equilibrate
import albeck_modules
import lopez_modules

assemble_olig_sequential = assemble_pore_sequential

def lig_to_bid_monomers():
     """Declare the monomers needed for the DISC modules
     """
     Monomer('Trail', ['b', 's1', 's2'])  # TRAIL monomer, start with pre-trimerized ligand
     Monomer('DR4', ['bl', 'bf', 's1', 's2']) # Death receptor 4 bl: ligand binding site, bf: fadd binding site
     Monomer('DR5', ['bl', 'bf', 's1', 's2']) # Death receptor 5 bl: ligand binding site, bf: fadd binding site
     Monomer('Fadd', ['bx', 'bc'])   # FADD bx: binding to complex, bc: binding to caspase 8
     Monomer('flip', ['bf']) # flip
     Monomer('C8', ['bf', 'state'], {'state':['pro', 'A']}) # pro-Caspase-8 monomer
     Monomer('C8dim', ['bf']) # active Caspase-8 dimer
     Monomer('BAR', ['bf']) # BAR
     Monomer('IETD', ['bi', 'bf', 'state'], {'state':['C', 'Y']}) # IETD subunit with YFP or CFP
     Monomer('CFP', ['bf', 'state'], {'state':['I', 'F']}) # truncated CFP, states: IETD, FREE
     Monomer('YFP', ['bf', 'state'], {'state':['I', 'F']}) # truncated CFP, states: IETD, FREE
   
def lig_to_bid_rates():
     """ The trail trimer-sdDR monomer binding rates were pulled from
     Reis + Cool 2011.  The trimer monomer rate was converted to the
     cellular volume. The Ttrimer-DRtrimer interaction was set to one
     order of magnitude lower than the Ttrimer-DRmonomer interaction
     and the Ttrimer-DRdimer interaction as set to a value halfway
     between the two. All other values were adapted from Albeck Plos
     2008.
     """
     Parameter('ttdr4mf', 3.8e-05)  # 6.3e5 M^-1 s^-1 in pL molecules^-1 s^-1
     Parameter('ttdr4mr', 1.10e-04)
     # TT binding to DR dimers- 4
     Parameter('ttdr4df', 2.09e-05)  
     Parameter('ttdr4dr', 1.10e-04)
     # TT binding to DR trimers- 4
     Parameter('ttdr4tf', 3.8e-06)
     Parameter('ttdr4tr', 1.10e-04)
     # TT binding to DR monomer- 5
     Parameter('ttdr5mf', 11.9e-05)  # 11.9e5 M^-1 s^-1 in pL molecules^-1 s^-1
     Parameter('ttdr5mr', 0.36e-04)
     # TT binding to DR dimers- 5
     Parameter('ttdr5df', 6.54e-05)  
     Parameter('ttdr5dr', 1.10e-04)
     # TT binding to DR trimers- 5
     Parameter('ttdr5tf', 11.9e-06)     
     Parameter('ttdr5tr', 0.36e-04)
     # DR4 trimerization
     Parameter('kdr4dimf',  2.040816e-04) # k / v**2
     Parameter('kdr4dimr',  1.0e-3      )
     Parameter('kdr4trimf', 2.040816e-04)
     Parameter('kdr4trimr', 1.0e-3      )
     # DR5 trimerization
     Parameter('kdr5dimf',  2.040816e-04) # k / v**2
     Parameter('kdr5dimr',  1.0e-3      )
     Parameter('kdr5trimf', 2.040816e-04)
     Parameter('kdr5trimr', 1.0e-3      )
     # Fadd LDR4C complex
     Parameter('faddldr4c1f', 1.0e-6)
     Parameter('faddldr4c1r', 1.0e-03)
     Parameter('faddldr4c2f', 1.0e-6)
     Parameter('faddldr4c2r', 1.0e-03)
     Parameter('faddldr4c3f', 1.0e-6)
     Parameter('faddldr4c3r', 1.0e-03)
     # Fadd LDR5C complex
     Parameter('faddldr5c1f', 1.0e-6)
     Parameter('faddldr5c1r', 1.0e-03)
     Parameter('faddldr5c2f', 1.0e-6)
     Parameter('faddldr5c2r', 1.0e-03)
     Parameter('faddldr5c3f', 1.0e-6)
     Parameter('faddldr5c3r', 1.0e-03)
     # pC8 FADD binding pC8_fadd_b
     Parameter('pc8faddf', 1.0e-6)
     Parameter('pc8faddr', 1.0e-03)
     # pC8 activation to C8 within the same FADD trimer
     Parameter('pc8dimacts', 1.0e-3)
     # pC8 activation to C8 across separate FADD trimers
     Parameter('pc8dimacto', 1.0e-3)
     # Bid cleavage by C8
     Parameter('kc8bidf', 1.0e-06)
     Parameter('kc8bidr', 1.0e-03)
     Parameter('kc8bidc', 1.0    )
     # IETDC cleavage by C8
     Parameter('kc8IETDYf', 1.0e-06)
     Parameter('kc8IETDYr', 1.0e-03)
     Parameter('kc8IETDYc', 1.0    )
     # IETDY cleavage by C8
     Parameter('kc8IETDCf', 1.0e-06)
     Parameter('kc8IETDCr', 1.0e-03)
     Parameter('kc8IETDCc', 1.0    )
     # CFP-IETD cleavage by C8
     Parameter('kc8CFPf', 1.0e-06)
     Parameter('kc8CFPr', 1.0e-03)
     Parameter('kc8CFPc', 1.0    )
     # YFP-IETD cleavage by C8
     Parameter('kc8YFPf', 1.0e-06)
     Parameter('kc8YFPr', 1.0e-03)
     Parameter('kc8YFPc', 1.0    )
     # DISC inhibition by FLIP
     Parameter('kflipdiscf', 1.0e-06)
     Parameter('kflipdiscr', 1.0e-03)
     # C8 inhibition by BAR
     Parameter('kbarc8f', 1.0e-06)
     Parameter('kbarc8r', 1.0e-03)

def declare_initial_conditions():
     Parameter('Trail_0'  ,   3e3) #* Ligand correspond to 50 ng/ml SuperKiller TRAIL
     Parameter('DR4_0'    ,   3e3) #* death receptor 4, JRoux
     Parameter('DR5_0'    ,  26e3) #* death receptor 5, JRoux
     Parameter('Fadd_0'   , 180e3) #* Fadd
     Parameter('flip_0'   ,  14e3) #* Flip
     Parameter('C8_0'     , 151e3) #* procaspase-8 
     Parameter('BAR_0'    , 1.0e3) #  Bifunctional apoptosis regulator
     Parameter('IETD_0'     ,4.72e6) # IC-RP initial

     alias_model_components()
     Bid_0.value = 2.24e6 #* NEW Bid values from JR

     Initial((Trail(b=None, s1=1, s2=2) % Trail(b=None, s1=2, s2=3) % Trail(b=None, s1=3, s2=1)), Trail_0)
     Initial(DR4(bl=None, bf=None, s1=None, s2=None), DR4_0)
     Initial(DR5(bl=None, bf=None, s1=None, s2=None), DR5_0)
     Initial(Fadd(bx=None, bc=None), Fadd_0)
     Initial(flip(bf=None), flip_0)
     Initial(C8(bf=None, state='pro'), C8_0)
     Initial(BAR(bf=None), BAR_0)
     Initial(IETD(bi=1, bf=None, state='C')%IETD(bi=1, bf=None, state='Y'), IETD_0)
     

def lig_to_bid():
     """Defines the interactions from the initial ligand cue (e.g. TRAIL) to Bid
     activation. This is an update to albeck's earm_1_0
    This function depends specifically
    This function uses TRAIL, DR4, DR5, Fadd, flip, C8, BAR, and Bid monomers and their
    associated parameters to generate the rules that describe Ligand
    to Receptor binding, DISC formation, Caspase8 activation and
    inhibition by flip and BAR.
    Due to the complexity of the species this function makes extensive use of aliasing.
    """
     alias_model_components()

     # Trail binding to DR
     # aliases for TRAIL
     # -----------------
     # Trimerized Trail unbound/bound aliases
     TTrail_U  = MatchOnce(Trail(b=None, s1=1, s2=2) % Trail(b=None, s1=2, s2=3) % Trail(b=None, s1=3, s2=1))
     TTrail_B1 = MatchOnce(Trail(b=4,    s1=1, s2=2) % Trail(b=None, s1=2, s2=3) % Trail(b=None, s1=3, s2=1))
     TTrail_B2 = MatchOnce(Trail(b=5,    s1=1, s2=2) % Trail(b=6,    s1=2, s2=3) % Trail(b=None, s1=3, s2=1)) 
     TTrail_B3 = MatchOnce(Trail(b=4,    s1=1, s2=2) % Trail(b=5,    s1=2, s2=3) % Trail(b=6,    s1=3, s2=1))
     TTrail_B3N = Trail(b=4,    s1=1, s2=2) % Trail(b=5,    s1=2, s2=3) % Trail(b=6,    s1=3, s2=1)

     # DR monomer, dimer, trimer aliases:
     # ----------------------------------
     # unbound oligomers
     DR4_mono_U = DR4(bl=None, bf=None, s1=None,  s2=None)
     DR4_dim_U  = DR4(bl=None, bf=None, s1=1,     s2=None)    % DR4(bl=None, bf=None, s1=None, s2=1)
     DR4_trim_U = MatchOnce(DR4(bl=None, bf=None, s1=1, s2=2) % DR4(bl=None, bf=None, s1=2,    s2=3) % DR4(bl=None, bf=None, s1=3, s2=1))
     DR5_mono_U = DR5(bl=None, bf=None, s1=None, s2=None)
     DR5_dim_U  = DR5(bl=None, bf=None, s1=1,    s2=None)     % DR5(bl=None, bf=None, s1=None, s2=1)
     DR5_trim_U = MatchOnce(DR5(bl=None, bf=None, s1=1, s2=2) % DR5(bl=None, bf=None, s1=2,    s2=3) % DR5(bl=None, bf=None, s1=3, s2=1))

     # bound oligomers
     DR4_mono_B = DR4(bl=4,    bf=None, s1=None, s2=None)
     DR4_dim_B  = MatchOnce(DR4(bl=5,    bf=None, s1=4, s2=None) % DR4(bl=6, bf=None, s1=None, s2=4))
     DR4_trim_B = MatchOnce(DR4(bl=4,    bf=None, s1=7, s2=8   ) % DR4(bl=5, bf=None, s1=8,    s2=9) % DR4(bl=6, bf=None, s1=9, s2=7))
     DR5_mono_B = DR5(bl=4,    bf=None, s1=None, s2=None)
     DR5_dim_B  = MatchOnce(DR5(bl=5,    bf=None, s1=4, s2=None) % DR5(bl=6, bf=None, s1=None, s2=4))
     DR5_trim_B = MatchOnce(DR5(bl=4,    bf=None, s1=7, s2=8   ) % DR5(bl=5, bf=None, s1=8,    s2=9) % DR5(bl=6, bf=None, s1=9, s2=7))

     # bound and FADD
     DR4_trim_BN =  DR4(bl=4, bf=None, s1=7, s2=8) % DR4(bl=5, bf=None, s1=8, s2=9) % DR4(bl=6, bf=None, s1=9, s2=7)
     DR4_trim_BB1 = DR4(bl=4,   bf=10, s1=7, s2=8) % DR4(bl=5, bf=None, s1=8, s2=9) % DR4(bl=6, bf=None, s1=9, s2=7)
     DR4_trim_BB2 = DR4(bl=4,   bf=10, s1=7, s2=8) % DR4(bl=5, bf=11,   s1=8, s2=9) % DR4(bl=6, bf=None, s1=9, s2=7)
     DR4_trim_BB3 = DR4(bl=4,   bf=10, s1=7, s2=8) % DR4(bl=5, bf=11,   s1=8, s2=9) % DR4(bl=6, bf=12,   s1=9, s2=7)
     DR5_trim_BN =  DR5(bl=4, bf=None, s1=7, s2=8) % DR5(bl=5, bf=None, s1=8, s2=9) % DR5(bl=6, bf=None, s1=9, s2=7)
     DR5_trim_BB1 = DR5(bl=4,   bf=10, s1=7, s2=8) % DR5(bl=5, bf=None, s1=8, s2=9) % DR5(bl=6, bf=None, s1=9, s2=7)
     DR5_trim_BB2 = DR5(bl=4,   bf=10, s1=7, s2=8) % DR5(bl=5, bf=11,   s1=8, s2=9) % DR5(bl=6, bf=None, s1=9, s2=7)
     DR5_trim_BB3 = DR5(bl=4,   bf=10, s1=7, s2=8) % DR5(bl=5, bf=11,   s1=8, s2=9) % DR5(bl=6, bf=12,   s1=9, s2=7)

     # DR multimers
     # ------------
     olig_max_size = 3
     olig_rates = [[2.040816e-04,  # 1.0e-6/v**2
                    1e-3]] * (olig_max_size - 1)
     assemble_olig_sequential(DR4(bl = None, bf=None), olig_max_size, olig_rates)
     assemble_olig_sequential(DR5(bl = None, bf=None), olig_max_size, olig_rates)

     # Trail binding to DR rules:
     # --------------------------
     # Paper Carlos R. Reis, Robbert H. Cool rates 2011
     # FIXME: can we replace these with a bind table? or a simple bind call?
     Rule('TRAIL_DR4mono', TTrail_U + DR4_mono_U <> TTrail_B1 % DR4_mono_B, ttdr4mf, ttdr4mr)
     Rule('TRAIL_DR4dim',  TTrail_U + DR4_dim_U  <> TTrail_B2 % DR4_dim_B,  ttdr4df, ttdr4dr)
     Rule('TRAIL_DR4trim', TTrail_U + DR4_trim_U <> TTrail_B3 % DR4_trim_B, ttdr4tf, ttdr4tr)
     Rule('TRAIL_DR5mono', TTrail_U + DR5_mono_U <> TTrail_B1 % DR5_mono_B, ttdr5mf, ttdr5mr)
     Rule('TRAIL_DR5dim',  TTrail_U + DR5_dim_U  <> TTrail_B2 % DR5_dim_B,  ttdr5df, ttdr5dr)
     Rule('TRAIL_DR5trim', TTrail_U + DR5_trim_U <> TTrail_B3 % DR5_trim_B, ttdr5tf, ttdr5tr)

     # Ligand Death-receptor complex: 
     # ------------------------------
     LDR4C =    TTrail_B3N % DR4_trim_BN
     LDR4C_B1 = TTrail_B3N % DR4_trim_BB1
     LDR4C_B2 = TTrail_B3N % DR4_trim_BB2
     LDR4C_B3 = TTrail_B3N % DR4_trim_BB3
     LDR5C =    TTrail_B3N % DR5_trim_BN
     LDR5C_B1 = TTrail_B3N % DR5_trim_BB1
     LDR5C_B2 = TTrail_B3N % DR5_trim_BB2
     LDR5C_B3 = TTrail_B3N % DR5_trim_BB3
     
     # FIXME: Can these all be replaced with simple-bind calls?
     # Fadd binding LDRC rule
     # -------------------------------------------------------
     Rule("Fadd_LDR4C_cplx1", LDR4C + Fadd(bx = None, bc=None) <> LDR4C_B1 % Fadd(bx=10, bc=None), faddldr4c1f, faddldr4c1r)
     Rule("Fadd_LDR4C_cplx2", LDR4C_B1 % Fadd(bx=10, bc=None) + Fadd(bx = None, bc=None) <>
                              LDR4C_B2 % Fadd(bx=10, bc=None) % Fadd(bx=11, bc=None), faddldr4c2f, faddldr4c2r)
     Rule("Fadd_LDR4C_cplx3", LDR4C_B2 % Fadd(bx=10, bc=None) % Fadd(bx=11, bc=None) + Fadd(bx = None, bc=None) <>
                              LDR4C_B3 % Fadd(bx=10, bc=None) % Fadd(bx=11, bc=None) % Fadd(bx=12, bc=None), faddldr4c3f, faddldr4c3r)
     Rule("Fadd_LDR5C_cplx1", LDR5C + Fadd(bx = None, bc=None) <> LDR5C_B1 % Fadd(bx=10, bc=None), faddldr5c1f, faddldr5c1r)
     Rule("Fadd_LDR5C_cplx2", LDR5C_B1 % Fadd(bx=10, bc=None) + Fadd(bx = None, bc=None) <>
                              LDR5C_B2 % Fadd(bx=10, bc=None) % Fadd(bx=11, bc=None), faddldr5c2f, faddldr5c2f)
     Rule("Fadd_LDR5C_cplx3", LDR5C_B2 % Fadd(bx=10, bc=None) % Fadd(bx=11, bc=None) + Fadd(bx = None, bc=None) <>
                              LDR5C_B3 % Fadd(bx=10, bc=None) % Fadd(bx=11, bc=None) % Fadd(bx=12, bc=None), faddldr5c3f, faddldr5c3f)

     # Caspase 8 binding to Fadd, creates DISC
     # ---------------------------------------
     Rule("C8_fadd_b", Fadd(bc=None, bx=ANY) + C8(bf=None, state='pro') <> Fadd(bc=1, bx=ANY) % C8(bf=1, state='pro'), pc8faddf, pc8faddr)

     # Caspase 8 activation within the same DISC
     # -----------------------------------------------------------------
     Rule("C8_dim_act_s", C8(bf=ANY, state='pro') % C8(bf=ANY, state='pro') >> C8dim(bf=None), pc8dimacts)

     # Truncation of Bid
     # FIXME: use catalysis function here
     # ----------------------------------
     Rule("C8_bid_cplx", C8dim(bf=None) + Bid(bf = None, state='U') <>
          C8dim(bf=1) % Bid(bf = 1, state='U'), kc8bidf, kc8bidr)
     Rule("C8_cplx_act", C8dim(bf=1) % Bid(bf = 1, state='U') >>
          C8dim(bf=None) + Bid(bf = None, state='T'), kc8bidc)
     
     # truncation of IC-RP by Bid
     # ICRP is composed of CYP-IETD-IETD-YFP but truncation at any IETD should yield signal
     # allow C8 to bind to IC-RP at any of two sites and truncate
     Rule("IETDC_C8_cplx", IETD(bi=1, bf=None, state='C')%IETD(bi=1, bf=None, state='Y') + C8dim(bf=None) <>
          IETD(bi=1, bf=None, state='C')%IETD(bi=1, bf=2, state='Y') % C8dim(bf=2), kc8IETDCf, kc8IETDCr)
     Rule("IETDC_C8_diss",IETD(bi=1, bf=None, state='C')%IETD(bi=1, bf=2, state='Y') % C8dim(bf=2) >>
          CFP(bf=None, state='I') + YFP(bf=None, state='F') + C8dim(bf=None), kc8IETDCc)

     Rule("IETDY_C8_cplx", IETD(bi=1, bf=None, state='C')%IETD(bi=1, bf=None, state='Y') + C8dim(bf=None) <>
          IETD(bi=1, bf=2, state='C')%IETD(bi=1, bf=None, state='Y') % C8dim(bf=2), kc8IETDYf, kc8IETDYr)
     Rule("IETDY_C8_diss",IETD(bi=1, bf=2)%IETD(bi=1, bf=None) % C8dim(bf=2) >>
          CFP(bf=None, state='F') + YFP(bf=None, state='I') + C8dim(bf=None), kc8IETDYc)

     # Now process the remaining CFP:IETD complexes, expressed here as a state change
     Rule("CFPI_C8_cplx", CFP(bf=None, state='I') + C8dim(bf=None) <>
          CFP(bf=1, state='I') % C8dim(bf=1), kc8CFPf, kc8CFPr)
     Rule("CFPI_C8_diss", CFP(bf=1, state='I') % C8dim(bf=1) >>
          CFP(bf=None, state='F') + C8dim(bf=None), kc8CFPc)
     
     Rule("YFPI_C8_cplx", YFP(bf=None, state='I') + C8dim(bf=None) <>
          YFP(bf=1, state='I') % C8dim(bf=1), kc8YFPf, kc8YFPr)
     Rule("YFPI_C8_diss", YFP(bf=1, state='I') % C8dim(bf=1) >>
          YFP(bf=None, state='F') + C8dim(bf=None), kc8YFPc)

     # flip takes a C8 spot in DISC
     # ----------------------------
     # FIXME: THIS SHOULD NOT GENERATE Fadd:flip where fadd is not bound to a complex...?
     Rule("flip_fadd_cplx", Fadd(bx=1, bc=None) + flip(bf=None) <>  Fadd(bx=1, bc=2) % flip(bf=2), kflipdiscf, kflipdiscr)

     # BAR inhibits C8
     # ---------------
     Rule("BAR_C8_cplx", C8dim(bf=None) + BAR(bf = None) <>
          C8dim(bf=1) % BAR(bf=1), kbarc8f, kbarc8r)
