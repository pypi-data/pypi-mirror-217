def angle_0_360(v1, v2, reference_direction):
    v1 = v1 / numpy.linalg.norm(v1)
    v2 = v2 / numpy.linalg.norm(v2)
    cos_theta = numpy.dot(v1, v2)
    sin_theta = numpy.sign(numpy.dot(numpy.cross(v1, v2), reference_direction)) * numpy.linalg.norm(numpy.cross(v1, v2))
    atg = numpy.degrees(numpy.arctan2(sin_theta, cos_theta))
    if atg < 0:
        theta = atg + 360
    else:
        theta = atg
    return theta

h = np.array([0, 25, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140,
              150, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800,
              900, 1000])
r = np.array([1.225, 4.008e-2, 1.841e-2, 3.996e-3, 1.027e-3, 3.097e-4, 8.283e-5,
              1.846e-5, 3.416e-6, 5.606e-7, 9.708e-8, 2.222e-8, 8.152e-9, 3.831e-9,
              2.076e-9, 5.194e-10, 2.541e-10, 6.073e-11, 1.916e-11, 7.014e-12,
              2.803e-12, 1.184e-12, 5.215e-13, 1.137e-13, 3.070e-14, 1.136e-14,
              5.759e-15, 3.561e-15])
H = np.array([7.310, 6.427, 6.546, 7.360, 8.342, 7.583, 6.661, 5.927, 5.533,
              5.703, 6.782, 9.973, 13.243, 16.322, 21.652, 27.974, 34.934,
              43.342, 49.755, 54.513, 58.019, 60.980, 65.654, 76.377, 100.587,
              147.203, 208.020])

def atmopshere(height):
    if height > 1000:
        height = 1000
    elif height < 0:
        height = 0
    i = 1
    for j in range(27):
        if height >= h[j] and height < h[j + 1]:
            i = j
    if height == 1000:
        i = 27
    density = r[i] * np.exp(-(height - h[i]) / H[i])
    return density

def orb_elems_from_rv(r, v, mu):
    h = np.cross(r, v)
    B = np.cross(v, h) - mu * r / np.linalg.norm(r)
    N = np.cross(np.array([0, 0, 1]), h)
    Omega = angle_0_360(np.array([1, 0, 0]), N, np.array([0, 0, 1]))
    i = np.degrees(np.arccos(h[2] / np.linalg.norm(h)))
    omega = np.degrees(np.arccos(np.dot(N, B) / (np.linalg.norm(N) * np.linalg.norm(B))))
    nu = angle_0_360(B, r, np.array([0, 0, 1]))
    a = -mu / (2 * ((np.dot(v, v) / 2) - mu / np.linalg.norm(r)))
    e = np.linalg.norm(B / mu)

    return Omega, i, omega, nu, a, e


def rv_from_orb_elems(a, e, i, Omega, omega, ni, mu):
    p = a * (1 - e ** 2)
    r_perifocal = p / (1 + e * np.cos(np.radians(ni))) * np.array([
        np.cos(np.radians(ni)),
        np.sin(np.radians(ni)),
        0])
    v_perifocal = np.sqrt(mu / p) * np.array([
        -np.sin(np.radians(ni)),
        e + np.cos(np.radians(ni)),
        0])
    perifocal_equatorial = np.dot(np.dot(np.array([
        [-np.sin(np.radians(Omega)), np.cos(np.radians(Omega)), 0],
        [np.cos(np.radians(Omega)), np.sin(np.radians(Omega)), 0],
        [0, 0, 1]]), np.array([[1, 0, 0], [0, np.cos(np.radians(i)), -np.sin(np.radians(i))], [0, np.sin(np.radians(i)), np.cos(np.radians(i))]])),
        np.array([[np.cos(np.radians(omega)), -np.sin(np.radians(omega)), 0],[np.sin(np.radians(omega)), np.cos(np.radians(omega)), 0],[0, 0, 1]]))

    r = np.dot(perifocal_equatorial, r_perifocal)
    v = np.dot(perifocal_equatorial, v_perifocal)
    return r, v