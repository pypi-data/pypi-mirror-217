import numpy as np

def rot_z_axis(v, pts):
  v_fr = np.array((0., 0., 1.))
  if np.all(v == v_fr):
    return pts
  v_to = v / np.linalg.norm(v)
  cos_theta = v_to[2]
  # if v_fr x v_to = (0,0,1) x (a, b, c) = (-b, a, 0)
  # ||v_fr x v_to|| = sqrt(b^2 + a^2)
  sin_theta = np.linalg.norm(v_to[:2])
  G = np.array([[cos_theta, -sin_theta, 0.],
                [sin_theta, cos_theta, 0.],
                [0., 0., 1.]])

  u = v_fr
  v_unnorm = np.array([v_to[0], v_to[1], 0.])
  v = v_unnorm / np.linalg.norm(v_unnorm)
  # if v_to x v_fr = (a, b, c) x (0,0,1) = (b, -a, 0)
  w =  np.array([v_to[1], -v_to[0], 0.])
  F_inv = np.column_stack((u, v, w))
  return (F_inv @ G @ np.linalg.solve(F_inv, pts.T)).T


def circle(center, normal, radius, resolution):
  pts = np.empty([resolution, 3])
  for i in range(resolution):
    theta = (i * 2. * np.pi) / resolution
    pts[i,:] = radius * np.array((np.cos(theta), np.sin(theta), 0.))
  # Rotate to normal
  pts = rot_z_axis(normal, pts)
  # Add center
  pts += center[np.newaxis, :]
  return pts
