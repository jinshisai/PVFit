from channelfit import ChannelFit

'-------- INPUTS --------'
cubefits = './channelfit/IRAS16253_SBLB_C18O_robust_2.0.imsub.fits'
center = '16h28m21.61526785s -24d36m24.32538414s'
pa = 113 - 180  # deg
incl = 65  # deg
vsys = 4  # km/s
dist = 139  # pc
sigma = 2e-3  # Jy/beam; None means automatic calculation.
rmax = 1 * dist  # au
vlim = (-2.7, -1.0, 1.0, 2.7)  # km/s; from vsys
'------------------------'


'-------- HOW TO DO EACH STEP --------'
if __name__ == '__main__':
    filehead = cubefits.replace('.fits', '')
    chan = ChannelFit(scaling='mom0ft', progressbar=True)
    chan.makegrid(cubefits=cubefits, center=center, pa=pa, incl=incl,
                  vsys=vsys, dist=dist, sigma=sigma, rmax=rmax, vlim=vlim,
                  skipto=5)
    chan.fitting(Mstar_range=[0.01, 1.0],
                 Rc_range=[3, 300],
                 fixed_params={'cs': 0.4, 'h1': 0, 'h2': -1, 'Rin': 0,
                               'pI': 0, 'Ienv': 0,
                               'xoff': 0, 'yoff': 0, 'voff': 0, 'incl': 0},
                 kwargs_emcee_corner={'nwalkers_per_ndim': 2,
                                      'nburnin': 100,
                                      'nsteps': 300,
                                      'rangelevel': 0.9},
                 filename=filehead)
    p = chan.popt
    chan.modeltofits(**p, filehead=filehead)
    for s in ['obs', 'model', 'residual']:
        chan.plotmom(mode=s, **p, filename=f'{filehead}.{s}mom01.png')
'-------------------------------------'