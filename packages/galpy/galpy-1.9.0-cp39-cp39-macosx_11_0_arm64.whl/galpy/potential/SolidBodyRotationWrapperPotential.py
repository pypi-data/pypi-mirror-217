###############################################################################
#   SolidBodyRotationWrapperPotential.py: Wrapper to make a potential rotate
#                                         with a fixed pattern speed, around
#                                         the z axis
###############################################################################
from ..util import conversion
from .WrapperPotential import parentWrapperPotential


class SolidBodyRotationWrapperPotential(parentWrapperPotential):
    """Potential wrapper class that implements solid-body rotation around the z-axis. Can be used to make a bar or other perturbation rotate. The potential is rotated by replacing

    .. math::

        \\phi \\rightarrow \\phi + \\Omega \\times t + \\mathrm{pa}

    with :math:`\\Omega` the fixed pattern speed and :math:`\\mathrm{pa}` the position angle at :math:`t=0`.
    """

    def __init__(self, amp=1.0, pot=None, omega=1.0, pa=0.0, ro=None, vo=None):
        """
        NAME:

           __init__

        PURPOSE:

           initialize a SolidBodyRotationWrapper Potential

        INPUT:

           amp - amplitude to be applied to the potential (default: 1.)

           pot - Potential instance or list thereof; this potential is made to rotate around the z axis by the wrapper

           omega= (1.) the pattern speed (can be a Quantity)

           pa= (0.) the position angle (can be a Quantity)

        OUTPUT:

           (none)

        HISTORY:

           2017-08-22 - Started - Bovy (UofT)

        """
        omega = conversion.parse_frequency(omega, ro=self._ro, vo=self._vo)
        pa = conversion.parse_angle(pa)
        self._omega = omega
        self._pa = pa
        self.hasC = True
        self.hasC_dxdv = True

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
           2016-11-02 - Written - Bovy (UofT)
        """
        return self._omega

    def _wrap(self, attribute, *args, **kwargs):
        kwargs["phi"] = (
            kwargs.get("phi", 0.0) - self._omega * kwargs.get("t", 0.0) - self._pa
        )
        return self._wrap_pot_func(attribute)(self._pot, *args, **kwargs)
