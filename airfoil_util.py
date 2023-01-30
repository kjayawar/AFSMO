import numpy as np

def translate_le_to_origin(points):
	"""
	accepts a list of points in a form of 2d numpy array[[x1,y1], [x2,y2], ...]
	Translates the points such that the LE sits on the origin [0,0]
	"""
	le = points[points[:,0].argmin()]
	le_offset = 0 - le
	return points + le_offset

def find_te_point(points):
	"""
	airfoil TE could have finite thickness and hence,
	its best to calculate the midpoint of the upper and lower
	TE points to find the actual TE coordinate instead of choosing
	the point with largest x value
	"""
	return (points[0] + points[-1])/2

def de_rotate(points, te_point, te_target=(1,0)):
	"""
	Instead of using 2x2 rotation matrix to rotate each point about origin,
	its easier to use complex numbers. Because complex transformation allows
	to do rotation in one go plus scaling is automatically been taken care of.
	https://math.stackexchange.com/a/2119532/759148
	"""
	cmplx_points = np.array([complex(x,y) for x,y in points])
	e_iθ = complex(*te_target) / complex(*te_point)
	derotated = cmplx_points * e_iθ
	return derotated.real, derotated.imag

def normalize_airfoil(points):
	""" Scales the airfoil for unit chord and de-rotates """
	points = translate_le_to_origin(points)
	return de_rotate(points, find_te_point(points))
