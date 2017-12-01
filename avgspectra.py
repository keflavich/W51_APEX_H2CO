import numpy as np
import os
import glob
import pyspeckit
from astropy import units as u
from spectral_cube import SpectralCube

import pylab as pl
pl.close('all')


line_to_image_list = [
    ('H2CO303_202', "218.22219GHz",0.5, 0),
    ('H2CO321_220', "218.76007GHz",1.2, 1),
    ('H2CO322_221', "218.47564GHz",0.5, 0),
    ('12CO2-1', "230.538GHz",1.2, 2),
    ('HC3N24-23', "218.32471GHz",1.2, 1),
    #('HC3Nv7=124-23', "219.17358GHz",1.2, 1),
    #('HC3Nv7=1_24-23','218.86063GHz',1.2, 1),
    #('HC3Nv7=2_24-23','219.67465GHz',1.2, 1), # different velocities from CDMS, SLAIM
    ('OCS18-17', "218.90336GHz",1.2, 1),
    ('OCS19-18', "231.06099GHz",1.2, 2),
    ('SO65-54', "219.94944GHz",1.2, 1),
    ('c-HCCCH616-505', "217.82217GHz", 1.2, -1),
    ('c-HCCCH514-423', "217.94004GHz", 1.2, -1),
    #('HNCO10110-919', "218.98102GHz",1.2, 1),
    #('HNCO1028-927', "219.73719GHz",1.2, 1),
    #('HNCO10010-909','219.79828GHz',1.2, 1),
    #('HNCO1055-954', '219.39241GHz',1.2, 1),# E_U = 1000 K (maybe exclude?)
    #('HNCO1046-945', '219.54708GHz',1.2, 1),
    #('HNCO1038-937', '219.65677GHz',1.2, 1),
    #('HNCO28128-29029', '231.873255GHz',1.2, 2),
    #('HNCO1019-918', "220.58476GHz",-1, -1),
    #('HNCO1046-945', "219.54711GHz",-1, -1),
    #('HNCO1038-937', "219.6568GHz",-1, -1),
    ('CH3OH422-312', "218.44005GHz",0.5, 0),
    ('CH3OH423-514', "234.68345GHz",1.2, 3), # LB
    ('CH3OH5m42-6m34', "234.69847GHz",1.2, 3),
    #('CH3OH5m42-6m43', "234.69847GHz",1.2, 3), # this one is a typo
    ('CH3OH808-716', "220.07849GHz",1.2, 1),
    ('CH3OH1029-936','231.28115GHz',1.2, 2),
    ('CH3OH18315-17414','233.79580GHz',1.2, 3),
    ('CH3OH25322-24420','219.98399GHz',1.2, 1),
    ('CH3OH23519-22617','219.99394GHz',1.2, 1),
    #('13CH3OH515-414','234.01158GHz',1.2,3),
    ('CH3OH_10m38-11m210', '232.94583GHz', -1, -1),
    ('CH3OH_18316-17413', '232.78359GHz', -1, -1),
    ('CH3OH_514-422', '216.94556GHz', -1, -1),
    ('CH3OH_3m22-220', '221.29447GHz', -1, -1),
    ('CH3OH_10m55-11m48', '220.40137GHz', -1, -1),
    ('13CS5-4', "231.22069GHz",1.2, 2),
    #('PN5-4', "234.93569GHz",1.2, 3),
    #('NH2CHO11210-1029', "232.27363GHz",1.2, 2),
    #('NH2CHO1156-1055', "233.59451GHz",1.2, 3),
    ('H30alpha', "231.90093GHz", 1.2, 2),
    ('C18O2-1', "219.56036GHz", 1.2, 1),
    #('H2CCO11-10', "220.17742GHz", 1.2, 1),
    #('HCOOH431-524', "219.09858GHz", 1.2, 1),
    #('CH3OCHO17314-16313E','218.28083GHz',0.5, 0), # this doublet is really pretty; the lines are near identical
    #('CH3OCHO17314-16313A','218.29787GHz',0.5, 0),
    #('CH3OCHO17413-16412A','220.19027GHz',1.2, 1),
    #('CH3OCHO1249-1138E','231.01908GHz',1.2, 2),
    #('CH3CH2CN24321-23320','218.39002GHz',0.5, 0),
    #('CH3CH2CN24222-23221','219.50559GHz',1.2, 1),
    #('Acetone21120-20219AE','219.21993GHz',1.2, 1),
    #('Acetone21120-20119EE','219.24214GHz',1.2, 1),
    #('Acetone871-744AE', '218.24017GHz',0.5,0), # EU=32 K, but low intensity
    #('Acetone1294-1183EE', '218.63385GHz',1.2,1),
    #('Acetone12112-11101AE', '234.86136GHz',1.2,3),
    #('H213CO312-211','219.90849GHz',1.2, 1),
    #('CH3CH2OH550-541','231.02517GHz',1.2, 2),
    #('O13CS18-17','218.19898GHz',0.5, 0),
    #('CH3OCH323321-23222AA','218.49441GHz',0.5, 0),
    #('CH3OCH313013-12112AA','231.98772GHz',1.2, 2),
    #('CH3OCH323321-23222EE','218.49192GHz',0.5, 0),
    ('N2D+_3-2', '231.32183GHz', 1.2, 2),
    #('13CH3CN_138-138', '231.95537GHz', 1.2, 2),
    #('13CH3CN_137-137', '232.02061GHz', 1.2, 2),
    #('13CH3CN_136-136', '232.07720GHz', 1.2, 2),
    #('13CH3CN_135-135', '232.12512GHz', 1.2, 2),
    #('13CH3CN_134-134', '232.16436GHz', 1.2, 2),
    #('13CH3CN_133-133', '232.19489GHz', 1.2, 2),
    #('13CH3CN_132-132', '232.21671GHz', 1.2, 2),
    #('13CH3CN_131-131', '232.22980GHz', 1.2, 2),
    #('13CH3CN_130-130', '232.23419GHz', 1.2, 2),
    # longbaseline only
    ('13CO2-1', "220.39868GHz", -1, -1),
    ('CH3CNv8=1_123-113l-1', "221.33822GHz",-1, -1),
    ('CH3CNv8=1_124-114l-1', "221.29988GHz",-1, -1),
    ('CH3CNv8=1_123-113l+1', "221.40351GHz",-1, -1),
    ('CH3CNv8=1_122-112l-1', "221.36767GHz",-1, -1),
    ('CH3CNv8=1_125-115l+1', "221.35029GHz",-1, -1),
    ('CH3CNv8=1_126-116l+1', "221.31186GHz",-1, -1),
    ('CH3CNv8=1_127-117l+1', "221.26513GHz",-1, -1),
    ('CH3CNv8=1_125-115l-1', "221.25235GHz",-1, -1),
    #('NH2CHO1138-1037', "234.31548GHz", -1, -1),
    #('NH2CHO1037-11110', "220.53838GHz", -1, -1),
    #('NH2CHO12012-11111', "221.31264GHz", -1, -1),
    #('NH2CHO1019-918', "218.45965GHz", -1, -1),
    ('CH3CN_128-118', '220.47582GHz', -1, -1),
    ('CH3CN_127-117', '220.53933GHz', -1, -1),
    ('CH3CN_126-116', '220.59443GHz', -1, -1),
    ('CH3CN_125-115', '220.64109GHz', -1, -1),
    ('CH3CN_124-114', '220.67929GHz', -1, -1),
    ('CH3CN_123-113', '220.70902GHz', -1, -1),
    ('CH3CN_122-112', '220.73026GHz', -1, -1),
    #('CH3OCHO_955-844E', '234.47941GHz', -1, -1), probably not real
    #('CH3OCHO_954-845E', '235.088GHz', -1, -1),
    #('CH3OCHO_991-982E', '235.19268GHz', -1, -1), probably not real
    #('CH3OCHO_990-981E', '235.2157GHz', -1, -1),
    #('CH3OCHO_991-982A', '235.26332GHz', -1, -1),
    ('SO2_422-313', '235.1517GHz', -1, -1),
    ('SO2_28325-28226', '234.18705GHz', -1, -1),
    ('SO2_16610-17513', '234.42157GHz', -1, -1),
    #('CH3OCHO_1138-1029E', '235.31514GHz', -1, -1), probably not real
    #('CH3OCHO_1138-1029A', '235.37525GHz', -1, -1), probably not real
    #('CH3OCH31394-1486EE','231.89851GHz',-1,-1,), probably not real (on top of H30a)
    #('g-CH3CH2OH_13211-12210', '230.67255GHz', 1.2, 2),
    #('g-CH3CH2OH_651-541', '230.79351GHz', 1.2, 2),
    #('t-CH3CH2OH_16511-16412', '230.95379GHz', 1.2, 2),
    #('t-CH3CH2OH_14014-13113', '230.99138GHz', 1.2, 2),
    #('SO2_22715-23618', '219.27594GHz', 1.2, 1),
    #('SO2_16610-17513', '234.42159GHz', 1.2, 3),
    #('SO2v2=1_20218-19317', '218.99583GHz', 1.2, 1),
    #('SO2v2=1_22220-22121', '219.46555GHz', 1.2, 1),
    #('SO2v2=1_16313-16214', '220.16524GHz', 1.2, 1),
    #('SO2v2=1_642-735', '232.21031GHz', 1.2, 2),
    #('CH3NCO_25223-24222', '217.15093GHz', -1, -1),
    #('CH3NCO_2500-2400', '217.59517GHz', -1, -1),
    #('CH3NCO_2520-2420', '217.65209GHz', -1, -1),
    #('CH3NCO_25124-24123', '218.54180GHz', 0.5, 0),
    #('CH3NCO_27226-26225', '234.08812GHz', 1.2, 3),
    #('CH3SH_130-121', '217.458GHz', -1, -1),
    #('CH3SH_152-151', '234.19145GHz', 1.2, 3),
    #('CH3SH_162-161', '231.75891GHz', 1.2, 2),
    #('CH3SH_73-82', '230.64608GHz', 1.2, 2),
    #('CH3SH_232-231', '218.18612GHz', 0.5, 0),
    ('SiO_5-4', '217.10498GHz', -1, -1),

]

velo = 60*u.km/u.s

species_names = [x[0] for x in line_to_image_list]
frequencies = u.Quantity([float(x[1].strip("GHz")) for x in line_to_image_list],
                         unit=u.GHz)

for fn in glob.glob("*merge.fits"):
    outf = 'avspec/avg_{0}'.format(fn)
    if not os.path.exists(outf):
        cube = SpectralCube.read(fn)
        cube.allow_huge_operations=True
        mad = cube.mad_std(axis=0)
        sum = (cube*mad).sum(axis=(1,2))
        mean = sum/np.nansum(mad)
        mean.write('avspec/weighted_avg_{0}'.format(fn), overwrite=True)
        mn = cube.mean(axis=(1,2))
        mn.write(outf, overwrite=True)

for fn in glob.glob("*merge.fits"):
    spw = pyspeckit.Spectrum('avspec/weighted_avg_{0}'.format(fn))
    sp = pyspeckit.Spectrum('avspec/avg_{0}'.format(fn))
    sp.plotter()
    #spw.plotter(axis=sp.plotter.axis, clear=False, color='b')
    sp.plotter.savefig('avspec/avg_{0}'.format(fn.replace(".fits",".png")))
    med = np.median(sp.data)
    sp.plotter.axis.set_ylim(med-0.1, med+0.2)
    sp.plotter.savefig('avspec/avg_yzoom_{0}'.format(fn.replace(".fits",".png")))


    plot_kwargs = {'color':'r', 'linestyle':'--'}
    annotate_kwargs = {'color': 'r'}
    sp.plotter.line_ids(species_names, u.Quantity(frequencies),
                        velocity_offset=velo, plot_kwargs=plot_kwargs,
                        annotate_kwargs=annotate_kwargs)

    sp.plotter.savefig('avspec/lineid_avg_{0}'.format(fn.replace(".fits",".png")))
