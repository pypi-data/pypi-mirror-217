###############################################################################
#   CosmphiDiskPotential: cos(mphi) potential
###############################################################################
import numpy

from ..util import conversion
from .planarPotential import planarPotential

_degtorad = numpy.pi / 180.0


class CosmphiDiskPotential(planarPotential):
    """Class that implements the disk potential

    .. math::

        \\Phi(R,\\phi) = \\mathrm{amp}\\,\\phi_0\\,\\,\\cos\\left[m\\,(\\phi-\\phi_b)\\right]\\times \\begin{cases}
        \\left(\\frac{R}{R_1}\\right)^p\\,, & \\text{for}\\ R \\geq R_b\\\\
        \\left[2-\\left(\\frac{R_b}{R}\\right)^p\\right]\\times\\left(\\frac{R_b}{R_1}\\right)^p\\,, & \\text{for}\\ R\\leq R_b.
        \\end{cases}

    This potential can be grown between  :math:`t_{\\mathrm{form}}` and  :math:`t_{\\mathrm{form}}+T_{\\mathrm{steady}}` in a similar way as DehnenBarPotential by wrapping it with a DehnenSmoothWrapperPotential

   """

    def __init__(
        self,
        amp=1.0,
        phib=25.0 * _degtorad,
        p=1.0,
        phio=0.01,
        m=4,
        r1=1.0,
        rb=None,
        cp=None,
        sp=None,
        ro=None,
        vo=None,
    ):
        """
        NAME:

           __init__

        PURPOSE:

           initialize an cosmphi disk potential

        INPUT:

           amp= amplitude to be applied to the potential (default:
           1.), degenerate with phio below, but kept for overall
           consistency with potentials

           m= cos( m * (phi - phib) ), integer

           p= power-law index of the phi(R) = (R/Ro)^p part

           r1= (1.) normalization radius for the amplitude (can be Quantity); amp x phio is only the potential at (R,phi) = (r1,pib) when r1 > rb; otherwise more complicated

           rb= (None) if set, break radius for power-law: potential R^p at R > Rb, R^-p at R < Rb, potential and force continuous at Rb


           Either:

              a) phib= angle (in rad; default=25 degree; or can be Quantity)

                 phio= potential perturbation (in terms of phio/vo^2 if vo=1 at Ro=1; or can be Quantity with units of velocity-squared)

              b) cp, sp= m * phio * cos(m * phib), m * phio * sin(m * phib); can be Quantity with units of velocity-squared)

        OUTPUT:

           (none)

        HISTORY:

           2011-10-27 - Started - Bovy (IAS)

           2017-09-16 - Added break radius rb - Bovy (UofT)

        """
        planarPotential.__init__(self, amp=amp, ro=ro, vo=vo)
        phib = conversion.parse_angle(phib)
        r1 = conversion.parse_length(r1, ro=self._ro)
        rb = conversion.parse_length(rb, ro=self._ro)
        phio = conversion.parse_energy(phio, vo=self._vo)
        cp = conversion.parse_energy(cp, vo=self._vo)
        sp = conversion.parse_energy(sp, vo=self._vo)
        # Back to old definition
        self._r1p = r1**p
        self._amp /= self._r1p
        self.hasC = False
        self._m = int(m)  # make sure this is an int
        if cp is None or sp is None:
            self._phib = phib
            self._mphio = phio * self._m
        else:
            self._mphio = numpy.sqrt(cp * cp + sp * sp)
            self._phib = numpy.arctan(sp / cp) / self._m
            if m < 2.0 and cp < 0.0:
                self._phib = numpy.pi + self._phib
        self._p = p
        if rb is None:
            self._rb = 0.0
            self._rbp = 1.0  # never used, but for p < 0 general expr fails
            self._rb2p = 1.0
        else:
            self._rb = rb
            self._rbp = self._rb**self._p
            self._rb2p = self._rbp**2.0
        self._mphib = self._m * self._phib
        self.hasC = True
        self.hasC_dxdv = True

    def _evaluate(self, R, phi=0.0, t=0.0):
        """
        NAME:
           _evaluate
        PURPOSE:
           evaluate the potential at R,phi,t
        INPUT:
           R - Galactocentric cylindrical radius
           phi - azimuth
           t - time
        OUTPUT:
           Phi(R,phi,t)
        HISTORY:
           2011-10-19 - Started - Bovy (IAS)
        """
        if R < self._rb:
            return (
                self._mphio
                / self._m
                * numpy.cos(self._m * phi - self._mphib)
                * self._rbp
                * (2.0 * self._r1p - self._rbp / R**self._p)
            )
        else:
            return (
                self._mphio
                / self._m
                * R**self._p
                * numpy.cos(self._m * phi - self._mphib)
            )

    def _Rforce(self, R, phi=0.0, t=0.0):
        """
        NAME:
           _Rforce
        PURPOSE:
           evaluate the radial force for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           phi - azimuth
           t - time
        OUTPUT:
           the radial force
        HISTORY:
           2011-10-19 - Written - Bovy (IAS)
        """
        if R < self._rb:
            return (
                -self._p
                * self._mphio
                / self._m
                * self._rb2p
                / R ** (self._p + 1.0)
                * numpy.cos(self._m * phi - self._mphib)
            )
        else:
            return (
                -self._p
                * self._mphio
                / self._m
                * R ** (self._p - 1.0)
                * numpy.cos(self._m * phi - self._mphib)
            )

    def _phitorque(self, R, phi=0.0, t=0.0):
        """
        NAME:
           _phitorque
        PURPOSE:
           evaluate the azimuthal torque for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           phi - azimuth
           t - time
        OUTPUT:
           the azimuthal torque
        HISTORY:
           2011-10-19 - Written - Bovy (IAS)
        """
        if R < self._rb:
            return (
                self._mphio
                * numpy.sin(self._m * phi - self._mphib)
                * self._rbp
                * (2.0 * self._r1p - self._rbp / R**self._p)
            )
        else:
            return self._mphio * R**self._p * numpy.sin(self._m * phi - self._mphib)

    def _R2deriv(self, R, phi=0.0, t=0.0):
        if R < self._rb:
            return (
                -self._p
                * (self._p + 1.0)
                * self._mphio
                / self._m
                * self._rb2p
                / R ** (self._p + 2.0)
                * numpy.cos(self._m * phi - self._mphib)
            )
        else:
            return (
                self._p
                * (self._p - 1.0)
                / self._m
                * self._mphio
                * R ** (self._p - 2.0)
                * numpy.cos(self._m * phi - self._mphib)
            )

    def _phi2deriv(self, R, phi=0.0, t=0.0):
        if R < self._rb:
            return (
                -self._m
                * self._mphio
                * numpy.cos(self._m * phi - self._mphib)
                * self._rbp
                * (2.0 * self._r1p - self._rbp / R**self._p)
            )
        else:
            return (
                -self._m
                * self._mphio
                * R**self._p
                * numpy.cos(self._m * phi - self._mphib)
            )

    def _Rphideriv(self, R, phi=0.0, t=0.0):
        if R < self._rb:
            return (
                -self._p
                * self._mphio
                / self._m
                * self._rb2p
                / R ** (self._p + 1.0)
                * numpy.sin(self._m * phi - self._mphib)
            )
        else:
            return (
                -self._p
                * self._mphio
                * R ** (self._p - 1.0)
                * numpy.sin(self._m * phi - self._mphib)
            )


class LopsidedDiskPotential(CosmphiDiskPotential):
    """Class that implements the disk potential

     .. math::

         \\Phi(R,\\phi) = \\mathrm{amp}\\,\\phi_0\\,\\left(\\frac{R}{R_1}\\right)^p\\,\\cos\\left(\\phi-\\phi_b\\right)

    Special case of CosmphiDiskPotential with m=1; see documentation for CosmphiDiskPotential
    """

    def __init__(
        self,
        amp=1.0,
        phib=25.0 * _degtorad,
        p=1.0,
        phio=0.01,
        r1=1.0,
        cp=None,
        sp=None,
        ro=None,
        vo=None,
    ):
        CosmphiDiskPotential.__init__(
            self, amp=amp, phib=phib, p=p, phio=phio, m=1.0, cp=cp, sp=sp, ro=ro, vo=vo
        )
        self.hasC = True
        self.hasC_dxdv = True
