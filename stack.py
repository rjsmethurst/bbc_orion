import numpy as N
import pylab as P
import matplotlib.image as plt
from scipy.misc import imsave

from glob import glob

from astrometry.util.util import *
from astrometry.util.resample import *
from astrometry.net.enhance import *

ra, dec = 83, 2
pixscale = 1./50.
W, H, B  = 1200, 900, 3
targetwcs = Tan(ra, dec, W/2.+0.5, H/2.+0.5, -pixscale, 0., 0., pixscale, float(W), float(H))

enhance = EnhanceImage(W*H, 3, random=True)
P.ion()
print 'construction', N.shape(enhance.enhI)

#wcsfns = ['/Users/becky/Videos/orion/orion_flickr_doug_german_budget_astro.wcs.fits', '/Users/becky/Videos/orion/orion_belt_flickr_jonathon_howell.wcs.fits']
#imgfns = ['/Users/becky/Videos/orion/orion_flickr_doug_german_budget_astro.jpg', '/Users/becky/Videos/orion/orion_belt_flickr_jonathon_howell.jpg']  
#wcsfns = ['/Users/becky/Videos/orion/dotnet/orion_belt_m42_callum_hayton.wcs.fits',  '/Users/becky/Videos/orion/dotnet/orion_flickr.wcs.fits', '/Users/becky/Videos/orion/dotnet/orion_flickr_doug_german_budget_astro_astrometry.wcs.fits']
#imgfns = ['/Users/becky/Videos/orion/dotnet/orion_belt_m42_callum_hayton.jpg', '/Users/becky/Videos/orion/dotnet/orion_flickr.jpg', '/Users/becky/Videos/orion/dotnet/orion_flickr_doug_german_budget_astro.jpg']
#wcsfns = ['/Users/becky/Videos/orion/iwonder/orion_flickr_callum_hayton.wcs.fits',  '/Users/becky/Videos/orion/iwonder/orion_belt_flickr_jonathon_howell.wcs.fits', '/Users/becky/Videos/orion/iwonder/orion_flickr_doug_german_budget_astro_astrometry.wcs.fits','/Users/becky/Videos/orion/iwonder/orion_flickr_ken_lord.wcs.fits']
#imgfns = ['/Users/becky/Videos/orion/iwonder/orion_flickr_callum_hayton.jpg', '/Users/becky/Videos/orion/iwonder/orion_belt_flickr_jonathon_howell.jpg', '/Users/becky/Videos/orion/iwonder/orion_flickr_doug_german_budget_astro.jpg', '/Users/becky/Videos/orion/iwonder/orion_flickr_ken_lord.jpg']
wcsfns = glob('/Users/becky/Videos/orion/iwonder/*.wcs*')
imgfns = glob('/Users/becky/Videos/orion/iwonder/*.jpg')
todo = zip(wcsfns, imgfns)


n=0
for wcsfn, imgfn in todo:
     wcs = Sip(wcsfn)
     img = plt.imread(imgfn)
     imx = (img.astype(N.float32) / 255.)
     try:
             Yo,Xo,Yi,Xi,nil = resample_with_wcs(targetwcs, wcs, [], 3)
     except NoOverlapError:
             print 'No actual overlap'
             continue
     print len(Yo), 'resampled pixels'
     if len(Yo) == 0:
             continue
     #resampled_img = N.zeros((H,W,3), imx.dtype)
     resampled_mask = N.zeros((H,W), bool)
     #for band in range(3):
             #resampled_img[Yo, Xo, band] = imx[Yi, Xi, band]
     resampled_mask[Yo, Xo] = True
     print 'before update', N.shape(enhance.enhI)
     enhance.update(mask = resampled_mask.ravel(), img= imx[Yi, Xi, :])
     print 'after update', N.shape(enhance.enhI)
     stack = enhance.stretch_to_match(plt.imread('/Users/becky/Videos/orion/iwonder/orion_flickr_callum_hayton.jpg').astype(N.float32)/255.).reshape((H,W,3))
     n+=1
     imsave('/Users/becky/Videos/orion/iwonder/all_stack_wide_step_number_'+str(n)+'.png', N.flipud(stack))

# stack = enhance.enhI.reshape(H,W,3)
# P.figure()
# P.imshow(stack,  origin='lower')

# stretch = enhance.stretch_to_match(imx).reshape((H,W,3))
# P.figure()
# P.imshow(stretch, origin='lower')


# stretch = enhance.stretch_to_match(plt.imread(imgfns[-1]).astype(N.float32)/255.).reshape((H,W,3))
# P.figure()
# P.imshow(stretch, origin='lower')