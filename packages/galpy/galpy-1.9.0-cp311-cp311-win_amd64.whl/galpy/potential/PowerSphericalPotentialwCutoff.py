###############################################################################
#   PowerSphericalPotentialwCutoff.py: spherical power-law potential w/ cutoff
#
#                                     amp
#                          rho(r)= ---------   e^{-(r/rc)^2}
#                                   r^\alpha
###############################################################################
import numpy
from scipy import special

from ..util import conversion
from ..util._optional_deps import _JAX_LOADED
from .Potential import Potential, kms_to_kpcGyrDecorator

if _JAX_LOADED:
    import jax.numpy as jnp
    import jax.scipy.special as jspecial


class PowerSphericalPotentialwCutoff(Potential):
    """Class that implements spherical potentials that are derived from
    power-law density models

    .. math::

        \\rho(r) = \\mathrm{amp}\\,\\left(\\frac{r_1}{r}\\right)^\\alpha\\,\\exp\\left(-(r/rc)^2\\right)

    """

    def __init__(
        self, amp=1.0, alpha=1.0, rc=1.0, normalize=False, r1=1.0, ro=None, vo=None
    ):
        """
        NAME:

           __init__

        PURPOSE:

           initialize a power-law-density potential

        INPUT:

           amp= amplitude to be applied to the potential (default: 1); can be a Quantity with units of mass density or Gxmass density

           alpha= inner power

           rc= cut-off radius (can be Quantity)

           r1= (1.) reference radius for amplitude (can be Quantity)

           normalize= if True, normalize such that vc(1.,0.)=1., or, if given as a number, such that the force is this fraction of the force necessary to make vc(1.,0.)=1.

           ro=, vo= distance and velocity scales for translation into internal units (default from configuration file)

        OUTPUT:

           (none)

        HISTORY:

           2013-06-28 - Written - Bovy (IAS)

        """
        Potential.__init__(self, amp=amp, ro=ro, vo=vo, amp_units="density")
        r1 = conversion.parse_length(r1, ro=self._ro)
        rc = conversion.parse_length(rc, ro=self._ro)
        self.alpha = alpha
        # Back to old definition
        self._amp *= r1**self.alpha
        self.rc = rc
        self._scale = self.rc
        if normalize or (
            isinstance(normalize, (int, float)) and not isinstance(normalize, bool)
        ):  # pragma: no cover
            self.normalize(normalize)
        self.hasC = True
        self.hasC_dxdv = True
        self.hasC_dens = True
        self._nemo_accname = "PowSphwCut"

    def _evaluate(self, R, z, phi=0.0, t=0.0):
        """
        NAME:
           _evaluate
        PURPOSE:
           evaluate the potential at R,z
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           Phi(R,z)
        HISTORY:
           2013-06-28 - Started - Bovy (IAS)
        """
        r = numpy.sqrt(R**2.0 + z**2.0)
        out = (
            2.0
            * numpy.pi
            * self.rc ** (3.0 - self.alpha)
            * (
                1
                / self.rc
                * special.gamma(1.0 - self.alpha / 2.0)
                * special.gammainc(1.0 - self.alpha / 2.0, (r / self.rc) ** 2.0)
                - special.gamma(1.5 - self.alpha / 2.0)
                * special.gammainc(1.5 - self.alpha / 2.0, (r / self.rc) ** 2.0)
                / r
            )
        )
        if isinstance(r, (float, int)):
            if r == 0:
                return 0.0
            else:
                return out
        else:
            out[r == 0] = 0.0
            return out

    def _Rforce(self, R, z, phi=0.0, t=0.0):
        """
        NAME:
           _Rforce
        PURPOSE:
           evaluate the radial force for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           the radial force
        HISTORY:
           2013-06-26 - Written - Bovy (IAS)
        """
        r = numpy.sqrt(R * R + z * z)
        return -self._mass(r) * R / r**3.0

    def _zforce(self, R, z, phi=0.0, t=0.0):
        """
        NAME:
           _zforce
        PURPOSE:
           evaluate the vertical force for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           the vertical force
        HISTORY:
           2013-06-26 - Written - Bovy (IAS)
        """
        r = numpy.sqrt(R * R + z * z)
        return -self._mass(r) * z / r**3.0

    def _R2deriv(self, R, z, phi=0.0, t=0.0):
        """
        NAME:
           _Rderiv
        PURPOSE:
           evaluate the second radial derivative for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           the second radial derivative
        HISTORY:
           2013-06-28 - Written - Bovy (IAS)
        """
        r = numpy.sqrt(R * R + z * z)
        return 4.0 * numpy.pi * r ** (-2.0 - self.alpha) * numpy.exp(
            -((r / self.rc) ** 2.0)
        ) * R**2.0 + self._mass(r) / r**5.0 * (z**2.0 - 2.0 * R**2.0)

    def _z2deriv(self, R, z, phi=0.0, t=0.0):
        """
        NAME:
           _z2deriv
        PURPOSE:
           evaluate the second vertical derivative for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t- time
        OUTPUT:
           the second vertical derivative
        HISTORY:
           2013-06-28 - Written - Bovy (IAS)
        """
        r = numpy.sqrt(R * R + z * z)
        return 4.0 * numpy.pi * r ** (-2.0 - self.alpha) * numpy.exp(
            -((r / self.rc) ** 2.0)
        ) * z**2.0 + self._mass(r) / r**5.0 * (R**2.0 - 2.0 * z**2.0)

    def _Rzderiv(self, R, z, phi=0.0, t=0.0):
        """
        NAME:
           _Rzderiv
        PURPOSE:
           evaluate the mixed R,z derivative for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t- time
        OUTPUT:
           d2phi/dR/dz
        HISTORY:
           2013-08-28 - Written - Bovy (IAS)
        """
        r = numpy.sqrt(R * R + z * z)
        return (
            R
            * z
            * (
                4.0
                * numpy.pi
                * r ** (-2.0 - self.alpha)
                * numpy.exp(-((r / self.rc) ** 2.0))
                - 3.0 * self._mass(r) / r**5.0
            )
        )

    def _rforce_jax(self, r):
        """
        NAME:
           _rforce_jax
        PURPOSE:
           evaluate the spherical radial force for this potential using JAX; use incomplete gamma implementation rather than hypergeometric, because JAX doesn't have the hypergeometric functions currently
        INPUT:
           r - Galactocentric spherical radius
        OUTPUT:
           the radial force
        HISTORY:
           2022-05-10 - Written - Bovy (UofT)
        """
        if not _JAX_LOADED:  # pragma: no cover
            raise ImportError(
                "Making use of the _rforce_jax function requires the google/jax library"
            )
        return (
            -self._amp
            * 2.0
            * numpy.pi
            * self.rc ** (3.0 - self.alpha)
            * jspecial.gammainc(1.5 - 0.5 * self.alpha, (r / self.rc) ** 2.0)
            * numpy.exp(jspecial.gammaln(1.5 - 0.5 * self.alpha))
            / r**2
        )

    def _ddensdr(self, r, t=0.0):
        """
        NAME:
           _ddensdr
        PURPOSE:
            evaluate the radial density derivative for this potential
        INPUT:
           r - spherical radius
           t= time
        OUTPUT:
           the density derivative
        HISTORY:
           2021-12-15 - Written - Lane (UofT)
        """
        return (
            -self._amp
            * r ** (-1.0 - self.alpha)
            * numpy.exp(-((r / self.rc) ** 2.0))
            * (2.0 * r**2.0 / self.rc**2.0 + self.alpha)
        )

    def _d2densdr2(self, r, t=0.0):
        """
        NAME:
           _d2densdr2
        PURPOSE:
           evaluate the second radial density derivative for this potential
        INPUT:
           r - spherical radius
           t= time
        OUTPUT:
           the 2nd density derivative
        HISTORY:
           2021-12-15 - Written - Lane (UofT)
        """
        return (
            self._amp
            * r ** (-2.0 - self.alpha)
            * numpy.exp(-((r / self.rc) ** 2))
            * (
                self.alpha**2.0
                + self.alpha
                + 4 * self.alpha * r**2.0 / self.rc**2.0
                - 2.0 * r**2.0 / self.rc**2.0
                + 4.0 * r**4.0 / self.rc**4.0
            )
        )

    def _ddenstwobetadr(self, r, beta=0):
        """
        NAME:
           _ddenstwobetadr
        PURPOSE:
           evaluate the radial density derivative x r^(2beta) for this potential
        INPUT:
           r - spherical radius
           beta= (0)
        OUTPUT:
           d (rho x r^{2beta} ) / d r
        HISTORY:
           2021-03-15 - Written - Lane (UofT)
        """
        if not _JAX_LOADED:  # pragma: no cover
            raise ImportError(
                "Making use of _rforce_jax function requires the google/jax library"
            )
        return (
            -self._amp
            * jnp.exp(-((r / self.rc) ** 2.0))
            / r ** (self.alpha - 2.0 * beta)
            * ((self.alpha - 2.0 * beta) / r + 2.0 * r / self.rc**2.0)
        )

    def _dens(self, R, z, phi=0.0, t=0.0):
        """
        NAME:
           _dens
        PURPOSE:
           evaluate the density for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           the density
        HISTORY:
           2013-06-28 - Written - Bovy (IAS)
        """
        r = numpy.sqrt(R**2.0 + z**2.0)
        return 1.0 / r**self.alpha * numpy.exp(-((r / self.rc) ** 2.0))

    def _mass(self, R, z=None, t=0.0):
        """
        NAME:
           _mass
        PURPOSE:
           evaluate the mass within R for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           t - time
        OUTPUT:
           the mass enclosed
        HISTORY:
           2013-XX-XX - Written - Bovy (IAS)
           2021-04-07 - Switched to hypergeometric function equivalent to incomplete gamma function for better behavior at alpha < -3 - Bovy (UofT)
        """
        if z is not None:
            raise AttributeError  # use general implementation
        R = numpy.array(R)
        out = numpy.ones_like(R)
        out[~numpy.isinf(R)] = (
            2.0
            * numpy.pi
            * R[~numpy.isinf(R)] ** (3.0 - self.alpha)
            / (1.5 - self.alpha / 2.0)
            * special.hyp1f1(
                1.5 - self.alpha / 2.0,
                2.5 - self.alpha / 2.0,
                -((R[~numpy.isinf(R)] / self.rc) ** 2.0),
            )
        )
        out[numpy.isinf(R)] = (
            2.0
            * numpy.pi
            * self.rc ** (3.0 - self.alpha)
            * special.gamma(1.5 - self.alpha / 2.0)
        )
        return out

    @kms_to_kpcGyrDecorator
    def _nemo_accpars(self, vo, ro):
        """
        NAME:

           _nemo_accpars

        PURPOSE:

           return the accpars potential parameters for use of this potential with NEMO

        INPUT:

           vo - velocity unit in km/s

           ro - length unit in kpc

        OUTPUT:

           accpars string

        HISTORY:

           2014-12-18 - Written - Bovy (IAS)

        """
        ampl = self._amp * vo**2.0 * ro ** (self.alpha - 2.0)
        return f"0,{ampl},{self.alpha},{self.rc*ro}"
