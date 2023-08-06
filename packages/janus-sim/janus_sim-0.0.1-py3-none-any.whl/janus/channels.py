from __future__ import annotations
from abc import ABC, abstractmethod

from enum import Enum
from functools import total_ordering

import jax.numpy as jnp
from jaxtyping import Array, Float

from typing import Tuple, Union, List, Optional, Dict

from janus.util import exprel


Scalar = Float[Array, ""]


@total_ordering
class Ion(Enum):
  Ca = 1
  K = 2
  Na = 3
  NSC1 = 4

  def __lt__(self, other):
    if self.__class__ is other.__class__:
      return self.value < other.value
    return NotImplemented


class VoltageGatedIonChannel(ABC):

  subunit_dim: int
  ion: Ion

  @classmethod
  @abstractmethod
  def activation(cls, subunit_states: Float[Array, " subunit_dim"]) -> Scalar:
    ...

  @classmethod
  @abstractmethod
  def subunit_dynamics(
          cls,
          voltage: Scalar
          ) -> Tuple[Float[Array, " subunit_dim"], Float[Array, " subunit_dim"]]:
    ...

  @classmethod
  @abstractmethod
  def resting_state(cls, voltage: Scalar) -> Float[Array, " subunit_dim"]:
    ...


class CaGatedIonChannel(ABC):

  subunit_dim: int
  ion: Ion

  @classmethod
  @abstractmethod
  def activation(cls, subunit_states: Float[Array, " subunit_dim"]) -> Scalar:
    ...

  @classmethod
  @abstractmethod
  def subunit_dynamics(
          cls,
          voltage: Scalar,
          cai: Scalar
          ) -> Tuple[Float[Array, " subunit_dim"], Float[Array, " subunit_dim"]]:
    ...

  @classmethod
  @abstractmethod
  def resting_state(cls, voltage: Scalar, cai: Scalar) -> Float[Array, " subunit_dim"]:
    ...


IonChannel = Union[VoltageGatedIonChannel, CaGatedIonChannel]


class NaTs(VoltageGatedIonChannel):

  subunit_dim: int = 2
  ion: Ion = Ion.Na
  T: float = 34.

  @classmethod
  def activation(cls, subunit_states: Float[Array, " subunit_dim"]) -> Scalar:
    return jnp.power(subunit_states[0], 3) * subunit_states[1]

  @classmethod
  def m_alpha(cls, v: Scalar) -> Scalar:
    return (0.182 * 6) / exprel(-(v + 40.) / 6.)

  @classmethod
  def m_beta(cls, v: Scalar) -> Scalar:
    return (0.124 * 6) / exprel((v + 40.) / 6.)

  @classmethod
  def h_alpha(cls, v: Scalar) -> Scalar:
    return (0.015 * 6) / exprel((v + 66.) / 6.)

  @classmethod
  def h_beta(cls, v: Scalar) -> Scalar:
    return (0.015 * 6) / exprel(-(v + 66.) / 6.)

  @classmethod
  def subunit_dynamics(
          cls, v: Scalar) -> Tuple[Float[Array, " subunit_dim"], Float[Array, " subunit_dim"]]:
    q_t = jnp.power(2.3, (cls.T - 23.)/10.)
    ma = cls.m_alpha(v)
    mb = cls.m_beta(v)
    ha = cls.h_alpha(v)
    hb = cls.h_beta(v)
    A_diag = - q_t * jnp.array([ma + mb, ha + hb]).reshape([2])
    b = q_t * jnp.array([ma, ha]).reshape([2])
    return A_diag, b

  @classmethod
  def resting_state(cls, v: Scalar) -> Float[Array, " subunit_dim"]:
    ma = cls.m_alpha(v)
    mb = cls.m_beta(v)
    ha = cls.h_alpha(v)
    hb = cls.h_beta(v)
    return jnp.array([ma / (ma + mb), ha / (ha + hb)]).reshape([2])


class NaP(VoltageGatedIonChannel):

  subunit_dim: int = 2
  ion: Ion = Ion.Na
  T: float = 34.

  @classmethod
  def activation(cls, subunit_states: Float[Array, " subunit_dim"]) -> Scalar:
    return subunit_states[0] * subunit_states[1]

  @classmethod
  def subunit_dynamics(
          cls, v: Scalar) -> Tuple[Float[Array, " subunit_dim"], Float[Array, " subunit_dim"]]:
    c = jnp.array(1e12)
    q_t = jnp.power(2.3, (cls.T - 21.)/10.)
    m_inf = 1.0/(1 + jnp.exp(-(v + 52.6) / 4.6))
    alpha_h = (2.88e-6 * 4.63) / exprel((v + 17.013) / 4.63)
    beta_h = (6.94e-6 * 2.63) / exprel(-(v + 64.4) / 2.63)
    A_diag = - jnp.array([c, q_t * (alpha_h + beta_h)]).reshape([2])
    b =  jnp.array([m_inf * c, q_t * alpha_h]).reshape([2])
    return A_diag, b

  @classmethod
  def resting_state(cls, v: Scalar) -> Float[Array, " subunit_dim"]:
    return jnp.array([1. / (1 + jnp.exp(-(v + 52.6) / 4.6)),
                      1. / (1. + jnp.exp((v + 48.8) / 10.))]).reshape([2])


class KT(VoltageGatedIonChannel):

  subunit_dim: int = 2
  ion: Ion = Ion.K
  T: float = 34.

  @classmethod
  def activation(cls, subunit_states: Float[Array, " subunit_dim"]) -> Scalar:
    return jnp.power(subunit_states[0], 4) * subunit_states[1]

  @classmethod
  def m_inf(cls, v: Scalar) -> Scalar:
    return 1. / (1. + jnp.exp(-(v + 47.) / 29.))

  @classmethod
  def m_tau(cls, v: Scalar) -> Scalar:
    return 0.34 + (0.92 / jnp.exp(jnp.square((v + 71.) / 59.)))

  @classmethod
  def h_inf(cls, v: Scalar) -> Scalar:
    return 1. / (1. + jnp.exp((v + 66.) / 10.))

  @classmethod
  def h_tau(cls, v: Scalar) -> Scalar:
    return 8. + (49. / jnp.exp(jnp.square((v + 73.) / 23.)))

  @classmethod
  def subunit_dynamics(
          cls, v: Scalar) -> Tuple[Float[Array, " subunit_dim"], Float[Array, " subunit_dim"]]:
    q_t = jnp.power(2.3, (cls.T - 21.)/10.)
    mt = cls.m_tau(v)
    ht = cls.h_tau(v)
    A_diag = - q_t * jnp.array([1. / mt, 1./ht]).reshape([2])
    b = q_t * jnp.array([cls.m_inf(v) / mt, cls.h_inf(v) / ht]).reshape([2])
    return A_diag, b

  @classmethod
  def resting_state(cls, v: Scalar) -> Float[Array, " subunit_dim"]:
    mi = cls.m_inf(v)
    hi = cls.h_inf(v)
    return jnp.array([mi, hi]).reshape([2])


class KP(VoltageGatedIonChannel):

  subunit_dim: int = 2
  ion: Ion = Ion.K
  T: float = 34.

  @classmethod
  def activation(cls, subunit_states: Float[Array, " subunit_dim"]) -> Scalar:
    return jnp.power(subunit_states[0], 2) * subunit_states[1]

  @classmethod
  def m_inf(cls, v: Scalar) -> Scalar:
    return 1. / (1. + jnp.exp(-(v + 14.3) / 14.6))

  @classmethod
  def m_tau(cls, v: Scalar) -> Scalar:
    return jnp.where(
        v < -50.,
        1.25 + 175.03 * jnp.exp(0.026 * v),
        1.25 + 13. * jnp.exp(-0.026 * v))

  @classmethod
  def h_inf(cls, v: Scalar) -> Scalar:
    return 1. / (1. + jnp.exp((v + 54.) / 11.))

  @classmethod
  def h_tau(cls, v: Scalar) -> Scalar:
    return 360. + (24. * v + 2330.) / jnp.exp(jnp.square((v + 75.) / 48.))

  @classmethod
  def subunit_dynamics(
          cls, v: Scalar) -> Tuple[Float[Array, " subunit_dim"], Float[Array, " subunit_dim"]]:
    q_t = jnp.power(2.3, (cls.T - 21.)/10.)
    mt = cls.m_tau(v)
    ht = cls.h_tau(v)
    A_diag = - q_t * jnp.array([1. / mt, 1./ht]).reshape([2])
    b = q_t * jnp.array([cls.m_inf(v) / mt, cls.h_inf(v) / ht]).reshape([2])
    return A_diag, b

  @classmethod
  def resting_state(cls, v: Scalar) -> Float[Array, " subunit_dim"]:
    mi = cls.m_inf(v)
    hi = cls.h_inf(v)
    return jnp.array([mi, hi]).reshape([2])


class Kv3(VoltageGatedIonChannel):

  subunit_dim: int = 1
  ion: Ion = Ion.K

  @classmethod
  def activation(cls, subunit_states: Float[Array, " subunit_dim"]) -> Scalar:
    return subunit_states[0]

  @classmethod
  def m_inf(cls, v: Scalar) -> Scalar:
    return 1. / (1. + jnp.exp(-(v - 18.7) / 9.7))

  @classmethod
  def m_tau(cls, v: Scalar) -> Scalar:
    return 4. / (1. + jnp.exp(-(v + 45.6) / 44.14))

  @classmethod
  def subunit_dynamics(
          cls, v: Scalar) -> Tuple[Float[Array, " subunit_dim"], Float[Array, " subunit_dim"]]:
    mt = cls.m_tau(v)
    A_diag = -  jnp.array([1. / mt]).reshape([1])
    b = jnp.array([cls.m_inf(v) / mt]).reshape([1])
    return A_diag, b

  @classmethod
  def resting_state(cls, v: Scalar) -> Float[Array, " subunit_dim"]:
    return jnp.array([cls.m_inf(v)]).reshape([1])


class Kv7(VoltageGatedIonChannel):

  subunit_dim: int = 1
  ion: Ion = Ion.K
  T: float = 34.

  @classmethod
  def activation(cls, subunit_states: Float[Array, " subunit_dim"]) -> Scalar:
    return subunit_states[0]

  @classmethod
  def alpha_m(cls, v: Scalar) -> Scalar:
    return 0.0033 * jnp.exp(0.1 * (v + 35.))

  @classmethod
  def beta_m(cls, v: Scalar) -> Scalar:
    return 0.0033 * jnp.exp(-0.1 * (v + 35.))

  @classmethod
  def subunit_dynamics(
          cls, v: Scalar) -> Tuple[Float[Array, " subunit_dim"], Float[Array, " subunit_dim"]]:
    q_t = jnp.power(2.3, (cls.T - 21.)/10.)
    am = cls.alpha_m(v)
    bm = cls.beta_m(v)
    A_diag = - q_t * jnp.array([am + bm]).reshape([1])
    b = q_t * jnp.array([am]).reshape([1])
    return A_diag, b

  @classmethod
  def resting_state(cls, v: Scalar) -> Float[Array, " subunit_dim"]:
    am = cls.alpha_m(v)
    bm = cls.beta_m(v)
    return jnp.array([am / (am + bm)]).reshape([1])


class CaLVA(VoltageGatedIonChannel):

  subunit_dim: int = 2
  ion: Ion = Ion.Ca
  T: float = 34.

  @classmethod
  def activation(cls, subunit_states: Float[Array, " subunit_dim"]) -> Scalar:
    return jnp.power(subunit_states[0], 2) * subunit_states[1]

  @classmethod
  def m_inf(cls, v: Scalar) -> Scalar:
    return 1. / (1. + jnp.exp(-(v + 40.) / 6.))

  @classmethod
  def m_tau(cls, v: Scalar) -> Scalar:
    return 5. + (20. / (1 + jnp.exp((v + 35.) / 5.)))

  @classmethod
  def h_inf(cls, v: Scalar) -> Scalar:
    return 1. / (1. + jnp.exp((v + 90.) / 6.4))

  @classmethod
  def h_tau(cls, v: Scalar) -> Scalar:
    return 20. + (50. /(1. + jnp.exp((v + 50.) / 7.)))

  @classmethod
  def subunit_dynamics(
          cls, v: Scalar) -> Tuple[Float[Array, " subunit_dim"], Float[Array, " subunit_dim"]]:
    q_t = jnp.power(2.3, (cls.T - 21.)/10.)
    mt = cls.m_tau(v)
    ht = cls.h_tau(v)
    A_diag = - q_t * jnp.array([1. / mt, 1./ht]).reshape([2])
    b = q_t * jnp.array([cls.m_inf(v) / mt, cls.h_inf(v) / ht]).reshape([2])
    return A_diag, b

  @classmethod
  def resting_state(cls, v: Scalar) -> Float[Array, " subunit_dim"]:
    mi = cls.m_inf(v)
    hi = cls.h_inf(v)
    return jnp.array([mi, hi]).reshape([2])


class CaHVA(VoltageGatedIonChannel):

  subunit_dim: int = 2
  ion: Ion = Ion.Ca

  @classmethod
  def activation(cls, subunit_states: Float[Array, " subunit_dim"]) -> Scalar:
    return jnp.power(subunit_states[0], 2) * subunit_states[1]

  @classmethod
  def m_alpha(cls, v: Scalar) -> Scalar:
    return (0.055 * 3.8) / exprel(-(v + 27.) / 3.8)

  @classmethod
  def m_beta(cls, v: Scalar) -> Scalar:
    return 0.94 * jnp.exp(- (v + 75.) / 17.)

  @classmethod
  def h_alpha(cls, v: Scalar) -> Scalar:
    return 0.000457 * jnp.exp(-(v + 13.) / 50.)

  @classmethod
  def h_beta(cls, v: Scalar) -> Scalar:
    return (0.0065 / (jnp.exp(-(v + 15.) / 28.) + 1.))

  @classmethod
  def subunit_dynamics(
          cls, v: Scalar) -> Tuple[Float[Array, " subunit_dim"], Float[Array, " subunit_dim"]]:
    ma = cls.m_alpha(v)
    mb = cls.m_beta(v)
    ha = cls.h_alpha(v)
    hb = cls.h_beta(v)
    A_diag = - jnp.array([ma + mb, ha + hb]).reshape([2])
    b = jnp.array([ma, ha]).reshape([2])
    return A_diag, b

  @classmethod
  def resting_state(cls, v: Scalar) -> Float[Array, " subunit_dim"]:
    ma = cls.m_alpha(v)
    mb = cls.m_beta(v)
    ha = cls.h_alpha(v)
    hb = cls.h_beta(v)
    return jnp.array([ma / (ma + mb), ha / (ha + hb)]).reshape([2])


class SK(CaGatedIonChannel):

  subunit_dim: int = 1
  ion: Ion = Ion.K

  @classmethod
  def activation(cls, subunit_states: Float[Array, " subunit_dim"]) -> Scalar:
    return subunit_states[0]

  @classmethod
  def z_inf(cls, cai: Scalar) -> Scalar:
    return  1./(1. + jnp.power(0.00043 / cai, 4.8))

  @classmethod
  def subunit_dynamics(
          cls,
          v: Scalar,
          cai: Scalar
          ) -> Tuple[Float[Array, " subunit_dim"], Float[Array, " subunit_dim"]]:
    del v
    zinf = cls.z_inf(cai)
    ztau = 1.
    A = jnp.array([-1. / ztau]).reshape([1])
    b = jnp.array([zinf / ztau]).reshape([1])
    return A, b

  @classmethod
  def resting_state(cls, v: Scalar, cai: Scalar) -> Float[Array, " subunit_dim"]:
    del v
    return jnp.array([cls.z_inf(cai)]).reshape([1])

class HCN(VoltageGatedIonChannel):

  subunit_dim: int = 1
  ion: Ion = Ion.NSC1

  @classmethod
  def activation(cls, subunit_states: Float[Array, " subunit_dim"]) -> Scalar:
    return subunit_states[0]

  @classmethod
  def m_alpha(cls, v: Scalar) -> Scalar:
    return (0.001 * 6.43 * 11.9) / exprel((v + 154.9) / 11.9)

  @classmethod
  def m_beta(cls, v: Scalar) -> Scalar:
    return 0.001 * 193. * jnp.exp(v / 33.1)

  @classmethod
  def subunit_dynamics(
          cls, v: Scalar) -> Tuple[Float[Array, " subunit_dim"], Float[Array, " subunit_dim"]]:
    ma = cls.m_alpha(v)
    mb = cls.m_beta(v)
    A_diag = - jnp.array([ma + mb]).reshape([1])
    b = jnp.array([ma]).reshape([1])
    return A_diag, b

  @classmethod
  def resting_state(cls, v: Scalar) -> Float[Array, " subunit_dim"]:
    ma = cls.m_alpha(v)
    mb = cls.m_beta(v)
    return jnp.array([ma / (ma + mb)]).reshape([1])


class OGHHPotassium(VoltageGatedIonChannel):

  subunit_dim: int = 1
  ion: Ion = Ion.K

  @classmethod
  def activation(cls, subunit_states: Float[Array, " subunit_dim"]) -> Scalar:
    return jnp.power(subunit_states[0], 4)

  @classmethod
  def alpha_n(cls, v: Scalar) -> Scalar:
    im = (10. - 65. - v) / 10.
    return .1 / exprel(im)

  @classmethod
  def beta_n(cls, v: Scalar) -> Scalar:
    return 0.125 * jnp.exp((-65. - v) / 80.)

  @classmethod
  def subunit_dynamics(
          cls, v: Scalar) -> Tuple[Float[Array, " subunit_dim"], Float[Array, " subunit_dim"]]:
    alpha = cls.alpha_n(v)
    beta = cls.beta_n(v)
    A_diag = - alpha - beta
    b = alpha
    return A_diag, b

  @classmethod
  def resting_state(cls, v: Scalar) -> Float[Array, " subunit_dim"]:
    na = cls.alpha_n(v)
    nb = cls.beta_n(v)
    return jnp.array([na / (na + nb)]).reshape([1])


class OGHHSodium(VoltageGatedIonChannel):

  subunit_dim: int = 2
  ion: Ion = Ion.Na

  @classmethod
  def activation(cls, subunit_states: Float[Array, " subunit_dim"]) -> Scalar:
    return jnp.power(subunit_states[0], 3) * subunit_states[1]

  @classmethod
  def alpha_m(cls, v: Scalar) -> Scalar:
    im = (25. - 65. - v) / 10.
    return 1. / exprel(im)

  @classmethod
  def alpha_h(cls, v: Scalar) -> Scalar:
    return 0.07 * jnp.exp((-65. - v) / 20.)

  @classmethod
  def beta_m(cls, v: Scalar) -> Scalar:
    return 4. * jnp.exp((-65. - v) / 18.)

  @classmethod
  def beta_h(cls, v: Scalar) -> Scalar:
    return 1. / (jnp.exp((30. - 65. - v) / 10.) + 1.)

  @classmethod
  def subunit_dynamics(
          cls, v: Scalar) -> Tuple[Float[Array, " subunit_dim"], Float[Array, " subunit_dim"]]:
    am = cls.alpha_m(v)
    bm = cls.beta_m(v)
    ah = cls.alpha_h(v)
    bh = cls.beta_h(v)
    A_diag = - jnp.array([am + bm, ah + bh]).reshape([2])
    b = jnp.array([am, ah]).reshape([2])
    return A_diag, b

  @classmethod
  def resting_state(cls, v: Scalar) -> Float[Array, " subunit_dim"]:
    am = cls.alpha_m(v)
    bm = cls.beta_m(v)
    ah = cls.alpha_h(v)
    bh = cls.beta_h(v)
    return jnp.array([am / (am + bm), ah / (ah + bh)]).reshape([2])


class ChannelGroup:

  state_dim: int
  channels: List[type[IonChannel]]

  def __init__(self, channels: List[type[IonChannel]]):
    self.state_dim = sum([c.subunit_dim for c in channels])
    self.channels = channels

  def resting_state(
          self,
          v: Union[Scalar, float],
          cai: Optional[Union[Scalar, float]]) -> Float[Array, " state_dim"]:
    """Compute the resting state of the channel group.

    Args:
      v: The resting voltage in millivolts.
      cai: The resting interior calcium ion concentration in millimolar. Can pass in None
        if there are no calcium-gated channels
    Returns:
      state: A vector of dimension state_dim, the resting state of all channels in the group.
    """
    states = []
    for c in self.channels:
      if issubclass(c, VoltageGatedIonChannel):
        states.append(c.resting_state(v))
      elif issubclass(c, CaGatedIonChannel):
        assert cai is not None
        states.append(c.resting_state(v, cai))
      else:
        assert False, f"Weird ion channel found, {c}" # Should never happen
    return jnp.concatenate(states, axis=0)

  def activation(self, state: Float[Array, " state_dim"]) -> Float[Array, " num_channels"]:
    """Compute the activation of each channel in the group.

    Args:
      state: The subunit state of the channel group.
    Returns:
      act: The activation of each channel.
    """
    sub_i = 0
    acts = []
    for channel in self.channels:
      channel_state = state[sub_i:sub_i + channel.subunit_dim]
      acts.append(channel.activation(channel_state))
      sub_i += channel.subunit_dim
    all_acts = jnp.stack(acts).reshape(len(self.channels))
    return all_acts

  def state_dynamics(
          self,
          v: Scalar,
          cai: Optional[Scalar]
          ) -> Tuple[Float[Array, " state_dim"], Float[Array, " state_dim"]]:
    """Compute the conditionally linear dynamics of the channel states in the group.

    Args:
      v: The voltage in millivolts.
      cai: The calcium ion concentration, in millimolar. Can pass in None if there are
        no calcium-gated channels.
    Returns:
      A_diag: The diagonal of the A matrix in the linear ODE.
      b: The drift term in the linear ODE.
    """
    outs = []
    for c in self.channels:
      if issubclass(c, VoltageGatedIonChannel):
        outs.append(c.subunit_dynamics(v))
      elif issubclass(c, CaGatedIonChannel):
        assert cai is not None
        outs.append(c.subunit_dynamics(v, cai))
      else:
        assert False, f"Weird ion channel found, {c}" # Should never happen
    A_diag = jnp.concatenate([o[0] for o in outs], axis=0)
    b = jnp.concatenate([o[1] for o in outs], axis=0)
    return A_diag, b

  def reversal_potentials(
          self,
          ion_reversals: Dict[Ion, Scalar]
          ) -> Float[Array, " num_channels"]:
    pots = []
    for c in self.channels:
      pots.append(ion_reversals[c.ion])
    return jnp.stack(pots).reshape([len(self.channels)])

  def ca_mask(self) -> Float[Array, " num_channels"]:
    pots = []
    for c in self.channels:
      pots.append(c.ion == Ion.Ca)
    return jnp.stack(pots).reshape([len(self.channels)]) * 1.


ALLEN_CHANNEL_NAMES = {
  "Im": Kv7,
  "Ih": HCN,
  "NaTs": NaTs,
  "Nap": NaP,
  "K_P": KP,
  "K_T": KT,
  "SK": SK,
  "Kv3_1": Kv3,
  "Ca_HVA": CaHVA,
  "Ca_LVA": CaLVA
}

ALLEN_ION_NAMES = {
  "na": Ion.Na,
  "k": Ion.K,
  "ca": Ion.Ca,
  "nsc1": Ion.NSC1
}
