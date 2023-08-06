###############################################################################
#   SteadyLogSpiralPotential: a steady-state spiral potential
###############################################################################
import numpy

from ..util import conversion
from .planarPotential import planarPotential

_degtorad = numpy.pi / 180.0


class SteadyLogSpiralPotential(planarPotential):
    """Class that implements a steady-state spiral potential

    .. math::

        \\Phi(R,\\phi) = \\frac{\\mathrm{amp}\\times A}{\\alpha}\\,\\cos\\left(\\alpha\\,\\ln R - m\\,(\\phi-\\Omega_s\\,t-\\gamma)\\right)


    Can be grown in a similar way as the DehnenBarPotential, but using :math:`T_s = 2\\pi/\\Omega_s` to normalize :math:`t_{\\mathrm{form}}` and :math:`t_{\\mathrm{steady}}`. If the pattern speed is zero, :math:`t_\\mathrm{form}` and :math:`t_\\mathrm{steady}` are straight times, not times divided by the spiral period.

    """

    def __init__(
        self,
        amp=1.0,
        omegas=0.65,
        A=-0.035,
        alpha=-7.0,
        m=2,
        gamma=numpy.pi / 4.0,
        p=None,
        tform=None,
        tsteady=None,
        ro=None,
        vo=None,
    ):
        """
        NAME:

           __init__

        PURPOSE:

           initialize a logarithmic spiral potential

        INPUT:

           amp - amplitude to be applied to the potential (default:
           1., A below)

           gamma - angle between sun-GC line and the line connecting the peak of the spiral pattern at the Solar radius (in rad; default=45 degree; or can be Quantity)

           A - amplitude (alpha*potential-amplitude; default=0.035; can be Quantity

           omegas= - pattern speed (default=0.65; can be Quantity)

           m= number of arms

           Either provide:

              a) alpha=

              b) p= pitch angle (rad; can be Quantity)

           tform - start of spiral growth / spiral period (default: -Infinity)

           tsteady - time from tform at which the spiral is fully grown / spiral period (default: 2 periods)

        OUTPUT:

           (none)

        HISTORY:

           2011-03-27 - Started - Bovy (NYU)

        """
        planarPotential.__init__(self, amp=amp, ro=ro, vo=vo)
        gamma = conversion.parse_angle(gamma)
        p = conversion.parse_angle(p)
        A = conversion.parse_energy(A, vo=self._vo)
        omegas = conversion.parse_frequency(omegas, ro=self._ro, vo=self._vo)
        self._omegas = omegas
        self._A = A
        self._m = m
        self._gamma = gamma
        if not p is None:
            self._alpha = self._m / numpy.tan(p)
        else:
            self._alpha = alpha
        self._ts = 2.0 * numpy.pi / self._omegas if self._omegas != 0.0 else 1.0
        if not tform is None:
            self._tform = tform * self._ts
        else:
            self._tform = None
        if not tsteady is None:
            self._tsteady = self._tform + tsteady * self._ts
        else:
            if self._tform is None:
                self._tsteady = None
            else:
                self._tsteady = self._tform + 2.0 * self._ts
        self.hasC = True

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
           2011-03-27 - Started - Bovy (NYU)
        """
        if not self._tform is None:
            if t < self._tform:
                smooth = 0.0
            elif t < self._tsteady:
                deltat = t - self._tform
                xi = 2.0 * deltat / (self._tsteady - self._tform) - 1.0
                smooth = (
                    3.0 / 16.0 * xi**5.0
                    - 5.0 / 8 * xi**3.0
                    + 15.0 / 16.0 * xi
                    + 0.5
                )
            else:  # spiral is fully on
                smooth = 1.0
        else:
            smooth = 1.0
        return (
            smooth
            * self._A
            / self._alpha
            * numpy.cos(
                self._alpha * numpy.log(R)
                - self._m * (phi - self._omegas * t - self._gamma)
            )
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
           2010-11-24 - Written - Bovy (NYU)
        """
        if not self._tform is None:
            if t < self._tform:
                smooth = 0.0
            elif t < self._tsteady:
                deltat = t - self._tform
                xi = 2.0 * deltat / (self._tsteady - self._tform) - 1.0
                smooth = (
                    3.0 / 16.0 * xi**5.0
                    - 5.0 / 8 * xi**3.0
                    + 15.0 / 16.0 * xi
                    + 0.5
                )
            else:  # spiral is fully on
                smooth = 1.0
        else:
            smooth = 1.0
        return (
            smooth
            * self._A
            / R
            * numpy.sin(
                self._alpha * numpy.log(R)
                - self._m * (phi - self._omegas * t - self._gamma)
            )
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
           2010-11-24 - Written - Bovy (NYU)
        """
        if not self._tform is None:
            if t < self._tform:
                smooth = 0.0
            elif t < self._tsteady:
                deltat = t - self._tform
                xi = 2.0 * deltat / (self._tsteady - self._tform) - 1.0
                smooth = (
                    3.0 / 16.0 * xi**5.0
                    - 5.0 / 8 * xi**3.0
                    + 15.0 / 16.0 * xi
                    + 0.5
                )
            else:  # spiral is fully on
                smooth = 1.0
        else:
            smooth = 1.0
        return (
            -smooth
            * self._A
            / self._alpha
            * self._m
            * numpy.sin(
                self._alpha * numpy.log(R)
                - self._m * (phi - self._omegas * t - self._gamma)
            )
        )

    def wavenumber(self, R):
        """
        NAME:


           wavenumber

        PURPOSE:

           return the wavenumber at radius R (d f(R)/ d R in Phi_a(R) = F(R) e^[i f(R)]; see Binney & Tremaine 2008)

        INPUT:

           R - Cylindrical radius

        OUTPUT:

           wavenumber at R

        HISTORY:

           2014-08-23 - Written - Bovy (IAS)

        """
        return self._alpha / R

    def OmegaP(self):
        """
        NAME:


           OmegaP

        PURPOSE:

           return the pattern speed

        INPUT:

           (none)

        OUTPUT:

           pattern speed

        HISTORY:

           2011-10-10 - Written - Bovy (IAS)

        """
        return self._omegas

    def m(self):
        """
        NAME:


           m

        PURPOSE:

           return the number of arms

        INPUT:

           (none)

        OUTPUT:

           number of arms

        HISTORY:

           2014-08-23 - Written - Bovy (IAS)

        """
        return self._m

    def tform(self):  # pragma: no cover
        """
        NAME:

           tform

        PURPOSE:

           return formation time of the bar

        INPUT:

           (none)

        OUTPUT:

           tform in normalized units

        HISTORY:

           2011-03-08 - Written - Bovy (NYU)

        """
        return self._tform
