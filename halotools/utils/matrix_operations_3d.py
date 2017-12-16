"""
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
from astropy.utils.misc import NumpyRNGContext


__all__ = ('elementwise_dot', 'elementwise_norm', 'normalized_vectors',
            'angles_between_list_of_vectors')


def elementwise_dot(x, y):
    """ Calculate the dot product between
    each pair of elements in two input lists of 3d points.

    Parameters
    ----------
    x : ndarray
        Numpy array of shape (npts, 3) storing a collection of 3d points

    y : ndarray
        Numpy array of shape (npts, 3) storing a collection of 3d points

    Returns
    -------
    result : ndarray
        Numpy array of shape (npts, ) storing the dot product between each
        pair of corresponding points in x and y.

    Examples
    --------
    >>> npts = int(1e3)
    >>> x = np.random.random((npts, 3))
    >>> y = np.random.random((npts, 3))
    >>> dots = elementwise_dot(x, y)
    """
    x = np.atleast_2d(x)
    y = np.atleast_2d(y)
    return np.sum(x*y, axis=1)


def elementwise_norm(x):
    """ Calculate the normalization of each element in a list of 3d points.

    Parameters
    ----------
    x : ndarray
        Numpy array of shape (npts, 3) storing a collection of 3d points

    Returns
    -------
    result : ndarray
        Numpy array of shape (npts, ) storing the norm of each 3d point in x.

    Examples
    --------
    >>> npts = int(1e3)
    >>> x = np.random.random((npts, 3))
    >>> norms = elementwise_norm(x)
    """
    x = np.atleast_2d(x)
    return np.sqrt(np.sum(x**2, axis=1))


def normalized_vectors(vectors):
    """ Return a unit-vector for each 3d vector in the input list of 3d points.

    Parameters
    ----------
    x : ndarray
        Numpy array of shape (npts, 3) storing a collection of 3d points

    Returns
    -------
    normed_x : ndarray
        Numpy array of shape (npts, 3)

    Examples
    --------
    >>> npts = int(1e3)
    >>> x = np.random.random((npts, 3))
    >>> normed_x = normalized_vectors(x)
    """
    vectors = np.atleast_2d(vectors)
    npts = vectors.shape[0]
    return vectors/elementwise_norm(vectors).reshape((npts, -1))


def angles_between_list_of_vectors(v0, v1, tol=1e-3):
    """ Calculate the angle between a collection of 3d vectors

    Examples
    --------
    v0 : ndarray
        Numpy array of shape (npts, 3) storing a collection of 3d vectors

        Note that the normalization of `v0` will be ignored.

    v1 : ndarray
        Numpy array of shape (npts, 3) storing a collection of 3d vectors

        Note that the normalization of `v1` will be ignored.

    tol : float, optional
        Acceptable numerical error for errors in angle.
        This variable is only used to round off numerical noise that otherwise
        causes exceptions to be raised by the inverse cosine function.
        Default is 0.001.

    Returns
    -------
    angles : ndarray
        Numpy array of shape (npts, ) storing the angles between each pair of
        corresponding points in v0 and v1.

        Returned values are in units of radians spanning [0, pi].

    Examples
    --------
    >>> npts = int(1e4)
    >>> v0 = np.random.random((npts, 3))
    >>> v1 = np.random.random((npts, 3))
    >>> angles = angles_between_list_of_vectors(v0, v1)
    """
    dot = elementwise_dot(normalized_vectors(v0), normalized_vectors(v1))

    #  Protect against tiny numerical excesses beyond the range [-1 ,1]
    mask1 = (dot > 1) & (dot < 1 + tol)
    dot = np.where(mask1, 1., dot)
    mask2 = (dot < -1) & (dot > -1 - tol)
    dot = np.where(mask2, -1., dot)

    return np.arccos(dot)
