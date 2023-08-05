import numpy as np
from ophyd.pseudopos import pseudo_position_argument, real_position_argument
from ophyd import PseudoPositioner, PseudoSingle, EpicsMotor
from ophyd import Component as Cpt, FormattedComponent as FCpt, Device

from .._iconfig import load_config
from .instrument_registry import registry


um_per_mm = 1000


class RowlandPositioner(PseudoPositioner):
    """A pseudo positioner describing a rowland circle.

    Real Axes
    =========
    x
    y
    z
    z1

    Pseudo Axes
    ===========
    D
      In mm
    theta
      In degrees
    alpha
      In degrees
    """

    def __init__(
        self,
        x_motor_pv: str,
        y_motor_pv: str,
        z_motor_pv: str,
        z1_motor_pv: str,
        *args,
        **kwargs
    ):
        self.x_motor_pv = x_motor_pv
        self.y_motor_pv = y_motor_pv
        self.z_motor_pv = z_motor_pv
        self.z1_motor_pv = z1_motor_pv
        super().__init__(*args, **kwargs)

    # Pseudo axes
    D: PseudoSingle = Cpt(PseudoSingle, name="D", limits=(0, 1000))
    theta: PseudoSingle = Cpt(PseudoSingle, name="theta", limits=(0, 180))
    alpha: PseudoSingle = Cpt(PseudoSingle, name="alpha", limits=(0, 180))

    # Real axes
    x: EpicsMotor = FCpt(EpicsMotor, "{x_motor_pv}", name="x")
    y: EpicsMotor = FCpt(EpicsMotor, "{y_motor_pv}", name="y")
    z: EpicsMotor = FCpt(EpicsMotor, "{z_motor_pv}", name="z")
    z1: EpicsMotor = FCpt(EpicsMotor, "{z1_motor_pv}", name="z1")

    @pseudo_position_argument
    def forward(self, pseudo_pos):
        """Run a forward (pseudo -> real) calculation"""
        # Convert distance to microns and degrees to radians
        D = pseudo_pos.D * um_per_mm
        theta = pseudo_pos.theta / 180.0 * np.pi
        alpha = pseudo_pos.alpha / 180.0 * np.pi
        # Convert virtual positions to real positions
        x = D * (np.sin(theta + alpha)) ** 2
        y = D * ((np.sin(theta + alpha)) ** 2 - (np.sin(theta - alpha)) ** 2)
        z1 = D * np.sin(theta - alpha) * np.cos(theta + alpha)
        z2 = D * np.sin(theta - alpha) * np.cos(theta - alpha)
        z = z1 + z2
        return self.RealPosition(
            x=x,
            y=y,
            z=z,
            z1=z1,
        )

    @real_position_argument
    def inverse(self, real_pos):
        """Run an inverse (real -> pseudo) calculation"""
        return self.PseudoPosition(D=0, theta=0, alpha=0)
        # Expand the variables
        x = real_pos.x
        y = real_pos.y
        z = real_pos.z
        z1 = real_pos.z1
        # Invert the calculation, first for 'd'
        a = y
        b = -x
        c = z1**2
        d = -(z1**2 * y)  # Maybe needs parens?
        p = (3 * a * c - b**2) / (3 * a**2)
        q = (2 * b**3 - 9 * a * b * c + 27 * a**2 * d) / (27 * a**3)
        D = (-(q / 2) + (q**2 / 4 + p**3 / 27) ** 0.5) ** (1 / 3) + (
            -(q / 2) - (q**2 / 4 + p**3 / 27) ** 0.5
        ) ** (1 / 3)
        # D = x / ((1 - (z1 ** 2 / (D ** 2 * y + z1 ** 2))) ** 2)
        # cos(theta + alpha) = (z1 ** 2 / (D ** 2 * y + z1 ** 2)) ** 0.5
        print(a, b, c, d)
        print(p, q, D)
        return self.PseudoPosition(D=D, theta=0, alpha=0)


# Rewrite the following four equations so that they calculate D, theta and alpha based on inputting x, y, z1 and z.

#         x = D * (sin(theta + alpha)) ** 2
#         y = D * ((sin(theta + alpha)) ** 2 - (sin(theta - alpha)) ** 2)
#         z1 = D * sin(theta - alpha) * cos(theta + alpha)
#         z = z1 + D * sin(theta - alpha) * cos(theta - alpha)

# To calculate D, theta, and alpha based on x, y, z1, and z, we can rearrange the given equations as follows:

# D = x / (sin(theta + alpha)) ** 2

# sin(theta - alpha) = z1 / (D * cos(theta + alpha))

# cos(theta - alpha) = (z - z1) / (D * sin(theta - alpha))

# Substitute the above two equations into the expression for y:

# y = D * ((sin(theta + alpha)) ** 2 - (sin(theta - alpha)) ** 2)

# y = D * ((sin(theta + alpha)) ** 2 - (z1 / (D * cos(theta + alpha))) ** 2)

# y = D * ((sin(theta + alpha)) ** 2 - (z1 ** 2 / D ** 2) * (cos(theta + alpha)) ** (-2))

# Solve for cos(theta + alpha) in the above equation:

# cos(theta + alpha) = (z1 ** 2 / (D ** 2 * y + z1 ** 2)) ** 0.5

# Substitute the value of cos(theta + alpha) into the equation for sin(theta - alpha):

# sin(theta - alpha) = z1 / (D * (z1 ** 2 / (D ** 2 * y + z1 ** 2)) ** 0.5)

# Simplify the above equation:

# sin(theta - alpha) = (z1 ** 2 / (D ** 2 * y + z1 ** 2)) ** 0.5

# Finally, substitute the values of cos(theta + alpha) and sin(theta - alpha) into the equation for D:

# D = x / ((sin(theta + alpha)) ** 2)

# D = x / ((1 - (z1 ** 2 / (D ** 2 * y + z1 ** 2))) ** 2)

# This equation can be solved numerically to obtain the value of D. Once D is known, we can use the equations for cos(theta + alpha) and sin(theta - alpha) to calculate theta and alpha.


@registry.register
class LERIXSpectrometer(Device):
    rowland = Cpt(
        RowlandPositioner,
        x_motor_pv="vme_crate_ioc:m1",
        y_motor_pv="vme_crate_ioc:m2",
        z_motor_pv="vme_crate_ioc:m3",
        z1_motor_pv="vme_crate_ioc:m4",
        name="rowland",
    )


def load_lerix_spectrometers(config=None):
    if config is None:
        config = load_config()
    # Create spectrometers
    for name, cfg in config.get("lerix", {}).items():
        rowland = cfg["rowland"]
        device = RowlandPositioner(
            name=name,
            x_motor_pv=rowland["x_motor_pv"],
            y_motor_pv=rowland["y_motor_pv"],
            z_motor_pv=rowland["z_motor_pv"],
            z1_motor_pv=rowland["z1_motor_pv"],
            labels={"lerix_spectrometers"},
        )
        registry.register(device)
