import jax
import jax.numpy as jnp


def _simple_exprel(x):
  return jnp.expm1(x) / x


@jax.custom_jvp
def exprel(x):
  return jnp.where(jnp.equal(x, 0.), jnp.array(1.), _simple_exprel(x))


@exprel.defjvp
def jax_exprel_jvp(xs, x_dots):
  x = xs[0]
  x_dot = x_dots[0]
  primal_out = exprel(x)
  tangent_out = jnp.where(
      jnp.less_equal(jnp.abs(x), 1e-2),
      0.5 + (x / 3.) + jnp.square(x) / 8.,
      jnp.vectorize(jax.grad(_simple_exprel))(x))
  return primal_out, tangent_out * x_dot
