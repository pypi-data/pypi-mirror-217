import os
import pickle

import numpy

from ..util import conversion, plot
from ..util.conversion import (
    parse_length,
    parse_velocity,
    physical_conversion,
    potential_physical_input,
)


def plotRotcurve(Pot, *args, **kwargs):
    """
    NAME:

       plotRotcurve

    PURPOSE:

       plot the rotation curve for this potential (in the z=0 plane for
       non-spherical potentials)

    INPUT:

       Pot - Potential or list of Potential instances

       Rrange - Range in R to consider (needs to be in the units that you are plotting; can be Quantity)

       grid= grid in R

       phi= (None) azimuth to use for non-axisymmetric potentials

       savefilename= save to or restore from this savefile (pickle)

       +galpy.util.plot.plot args and kwargs

    OUTPUT:

       plot to output device

    HISTORY:

       2010-07-10 - Written - Bovy (NYU)

       2016-06-15 - Added phi= keyword for non-axisymmetric potential - Bovy (UofT)

    """
    # Using physical units or not?
    if isinstance(Pot, list):
        potro = Pot[0]._ro
        roSet = Pot[0]._roSet
        potvo = Pot[0]._vo
        voSet = Pot[0]._voSet
    else:
        potro = Pot._ro
        roSet = Pot._roSet
        potvo = Pot._vo
        voSet = Pot._voSet
    # Following just to deal with Quantity ro/vo and check whether they are set
    _ro = parse_length(kwargs.get("ro", None), ro=potro)
    _vo = parse_velocity(kwargs.get("vo", None), vo=potvo)
    if (
        kwargs.get("use_physical", True)
        and (not _ro is None or roSet)
        and (not _vo is None or voSet)
    ):
        use_physical = True
        potro = kwargs.get("ro", potro)
        potvo = kwargs.get("vo", potvo)
        xlabel = r"$R\,(\mathrm{kpc})$"
        ylabel = r"$v_c(R)\,(\mathrm{km\,s}^{-1})$"
        Rrange = kwargs.pop("Rrange", [0.01 * potro, 5.0 * potro])
    else:
        use_physical = False
        xlabel = r"$R/R_0$"
        ylabel = r"$v_c(R)/v_c(R_0)$"
        Rrange = kwargs.pop("Rrange", [0.01, 5.0])
    # Parse ro
    potro = conversion.parse_length_kpc(potro)
    potvo = conversion.parse_velocity_kms(potvo)
    Rrange[0] = conversion.parse_length_kpc(Rrange[0])
    Rrange[1] = conversion.parse_length_kpc(Rrange[1])
    if use_physical:
        Rrange[0] /= potro
        Rrange[1] /= potro
    grid = kwargs.pop("grid", 1001)
    savefilename = kwargs.pop("savefilename", None)
    phi = kwargs.pop("phi", None)
    if not savefilename is None and os.path.exists(savefilename):
        print("Restoring savefile " + savefilename + " ...")
        savefile = open(savefilename, "rb")
        rotcurve = pickle.load(savefile)
        Rs = pickle.load(savefile)
        savefile.close()
    else:
        Rs = numpy.linspace(Rrange[0], Rrange[1], grid)
        rotcurve = calcRotcurve(Pot, Rs, phi=phi)
        if not savefilename == None:
            print("Writing savefile " + savefilename + " ...")
            savefile = open(savefilename, "wb")
            pickle.dump(rotcurve, savefile)
            pickle.dump(Rs, savefile)
            savefile.close()
    if use_physical:
        Rs *= potro
        rotcurve *= potvo
        Rrange[0] *= potro
        Rrange[1] *= potro
    if not "xlabel" in kwargs:
        kwargs["xlabel"] = xlabel
    if not "ylabel" in kwargs:
        kwargs["ylabel"] = ylabel
    if not "xrange" in kwargs:
        kwargs["xrange"] = Rrange
    if not "yrange" in kwargs:
        kwargs["yrange"] = [0.0, 1.2 * numpy.amax(rotcurve)]
    kwargs.pop("ro", None)
    kwargs.pop("vo", None)
    kwargs.pop("use_physical", None)
    return plot.plot(Rs, rotcurve, *args, **kwargs)


def calcRotcurve(Pot, Rs, phi=None, t=0.0):
    """
    NAME:

       calcRotcurve

    PURPOSE:

       calculate the rotation curve for this potential (in the z=0 plane for
       non-spherical potentials)

    INPUT:

       Pot - Potential or list of Potential instances

       Rs - (array of) radius(i)

       phi= (None) azimuth to use for non-axisymmetric potentials

       ts - instantaneous time (optional)

    OUTPUT:

       array of vc

    HISTORY:

       2011-04-13 - Written - Bovy (NYU)

       2016-06-15 - Added phi= keyword for non-axisymmetric potential - Bovy (UofT)

    """
    try:
        grid = len(Rs)
    except TypeError:
        grid = 1
        Rs = numpy.array([Rs])
    rotcurve = numpy.zeros(grid)
    for ii in range(grid):
        rotcurve[ii] = vcirc(Pot, Rs[ii], phi=phi, t=t, use_physical=False)
    return rotcurve


@potential_physical_input
@physical_conversion("velocity", pop=True)
def vcirc(Pot, R, phi=None, t=0.0):
    """

    NAME:

       vcirc

    PURPOSE:

       calculate the circular velocity at R in potential Pot

    INPUT:

       Pot - Potential instance or list of such instances

       R - Galactocentric radius (can be Quantity)

       phi= (None) azimuth to use for non-axisymmetric potentials

       t= time (optional; can be Quantity)

    OUTPUT:

       circular rotation velocity

    HISTORY:

       2011-10-09 - Written - Bovy (IAS)

       2016-06-15 - Added phi= keyword for non-axisymmetric potential - Bovy (UofT)

    """
    from ..potential import PotentialError, evaluateplanarRforces

    try:
        return numpy.sqrt(
            -R * evaluateplanarRforces(Pot, R, phi=phi, t=t, use_physical=False)
        )
    except PotentialError:
        from ..potential import toPlanarPotential

        Pot = toPlanarPotential(Pot)
        return numpy.sqrt(
            -R * evaluateplanarRforces(Pot, R, phi=phi, t=t, use_physical=False)
        )


@potential_physical_input
@physical_conversion("frequency", pop=True)
def dvcircdR(Pot, R, phi=None, t=0.0):
    """

    NAME:

       dvcircdR

    PURPOSE:

       calculate the derivative of the circular velocity wrt R at R in potential Pot

    INPUT:

       Pot - Potential instance or list of such instances

       R - Galactocentric radius (can be Quantity)

       phi= (None) azimuth to use for non-axisymmetric potentials

       t= time (optional; can be Quantity)

    OUTPUT:

       derivative of the circular rotation velocity wrt R

    HISTORY:

       2013-01-08 - Written - Bovy (IAS)

       2016-06-28 - Added phi= keyword for non-axisymmetric potential - Bovy (UofT)

    """
    from ..potential import (
        PotentialError,
        evaluateplanarR2derivs,
        evaluateplanarRforces,
    )

    tvc = vcirc(Pot, R, phi=phi, t=t, use_physical=False)
    try:
        return (
            0.5
            * (
                -evaluateplanarRforces(Pot, R, phi=phi, t=t, use_physical=False)
                + R * evaluateplanarR2derivs(Pot, R, phi=phi, t=t, use_physical=False)
            )
            / tvc
        )
    except PotentialError:
        from ..potential import RZToplanarPotential

        Pot = RZToplanarPotential(Pot)
        return (
            0.5
            * (
                -evaluateplanarRforces(Pot, R, phi=phi, t=t, use_physical=False)
                + R * evaluateplanarR2derivs(Pot, R, phi=phi, t=t, use_physical=False)
            )
            / tvc
        )
