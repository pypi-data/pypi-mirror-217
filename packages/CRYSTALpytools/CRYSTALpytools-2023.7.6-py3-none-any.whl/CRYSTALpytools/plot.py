#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions to visualize CRYSTAL outputs.
"""
def plot_vecfield2D_m(header, dens, quivscale, name='MAG', levels=150, dpi=400):
    """
    Plots the 2D magnetization vector field.

    Args:
        header (list): List containing information about the fort.25 header.
        dens (numpy.ndarray): Array containing the vector field data.
        quivscale (float): Scale factor for the quiver plot.
        name (str, optional):  Name used for saving the plots.
        levels (int or array-like, optional): Determines the number and positions of the contour lines/regions.
        dpi (int, optional): DPI (dots per inch) for the output image. Default is 400.

    Returns:
        None
    """
    import matplotlib.pyplot as plt
    import numpy as np

    for i in range(2, 20):
        if (header[0] % i) == 0:
            nrow_split = int(header[0]/i)

    for i in range(2, 20):
        if (header[1] % i) == 0:
            ncol_split = int(header[1]/i)

    # initializes the arrays
    projx_m = np.zeros((nrow_split, ncol_split), dtype=float)
    projy_m = np.zeros((nrow_split, ncol_split), dtype=float)
    mod_m = np.zeros((header[0], header[1]), dtype=float)

    # Generates the meshgrid
    mesh_x = np.zeros((header[0], header[1]), dtype=float)
    mesh_y = np.zeros((header[0], header[1]), dtype=float)
    mesh_projx = np.zeros((nrow_split, ncol_split), dtype=float)
    mesh_projy = np.zeros((nrow_split, ncol_split), dtype=float)

    T = np.array([[np.sqrt(1 - header[4]**2)*header[2], 0],
                  [header[4]*header[2], header[3]]])  # Change of basis matrix

    for i in range(0, header[0]):
        for j in range(0, header[1]):
            mesh_x[i, j] = np.dot(T, np.array([i, j]))[0]
            mesh_y[i, j] = np.dot(T, np.array([i, j]))[1]

    mesh_x = mesh_x * 0.529177249  # Bohr to Angstrom conversion
    mesh_y = mesh_y * 0.529177249

    r = 0
    s = 0
    step_nrow = int(header[0]/nrow_split)
    step_ncol = int(header[1]/ncol_split)
    for i in range(0, nrow_split):
        for j in range(0, ncol_split):
            mesh_projx[i, j] = mesh_x[r, s]
            mesh_projy[i, j] = mesh_y[r, s]
            s += step_ncol
        s = 0
        r += step_nrow

    # Creates the orthogonal vectorial basis for the projections
    CB = header[7] - header[6]
    BA = header[6] - header[5]
    if header[4] == 0:
        mod_BA = np.sqrt(BA[0]**2 + BA[1]**2 + BA[2]**2)
        mod_CB = np.sqrt(CB[0]**2 + CB[1]**2 + CB[2]**2)
        v1 = BA/mod_BA
        v2 = CB/mod_CB
    else:
        BA = BA - ((np.dot(BA, CB))/(np.dot(BA, BA)))*CB
        mod_BA = np.sqrt(BA[0]**2 + BA[1]**2 + BA[2]**2)
        mod_CB = np.sqrt(CB[0]**2 + CB[1]**2 + CB[2]**2)
        v1 = BA/mod_BA
        v2 = CB/mod_CB

    # Calculates the modulus of the vectorial field
    for i in range(0, header[0]):
        for j in range(0, header[1]):
            mod_m[i, j] = np.sqrt((dens[i, j, 0]**2) +
                                  (dens[i, j, 1]**2)+(dens[i, j, 2]**2))

    # Calculates the projections of the vectors in the ABC plane
    ABC_normal = np.cross(BA, CB)
    mod_normal = np.sqrt(ABC_normal[0]**2 +
                         ABC_normal[1]**2 + ABC_normal[2]**2)

    for i in range(0, nrow_split):
        for j in range(0, ncol_split):
            projx_m[i, j] = np.dot((1/(mod_normal**2))*np.cross(ABC_normal,
                                                                np.cross(np.array([dens[int(i*step_nrow), int(j*step_ncol), 0], dens[int(i*step_nrow), int(j*step_ncol), 1],
                                                                                   dens[int(i*step_nrow), int(j*step_ncol), 2]]), ABC_normal)), v2)
            projy_m[i, j] = np.dot((1/(mod_normal**2))*np.cross(ABC_normal,
                                                                np.cross(np.array([dens[int(i*step_nrow), int(j*step_ncol, 0)], dens[int(i*step_nrow), int(j*step_ncol), 1],
                                                                                   dens[int(i*step_nrow), int(j*step_ncol), 2]]), ABC_normal)), v1)

    # Plotting

    m = plt.figure()
    m = plt.contourf(mesh_x, mesh_y, mod_m, levels, cmap='cool')
    m = plt.colorbar(mappable=m)
    m = plt.quiver(mesh_projx, mesh_projy, projx_m, projy_m, scale=quivscale)
    m = plt.xlabel('$\AA$')
    m = plt.ylabel('$\AA$')
    m = plt.savefig(name, dpi=dpi)

    plt.show()


def plot_vecfield2D_j(header, dens, quivscale, name='SC', levels=150, dpi=400):
    """
    Plots the 2D vector field of the spin current.

    Args:
        header (list): List containing information about the fort.25 header.
        dens (numpy.ndarray): Array representing the vector field.
        quivscale (float): Scale factor for the quiver plot.
        name (str, optional):  Name used for saving the plots.
        levels (int or array-like, optional): Determines the number and positions of the contour lines/regions.
        dpi (int, optional): DPI (dots per inch) for the output image. Defaults to 400.

    Returns:
        None
    """
    import matplotlib.pyplot as plt
    import numpy as np

    for i in range(2, 20):
        if (header[0] % i) == 0:
            nrow_split = int(header[0]/i)

    for i in range(2, 20):
        if (header[1] % i) == 0:
            ncol_split = int(header[1]/i)

    # initializes the arrays
    projx_j = np.zeros((nrow_split, ncol_split), dtype=float)
    projy_j = np.zeros((nrow_split, ncol_split), dtype=float)
    mod_j = np.zeros((header[0], header[1]), dtype=float)

    # Generates the meshgrid
    mesh_x = np.zeros((header[0], header[1]), dtype=float)
    mesh_y = np.zeros((header[0], header[1]), dtype=float)
    mesh_projx = np.zeros((nrow_split, ncol_split), dtype=float)
    mesh_projy = np.zeros((nrow_split, ncol_split), dtype=float)

    T = np.array([[np.sqrt(1 - header[4]**2)*header[2], 0],
                  [header[4]*header[2], header[3]]])  # Change of basis matrix

    for i in range(0, header[0]):
        for j in range(0, header[1]):
            mesh_x[i, j] = np.dot(T, np.array([i, j]))[0]
            mesh_y[i, j] = np.dot(T, np.array([i, j]))[1]

    mesh_x = mesh_x * 0.529177249  # Bohr to Angstrom conversion
    mesh_y = mesh_y * 0.529177249

    r = 0
    s = 0
    step_nrow = int(header[0]/nrow_split)
    step_ncol = int(header[1]/ncol_split)
    for i in range(0, nrow_split):
        for j in range(0, ncol_split):
            mesh_projx[i, j] = mesh_x[r, s]
            mesh_projy[i, j] = mesh_y[r, s]
            s += step_ncol
        s = 0
        r += step_nrow

    # Creates the orthogonal vectorial basis for the projections
    CB = header[7] - header[6]
    BA = header[6] - header[5]
    if header[4] == 0:
        mod_BA = np.sqrt(BA[0]**2 + BA[1]**2 + BA[2]**2)
        mod_CB = np.sqrt(CB[0]**2 + CB[1]**2 + CB[2]**2)
        v1 = BA/mod_BA
        v2 = CB/mod_CB
    else:
        BA = BA - ((np.dot(BA, CB))/(np.dot(BA, BA)))*CB
        mod_BA = np.sqrt(BA[0]**2 + BA[1]**2 + BA[2]**2)
        mod_CB = np.sqrt(CB[0]**2 + CB[1]**2 + CB[2]**2)
        v1 = BA/mod_BA
        v2 = CB/mod_CB

    # Calculates the modulus of the vectorial field
    for i in range(0, header[0]):
        for j in range(0, header[1]):
            mod_j[i, j] = np.sqrt((dens[i, j, 0]**2) +
                                  (dens[i, j, 1]**2)+(dens[i, j, 2]**2))

    # Calculates the projections of the vectors in the ABC plane
    ABC_normal = np.cross(BA, CB)
    mod_normal = np.sqrt(ABC_normal[0]**2 +
                         ABC_normal[1]**2 + ABC_normal[2]**2)

    for i in range(0, nrow_split):
        for j in range(0, ncol_split):
            projx_j[i, j] = np.dot((1/(mod_normal**2))*np.cross(ABC_normal,
                                                                np.cross(np.array([dens[int(i*step_nrow), int(j*step_ncol), 0], dens[int(i*step_nrow), int(j*step_ncol), 1],
                                                                                   dens[int(i*step_nrow), int(j*step_ncol), 2]]), ABC_normal)), v2)
            projy_j[i, j] = np.dot((1/(mod_normal**2))*np.cross(ABC_normal,
                                                                np.cross(np.array([dens[int(i*step_nrow), int(j*step_ncol), 0], dens[int(i*step_nrow), int(j*step_ncol), 1],
                                                                                   dens[int(i*step_nrow), int(j*step_ncol), 2]]), ABC_normal)), v1)

    j = plt.figure()
    j = plt.contourf(mesh_x, mesh_y, mod_j, levels, cmap='winter')
    j = plt.colorbar(mappable=j)
    j = plt.quiver(mesh_projx, mesh_projy, projx_j, projy_j, scale=quivscale)
    j = plt.xlabel('$\AA$')
    j = plt.ylabel('$\AA$')
    j = plt.savefig(name, dpi=dpi)

    plt.show()


def plot_vecfield2D_J(header, dens_JX, dens_JY, dens_JZ, quivscale, name='SCD', levels=150, dpi=400):
    """
    Plots the 2D spin current density vector fields.

    Args:
        header (list): List containing information about the fort.25 header.
        dens_JX (numpy.ndarray): Array representing the X-component of the spin current density.
        dens_JY (numpy.ndarray): Array representing the Y-component of the spin current density.
        dens_JZ (numpy.ndarray): Array representing the Z-component of the spin current density.
        quivscale: Scale factor for the quiver plot.
        name (str, optional): Name used for saving the plots.
        levels (int or array-like, optional): Determines the number and positions of the contour lines/regions.
        dpi (int, optional): DPI (Dots per inch) for saving the plots. Defaults to 400.

    Returns:
        None
    """
    import matplotlib.pyplot as plt
    import numpy as np

    for i in range(2, 20):
        if (header[0] % i) == 0:
            nrow_split = int(header[0]/i)

    for i in range(2, 20):
        if (header[1] % i) == 0:
            ncol_split = int(header[1]/i)

    # initializes the arrays
    projx_JX = np.zeros((nrow_split, ncol_split), dtype=float)
    projy_JX = np.zeros((nrow_split, ncol_split), dtype=float)
    mod_JX = np.zeros((header[0], header[1]), dtype=float)
    projx_JY = np.zeros((nrow_split, ncol_split), dtype=float)
    projy_JY = np.zeros((nrow_split, ncol_split), dtype=float)
    mod_JY = np.zeros((header[0], header[1]), dtype=float)
    projx_JZ = np.zeros((nrow_split, ncol_split), dtype=float)
    projy_JZ = np.zeros((nrow_split, ncol_split), dtype=float)
    mod_JZ = np.zeros((header[0], header[1]), dtype=float)

    # Generates the meshgrid
    mesh_x = np.zeros((header[0], header[1]), dtype=float)
    mesh_y = np.zeros((header[0], header[1]), dtype=float)
    mesh_projx = np.zeros((nrow_split, ncol_split), dtype=float)
    mesh_projy = np.zeros((nrow_split, ncol_split), dtype=float)

    T = np.array([[np.sqrt(1 - header[4]**2)*header[2], 0],
                  [header[4]*header[2], header[3]]])  # Change of basis matrix

    for i in range(0, header[0]):
        for j in range(0, header[1]):
            mesh_x[i, j] = np.dot(T, np.array([i, j]))[0]
            mesh_y[i, j] = np.dot(T, np.array([i, j]))[1]

    mesh_x = mesh_x * 0.529177249  # Bohr to Angstrom conversion
    mesh_y = mesh_y * 0.529177249

    r = 0
    s = 0
    step_nrow = int(header[0]/nrow_split)
    step_ncol = int(header[1]/ncol_split)
    for i in range(0, nrow_split):
        for j in range(0, ncol_split):
            mesh_projx[i, j] = mesh_x[r, s]
            mesh_projy[i, j] = mesh_y[r, s]
            s += step_ncol
        s = 0
        r += step_nrow

    # Creates the orthogonal vectorial basis for the projections
    CB = header[7] - header[6]
    BA = header[6] - header[5]
    if header[4] == 0:
        mod_BA = np.sqrt(BA[0]**2 + BA[1]**2 + BA[2]**2)
        mod_CB = np.sqrt(CB[0]**2 + CB[1]**2 + CB[2]**2)
        v1 = BA/mod_BA
        v2 = CB/mod_CB
    else:
        BA = BA - ((np.dot(BA, CB))/(np.dot(BA, BA)))*CB
        mod_BA = np.sqrt(BA[0]**2 + BA[1]**2 + BA[2]**2)
        mod_CB = np.sqrt(CB[0]**2 + CB[1]**2 + CB[2]**2)
        v1 = BA/mod_BA
        v2 = CB/mod_CB

    # Calculates the modulus of the vectorial field
    for i in range(0, header[0]):
        for j in range(0, header[1]):
            mod_JX[i, j] = np.sqrt(
                (dens_JX[i, j, 0]**2)+(dens_JX[i, j, 1]**2)+(dens_JX[i, j, 2]**2))
            mod_JY[i, j] = np.sqrt(
                (dens_JY[i, j, 0]**2)+(dens_JY[i, j, 1]**2)+(dens_JY[i, j, 2]**2))
            mod_JZ[i, j] = np.sqrt(
                (dens_JZ[i, j, 0]**2)+(dens_JZ[i, j, 1]**2)+(dens_JZ[i, j, 2]**2))

    # Calculates the projections of the vectors in the ABC plane
    ABC_normal = np.cross(BA, CB)
    mod_normal = np.sqrt(ABC_normal[0]**2 +
                         ABC_normal[1]**2 + ABC_normal[2]**2)

    for i in range(0, nrow_split):
        for j in range(0, ncol_split):
            projx_JX[i, j] = np.dot((1/(mod_normal**2))*np.cross(ABC_normal,
                                    np.cross(np.array([dens_JX[int(i*step_nrow), int(j*step_ncol), 0], dens_JX[int(i*step_nrow), int(j*step_ncol), 1],
                                                       dens_JX[int(i*step_nrow), int(j*step_ncol), 2]]), ABC_normal)), v2)
            projy_JX[i, j] = np.dot((1/(mod_normal**2))*np.cross(ABC_normal,
                                    np.cross(np.array([dens_JX[int(i*step_nrow), int(j*step_ncol), 0], dens_JX[int(i*step_nrow), int(j*step_ncol), 1],
                                                       dens_JX[int(i*step_nrow), int(j*step_ncol), 2]]), ABC_normal)), v1)
            projx_JY[i, j] = np.dot((1/(mod_normal**2))*np.cross(ABC_normal,
                                    np.cross(np.array([dens_JY[int(i*step_nrow), int(j*step_ncol), 0], dens_JY[int(i*step_nrow), int(j*step_ncol), 1],
                                                       dens_JY[int(i*step_nrow), int(j*step_ncol), 2]]), ABC_normal)), v2)
            projy_JY[i, j] = np.dot((1/(mod_normal**2))*np.cross(ABC_normal,
                                    np.cross(np.array([dens_JY[int(i*step_nrow), int(j*step_ncol), 0], dens_JY[int(i*step_nrow), int(j*step_ncol), 1],
                                                       dens_JY[int(i*step_nrow), int(j*step_ncol), 2]]), ABC_normal)), v1)
            projx_JZ[i, j] = np.dot((1/(mod_normal**2))*np.cross(ABC_normal,
                                    np.cross(np.array([dens_JZ[int(i*step_nrow), int(j*step_ncol), 0], dens_JZ[int(i*step_nrow), int(j*step_ncol), 1],
                                                       dens_JZ[int(i*step_nrow), int(j*step_ncol), 2]]), ABC_normal)), v2)
            projy_JZ[i, j] = np.dot((1/(mod_normal**2))*np.cross(ABC_normal,
                                    np.cross(np.array([dens_JZ[int(i*step_nrow), int(j*step_ncol), 0], dens_JZ[int(i*step_nrow), int(j*step_ncol), 1],
                                                       dens_JZ[int(i*step_nrow), int(j*step_ncol), 2]]), ABC_normal)), v1)

    # Plotting

    JX = plt.figure()
    JX = plt.contourf(mesh_x, mesh_y, mod_JX, levels, cmap='summer')
    JX = plt.colorbar(mappable=JX)
    JX = plt.quiver(mesh_projx, mesh_projy, projx_JX,
                    projy_JX, scale=quivscale)
    JX = plt.xlabel('$\AA$')
    JX = plt.ylabel('$\AA$')
    JX = plt.savefig(name+'_JX', dpi=dpi)

    JY = plt.figure()
    JY = plt.contourf(mesh_x, mesh_y, mod_JY, levels, cmap='summer')
    JY = plt.colorbar(mappable=JY)
    JY = plt.quiver(mesh_projx, mesh_projy, projx_JY,
                    projy_JY, scale=quivscale)
    JY = plt.xlabel('$\AA$')
    JY = plt.ylabel('$\AA$')
    JY = plt.savefig(name+'_JY', dpi=dpi)

    JZ = plt.figure()
    JZ = plt.contourf(mesh_x, mesh_y, mod_JZ, levels, cmap='summer')
    JZ = plt.colorbar(mappable=JZ)
    JZ = plt.quiver(mesh_projx, mesh_projy, projx_JZ,
                    projy_JZ, scale=quivscale)
    JZ = plt.xlabel('$\AA$')
    JZ = plt.ylabel('$\AA$')
    JZ = plt.savefig(name+'_JZ', dpi=dpi)

    plt.show()


def plot_phonon_band(bands, unit='cm-1', k_labels=None, mode='single',
                     not_scaled=False, energy_range=None, k_range=None,
                     color='blue', labels=None, linestl='-', linewidth=1,
                     line_freq0=None, title=None, figsize=None,
                     scheme=None, sharex=True, sharey=True, save_to_file=None):
    """
    A wrapper of plot_cry_bands for phonon band structure.

    Args:
        bands (BandsBASE|list): Bands object generated by `CRYSTALpytools.crystal_io.Crystal_output.read_pband` or
            a list of BandsBASE objects.
        unit (str): The unit of frequency. Can be 'cm-1' or 'THz'.
        k_labels (list): A list of high-symmetric k point labels. Greek alphabets should be, for example, 'Gamma'.
        mode (str): The plotting mode. Possible values are 'single', 'multi', 'compare', and 'surface'.
        not_scaled (bool): Whether to scale the x-axis for different volumes.
        energy_range (array): A 2x1 array specifying the energy range.
        k_range (array): A 2x1 array specifying the k-range.
        color (str|list): Color of plot lines. Should be consistent with bands.
        labels (str|list): Plot legend. Should be consistent with bands.
        linestl (str|list): Linestyle string. Should be consistent with bands.
        linewidth (float): The width of the plot lines.
        line_freq0 (str): The color of the frequency=0 line.
        title (str): The title of the plot.
        figsize (list): The figure size specified as [width, height].
        scheme (list|tuple): The layout of subplots.
        sharex (bool): Whether to share the x-axis among subplots.
        sharey (bool): Whether to share the y-axis among subplots.
        save_to_file (str): The file name to save the plot.

    Returns:
        None

    Raises:
        ValueError: If the specified unit is unknown.

    """
    import matplotlib.pyplot as plt
    from CRYSTALpytools.units import thz_to_cm, cm_to_thz
    import re

    if re.match(r'^cm\-1$', unit, re.IGNORECASE):
        unit = 'cm-1'
        is_thz = False
    elif re.match(r'^THz$', unit, re.IGNORECASE):
        unit = 'THz'
        is_thz = True
    else:
        raise ValueError('Unknown unit.')


    if not (isinstance(bands, list) or isinstance(bands, tuple)):
        bands = [bands]

    if line_freq0 == None:
        line_freq0 = (1., 0., 0., 0.) # Transparent

    for b in bands:
        if unit != b.unit:
            if unit == 'cm-1':
                b.bands[:, :, :] = thz_to_cm(b.bands[:, :, :])
            else:
                b.bands[:, :, :] = cm_to_thz(b.bands[:, :, :])
            b.unit = unit
    if len(bands) == 1:
        bands = bands[0]

    fig = plot_cry_bands(bands, k_labels=k_labels, energy_range=energy_range, title=title,
                         not_scaled=not_scaled, mode=mode, linestl=linestl, linewidth=linewidth,
                         color=color, fermi=line_freq0, k_range=k_range, labels=labels,
                         figsize=figsize, scheme=scheme, sharex=sharex, sharey=sharey)
    if is_thz == True:
        fig.supylabel('Frequency (THz)')
    else:
        fig.supylabel('Frequency (cm$^{-1}$)')

    if save_to_file != None:
        save_plot(save_to_file)

    plt.show()


def plot_electron_band(bands, unit='eV', k_labels=None, mode='single',
                       not_scaled=False, energy_range=None, k_range=None,
                       color='blue', labels=None, linestl='-', linewidth=1,
                       fermi='forestgreen', title=None, figsize=None,
                       scheme=None, sharex=True, sharey=True, save_to_file=None):
    """
    A wrapper of plot_cry_bands for electron band structure.

    Args:
        bands (BandsBASE|list): Bands object generated by `CRYSTALpytools.crystal_io.Properties_output.read_bands` or
            a list of BandsBASE objects.
        unit (str): The unit of energy. Can be 'eV' or 'Hartree'.
        k_labels (list): A list of high-symmetric k point labels. Greek alphabets should be, for example, 'Gamma'.
        mode (str): The plotting mode. Possible values are 'single', 'multi', 'compare', and 'surface'.
        not_scaled (bool): Whether to scale the x-axis for different volumes.
        energy_range (array): A 2x1 array specifying the energy range.
        k_range (array): A 2x1 array specifying the k-range.
        color (str|list): Color of plot lines. Should be consistent with bands.
        labels (str|list): Plot legend. Should be consistent with bands.
        linestl (str|list): Linestyle string. Should be consistent with bands.
        linewidth (float): The width of the plot lines.
        fermi (str): The color of the Fermi level line.
        title (str): The title of the plot.
        figsize (list): The figure size specified as [width, height].
        scheme (list|tuple): The layout of subplots.
        sharex (bool): Whether to share the x-axis among subplots.
        sharey (bool): Whether to share the y-axis among subplots.
        save_to_file (str): The file name to save the plot.

    Returns:
        None

    Raises:
        ValueError: If the specified unit is unknown.

    """
    import matplotlib.pyplot as plt
    from CRYSTALpytools.units import eV_to_H, H_to_eV
    import re

    if re.match(r'^eV$', unit, re.IGNORECASE):
        unit = 'eV'
        is_ev = True
    elif re.match(r'^Hartree$', unit, re.IGNORECASE):
        unit = 'Hartree'
        is_ev = False
    else:
        raise ValueError('Unknown unit.')

    if not (isinstance(bands, list) or isinstance(bands, tuple)):
        bands = [bands]

    for b in bands:
        if unit != b.unit:
            if unit == 'eV':
                b.bands[:, :, :] = H_to_eV(b.bands[:, :, :])
            else:
                b.bands[:, :, :] = eV_to_H(b.bands[:, :, :])
            b.unit = unit
    if len(bands) == 1:
        bands = bands[0]

    fig = plot_cry_bands(bands, k_labels=k_labels, energy_range=energy_range, title=title,
                         not_scaled=not_scaled, mode=mode, linestl=linestl, linewidth=linewidth,
                         color=color, fermi=fermi, k_range=k_range, labels=labels,
                         figsize=figsize, scheme=scheme, sharex=sharex, sharey=sharey)
    if is_ev == True:
        fig.supylabel('$E-E_{F}$ (eV)')
    else:
        fig.supylabel('$E-E_{F}$ (Hartree)')

    if save_to_file != None:
        save_plot(save_to_file)

    plt.show()

def plot_cry_bands(bands, k_labels, energy_range, title, not_scaled, mode, linestl,
                   linewidth, color, fermi, k_range, labels, figsize, scheme,
                   sharex, sharey):
    """
    The base function to plot electron / phonon density of states.

    Args:
        bands (Union[List, object]): List of band objects or a single band object.
        k_labels (Union[List[str], None]): List of strings specifying the labels for high symmetry points along the path.
        energy_range (Union[List[Union[int, float]], None]): List of two integers or floats specifying the energy range (min, max).
        title (Union[str, None]): Title of the plot.
        not_scaled (bool): Flag indicating whether to scale the band structure for comparison.
        mode (str): Mode of the plot ('single', 'multi', 'compare', 'surface').
        linestl (Union[str, List[str]]): Line style or list of line styles for the bands.
        linewidth (Union[int, List[int]]): Line width or list of line widths for the bands.
        color (Union[str, List[str]]): Color or list of colors for the bands.
        fermi (str): Color of the Fermi level.
        k_range (Union[List[str], None]): List of two strings specifying the range of k points to plot.
        labels (Union[List[str], None]): List of labels for the bands in multi-mode.
        figsize (Union[Tuple[int, int], None]): Figure size.
        scheme (Union[List[int], Tuple[int, int], None]): Subplot scheme in compare-mode (number of rows, number of columns).
        sharex (Union[bool, str]): Flag or 'row' or 'col' specifying sharing of x-axis.
        sharey (Union[bool, str]): Flag or 'row' or 'col' specifying sharing of y-axis.

    Raises:
        ValueError: If an invalid mode flag is specified or if there are errors in the input parameters.

    Returns:
        None
    """
    import matplotlib.pyplot as plt
    # import matplotlib.lines as mlines
    import numpy as np
    import sys
    import warnings

    greek = {'Alpha': '\u0391', 'Beta': '\u0392', 'Gamma': '\u0393', 'Delta': '\u0394', 'Epsilon': '\u0395', 'Zeta': '\u0396', 'Eta': '\u0397',
             'Theta': '\u0398', 'Iota': '\u0399', 'Kappa': '\u039A', 'Lambda': '\u039B', 'Mu': '\u039C', 'Nu': '\u039D', 'Csi': '\u039E',
             'Omicron': '\u039F', 'Pi': '\u03A0', 'Rho': '\u03A1', 'Sigma': '\u03A3', 'Tau': '\u03A4', 'Upsilon': '\u03A5', 'Phi': '\u03A6',
             'Chi': '\u03A7', 'Psi': '\u03A8', 'Omega': '\u03A9', 'Sigma_1': '\u03A3\u2081'}

    # Error check on the mode flag
    modes = ['single', 'multi', 'compare', 'surface']
    if mode not in modes:
        raise ValueError('The selected mode '+mode+' is not among the possible ones: ' + modes[0]+', ' + modes[1] + ', '+modes[2] + ', or '+modes[3])

    # Error chenk on k_label
    if k_labels is not None:

        if isinstance(k_labels, list):
            for element in k_labels:
                if not isinstance(element, str):
                    raise ValueError('k_label must be a list of strings:' +str(element)+' is not a string')

            if isinstance(bands, list):
                ref = bands[0].n_tick

                for i, file in enumerate(bands):
                    if file.n_tick != ref:
                        i = str(i)
                        raise ValueError('The ' + i + 'element your file list has a different number of High Symmetry Point!')
            else:
                ref = bands.n_tick

            if len(k_labels) < ref:
                diff = str(ref-len(k_labels))
                raise ValueError('You are lacking ' + diff +' High Symmetry Points in k_labels!')

            elif len(k_labels) > ref:
                diff = str(len(k_labels)-ref)
                raise ValueError('You have ' + diff + 'High Symmetry Points in excess in k_labels')

        else:
            raise ValueError('k_labels must be a list of strings')

    # Error check on energy range
    if energy_range != None:

        if isinstance(energy_range, list):

            if len(energy_range) > 2:
                raise ValueError('energy_range must be a list of two int or float (min,max)')

            for element in energy_range:
                if (not isinstance(element, int)) and (not isinstance(element, float)):
                    raise ValueError('energy_range must be a list of two int or float (min,max): ' +str(element)+', is neither a float or an int')

        else:
            raise ValueError('energy_range must be a list of two int or float (min,max)')

    # Error check on k_range
    if k_range is not None:
        if isinstance(k_range, list):
            if len(k_range) > 2:
                raise ValueError('k_range must be a list of two strings')

            for element in k_range:
                if not isinstance(element, str):
                    raise ValueError('k_label must be a list of two strings:' +str(element)+' is not a string')

        else:
            raise ValueError('k_range must be a list of two strings')

    # Error check on title
    if title != None:
        if not isinstance(title, str):
            raise ValueError('title needs to be a string')

    if (mode == modes[0]) or (mode == modes[1]) or (mode == modes[3]):

        # plotting of a single band object
        if mode == modes[0]:

            dx = bands.k_point_plot

            pltband = bands.bands
            no_bands = np.shape(pltband)[0]
            ymin = np.amin(pltband)
            ymax = np.amax(pltband)
            xmin = min(dx)
            xmax = max(dx)
            count1 = 0
            count2 = 0

            # band plot
            if figsize != None:
                fig, ax = plt.subplots(nrows=1, ncols=1, sharex=sharex, sharey=sharey, figsize=figsize)
            else:
                fig, ax = plt.subplots(nrows=1, ncols=1, sharex=sharex, sharey=sharey)

            for i in range(no_bands):

                if bands.spin == 1:
                    ax.plot(dx, pltband[i, :], color=color, linestyle=linestl, linewidth=linewidth)

                elif bands.spin == 2:
                    if count1 == count2:
                        ax.plot(dx, pltband[i, :, 0], color='red',
                                linestyle=linestl, linewidth=linewidth, label='Alpha')
                        ax.plot(dx, pltband[i, :, 1], color='black',
                                linestyle=linestl, linewidth=linewidth, label='Beta')
                    else:
                        ax.plot(dx, pltband[i, :, 0], color='red',
                                 linestyle=linestl, linewidth=linewidth)
                        ax.plot(dx, pltband[i, :, 1], color='black',
                                linestyle=linestl, linewidth=linewidth)
                    count1 += 1

        # plot of multiple band objects on a single plot
        elif mode == modes[1]:

            # Error check on the band on the 'multi' mode flag
            if not isinstance(bands, list):
                raise ValueError('When you choose a ' +modes[1]+' plot bands needs to be a list of band objects')
            # Error check on color for the 'multi' mode flag
            if isinstance(color, list):
                if len(color) != len(bands):
                    raise ValueError('The number of colors is inconsistent with the number of objects you want to plot')
            else:
                color = ['dimgrey', 'blue', 'indigo', 'slateblue',
                         'thistle', 'purple', 'orchid', 'crimson']

            # Warning comparison with band.spin==2
            for m in bands:
                if m.spin == 2:
                    warnings.warn("The 'multi' plot is not fully implemented at the moment for file with NSPIN = 2")

            # scaling that enables the comparison of band structure calculated at different pressures
            if not_scaled is False:
                reference = xmax = np.amax(bands[0].k_point_plot)
                xmin = np.amin(bands[0].k_point_plot)

            else:
                xmax = []
                xmin = []

            ymin = []
            ymax = []

            if figsize != None:
                fig, ax = plt.subplots(nrows=1, ncols=1, sharex=sharex, sharey=sharey, figsize=figsize)
            else:
                fig, ax = plt.subplots(nrows=1, ncols=1, sharex=sharex, sharey=sharey)

            # plot of all the bands obj present in the list
            for index, data in enumerate(bands):
                # scaling that enables the comparison of band structure calculated at different pressures
                if not_scaled == False:
                    k_max = np.amax(data.k_point_plot)
                    dx = (data.k_point_plot/k_max)*reference
                else:
                    dx = data.k_point_plot
                    xmin.append(np.amin(dx))
                    xmax.append(np.amax(dx))

                pltband = data.bands
                no_bands = np.shape(pltband)[0]
                ymin.append(np.amin(pltband))
                ymax.append(np.amax(pltband))

                count1 = 0
                count2 = 0

                # Effective plot
                for j in range(no_bands):

                    if (count1 == count2) and (labels is not None):
                        if data.spin == 1:
                            if isinstance(linestl, list):
                                if isinstance(linewidth, list):
                                    ax.plot(dx, pltband[j, :], color=color[index],
                                            linestyle=linestl[index], linewidth=linewidth[index], label=labels[index])
                                else:
                                    ax.plot(dx, pltband[j, :], color=color[index],
                                            linestyle=linestl[index], linewidth=linewidth, label=labels[index])
                            else:
                                if isinstance(linewidth, list):
                                    ax.plot(dx, pltband[j, :], color=color[index],
                                            linestyle=linestl, linewidth=linewidth[index], label=labels[index])
                                else:
                                    ax.plot(dx, pltband[j, :], color=color[index],
                                            linestyle=linestl, linewidth=linewidth, label=labels[index])
                        elif data.spin == 2:
                            ax.plot(dx, pltband[j, :, 0], color=color[index],
                                    linestyle=linestl, linewidth=linewidth, label=labels[index]+' Alpha')
                            ax.plot(dx, pltband[j, :, 1], color=color[index],
                                    linestyle='--', linewidth=linewidth, label=labels[index]+' Beta')

                    else:
                        if data.spin == 1:
                            if isinstance(linestl, list):
                                if isinstance(linewidth, list):
                                    ax.plot(dx, pltband[j, :], color=color[index],
                                            linestyle=linestl[index], linewidth=linewidth[index])
                                else:
                                    ax.plot(dx, pltband[j, :], color=color[index],
                                            linestyle=linestl[index], linewidth=linewidth)
                            else:
                                if isinstance(linewidth, list):
                                    ax.plot(dx, pltband[j, :], color=color[index],
                                            linestyle=linestl, linewidth=linewidth[index])
                                else:
                                    ax.plot(dx, pltband[j, :], color=color[index],
                                            linestyle=linestl, linewidth=linewidth)
                        elif data.spin == 2:
                            ax.plot(dx, pltband[j, :, 0], color=color[index],
                                    linestyle=linestl, linewidth=linewidth)
                            ax.plot(dx, pltband[j, :, 1], color=color[index],
                                    linestyle='--', linewidth=linewidth)

                    count1 += 1

            if (isinstance(xmin, list)) or (isinstance(xmax, list)):
                xmin = min(xmin)
                xmax = max(xmax)

            ymin = min(ymin)
            ymax = max(ymax)

        if mode == modes[3]:
            warnings.warn('The surface bands is not ready yet')
            sys.exit(0)

        # HSP line plot
        if isinstance(bands, list):
            hsp = bands[0].tick_position
        else:
            hsp = bands.tick_position

        if k_labels is not None:
            if len(hsp) != len(k_labels):
                if len(hsp) > len(k_labels):
                    raise ValueError('You have specified a number of label smalle than the number of High Simmetry Point along the path')
                elif len(hsp) < len(k_labels):
                    raise ValueError('You have more labels than the High Simmetry point along the path')

        hsp[len(hsp)-1] = xmax

        y_band = np.linspace(ymin*1.05, ymax*1.05, 2)

        for j in hsp:
            x_band = np.ones(2)*j
            ax.plot(x_band, y_band, color='black', linewidth=0.5)

        # plot of the fermi level
        x = np.linspace(xmin, xmax, 2)
        y = np.zeros(2)
        ax.plot(x, y, color=fermi, linewidth=2.5)

        # definition of the plot title
        if title is not None:
            fig.suptitle(title)

        if not isinstance(bands, list):
            if bands.spin == 2:
                fig.legend()
        else:
            if labels is not None:
                fig.legend()

    # compare mode plot
    elif mode == modes[2]:

        # Error check on type(bands)
        if not isinstance(bands, list):
            raise ValueError('When you choose a ' +modes[2]+' plot bands needs to be a list of band objects')
        # Error check on sharex and sharey option
        if (not isinstance(sharex, bool)) or (not isinstance(sharey, bool)):
            accepted_str = ['row', 'col']

            if (isinstance(sharex, str)) or (isinstance(sharey, str)):
                if sharex not in accepted_str:
                    raise ValueError('sharex can only be equal to row or col')
                elif sharey not in accepted_str:
                    raise ValueError('sharey can only be equal to row or col')
            else:
                raise ValueError('sharex and sharey have to be boolean')

        # Error check and definition of scheme
        if scheme is None:
            n_rows = 1
            n_col = len(bands)
        else:
            if (not isinstance(scheme, tuple)) and (not isinstance(scheme, list)):
                raise ValueError('scheme needs to be a tuple or a list')
                sys.exit(1)
            elif len(scheme) > 2:
                raise ValueError('scheme needs to be a tuple or a list of two elements (nrow,ncol)')
            else:
                n_rows = scheme[0]
                n_col = scheme[1]
        # Creation of the subplots
        if figsize is None:
            fig, axs = plt.subplots(nrows=n_rows, ncols=n_col,
                                    sharex=sharex, sharey=sharey, figsize=figsize)
        else:
            fig, axs = plt.subplots(nrows=n_rows, ncols=n_col,
                                    sharex=sharex, sharey=sharey, figsize=figsize)
        if n_rows == 1 and n_col == 1: # When axs is not a list
            axs = [axs]
        # Scaling with different size of the same brillouin zone
        if not_scaled is False:
            reference = xmax = np.amax(bands[0].k_point_plot)
            xmin = np.amin(bands[0].k_point_plot)

        else:
            xmax = []
            xmin = []

        ymin = []
        ymax = []
        count3 = 0

        # Plot of the different band structure into the subplots
        for col in range(n_col):
            for row in range(n_rows):
                data = bands[count3]
                if count3 == 0:
                    hsp = data.tick_position
                pltband = data.bands
                no_bands = np.shape(pltband)[0]
                if not_scaled is False:
                    k_max = np.amax(data.k_point_plot)
                    dx = (data.k_point_plot/k_max)*reference
                else:
                    dx = data.k_point_plot
                    xmin.append(np.amin(dx))
                    xmax.append(np.amax(dx))
                ymin.append(np.amin(pltband))
                ymax.append(np.amax(pltband))
                # Effective plotting action
                for j in range(no_bands):
                    if data.spin == 1:
                        if n_rows == 1:
                            axs[col].plot(
                                dx, pltband[j, :], color=color, linestyle=linestl, linewidth=linewidth)
                        else:
                            axs[row, col].plot(
                                dx, pltband[j, :], color=color, linestyle=linestl, linewidth=linewidth)
                    elif data.spin == 2:
                        if n_rows == 1:
                            axs[col].plot(dx, pltband[j, :, 0], color=color,
                                          linestyle='-', linewidth=linewidth, label='Alpha')
                            axs[col].plot(dx, pltband[j, :, 0], color=color,
                                          linestyle='--', linewidth=linewidth, label='Beta')
                        else:
                            axs[row, col].plot(
                                dx, pltband[j, :, 0], color=color, linestyle='-', linewidth=linewidth, label='Alpha')
                            axs[row, col].plot(
                                dx, pltband[j, :, 0], color=color, linestyle='--', linewidth=linewidth, label='Beta')

                # Plot of the HSPs lines
                yhsp = np.linspace(np.amin(pltband)+5, np.amax(pltband)+5, 2)
                for j in hsp:
                    xhsp = np.ones(2)*j
                    if n_rows == 1:
                        axs[col].plot(
                            xhsp, yhsp, color='black', linewidth=0.5)
                    else:
                        axs[row, col].plot(
                            xhsp, yhsp, color='black', linewidth=0.5)

                # Fermi level line plot
                xfermi = np.linspace(np.amin(pltband), np.amax(pltband), 2)
                yfermi = np.zeros(2)
                if n_rows == 1:
                    axs[col].plot(
                        xfermi, yfermi, color=fermi, linewidth=2.5)
                else:
                    axs[row, col].plot(
                        xfermi, yfermi, color=fermi, linewidth=2.5)

                # Definition of x and y limits
                if n_rows == 1:
                    if sharex is not True:
                        """hsp_label = []
                        for element in k_labels:
                            if element in k_labels:
                                g = greek.get(element)
                                hsp_label.append(g)
                        axs[col].set_xticks(hsp)
                        if k_labels is not None:
                            axs[col].set_xlabels(hsp_label)"""
                        warnings.warn('The sharex = False option has not been developed yet')
                    axs[col].set_xlim([np.amin(dx), np.amax(dx)])
                    if (sharey is not True) and (energy_range is not None):
                        axs[col].set_ylim([energy_range[0], energy_range[1]])
                    else:
                        axs[col].set_ylim([np.amin(pltband), np.amax(pltband)])
                else:
                    if sharex is not True:
                        """hsp_label = []
                        for element in k_labels:
                            if element in k_labels:
                                g = greek.get(element)
                                hsp_label.append(g)
                        axs[row, col].set_xticks(hsp)
                        if k_labels is not None:
                            axs[row, col].set_xlabels(hsp_label)"""
                        warnings.warn('The sharex = False option has not been developed yet')
                    axs[row, col].set_xlim([np.amin(dx), np.amax(dx)])
                    if (sharey is not True) and (energy_range is not False):
                        axs[row, col].set_ylim(
                            [energy_range[0], energy_range[1]])
                    else:
                        axs[row, col].set_ylim(
                            [np.amin(pltband), np.amax(pltband)])

                count3 += 1

        if (isinstance(ymin, list)) or (isinstance(ymax, list)):
            ymin = min(ymin)
            ymax = max(ymax)

    hsp_label = []
    high_sym_point = []
    if k_labels is not None:
        for n in k_labels:
            if n in greek:
                g = greek.get(n)
                hsp_label.append(g)
                high_sym_point.append(n)
            else:
                hsp_label.append(n)
                high_sym_point.append(n)

    # give the possibility through the k_range to select a shorter path than the one calculated
    high_sym_point2 = high_sym_point
    count = 0
    for i in high_sym_point2:
        repeat = high_sym_point2.count(i)
        if repeat != 1:
            for p in range(0, len(high_sym_point2)):
                if p != count:
                    repeat_count = 1
                    q = high_sym_point2[p]
                    r = high_sym_point[p]
                    if (q == i) & (q == r):
                        high_sym_point2[p] = i+str(repeat_count)
                        repeat_count += 1
                        if repeat_count > repeat:
                            repeat_count = 0
        count += 1

    path_dict = dict(zip(high_sym_point2, hsp))

    # definition of the ylim
    if (energy_range != None) and (sharey == True):
        ymin = energy_range[0]
        ymax = energy_range[1]

    # definition of the xlim
    if k_range != None:
        xmin = path_dict[k_range[0]]
        xmax = path_dict[k_range[1]]

    if k_labels != None:
        plt.xticks(hsp, hsp_label)
    else:
        plt.xticks(hsp)

    plt.ylim(ymin, ymax)
    if (mode == modes[0]) or (mode == modes[1]):
        plt.xlim(xmin, xmax)
    elif (mode == modes[2]) and (k_range is not None):
        warnings.warn('The k_range is not available yet for the compare mode')

    return fig


def plot_electron_dos(doss, unit='eV', beta='up', overlap=False, prj=None,
                      energy_range=None, dos_range=None, color='blue',
                      labels=None, linestl=None, linewidth=1, fermi='forestgreen',
                      title=None, figsize=None, save_to_file=None):
    """
    A wrapper of plot_cry_doss for electron density of states.

    Args:
        doss (DOSBASE): DOS obect generated by code:`CRYSTALpytools.crystal_io.Properties_output.read_doss`.
            Or a list of DOSBASE objects.
        unit (str): 'eV' or 'Hartree'
        beta (str): Plot spin-down state 'up' or 'down'
        overlap (bool): Plotting multiple lines into the same figure
        prj (list): Index of selected projection. Consistent with the
            index of the 2nd dimension of :code:`doss.doss`
        energy_range (list[float]): 2*1 list of energy range
        dos_range (list[float]): 2*1 list of DOS range
        color (str | list[str]): Color of plot lines. *Should be
            consistent with number of projections.*
        labels (str | list[str]): Plot legend. *Should be consistent with
            number of projections.*
        linestl (str | list[str]): linestyle string. *Should be consistent
            with number of projections.*
        linewidth (float)
        fermi (str): Color of Fermi level line.
        title (str)
        figsize (list[float])
        save_to_file (str): File name.

    Returns:
        None
    """
    import matplotlib.pyplot as plt
    from CRYSTALpytools.units import H_to_eV, eV_to_H
    import re

    if re.match(r'^ev$', unit, re.IGNORECASE):
        unit = 'eV'
        is_ev = True
    elif re.match(r'^hartree$', unit, re.IGNORECASE):
        unit = 'Hartree'
        is_ev = False
    else:
        raise ValueError('Unknown unit.')

    if not (isinstance(doss, list) or isinstance(doss, tuple)):
        doss = [doss]

    for d in doss:
        if unit != d.unit:
            if unit == 'eV':
                d.doss[:, 0, :] = H_to_eV(d.doss[:, 0, :])
                d.doss[:, 1:, :] = eV_to_H(d.doss[:, 1:, :])
            else:
                d.doss[:, 0, :] = eV_to_H(d.doss[:, 0, :])
                d.doss[:, 1:, :] = H_to_eV(d.doss[:, 1:, :])
            d.unit = unit
    if len(doss) == 1:
        doss = doss[0]

    fig = plot_cry_doss(doss, color=color, fermi=fermi, overlap=overlap,
                        labels=labels, figsize=figsize, linestl=linestl,
                        linewidth=linewidth, title=title, beta=beta,
                        energy_range=energy_range, dos_range=dos_range, prj=prj)
    if is_ev == True:
        fig.supylabel('DOS (states/eV)')
        fig.supxlabel('Energy (eV)')
    else:
        fig.supylabel('DOS (states/Hartree)')
        fig.supxlabel('Energy (Hartree)')

    if save_to_file != None:
        save_plot(save_to_file)

    plt.show()

def plot_phonon_dos(doss, unit='cm-1', overlap=False, prj=None,
                    freq_range=None, dos_range=None, color='blue',
                    labels=None, linestl=None, linewidth=1, line_freq0=None,
                    title=None, figsize=None, save_to_file=None):
    """
    A wrapper of plot_cry_doss for electron density of states.

    Args:
        doss (DOSBASE): DOS obect generated by code:`CRYSTALpytools.crystal_io.Crystal_output.read_pdos`.
            Or a list of DOSBASE objects.
        unit (str): 'cm-1' or 'THz'
        overlap (bool): Plotting multiple lines into the same figure
        prj (list): Index of selected projection. Consistent with the
            index of the 2nd dimension of :code:`doss.doss`
        freq_range (list[float]): 2*1 list of frequency range
        dos_range (list[float]): 2*1 list of DOS range
        color (str | list[str]): Color of plot lines. *Should be
            consistent with number of projections.*
        labels (str | list[str]): Plot legend. *Should be consistent with
            number of projections.*
        linestl (str | list[str]): linestyle string. *Should be consistent
            with number of projections.*
        linewidth (float)
        line_freq0 (str): Color of frequency = 0 line.
        title (str)
        figsize (list[float])
        save_to_file (str): File name.

    Returns:
        None
    """
    import matplotlib.pyplot as plt
    from CRYSTALpytools.units import cm_to_thz, thz_to_cm
    import re

    if re.match(r'^cm\-1$', unit, re.IGNORECASE):
        unit = 'cm-1'
        is_thz = False
    elif re.match(r'^thz$', unit, re.IGNORECASE):
        unit = 'THz'
        is_thz = True
    else:
        raise ValueError('Unknown unit.')

    if not (isinstance(doss, list) or isinstance(doss, tuple)):
        doss = [doss]

    for d in doss:
        if unit != d.unit:
            if unit == 'cm-1':
                d.doss[:, 0, :] = thz_to_cm(d.doss[:, 0, :])
                d.doss[:, 1:, :] = cm_to_thz(d.doss[:, 1:, :])
            else:
                d.doss[:, 0, :] = cm_to_thz(d.doss[:, 0, :])
                d.doss[:, 1:, :] = thz_to_cm(d.doss[:, 1:, :])
            d.unit = unit

    if line_freq0 == None:
        line_freq0 = (1., 0., 0., 0.) # Transparent
    if len(doss) == 1:
        doss = doss[0]

    fig = plot_cry_doss(doss, color=color, fermi=line_freq0, overlap=overlap,
                        labels=labels, figsize=figsize, linestl=linestl,
                        linewidth=linewidth, title=title, beta='up',
                        energy_range=freq_range, dos_range=dos_range, prj=prj)

    if is_thz == True:
        fig.supylabel('DOS (states/THz)')
        fig.supxlabel('Frequency (THz)')
    else:
        fig.supylabel('DOS (states/cm$^{-1}$)')
        fig.supxlabel('Frequency (cm$^{-1}$)')

    if save_to_file != None:
        save_plot(save_to_file)

    plt.show()

def plot_cry_doss(doss, color, fermi, overlap, labels, figsize, linestl,
                  linewidth, title, beta, energy_range, dos_range, prj):
    """
    The base function to plot electron / phonon density of states.

    Args:
        doss (object): The density of states object.
        color (str or list): The color(s) of the plot(s).
        fermi (str): The color of the Fermi level line.
        overlap (bool): True if the projections should overlap, False otherwise.
        labels (str or list): The label(s) for the plot(s).
        figsize (tuple): The figure size (width, height) in inches.
        linestl (str or list): The line style(s) for the plot(s).
        linewidth (float): The width of the line(s) in points.
        title (str): The title of the plot.
        beta (str): The beta value ('up' or 'down').
        energy_range (tuple): The energy range (xmin, xmax) for the x-axis.
        dos_range (tuple): The density of states range (ymin, ymax) for the y-axis.
        prj (None or list): The projection(s) to plot.

    Returns:
        None
    """
    import matplotlib.pyplot as plt
    import numpy as np
    import sys
    import warnings
    from os import path

    # Error check on beta
    accepted_beta = ['up', 'down']
    if beta not in accepted_beta:
        raise ValueError("Beta can be defined only as: 'up' or 'down'.")

    # Plot for overlap == True
    if overlap == True:

        # Error check on color for color in overlap == true and default list of color
        if (not isinstance(color, list)) and (doss.n_proj > 1):
            warnings.warn('When overlap is true color has to be a list!', stacklevel=2)
            color = ['blue', 'indigo', 'midgrey', 'crimson']
            if (len(color) < doss.n_proj) or (len(color) < len(prj)):
                raise ValueError('When overlap is true color has to be a list!')

        # Error check on labels for overlap == true
        if labels is not None:
            if not isinstance(labels, list) and (doss.n_proj > 1):
                raise ValueError('When overlap is true labels has to be a list')

        # Default for figsize
        if figsize is None:
            figsize = (12, 5)

        # Error check on color, labels, and linestl
        if (isinstance(color, list)) or (isinstance(labels, list)) or (isinstance(linestl, list)):
            if color is not None:
                if prj is None:
                    if (len(color) > doss.n_proj) or (len(color) < doss.n_proj):
                        if len(color) > doss.n_proj:
                            raise ValueError('The number of colors is greater than the number of projections!')
                        elif len(color) < doss.n_proj:
                            raise ValueError('The number of colors is less than the number of projections!')
                else:
                    if (len(color) > len(prj)) or (len(color) < len(prj)):
                        if len(color) > len(prj):
                            raise ValueError('The number of colors is greater than the number of projections required!')
                        elif len(color) < len(prj):
                            raise ValueError('The number of colors is less than the number of projections required!')

            if labels is not None:
                if prj is None:
                    if (len(labels) > doss.n_proj) or (len(labels) < doss.n_proj):
                        if len(labels) > doss.n_proj:
                            raise ValueError('The number of labels is greater than the number of projections!')
                        elif len(labels) < doss.n_proj:
                            raise ValueError('The number of labels is less than the number of projections!')
                else:
                    if (len(labels) > len(prj)) or (len(labels) < len(prj)):
                        if len(labels) > len(prj):
                            raise ValueError('The number of labels is greater than the number of projections required!')
                        elif len(color) < len(prj):
                            raise ValueError('The number of labels is less than the number of projections required!')

            if linestl is not None:
                if prj is None:
                    if (len(linestl) > doss.n_proj) or (len(linestl) < doss.n_proj):
                        if len(linestl) > doss.n_proj:
                            raise ValueError('The number of linestl is greater than the number of projections!')
                        elif len(linestl) < doss.n_proj:
                            raise ValueError('The number of linestl is less than the number of projections!')
                else:
                    if (len(linestl) > len(prj)) or (len(linestl) < len(prj)):
                        if len(linestl) > len(prj):
                            raise ValueError('The number of linestl is greater than the number of projections required!')
                        elif len(color) < len(prj):
                            raise ValueError('The number of linestl is less than the number of projections required!')

        # Creation of the figure
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
        # Creation of dx for the plot
        if doss.spin == 1:
            dx = doss.doss[:, 0]
        elif doss.spin == 2:
            dx = doss.doss[:, 0, :]
            dx_alpha = doss.doss[:, 0, 0]
            dx_beta = doss.doss[:, 0, 1]

        # Determination of xmin, xmax, ymin, and ymax
        xmin = np.amin(dx)
        xmax = np.amax(dx)
        ymin = np.amin(doss.doss[1:, :, :])
        ymax = np.amax(doss.doss[1:, :, :])

        # Plot of all projections
        if prj == None:
            for projection in range(1, doss.n_proj+1):
                # for projection in range(1, 2):
                if doss.spin == 1:
                    if doss.n_proj > 1:
                        if linestl is None:
                            ax.plot(dx, doss.doss[:, projection], color=color[projection-1],
                                    label=labels[projection-1], linewidth=linewidth)
                        else:
                            ax.plot(dx, doss.doss[:, projection], color=color[projection-1],
                                    label=labels[projection-1], linestyle=linestl[projection-1], linewidth=linewidth)
                    else:
                        ax.plot(dx, doss.doss[:, projection], color=color, linewidth=linewidth)
                elif doss.spin == 2:
                    if beta == accepted_beta[0]:
                        if doss.n_proj > 1:
                            ax.plot(dx_alpha, doss.doss[:, projection, 0], color=color[projection-1],
                                    label=labels[projection-1], linestyle='-', linewidth=linewidth)
                            ax.plot(dx_beta, -doss.doss[:, projection, 1], color=color[projection-1],
                                    label=labels[projection-1], linestyle='--', linewidth=linewidth)
                        else:
                            ax.plot(dx_alpha, doss.doss[:, projection, 0],
                                    linestyle='-', linewidth=linewidth)
                            ax.plot(dx_beta, -doss.doss[:, projection, 1],
                                    linestyle='--', linewidth=linewidth)
                    elif beta == accepted_beta[1]:
                        if doss.n_proj > 1:
                            ax.plot(dx_alpha, doss.doss[:, projection, 0], color=color[projection-1],
                                    label=labels[projection-1], linestyle='-', linewidth=linewidth)
                            ax.plot(dx_beta, doss.doss[:, projection, 1], color=color[projection-1],
                                    label=labels[projection-1], linestyle='--', linewidth=linewidth)

                        else:
                            ax.plot(dx_alpha, doss.doss[:, projection, 0], color=color,
                                    linestyle='-', linewidth=linewidth)
                            ax.plot(dx_beta, doss.doss[:, projection, 1], color=color,
                                    linestyle='--', linewidth=linewidth)

        # Plot of selected projections
        else:
            for index, projection in enumerate(prj):
                if doss.spin == 1:
                    if doss.n_proj > 1:
                        if linestl is None:
                            ax.plot(dx, doss.doss[:, projection], color=color[index],
                                    label=labels[index], linewidth=linewidth)
                        else:
                            ax.plot(dx, doss.doss[:, projection], color=color[index],
                                    label=labels[index], linestyle=linestl[index], linewidth=linewidth)
                    else:
                        ax.plot(dx, doss.doss[:, projection], color=color, linewidth=linewidth)
                elif doss.spin == 2:
                    if beta == accepted_beta[0]:
                        if doss.n_proj > 1:
                            ax.plot(dx_alpha, doss.doss[:, projection, 0], color=color[index],
                                    label=labels[index], linestyle='-', linewidth=linewidth)
                            ax.plot(dx_beta, -doss.doss[:, projection, 1], color=color[index],
                                    label=labels[index], linestyle='--', linewidth=linewidth)
                        else:
                            ax.plot(dx_alpha, doss.doss[:, projection, 0],
                                    linestyle='-', linewidth=linewidth)
                            ax.plot(dx_beta, -doss.doss[:, projection, 1],
                                    linestyle='--', linewidth=linewidth)
                    elif beta == accepted_beta[1]:
                        if doss.n_proj > 1:
                            ax.plot(dx_alpha, doss.doss[:, projection, 0], color=color[index],
                                    label=labels[index], linestyle='-', linewidth=linewidth)
                            ax.plot(dx_beta, doss.doss[:, projection, 1], color=color[index],
                                    label=labels[index], linestyle='--', linewidth=linewidth)
                        else:
                            ax.plot(dx_alpha, doss.doss[:, projection, 0], color=color,
                                    linestyle='-', linewidth=linewidth)
                            ax.plot(dx_beta, doss.doss[:, projection, 1], color=color,
                                    linestyle='--', linewidth=linewidth)

        yfermi_level = np.linspace(ymin*1.05, ymax*1.05, 2)
        xfermi_level = np.zeros(2)
        if beta == accepted_beta[0]:
            ax.plot(xfermi_level, yfermi_level, color=fermi, linewidth=1.5)
        else:
            yfermi_level = np.linspace(ymin*1.05, ymax*1.05, 2)
            ax.plot(xfermi_level, yfermi_level, color=fermi, linewidth=1.5)
        y_zero = np.zeros(2)
        x_zero = np.linspace(xmin, xmax, 2)
        ax.plot(x_zero, y_zero, color='black', linewidth=0.4)
        if dos_range is not None:
            ymin = dos_range[0]
            ymax = dos_range[1]
            plt.ylim(ymin, ymax)
        else:
            if doss.spin == 1:
                ymin = 0
                plt.ylim(ymin, ymax*1.05)
            elif doss.spin == 2:
                if beta == accepted_beta[0]:
                    ymin = 0
                    plt.ylim(ymin, ymax*1.05)
                elif beta == accepted_beta[1]:
                    plt.ylim(ymin*1.05, ymax*1.05)

    # Plot for overlap == False
    else:
        # Error checks on colors, labels, and linestl
        if isinstance(color, list):
            warnings.warn('When overlap is false color should be a string!',
                          stacklevel=2)
            color = 'blue'

        if isinstance(labels, list):
            warnings.warn('When overlap is false labels should be a string!',
                          stacklevel=2)
            labels = None

        if isinstance(linestl, list):
            warnings.warn('When overlap is false color should be a string!',
                          stacklevel=2)
            linestl = '-'

        # Creation of dx for the plot
        if doss.spin == 1:
            dx = doss.doss[:, 0]
        elif doss.spin == 2:
            dx = doss.doss[:, 0, :]
            dx_alpha = doss.doss[:, 0, 0]
            dx_beta = doss.doss[:, 0, 1]

        # Determination of xmin and xmax
        xmin = np.amin(dx)
        xmax = np.amax(dx)

        # Creation xfermi, x_zero, and y_zero
        xfermi = np.zeros(2)
        x_zero = np.linspace(xmin, xmax, 2)
        y_zero = np.zeros(2)

        # Creation of subplots for all projections
        if prj is None:
            fig, axs = plt.subplots(nrows=doss.n_proj, ncols=1, sharex=True, figsize=figsize)
            # If only one projection is generated, axs is not subscriptable
            if doss.n_proj == 1:
                axs = [axs]
        # Creation of subplots for selected projections
        else:
            fig, axs = plt.subplots(nrows=len(prj), ncols=1, sharex=True, figsize=figsize)
            # If only one projection is generated, axs is not subscriptable
            if len(prj) == 1:
                axs = [axs]

        # Plot for all projections
        if prj is None:
            for projection in range(doss.n_proj):
                if doss.spin == 1:
                    ymin = 0
                    ymax = np.amax(doss.doss[:, projection+1])
                    yfermi = np.linspace(ymin*1.05, ymax*1.05, 2)
                    axs[projection].plot(dx, doss.doss[:, projection+1],
                                         color=color, linestyle=linestl, linewidth=linewidth)
                    axs[projection].plot(xfermi, yfermi, color=fermi, linewidth=1.5)
                    if dos_range is not None:
                        ymin = dos_range[0]
                        ymax = dos_range[1]
                    axs[projection].set_ylim(ymin, ymax)
                elif doss.spin == 2:
                    if beta == accepted_beta[0]:
                        ymin = 0
                        ymax = np.amax(doss.doss[:, projection+1, :])
                        yfermi = np.linspace(ymin, ymax, 2)
                        axs[projection].plot(dx_alpha, doss.doss[:, projection+1, 0], color=color,
                                             linestyle='-', linewidth=linewidth, label='Alpha')
                        axs[projection].plot(dx_beta, -doss.doss[:, projection+1, 1], color=color,
                                             linestyle='--', linewidth=linewidth, label='Beta')
                        axs[projection].plot(xfermi, yfermi, color=fermi, linewidth=1.5)
                        if dos_range is not None:
                            ymin = dos_range[0]
                            ymax = dos_range[1]
                        axs[projection].set_ylim(ymin, ymax)
                    elif beta == accepted_beta[1]:
                        ymin = -np.amax(doss.doss[:, projection+1, :])
                        ymax = np.amax(doss.doss[:, projection+1, :])
                        yfermi = np.linspace(ymin, ymax, 2)
                        axs[projection].plot(dx_alpha, doss.doss[:, projection+1, 0], color=color,
                                             linestyle='-', linewidth=linewidth, label='Alpha')
                        axs[projection].plot(dx_beta, doss.doss[:, projection+1, 1], color=color,
                                             linestyle='--', linewidth=linewidth, label='Beta')
                        axs[projection].plot(x_zero, y_zero, linewidth=0.4)
                        axs[projection].plot(xfermi, yfermi, color=fermi, linewidth=2.5)
                        if dos_range is not None:
                            ymin = dos_range[0]
                            ymax = dos_range[1]
                        axs[projection].set_ylim(ymin, ymax)

        # Plot for selected projections
        else:
            for index, projection in enumerate(prj):
                if doss.spin == 1:
                    ymin = 0
                    ymax = np.amax(doss.doss[:, projection])
                    yfermi = np.linspace(ymin*1.05, ymax*1.05, 2)
                    axs[index].plot(dx, doss.doss[:, projection],
                                    color=color, linestyle=linestl, linewidth=linewidth)
                    axs[index].plot(xfermi, yfermi, color=fermi, linewidth=1.5)
                    if dos_range is not None:
                        ymin = dos_range[0]
                        ymax = dos_range[1]
                    axs[index].set_ylim(ymin, ymax)
                elif doss.spin == 2:
                    if beta == accepted_beta[0]:
                        ymin = 0
                        ymax = np.amax(doss.doss[:, projection, :])
                        yfermi = np.linspace(ymin*1.05, ymax*1.05, 2)
                        axs[index].plot(dx_alpha, doss.doss[:, projection, 0], color=color,
                                        linestyle='-', linewidth=linewidth, label='Alpha')
                        axs[index].plot(dx_beta, -doss.doss[:, projection, 1], color=color,
                                        linestyle='--', linewidth=linewidth, label='Beta')
                        axs[index].plot(
                            xfermi, yfermi, color=fermi, linewidth=1.5)
                        if dos_range is not None:
                            ymin = dos_range[0]
                            ymax = dos_range[1]
                        axs[index].set_ylim(ymin, ymax)
                    elif beta == accepted_beta[1]:
                        ymin = -np.amax(doss.doss[:, projection, :])
                        ymax = np.amax(doss.doss[:, projection, :])
                        yfermi = np.linspace(ymin*1.05, ymax*1.05, 2)
                        axs[index].plot(dx_alpha, doss.doss[:, projection, 0], color=color,
                                        linestyle='-', linewidth=linewidth, label='Alpha')
                        axs[index].plot(dx_beta, doss.doss[:, projection, 1], color=color,
                                        linestyle='--', linewidth=linewidth, label='Beta')
                        axs[index].plot(x_zero, y_zero, linewidth=0.4)
                        axs[index].plot(
                            xfermi, yfermi, color=fermi, linewidth=1.5)
                        if dos_range is not None:
                            ymin = dos_range[0]
                            ymax = dos_range[1]
                        axs[index].set_ylim(ymin, ymax)

        if (doss.spin == 2) and (beta == accepted_beta[1]):
            plt.legend()

    if energy_range is not None:
        xmin = energy_range[0]
        xmax = energy_range[1]
    plt.xlim(xmin, xmax)

    if title is not None:
        fig.suptitle(title)
    if labels is not None:
        plt.legend()

    return fig


def plot_electron_banddos(bands, doss, unit='eV', k_labels=None, dos_beta='down',
                          dos_prj=None, energy_range=None, dos_max_range=None,
                          color_band='blue', color_dos='blue', labels=None, linestl_band='-',
                          linestl_dos=None, linewidth=1, fermi='forestgreen',
                          title=None, figsize=None, save_to_file=None):
    """
    A wrapper of plot_cry_es for electron band structure + dos. For spin-polarized cases, beta state.

    Args:
        bands (BandsBASE|list): Bands object generated by CRYSTALpytools.crystal_io.Properties_output.read_bands
            or a list of BandsBASE objects.
        doss (DOSBASE): DOS object generated by CRYSTALpytools.crystal_io.Properties_output.read_doss
            or a list of DOSBASE objects.
        unit (str): Unit of energy. Valid options are 'eV' or 'Hartree'.
        k_labels (list): A list of high-symmetric k point labels. Greek alphabets should be
            represented as strings, for example, 'Gamma'.
        dos_beta (str): Spin state to plot. Valid options are 'Up' or 'down'. If 'down', the beta
            state will be plotted on the same side as the alpha state, otherwise on the other side.
        dos_prj (list): Index of selected projection. Consistent with the index of the 2nd dimension
            of doss.doss.
        energy_range (list): A list of two values representing the energy range to be plotted.
        dos_max_range (float): Maximum DOS range for the y-axis.
        color_band (str): Color of the electron bands in the plot.
        color_dos (str): Color of the density of states (DOS) in the plot.
        labels (list): A list of labels for the plot legend.
        linestl_band (str): Linestyle of the electron bands.
        linestl_dos (str): Linestyle of the density of states (DOS).
        linewidth (float): Width of the lines in the plot.
        fermi (str): Color of the Fermi level line.
        title (str): Title of the plot.
        figsize (list[float]): Size of the figure in inches (width, height).
        save_to_file (str): File name to save the plot.

    Returns:
        None

    Raises:
        ValueError: If the unit parameter is unknown.

    """
    import matplotlib.pyplot as plt
    from CRYSTALpytools.units import H_to_eV, eV_to_H
    import re

    if re.match(r'^ev$', unit, re.IGNORECASE):
        unit = 'eV'
        is_ev = True
    elif re.match(r'^hartree$', unit, re.IGNORECASE):
        unit = 'Hartree'
        is_ev = False
    else:
        raise ValueError('Unknown unit.')

    if unit != doss.unit:
        if unit == 'eV':
            doss.doss[:, 0, :] = H_to_eV(doss.doss[:, 0, :])
            doss.doss[:, 1:, :] = eV_to_H(doss.doss[:, 1:, :])
        else:
            doss.doss[:, 0, :] = eV_to_H(doss.doss[:, 0, :])
            doss.doss[:, 1:, :] = H_to_eV(doss.doss[:, 1:, :])
        doss.unit = unit
    if unit != bands.unit:
        if unit == 'eV':
            bands.bands[:, :, :] = H_to_eV(bands.bands[:, :, :])
        else:
            bands.bands[:, :, :] = eV_to_H(bands.bands[:, :, :])
        bands.unit = unit

    fig = plot_cry_es(bands=bands, doss=doss, k_labels=k_labels, color_bd=color_band,
                      color_doss=color_dos, fermi=fermi, energy_range=energy_range,
                      linestl_bd=linestl_band, linestl_doss=linestl_dos,
                      linewidth=linewidth, prj=dos_prj, figsize=figsize, labels=labels,
                      dos_max_range=dos_max_range, title=title, dos_beta=dos_beta)
    if is_ev == True:
        fig.supylabel('Energy (eV)')
    else:
        fig.supylabel('Energy (Hartree)')

    if save_to_file != None:
        save_plot(save_to_file)

    plt.show()


def plot_phonon_banddos(bands, doss, unit='cm-1', k_labels=None, dos_prj=None,
                        freq_range=None, dos_max_range=None, color_band='blue',
                        color_dos='blue', labels=None, linestl_band='-',
                        linestl_dos=None, linewidth=1, freq0_line=None,
                        title=None, figsize=None, save_to_file=None):
    """
    A wrapper of plot_cry_es for phonon band structure + dos. Only one pair is permitted.

    Args:
        bands (BandsBASE|list): Bands object generated by CRYSTALpytools.crystal_io.Properties_output.read_bands
            or a list of BandsBASE objects.
        doss (DOSBASE): DOS object generated by CRYSTALpytools.crystal_io.Properties_output.read_doss
            or a list of DOSBASE objects.
        unit (str): Unit of frequency. Valid options are 'cm-1' or 'THz'.
        k_labels (list): A list of high-symmetric k point labels. Greek alphabets should be
            represented as strings, for example, 'Gamma'.
        dos_prj (list): Index of selected projection. Consistent with the index of the 2nd dimension
            of doss.doss.
        freq_range (list): A list of two values representing the frequency range to be plotted.
        dos_max_range (float): Maximum DOS range for the y-axis.
        color_band (str): Color of the phonon bands in the plot.
        color_dos (str): Color of the density of states (DOS) in the plot.
        labels (list): A list of labels for the plot legend.
        linestl_band (str): Linestyle of the phonon bands.
        linestl_dos (str): Linestyle of the density of states (DOS).
        linewidth (float): Width of the lines in the plot.
        freq0_line (str): Color of the frequency=0 line.
        title (str): Title of the plot.
        figsize (list[float]): Size of the figure in inches (width, height).
        save_to_file (str): File name to save the plot.

    Returns:
        None

    Raises:
        ValueError: If the unit parameter is unknown.

    """
    import matplotlib.pyplot as plt
    from CRYSTALpytools.units import cm_to_thz, thz_to_cm
    import re

    if re.match(r'^cm\-1$', unit, re.IGNORECASE):
        unit = 'cm-1'
        is_thz = False
    elif re.match(r'^thz$', unit, re.IGNORECASE):
        unit = 'THz'
        is_thz = True
    else:
        raise ValueError('Unknown unit.')

    if unit != doss.unit:
        if unit == 'cm-1':
            doss.doss[:, 0, :] = thz_to_cm(doss.doss[:, 0, :])
            doss.doss[:, 1:, :] = cm_to_thz(doss.doss[:, 1:, :])
        else:
            doss.doss[:, 0, :] = cm_to_thz(doss.doss[:, 0, :])
            doss.doss[:, 1:, :] = thz_to_cm(doss.doss[:, 1:, :])
        doss.unit = unit
    if unit != bands.unit:
        if unit == 'cm-1':
            bands.bands[:, :, :] = thz_to_cm(bands.bands[:, :, :])
        else:
            bands.bands[:, :, :] = cm_to_thz(bands.bands[:, :, :])
        bands.unit = unit

    if line_freq0 == None:
        line_freq0 = (1., 0., 0., 0.) # Transparent

    fig = plot_cry_es(bands=bands, doss=doss, k_labels=k_labels, color_bd=color_band,
                      color_doss=color_dos, fermi=line_freq0, energy_range=energy_range,
                      linestl_bd=linestl_band, linestl_doss=linestl_dos,
                      linewidth=linewidth, prj=dos_prj, figsize=figsize, labels=labels,
                      dos_max_range=dos_max_range, title=title, dos_beta='up')
    if is_thz == True:
        fig.supylabel('Frequency (THz)')
    else:
        fig.supylabel('Frequency (cm$^{-1}$)')

    if save_to_file != None:
        save_plot(save_to_file)

    plt.show()


def plot_cry_es(bands, doss, k_labels, color_bd, color_doss, fermi, energy_range, linestl_bd,
                linestl_doss, linewidth, prj, figsize, labels, dos_max_range, title, dos_beta):
    """
    The base function to plot electron / phonon band structure + DOS

    Args:
        bands (object): Object containing band structure data
        doss (object): Object containing density of states data
        k_labels (list or None): List of labels for high symmetry points along the path
        color_bd (str): Color for the band structure plot
        color_doss (str or list or tuple): Color(s) for the density of states plot
        fermi (str): Color for the Fermi level lines
        energy_range (list or None): Range of energy values for the y-axis
        linestl_bd (str): Linestyle for the band structure plot
        linestl_doss (str or list or tuple or None): Linestyle(s) for the density of states plot
        linewidth (float): Width of the lines
        prj (list or None): List of projection indices for plotting specific projections
        figsize (tuple): Figure size (width, height)
        labels (str or list or tuple or None): Labels for the density of states plot
        dos_max_range (float or None): Maximum range of the density of states plot
        title (str or None): Title of the figure
        dos_beta (str): Beta state for the density of states plot ('up' or 'down')

    Returns:
        fig (object): Figure object containing the plotted data
    """
    import numpy as np
    import matplotlib.pyplot as plt
    import warnings
    from os import path

    # Dictionary of greek letters for the band plot in the electronic structure
    greek = {'Alpha': '\u0391', 'Beta': '\u0392', 'Gamma': '\u0393', 'Delta': '\u0394', 'Epsilon': '\u0395', 'Zeta': '\u0396', 'Eta': '\u0397',
             'Theta': '\u0398', 'Iota': '\u0399', 'Kappa': '\u039A', 'Lambda': '\u039B', 'Mu': '\u039C', 'Nu': '\u039D', 'Csi': '\u039E',
             'Omicron': '\u039F', 'Pi': '\u03A0', 'Rho': '\u03A1', 'Sigma': '\u03A3', 'Tau': '\u03A4', 'Upsilon': '\u03A5', 'Phi': '\u03A6',
             'Chi': '\u03A7', 'Psi': '\u03A8', 'Omega': '\u03A9', 'Sigma_1': '\u03A3\u2081'}

    if isinstance(color_doss, list) or isinstance(color_doss, tuple):
        # Error check on linestl_doss length when the prj kwargs is not used
        if (prj is None) and (len(color_doss) != doss.n_proj):
            if len(color_doss) > doss.n_proj:
                warnings.warn('You have a number of linestl_doss elements is greater than the number of projection!',
                              stacklevel=2)
            else:
                raise ValueError("You don't have enough elements in linestl_doss for the number of projection required")
        # Error check on linestl_doss length when the prj kwargs is used
        elif (prj is not None) and (len(color_doss) != len(prj)):
            if len(color_doss) > len(prj):
                warnings.warn('You have a number of linestl_doss element greater than the number of projection required(prj elements)!',
                              stacklevel=2)
            else:
                raise ValueError("You don't have enough elements in linestl_doss for the number of projection required(prj elements)")
    else:
        if prj == None:
            nprj = doss.n_proj
        else:
            nprj = len(prj)
        if nprj > 1:
            warnings.warn('Only one color / no color is given. All DOS projections are in the same color.')
        color_doss = [color_doss for i in range(nprj)]

    if isinstance(labels, list) or isinstance(labels, tuple):
        # Error check on labels length when the prj kwargs is not used
        if (prj is None) and (len(labels) != doss.n_proj):
            if len(labels) > doss.n_proj:
                warnings.warn('You have a number of labels greater than the number of projection!')
            else:
                raise ValueError("You don't have enough elements in labels for the numeber of projection required")
        # Error check on labels length when the prj kwargs is used
        elif (prj is not None) and (len(labels) != len(prj)):
            if len(labels) > len(prj):
                warnings.warn('You have a number of linestl_doss element greater than the number of projection required(prj elements)!',
                              stacklevel=2)
            else:
                raise ValueError("You don't have enough elements in linestl_doss for the number of projection required(prj elements)")
    else:
        if prj == None:
            nprj = doss.n_proj
        else:
            nprj = len(prj)
        if nprj > 1:
            warnings.warn('Label not given. No label is available for DOS.')
        labels = [None for i in range(nprj)]

    # DOS beta state
    if dos_beta == 'up':
        spin_idx = -1 # DOS in crystal output is distinguished by +/- sign already
        line_0 = False
    elif dos_beta == 'down':
        spin_idx = 1
        line_0 = True
    else:
        raise ValueError("'dos_beta' should be either 'up' or 'down'.")
    if doss.doss.shape[2] == 2:
        doss.doss[:, :, 1] = doss.doss[:, :, 1] * spin_idx

    # Definition and creation of the figure and the axes
    fig, axs = plt.subplots(nrows=1, ncols=2, gridspec_kw={'width_ratios': [2, 1]},
                            sharex=False, sharey=True, figsize=figsize)
    if title != None:
        fig.suptitle(title)

    # Definition of the hsp position variables
    hsp = bands.tick_position

    # Error check on k_labels lenght against the HSP poisitions
    if k_labels is not None:
        if len(hsp) != len(k_labels):
            if len(hsp) > len(k_labels):
                raise ValueError('You have specified a number of label smaller than the number of High Simmetry Point along the path')
            elif len(hsp) < len(k_labels):
                raise ValueError('You have more labels than the High Simmetry point along the path')

    # Local variable definition for the band plot
    dx_bd = bands.k_point_plot
    pltband = bands.bands
    no_bands = np.shape(pltband)[0]
    ymin_bd = np.amin(pltband)
    ymax_bd = np.amax(pltband)
    xmin_bd = np.amin(dx_bd)
    xmax_bd = np.amax(dx_bd)
    count1 = 0
    count2 = 0

    # band plot
    for i in range(no_bands):
        if bands.spin == 1:
            axs[0].plot(dx_bd, pltband[i, :], color=color_bd,
                        linestyle=linestl_bd, linewidth=linewidth)

        elif bands.spin == 2:
            if count1 == count2:
                axs[0].plot(dx_bd, pltband[i, :, 0], color=color_bd,
                            linestyle='-', linewidth=linewidth, label='Alpha')
                axs[0].plot(dx_bd, pltband[i, :, 1], color=color_bd,
                            linestyle='--', linewidth=linewidth, label='Beta')
            else:
                axs[0].plot(dx_bd, pltband[i, :, 0], color=color_bd,
                            linestyle='-', linewidth=linewidth)
                axs[0].plot(dx_bd, pltband[i, :, 1], color=color_bd,
                            linestyle='--', linewidth=linewidth)

        count1 += 1

    # Definition of dx for the doss plot
    if doss.spin == 1:
        dx_dos = doss.doss[:, 0]
    elif doss.spin == 2:
        dx_dos = doss.doss[:, 0, :]
        dx_alpha = doss.doss[:, 0, 0]
        dx_beta = doss.doss[:, 0, 1]

    # Determination of xmin, xmax, ymin, and ymax
    if prj != None:
        argplt = prj
    else:
        argplt = range(1, doss.doss.shape[1])

    # Plot a vertical line at 0 DOS. Only for spin polarized cases
    if line_0 == True and doss.spin == 2:
        xmin_dos = np.amin(doss.doss[:, argplt, 1])
        xmax_dos = np.amax(doss.doss[:, argplt, 0])
        # make the scale symmetric, for comparison
        xmin_dos = -max([abs(xmin_dos), abs(xmax_dos)])
        xmax_dos = -xmin_dos
    else:
        xmin_dos = 0.
        xmax_dos = np.amax(doss.doss[:, argplt, :])

    ymin_dos = np.amin(dx_dos)
    ymax_dos = np.amax(dx_dos)

    # Plot of all projections
    if prj is None:
        for projection in range(1, doss.n_proj+1):
            if doss.spin == 1:

                if doss.n_proj > 1:

                    if linestl_doss is None:
                        axs[1].plot(doss.doss[:, projection], dx_dos, color=color_doss[projection-1],
                                    label=labels[projection-1], linewidth=linewidth)

                    else:
                        axs[1].plot(doss.doss[:, projection], dx_dos, color=color_doss[projection-1],
                                    label=labels[projection-1], linestyle=linestl_doss[projection-1], linewidth=linewidth)

                else:
                    axs[1].plot(doss.doss[:, projection], dx_dos, color=color_doss[0],
                                linewidth=linewidth)

            elif doss.spin == 2:
                if doss.n_proj > 1:
                    axs[1].plot(doss.doss[:, projection, 0], dx_alpha, color=color_doss[projection-1],
                                label=labels[projection-1], linestyle='-', linewidth=linewidth)
                    axs[1].plot(doss.doss[:, projection, 1], dx_beta, color=color_doss[projection-1],
                                label=labels[projection-1], linestyle='--', linewidth=linewidth)
                else:
                    axs[1].plot(doss.doss[:, projection, 0], dx_alpha, color=color_doss[0],
                                linestyle='-', linewidth=linewidth)
                    axs[1].plot(doss.doss[:, projection, 1], dx_beta, color=color_doss[0],
                                linestyle='--', linewidth=linewidth)

    # Plot of a selected number of projections
    else:
        for index, projection in enumerate(prj):
            if doss.spin == 1:
                if doss.n_proj > 1:
                    if linestl_doss is None:
                        axs[1].plot(doss.doss[:, projection], dx_dos, color=color_doss[index],
                                    label=labels[index], linewidth=linewidth)
                    else:
                        axs[1].plot(doss.doss[:, projection], dx_dos, color=color_doss[index],
                                    label=labels[index], linestyle=linestl_doss[index], linewidth=linewidth)
                else:
                    axs[1].plot(doss.doss[:, projection], dx_dos, color=color_doss[0],
                                linewidth=linewidth)
            elif doss.spin == 2:
                if doss.n_proj > 1:
                    axs[1].plot(doss.doss[:, projection, 0], dx_alpha, color=color_doss[index],
                                label=labels[index], linestyle='-', linewidth=linewidth)
                    axs[1].plot(doss.doss[:, projection, 1], dx_beta, color=color_doss[index],
                                label=labels[index], linestyle='--', linewidth=linewidth)
                else:
                    axs[1].plot(doss.doss[:, projection, 0], dx_alpha, color=color_doss[0],
                                linestyle='-', linewidth=linewidth)
                    axs[1].plot(doss.doss[:, projection, 1], dx_beta, color=color_doss[0],
                                linestyle='--', linewidth=linewidth)

    if ymin_bd > ymin_dos:
        ymin = ymin_dos
    elif ymin_bd <= ymin_dos:
        ymin = ymin_bd

    if ymax_bd >= ymax_dos:
        ymax = ymax_bd
    elif ymax_bd < ymax_dos:
        ymax = ymax_dos

    xmax_bd = hsp[len(hsp)-1]
    # Plot of HSP lines
    yhsp = np.linspace(ymin-5, ymax+5, 2)
    for j in hsp:
        xhsp = np.ones(2)*j
        axs[0].plot(xhsp, yhsp, color='black', linewidth=0.5)

    # Creation if HSP label ticks
    hsp_label = []
    if k_labels is not None:
        for n in k_labels:
            if n in greek:
                g = greek.get(n)
                hsp_label.append(g)
            else:
                hsp_label.append(n)

    axs[0].set_xticks(hsp)
    if k_labels is not None:
        axs[0].set_xticklabels(hsp_label)

    xfermi_bd = np.linspace(xmin_bd, xmax_bd, 2)
    xfermi_dos = np.linspace(xmin_dos*1.05, xmax_dos*1.05, 2)
    yfermi = np.zeros(2)

    # Plot of fermi level lines both in the band and the doss plot
    axs[0].plot(xfermi_bd, yfermi, color=fermi, linewidth=1.5)
    axs[1].plot(xfermi_dos, yfermi, color=fermi, linewidth=1.5)

    axs[0].set_xlim(xmin_bd, xmax_bd)

    if dos_max_range is not None:
        xmax_dos = dos_max_range

    # if (prj is None) and (doss.n_proj not in prj):
    #    xmax_dos = np.amax(doss.doss[:, 1:doss.n_proj-1, :])

    if line_0 == True:
        axs[1].plot(np.zeros([2,]), [ymin, ymax], color='black', linewidth=0.5)
    axs[1].set_xlim(xmin_dos*1.05, xmax_dos*1.05)

    if energy_range is not None:
        ymin = energy_range[0]
        ymax = energy_range[1]

    plt.ylim(ymin, ymax)
    plt.legend()

    return fig


def plot_cry_contour(contour_obj, save_to_file=False):
    """
    Plot a contour plot.

    Args:
        contour_obj (object): Contour object representing the contour plot.
        save_to_file (bool, optional): If True, saves the plot to a file. Default is False.

    Returns:
        None

    Notes:
        - Plots a contour plot based on the data in the contour object.
        - Retrieves the data from the contour object and converts it to a 2D list.
        - Sets the figure size based on x_graph_param and y_graph_param attributes of the contour object.
        - Sets the x-axis and y-axis labels.
        - Creates a meshgrid using the x_points and y_points attributes of the contour object.
        - Defines contour levels, colors, linestyles, and fmt.
        - Plots the contour plot.
        - Saves the plot to a file named 'figure_TIPO_YYYY-MM-DD_HHMMSS.jpg' in the current directory.
        - If save_to_file is True, saves the plot to a file specified by save_to_file parameter.

    """
    import matplotlib.pyplot as plt
    import os
    import numpy as np
    import time

    df = contour_obj.df
    n_punti_x = contour_obj.npx

    for i in range(0, 8):
        df[i] = df[i].astype(float)

    flat_list = [item for sublist in df.values for item in sublist]

    cleaned_list = [x for x in flat_list if ~np.isnan(x)]

    l = [cleaned_list[x:x+n_punti_x]
         for x in range(0, len(cleaned_list), n_punti_x)]

    c = contour_obj.x_graph_param
    d = contour_obj.y_graph_param

    plt.rcParams["figure.figsize"] = [c, d]

    plt.xlabel(r'$\AA$', fontsize=18)
    plt.ylabel(r'$\AA$', fontsize=18)

    X, Y = np.meshgrid(contour_obj.x_points, contour_obj.y_points)

    levels = contour_obj.levels
    colors = contour_obj.colors
    linestyles = contour_obj.linestyles
    fmt = contour_obj.fmt

    # Change here to have or not the isovalues on the plot
    iso = True
    # iso = False

    if (iso == True):
        L = plt.contour(X, Y, l, levels=levels, colors=colors, linestyles=linestyles, linewidths=0.7,
                        alpha=1)
        plt.clabel(L, inline=1, fontsize=7, fmt=fmt)
    elif (iso == False):
        L = plt.contour(X, Y, l, levels=levels, colors=colors, linestyles=linestyles, linewidths=0.7,
                        alpha=1)

    path = os.path.join('./'+'figure_' + contour_obj.tipo +
                        '_' + time.strftime("%Y-%m-%d_%H%M%S") + '.jpg')
    plt.savefig(path, bbox_inches='tight', dpi=600)
    print('\nThe image has been saved in the current directory')

    if save_to_file != False:
        save_plot(save_to_file)

    plt.show()


def plot_cry_contour_differences(contour_obj, contour_obj_ref, save_to_file=False):
    """
    Plot the differences between two contour plots.

    Args:
        contour_obj (object): Contour object representing the original contour plot.
        contour_obj_ref (object): Contour object representing the reference contour plot.
        save_to_file (bool, optional): If True, saves the plot to a file. Default is False.

    Returns:
        None

    Notes:
        - Plots the differences between two contour plots.
        - Requires the contour objects to have a tipo attribute with values 'SURFLAPP', 'SURFLAPM', 'SURFRHOO', or 'SURFELFB'.
        - Calculates the difference between the dataframes of the two contour objects.
        - Sets the figure size based on x_graph_param and y_graph_param attributes of the contour object.
        - Sets the x-axis and y-axis labels.
        - Creates a meshgrid using the x_points and y_points attributes of the contour object.
        - Defines contour levels, colors, and linestyles.
        - Plots the contour differences.
        - Saves the plot to a file named 'figure_diff_TIPO_YYYY-MM-DD_HHMMSS.jpg' in the current directory.
        - If save_to_file is True, saves the plot to a file specified by save_to_file parameter.

    """
    import matplotlib.pyplot as plt
    import os
    import numpy as np
    import time
    import sys

    if (contour_obj.tipo == 'SURFLAPP') or (contour_obj.tipo == 'SURFLAPM') or (contour_obj.tipo == 'SURFRHOO') or (contour_obj.tipo == 'SURFELFB'):
        pass
    else:
        sys.exit(
            'Difference option only allowed for SURFLAPP, SURFLAPM, SURFRHOO and SURFELFB file')

    n_punti_x = contour_obj.npx

    df = contour_obj.df
    for i in range(0, 8):
        df[i] = df[i].astype(float)

    df_ref = contour_obj_ref.df
    for i in range(0, 8):
        df_ref[i] = df_ref[i].astype(float)

    df_diff = df - df_ref

    flat_list = [item for sublist in df_diff.values for item in sublist]

    cleaned_list = [x for x in flat_list if ~np.isnan(x)]

    l = [cleaned_list[x:x+n_punti_x]
         for x in range(0, len(cleaned_list), n_punti_x)]

    c = contour_obj.x_graph_param
    d = contour_obj.y_graph_param

    plt.rcParams["figure.figsize"] = [c, d]

    plt.xlabel(r'$\AA$', fontsize=18)
    plt.ylabel(r'$\AA$', fontsize=18)

    X, Y = np.meshgrid(contour_obj.x_points, contour_obj.y_points)

    ctr1dif = np.array([-8, -4, -2, -0.8, -0.4, -0.2, -0.08, -0.04, -0.02, -0.008, -0.004, -0.002, -0.0008, -0.0004, -0.0002, 0,
                       0.0002, 0.0004, 0.0008, 0.002, 0.004, 0.008, 0.02, 0.04, 0.08, 0.2, 0.4, 0.8, 2, 4, 8])
    colors1dif = ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'k', 'r', 'r', 'r', 'r', 'r', 'r', 'r',
                  'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r']
    ls1dif = ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', 'dotted', '-', '-', '-', '-',
              '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']

    levels = ctr1dif
    colors = colors1dif
    linestyles = ls1dif
    fmt = '%1.4f'

    # Change here to have or not the isovalues on the plot
    iso = True
    # iso = False

    if (iso == True):
        L = plt.contour(X, Y, l, levels=levels, colors=colors, linestyles=linestyles, linewidths=0.7,
                        alpha=1)
        plt.clabel(L, inline=1, fontsize=7, fmt=fmt)
    elif (iso == False):
        L = plt.contour(X, Y, l, levels=levels, colors=colors, linestyles=linestyles, linewidths=0.7,
                        alpha=1)

    path = os.path.join('./'+'figure_diff_' + contour_obj.tipo +
                        '_' + time.strftime("%Y-%m-%d_%H%M%S") + '.jpg')
    plt.savefig(path, bbox_inches='tight', dpi=600)
    print('\nThe image has been saved in the current directory')

    if save_to_file != False:
        save_plot(save_to_file)

    plt.show()


def plot_cry_xrd(xrd_obj, save_to_file=False):
    """
    Plot the X-ray diffraction pattern.

    Args:
        xrd_obj (object): XRD object containing the data for the X-ray diffraction pattern.
        save_to_file (bool, optional): If True, saves the plot to a file. Default is False.

    Returns:
        None

    Notes:
        - Plots the X-ray diffraction pattern.
        - Sets the figure size to [16, 9].
        - Sets the x-axis limit to (0, 30).
        - Saves the plot to a file named 'figure_XRD_YYYY-MM-DD_HHMMSS.jpg' in the current directory.
        - If save_to_file is True, saves the plot to a file specified by save_to_file parameter.

    """
    import matplotlib.pyplot as plt
    import os
    import time

    plt.rcParams["figure.figsize"] = [16, 9]

    plt.plot(xrd_obj.x, xrd_obj.y)

    plt.xlim((0, 30))

    path = os.path.join('./'+'figure_'+'XRD_' +
                        time.strftime("%Y-%m-%d_%H%M%S") + '.jpg')
    plt.title(xrd_obj.title, fontsize=20)
    plt.savefig(path, bbox_inches='tight', dpi=600)

    if save_to_file != False:
        save_plot(save_to_file)

    plt.show()


def plot_cry_rholine(rholine_obj, save_to_file=False):
    """
    Plot the resistivity as a function of distance.

    Args:
        rholine_obj (object): Rholine object containing the data for the resistivity.
        save_to_file (bool, optional): If True, saves the plot to a file. Default is False.

    Returns:
        None

    Notes:
        - Plots the resistivity as a function of distance.
        - Sets the x-axis label as 'd  [$\AA$]' and the y-axis label as r'$\rho$  [$\frac{e}{\AA^3}$]'.
        - Saves the plot to a file named 'figure_rholine_YYYY-MM-DD_HHMMSS.jpg' in the current directory.
        - If save_to_file is True, saves the plot to a file specified by save_to_file parameter.

    """
    import matplotlib.pyplot as plt
    import os
    import time

    plt.plot(rholine_obj.x, rholine_obj.y)

    plt.xlabel('d  [$\AA$]', fontsize=14)
    plt.ylabel(r'$\rho$  [$\frac{e}{\AA^3}$]', fontsize=16)

    path = os.path.join('./'+'figure_'+'rholine_' +
                        time.strftime("%Y-%m-%d_%H%M%S") + '.jpg')
    plt.title(rholine_obj.title, fontsize=15)
    plt.savefig(path, bbox_inches='tight', dpi=600)

    if save_to_file != False:
        save_plot(save_to_file)

    plt.show()


def plot_cry_seebeck_potential(seebeck_obj, save_to_file=False):
    """
    Plot the Seebeck coefficient as a function of chemical potential.

    Args:
        seebeck_obj (object): Seebeck object containing the data for the Seebeck coefficient.
        save_to_file (bool, optional): If True, saves the plot to a file. Default is False.

    Returns:
        None

    Notes:
        - Prompts the user to choose the direction to plot among S_xx, S_xy, S_xz, S_yx, S_yy, S_yz, S_yz, S_zx, S_zy, S_zz.
        - Plots the Seebeck coefficient as a function of chemical potential for each temperature.
        - Distinguishes between n-type and p-type conduction with dashed and solid lines, respectively.
        - If save_to_file is True, saves the plot to a file named 'seebeck_potential_at_T_K___YYYY-MM-DD_HHMMSS.jpg' for each temperature, and 'seebeck_potential_different_T_YYYY-MM-DD_HHMMSS.jpg' for all temperatures combined.

    """
    import sys
    import matplotlib.pyplot as plt
    import numpy as np
    import time

    case = input(
        'Please, choose the direction you want to plot. \nYou can choose among S_xx, S_xy, S_xz, S_yx, S_yy, S_yz, S_yz, S_zx, S_zy, S_zz\n')

    case = case.lower().replace('_', '')

    if case.isalpha() == True:
        pass
    else:
        sys.exit('Please, select a valid chioce')

    if case == 'sxx':
        col = 3
    elif case == 'sxy':
        col = 4
    elif case == 'sxz':
        col = 5
    elif case == 'syx':
        col = 6
    elif case == 'syy':
        col = 7
    elif case == 'syz':
        col = 8
    elif case == 'szx':
        col = 9
    elif case == 'szy':
        col = 10
    elif case == 'szz':
        col = 11

    else:
        sys.exit('please, choose a valid chioce')

    vol = seebeck_obj.volume

    x = []
    for k in range(0, len(seebeck_obj.all_data)):
        x.append(np.array(seebeck_obj.all_data[k].apply(
            lambda x: float(x.split()[0]))))

    carrier = []
    for k in range(0, len(seebeck_obj.all_data)):
        carrier.append(np.array(seebeck_obj.all_data[k].apply(
            lambda x: (float(x.split()[2])/vol))))

    y = []
    for k in range(0, len(seebeck_obj.all_data)):
        y.append(np.array(seebeck_obj.all_data[k].apply(
            lambda x: float(x.split()[col])*1000000)))

    yneg = []
    ypos = []
    xpos = []
    xneg = []
    yposfin = []
    xposfin = []
    ynegfin = []
    xnegfin = []

    for k in range(0, len(seebeck_obj.all_data)):
        for j in range(0, len(carrier[k])):
            if carrier[k][j] >= 0:
                xpos.append(x[k][j])
                ypos.append(y[k][j])
            else:
                xneg.append(x[k][j])
                yneg.append(y[k][j])
        yposfin.append(ypos)
        ynegfin.append(yneg)
        xposfin.append(xpos)
        xnegfin.append(xneg)
        xpos = []
        ypos = []
        xneg = []
        yneg = []

    print('To differentiate transport coefficients due to n-type or p-type conduction (electrons or holes as majority carriers) dashed and solid lines are used, respectively.')

    colours = ['royalblue', 'orange', 'green', 'red',
               'purple', 'brown', 'pink', 'grey', 'olive', 'cyan']

    endx = []
    endy = []

    for k in range(0, len(seebeck_obj.all_data)):
        endx = [xposfin[k][-1], xnegfin[k][0]]
        endy = [yposfin[k][-1], ynegfin[k][0]]
        plt.figure()
        plt.plot(endx, endy, color=colours[k])
        plt.plot(xposfin[k], yposfin[k], color=colours[k],
                 label=str(seebeck_obj.temp[k])+' K')
        plt.plot(xnegfin[k], ynegfin[k], '--', color=colours[k])
        plt.xlabel('Chemical Potential (eV)', fontsize=12)
        plt.ylabel('Seebeck Coefficient ($\mu$V/K)', fontsize=12)
        plt.axhline(0, color='k')
        plt.title('Seebeck at ' + str(seebeck_obj.temp[k]) + ' K')
        plt.legend(loc='upper left', fontsize=12)
        plt.savefig('seebeck_potential_at_' + str(seebeck_obj.temp[k]) + 'K___' + time.strftime(
            "%Y-%m-%d_%H%M%S") + '.jpg', format='jpg', dpi=600, bbox_inches='tight')
        plt.show()

    from matplotlib.pyplot import figure
    figure(figsize=(7, 7))
    for k in range(0, len(seebeck_obj.all_data)):
        endx = [xposfin[k][-1], xnegfin[k][0]]
        endy = [yposfin[k][-1], ynegfin[k][0]]
        plt.plot(endx, endy, color=colours[k])
        plt.plot(xposfin[k], yposfin[k], color=colours[k],
                 label=str(seebeck_obj.temp[k])+' K')
        plt.plot(xnegfin[k], ynegfin[k], '--', color=colours[k])
        plt.xlabel('Chemical Potential (eV)', fontsize=12)
        plt.axhline(0, color='k')
        plt.title('Seebeck at different T')
    plt.savefig('seebeck_potential_different_T_' + time.strftime("%Y-%m-%d_%H%M%S") +
                '.jpg', format='jpg', dpi=100, bbox_inches='tight')
    plt.show()
    if save_to_file != False:
        save_plot(save_to_file)


def plot_cry_sigma_potential(sigma_obj, save_to_file=False):
    """
    Plot the electrical conductivity as a function of chemical potential.

    Args:
        sigma_obj (object): Sigma object containing the data for electrical conductivity.
        save_to_file (bool, optional): If True, saves the plot to a file. Default is False.

    Returns:
        None

    Notes:
        - Prompts the user to choose the direction to plot among S_xx, S_xy, S_xz, S_yy, S_yz, S_zz.
        - Plots the electrical conductivity as a function of chemical potential for each temperature.
        - Distinguishes between n-type and p-type conduction with dashed and solid lines, respectively.
        - If save_to_file is True, saves the plot to a file named 'sigma_potential_at_T_K___YYYY-MM-DD_HHMMSS.jpg' for each temperature, and 'sigma_potential_different_T_YYYY-MM-DD_HHMMSS.jpg' for all temperatures combined.

    """
    import sys
    import matplotlib.pyplot as plt
    import numpy as np
    import time

    case = input(
        'Please, choose the direction you want to plot. \nYou can choose among S_xx, S_xy, S_xz, S_yy, S_yz, S_zz\n')

    case = case.lower().replace('_', '')

    if case.isalpha() == True:
        pass
    else:
        sys.exit('Please, select a valid chioce')

    if case == 'sxx':
        col = 3
    elif case == 'sxy':
        col = 4
    elif case == 'sxz':
        col = 5
    elif case == 'syy':
        col = 6
    elif case == 'syz':
        col = 7
    elif case == 'szz':
        col = 8
    else:
        sys.exit('please, choose a valid chioce')

    vol = sigma_obj.volume

    x = []
    for k in range(0, len(sigma_obj.all_data)):
        x.append(np.array(sigma_obj.all_data[k].apply(
            lambda x: float(x.split()[0]))))

    carrier = []
    for k in range(0, len(sigma_obj.all_data)):
        carrier.append(np.array(sigma_obj.all_data[k].apply(
            lambda x: (float(x.split()[2])/vol))))

    y = []
    for k in range(0, len(sigma_obj.all_data)):
        y.append(np.array(sigma_obj.all_data[k].apply(
            lambda x: float(x.split()[col]))))

    yneg = []
    ypos = []
    xpos = []
    xneg = []
    yposfin = []
    xposfin = []
    ynegfin = []
    xnegfin = []

    for k in range(0, len(sigma_obj.all_data)):
        for j in range(0, len(x[k])):
            if carrier[k][j] >= 0:
                xpos.append(x[k][j])
                ypos.append(y[k][j])
            else:
                xneg.append(x[k][j])
                yneg.append(y[k][j])
        yposfin.append(ypos)
        ynegfin.append(yneg)
        xposfin.append(xpos)
        xnegfin.append(xneg)
        xpos = []
        ypos = []
        xneg = []
        yneg = []

    print('To differentiate transport coefficients due to n-type or p-type conduction (electrons or holes as majority carriers) dashed and solid lines are used, respectively.')
    colours = []
    colours = ['royalblue', 'orange', 'green', 'red',
               'purple', 'brown', 'pink', 'grey', 'olive', 'cyan']
    endx = []
    endy = []

    for k in range(0, len(sigma_obj.all_data)):
        endx = [xposfin[k][-1], xnegfin[k][0]]
        endy = [yposfin[k][-1], ynegfin[k][0]]
        plt.figure()
        plt.plot(endx, endy, color=colours[k])
        plt.plot(xposfin[k], yposfin[k], color=colours[k],
                 label=str(sigma_obj.temp[k])+' K')
        plt.plot(xnegfin[k], ynegfin[k], '--', color=colours[k])
        plt.xlabel('Chemical Potential (eV)', fontsize=12)
        plt.ylabel('Electrical Conductivity (S/m)', fontsize=12)
        plt.axhline(0, color='k')
        plt.title('Sigma at '+str(sigma_obj.temp[k]) + 'K')
        plt.legend(loc='upper left', fontsize=12)
        plt.savefig('sigma_potential_at_' + str(sigma_obj.temp[k]) + 'K___' + time.strftime(
            "%Y-%m-%d_%H%M%S") + '.jpg', format='jpg', dpi=600, bbox_inches='tight')
        plt.show()

    for k in range(0, len(sigma_obj.all_data)):
        endx = [xposfin[k][-1], xnegfin[k][0]]
        endy = [yposfin[k][-1], ynegfin[k][0]]
        plt.plot(endx, endy, color=colours[k])
        plt.plot(xposfin[k], yposfin[k], color=colours[k],
                 label=str(sigma_obj.temp[k])+' K')
        plt.plot(xnegfin[k], ynegfin[k], '--', color=colours[k])
        plt.xlabel('Chemical Potential (eV)', fontsize=12)
        plt.ylabel('Electrical Conductivity (S/m)', fontsize=12)
        plt.title('Sigma at different T')
        plt.axhline(0, color='k')
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
    plt.savefig('sigma_potential_different_T_' + time.strftime("%Y-%m-%d_%H%M%S") +
                '.jpg', format='jpg', dpi=100, bbox_inches='tight')

    if save_to_file != False:
        save_plot(save_to_file)


def plot_cry_seebeck_carrier(seebeck_obj, save_to_file=False):
    """
    Plot the Seebeck coefficient as a function of charge carrier concentration.

    Args:
        seebeck_obj: Seebeck object containing the data for the Seebeck coefficient.
        save_to_file (optional): If True, saves the plot to a file. Default is False.

    Returns:
        None

    Notes:
        - Prompts the user to choose the direction to plot among S_xx, S_xy, S_xz, S_yx, S_yy, S_yz, S_yz, S_zx, S_zy, S_zz.
        - Plots the Seebeck coefficient as a function of charge carrier concentration for each temperature, distinguishing between n-type and p-type conduction.
        - If save_to_file is True, saves the plot to a file named 'seebeck_carrier_at_T_K___YYYY-MM-DD_HHMMSS.jpg' for each temperature, and 'seebeck_carrier_different_T_YYYY-MM-DD_HHMMSS.jpg' for all temperatures combined.
    """
    import sys
    import matplotlib.pyplot as plt
    import numpy as np
    import time

    case = input(
        'Please, choose the direction you want to plot. \nYou can choose among S_xx, S_xy, S_xz, S_yx, S_yy, S_yz, S_yz, S_zx, S_zy, S_zz\n')

    case = case.lower().replace('_', '')

    if case.isalpha() == True:
        pass
    else:
        sys.exit('Please, select a valid chioce')

    if case == 'sxx':
        col = 3
    elif case == 'sxy':
        col = 4
    elif case == 'sxz':
        col = 5
    elif case == 'syx':
        col = 6
    elif case == 'syy':
        col = 7
    elif case == 'syz':
        col = 8
    elif case == 'szx':
        col = 9
    elif case == 'szy':
        col = 10
    elif case == 'szz':
        col = 11
    else:
        sys.exit('please, choose a valid chioce')

    vol = seebeck_obj.volume

    x = []
    for k in range(0, len(seebeck_obj.all_data)):
        x.append(np.array(seebeck_obj.all_data[k].apply(
            lambda x: (float(x.split()[2])/vol))))
    y = []

    for k in range(0, len(seebeck_obj.all_data)):
        y.append(np.array(seebeck_obj.all_data[k].apply(
            lambda x: float(x.split()[col])*1000000)))

    yneg = []
    ypos = []
    xpos = []
    xneg = []
    yposfin = []
    xposfin = []
    ynegfin = []
    xnegfin = []

    for k in range(0, len(seebeck_obj.all_data)):
        for j in range(0, len(x[k])):
            if x[k][j] >= 0:
                xpos.append(x[k][j])
                ypos.append(y[k][j])
            else:
                xneg.append(x[k][j])
                yneg.append(y[k][j])
        yposfin.append(ypos)
        ynegfin.append(yneg)
        xposfin.append(xpos)
        xnegfin.append(xneg)
        xpos = []
        ypos = []
        xneg = []
        yneg = []

    print('To differentiate transport coefficients due to n-type or p-type conduction (electrons or holes as majority carriers) dashed and solid lines are used, respectively.')

    colours = []
    colours = ['royalblue', 'orange', 'green', 'red',
               'purple', 'brown', 'pink', 'grey', 'olive', 'cyan']

    for k in range(0, len(seebeck_obj.all_data)):
        endx = [xposfin[k][-1], xnegfin[k][0]]
        endy = [yposfin[k][-1], ynegfin[k][0]]
        plt.figure()
        plt.plot(endx, endy, color=colours[k])
        plt.plot(xposfin[k], yposfin[k], color=colours[k],
                 label=str(seebeck_obj.temp[k])+' K')
        plt.plot(abs(np.array(xnegfin[k])), ynegfin[k], '--', color=colours[k])
        plt.xlabel('Charge Carrier Concentration (cm$^{-3}$)', fontsize=12)
        plt.ylabel('Seebeck Coefficient ($\mu$V/K)', fontsize=12)
        plt.axhline(0, color='k')
        plt.title('Seebeck at ' + str(seebeck_obj.temp[k]) + ' K')
        plt.legend(loc='upper left', fontsize=12)
        plt.xscale('log')
        plt.show()

    from matplotlib.pyplot import figure

    figure(figsize=(7, 7))
    for k in range(0, len(seebeck_obj.all_data)):
        endx = [xposfin[k][-1], xnegfin[k][0]]
        endy = [yposfin[k][-1], ynegfin[k][0]]
        plt.plot(endx, endy, color=colours[k])
        plt.plot(xposfin[k], yposfin[k], color=colours[k],
                 label=str(seebeck_obj.temp[k])+' K')
        plt.plot(abs(np.array(xnegfin[k])), ynegfin[k], '--', color=colours[k])
        plt.xlabel('Charge Carrier Concentration (cm$^{-3}$)', fontsize=12)
        plt.ylabel('Seebeck Coefficient ($\mu$V/K)', fontsize=12)
        plt.axhline(0, color='k')
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
        plt.xscale('log')
        plt.title('Seebeck at different T')
    plt.savefig('seebeck_carrier_different_T_' + time.strftime("%Y-%m-%d_%H%M%S") +
                '.jpg', format='jpg', dpi=100, bbox_inches='tight')
    plt.show()

    if save_to_file != False:
        save_plot(save_to_file)


def plot_cry_sigma_carrier(sigma_obj, save_to_file=False):
    """
    Plot the electrical conductivity as a function of charge carrier concentration.

    Args:
        sigma_obj: Sigma object containing the data for the electrical conductivity.
        save_to_file (optional): If True, saves the plot to a file. Default is False.

    Returns:
        None

    Notes:
        - Prompts the user to choose the direction to plot among S_xx, S_xy, S_xz, S_yy, S_yz, S_zz.
        - Plots the electrical conductivity as a function of charge carrier concentration for each temperature, distinguishing between n-type and p-type conduction.
        - If save_to_file is True, saves the plot to a file named 'sigma_carrier_at_T_K___YYYY-MM-DD_HHMMSS.jpg' for each temperature, and 'sigma_carrier_different_T_YYYY-MM-DD_HHMMSS.jpg' for all temperatures combined.
    """
    import sys
    import matplotlib.pyplot as plt
    import numpy as np
    import time

    case = input(
        'Please, choose the direction you want to plot. \nYou can choose among S_xx, S_xy, S_xz, S_yy, S_yz, S_zz\n')

    case = case.lower().replace('_', '')

    if case.isalpha() == True:
        pass
    else:
        sys.exit('Please, select a valid chioce')

    if case == 'sxx':
        col = 3
    elif case == 'sxy':
        col = 4
    elif case == 'sxz':
        col = 5
    elif case == 'syy':
        col = 6
    elif case == 'syz':
        col = 7
    elif case == 'szz':
        col = 8
    else:
        sys.exit('please, choose a valid chioce')

    vol = sigma_obj.volume

    x = []
    for k in range(0, len(sigma_obj.all_data)):
        x.append(np.array(sigma_obj.all_data[k].apply(
            lambda x: (float(x.split()[2])/vol))))

    y = []
    for k in range(0, len(sigma_obj.all_data)):
        y.append(np.array(sigma_obj.all_data[k].apply(
            lambda x: float(x.split()[col]))))

    yneg = []
    ypos = []
    xpos = []
    xneg = []
    yposfin = []
    xposfin = []
    ynegfin = []
    xnegfin = []

    for k in range(0, len(sigma_obj.all_data)):
        for j in range(0, len(x[k])):
            if x[k][j] >= 0:
                xpos.append(x[k][j])
                ypos.append(y[k][j])
            else:
                xneg.append(x[k][j])
                yneg.append(y[k][j])
        yposfin.append(ypos)
        ynegfin.append(yneg)
        xposfin.append(xpos)
        xnegfin.append(xneg)
        xpos = []
        ypos = []
        xneg = []
        yneg = []

    print('To differentiate transport coefficients due to n-type or p-type conduction (electrons or holes as majority carriers) dashed and solid lines are used, respectively.')

    colours = []
    colours = ['royalblue', 'orange', 'green', 'red',
               'purple', 'brown', 'pink', 'grey', 'olive', 'cyan']

    for k in range(0, len(sigma_obj.all_data)):
        endx = [xposfin[k][-1], xnegfin[k][0]]
        endy = [yposfin[k][-1], ynegfin[k][0]]
        plt.figure()
        plt.plot(endx, endy, color=colours[k])
        plt.plot(xposfin[k], yposfin[k], color=colours[k],
                 label=str(sigma_obj.temp[k])+' K')
        plt.plot(abs(np.array(xnegfin[k])), ynegfin[k], '--', color=colours[k])
        plt.xlabel('Charge Carrier Concentration (cm$^{-3}$)', fontsize=12)
        plt.ylabel('Electrical Conductivity (S/m)', fontsize=12)
        plt.axhline(0, color='k')
        plt.title('Sigma at ' + str(sigma_obj.temp[k]) + 'K')
        plt.legend(loc='upper left', fontsize=12)
        plt.xscale('log')
        plt.savefig('sigma_carrier_at_' + str(sigma_obj.temp[k]) + 'K___' + time.strftime(
            "%Y-%m-%d_%H%M%S") + '.jpg', format='jpg', dpi=600, bbox_inches='tight')
        plt.show()

    for k in range(0, len(sigma_obj.all_data)):
        endx = [xposfin[k][-1], xnegfin[k][0]]
        endy = [yposfin[k][-1], ynegfin[k][0]]
        plt.plot(endx, endy, color=colours[k])
        plt.plot(xposfin[k], yposfin[k], color=colours[k],
                 label=str(sigma_obj.temp[k])+' K')
        plt.plot(abs(np.array(xnegfin[k])), ynegfin[k], '--', color=colours[k])
        plt.xlabel('Charge Carrier Concentration (cm$^{-3}$)', fontsize=12)
        plt.ylabel('Electrical Conductivity (S/m)', fontsize=12)
        plt.title('Sigma at different T')
        plt.axhline(0, color='k')
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
        plt.xscale('log')
    plt.savefig('sigma_carrier_different_T_' + time.strftime("%Y-%m-%d_%H%M%S") +
                '.jpg', format='jpg', dpi=100, bbox_inches='tight')

    if save_to_file != False:
        save_plot(save_to_file)


def plot_cry_powerfactor_potential(seebeck_obj, sigma_obj, save_to_file=False):
    """
    Plot the power factor for different potentials.

    Args:
        seebeck_obj: Seebeck object containing the data for the Seebeck coefficient.
        sigma_obj: Sigma object containing the data for the electrical conductivity.
        save_to_file (optional): If True, saves the plot to a file. Default is False.

    Returns:
        None

    Notes:
        - Prompts the user to choose the direction to plot among PF_xx, PF_xy, PF_xz, PF_yx, PF_yy, PF_yz, PF_yz, PF_zx, PF_zy, PF_zz.
        - Calculates the power factor using the Seebeck coefficient and electrical conductivity data for each temperature.
        - Plots the power factor for each temperature as a function of the chemical potential, distinguishing between n-type and p-type conduction.
        - If save_to_file is True, saves the plot to a file named 'powerfactor_potential_at_T_K___YYYY-MM-DD_HHMMSS.jpg' for each temperature, and 'powerfactor_potential_different_T_YYYY-MM-DD_HHMMSS.jpg' for all temperatures combined.
    """
    import sys
    import matplotlib.pyplot as plt
    import numpy as np
    import time

    case = input(
        'Please, choose the direction you want to plot. \nYou can choose among PF_xx, PF_xy, PF_xz, PF_yx, PF_yy, PF_yz, PF_yz, PF_zx, PF_zy, PF_zz\n')

    case = case.lower().replace('_', '')

    if case.isalpha() == True:
        pass
    else:
        sys.exit('Please, select a valid chioce')

    if case == 'pfxx':
        col = 3
    elif case == 'pfxy':
        col = 4
    elif case == 'pfxz':
        col = 5
    elif case == 'pfyx':
        col = 6
    elif case == 'pfyy':
        col = 7
    elif case == 'pfyz':
        col = 8
    elif case == 'pfzx':
        col = 9
    elif case == 'pfzy':
        col = 10
    elif case == 'pfzz':
        col = 11
    else:
        sys.exit('please, choose a valid chioce')

    if case == 'pfxx':
        cols = 3
    elif case == 'pfxy':
        cols = 4
    elif case == 'pfxz':
        cols = 5
    elif case == 'pfyx':
        cols = 4
    elif case == 'pfyy':
        cols = 6
    elif case == 'pfyz':
        cols = 7
    elif case == 'pfzx':
        cols = 5
    elif case == 'pfzy':
        cols = 7
    elif case == 'pfzz':
        cols = 8
    else:
        sys.exit('please, choose a valid chioce')

    x = []
    for k in range(0, len(seebeck_obj.all_data)):
        x.append(np.array(seebeck_obj.all_data[k].apply(
            lambda x: float(x.split()[0]))))

    vol = sigma_obj.volume
    carrier = []

    yse = []
    for k in range(0, len(seebeck_obj.all_data)):
        yse.append(np.array(seebeck_obj.all_data[k].apply(
            lambda x: float(x.split()[col]))))

    ysi = []
    for k in range(0, len(sigma_obj.all_data)):
        ysi.append(np.array(sigma_obj.all_data[k].apply(
            lambda x: float(x.split()[cols]))))

    carrier = []
    for k in range(0, len(seebeck_obj.all_data)):
        carrier.append(np.array(seebeck_obj.all_data[k].apply(
            lambda x: (float(x.split()[2])/vol))))

    ysineg = []
    ysipos = []
    xsipos = []
    xsineg = []
    ysiposfin = []
    xsiposfin = []
    ysinegfin = []
    xsinegfin = []

    yseneg = []
    ysepos = []
    xsepos = []
    xseneg = []
    yseposfin = []
    xseposfin = []
    ysenegfin = []
    xsenegfin = []

    for k in range(0, len(seebeck_obj.all_data)):
        for j in range(0, len(carrier[k])):
            if carrier[k][j] >= 0:
                xsipos.append(x[k][j])
                ysipos.append(ysi[k][j])
            else:
                xsineg.append(x[k][j])
                ysineg.append(ysi[k][j])
        ysiposfin.append(np.array(ysipos))
        ysinegfin.append(np.array(ysineg))
        xsiposfin.append(np.array(xsipos))
        xsinegfin.append(np.array(xsineg))
        xsipos = []
        ysipos = []
        xsineg = []
        ysineg = []

    for k in range(0, len(seebeck_obj.all_data)):
        for j in range(0, len(carrier[k])):
            if carrier[k][j] >= 0:
                xsepos.append(x[k][j])
                ysepos.append(yse[k][j])
            else:
                xseneg.append(x[k][j])
                yseneg.append(yse[k][j])

        yseposfin.append(np.array(ysepos))
        ysenegfin.append(np.array(yseneg))
        xseposfin.append(np.array(xsepos))
        xsenegfin.append(np.array(xseneg))
        xsepos = []
        ysepos = []
        xseneg = []
        yseneg = []

    pf_meta_pos = []
    for i in range(0, len(yseposfin)):
        pf_meta_pos.append(yseposfin[i]*yseposfin[i])

    pf_pos = []
    for i in range(0, len(pf_meta_pos)):
        pf_pos.append(pf_meta_pos[i] * ysiposfin[i])

    pf_meta_neg = []
    for i in range(0, len(ysenegfin)):
        pf_meta_neg.append(ysenegfin[i] * ysenegfin[i])

    pf_neg = []
    for i in range(0, len(pf_meta_neg)):
        pf_neg.append(pf_meta_neg[i] * ysinegfin[i])

    print('To differentiate transport coefficients due to n-type or p-type conduction (electrons or holes as majority carriers) dashed and solid lines are used, respectively.')

    colours = []
    colours = ['royalblue', 'orange', 'green', 'red',
               'purple', 'brown', 'pink', 'grey', 'olive', 'cyan']

    for k in range(0, len(seebeck_obj.all_data)):
        endx = [xsiposfin[k][-1], xsinegfin[k][0]]
        endy = [pf_pos[k][-1], pf_neg[k][0]]
        plt.figure()
        plt.plot(endx, endy, color=colours[k])
        plt.plot(xsiposfin[k], pf_pos[k], color=colours[k],
                 label=str(seebeck_obj.temp[k])+' K')
        plt.plot(xsinegfin[k], pf_neg[k], '--', color=colours[k])
        plt.xlabel('Chemical Potential (eV)', fontsize=12)
        plt.ylabel('Power Factor (10$^{-12}$WK$^{-2}$m$^{-1}$)', fontsize=12)
        plt.axhline(0, color='k')
        plt.title('Power Factor at ' + str(seebeck_obj.temp[k]) + ' K')
        plt.legend(loc='upper left', fontsize=12)
        plt.show()

    from matplotlib.pyplot import figure

    figure(figsize=(7, 7))
    for k in range(0, len(seebeck_obj.all_data)):
        endx = [xsiposfin[k][-1], xsinegfin[k][0]]
        endy = [pf_pos[k][-1], pf_neg[k][0]]
        plt.plot(endx, endy, color=colours[k])
        plt.plot(xsiposfin[k], pf_pos[k], color=colours[k],
                 label=str(seebeck_obj.temp[k])+' K')
        plt.plot(xsinegfin[k], pf_neg[k], '--', color=colours[k])
        plt.xlabel('Chemical Potential (eV)', fontsize=12)
        plt.axhline(0, color='k')
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
        plt.title('Power Factor at different T')

    plt.savefig('powerfactor_potential_different_T_' + time.strftime(
        "%Y-%m-%d_%H%M%S") + '.jpg', format='jpg', dpi=100, bbox_inches='tight')
    if save_to_file != False:
        save_plot(save_to_file)


def plot_cry_powerfactor_carrier(seebeck_obj, sigma_obj, save_to_file=False):
    """
    Plot the power factor for different charge carrier concentrations.

    Args:
        seebeck_obj: Seebeck object containing the data for the Seebeck coefficient.
        sigma_obj: Sigma object containing the data for the electrical conductivity.
        save_to_file (optional): If True, saves the plot to a file. Default is False.

    Returns:
        None

    Notes:
        - Prompts the user to choose the direction to plot among PF_xx, PF_xy, PF_xz, PF_yx, PF_yy, PF_yz, PF_yz, PF_zx, PF_zy, PF_zz.
        - Calculates the power factor using the Seebeck coefficient and electrical conductivity data for each temperature.
        - Plots the power factor for each temperature as a function of the charge carrier concentration, distinguishing between n-type and p-type conduction.
        - If save_to_file is True, saves the plot to a file named 'powerfactor_carrier_at_T_K___YYYY-MM-DD_HHMMSS.jpg' for each temperature, and 'powerfactor_carrier_different_T_YYYY-MM-DD_HHMMSS.jpg' for all temperatures combined.
    """
    import sys
    import matplotlib.pyplot as plt
    import numpy as np
    import time

    case = input(
        'Please, choose the direction you want to plot. \nYou can choose among PF_xx, PF_xy, PF_xz, PF_yx, PF_yy, PF_yz, PF_yz, PF_zx, PF_zy, PF_zz\n')

    case = case.lower().replace('_', '')

    if case.isalpha() == True:
        pass
    else:
        sys.exit('Please, select a valid chioce')

    if case == 'pfxx':
        col = 3
    elif case == 'pfxy':
        col = 4
    elif case == 'pfxz':
        col = 5
    elif case == 'pfyx':
        col = 6
    elif case == 'pfyy':
        col = 7
    elif case == 'pfyz':
        col = 8
    elif case == 'pfzx':
        col = 9
    elif case == 'pfzy':
        col = 10
    elif case == 'pfzz':
        col = 11
    else:
        sys.exit('please, choose a valid chioce')

    if case == 'pfxx':
        cols = 3
    elif case == 'pfxy':
        cols = 4
    elif case == 'pfxz':
        cols = 5
    elif case == 'pfyx':
        cols = 4
    elif case == 'pfyy':
        cols = 6
    elif case == 'pfyz':
        cols = 7
    elif case == 'pfzx':
        cols = 5
    elif case == 'pfzy':
        cols = 7
    elif case == 'pfzz':
        cols = 8
    else:
        sys.exit('please, choose a valid chioce')

    vol = sigma_obj.volume

    x = []
    for k in range(0, len(sigma_obj.all_data)):
        x.append(np.array(sigma_obj.all_data[k].apply(
            lambda x: (float(x.split()[2])/vol))))

    yse = []
    for k in range(0, len(seebeck_obj.all_data)):
        yse.append(np.array(seebeck_obj.all_data[k].apply(
            lambda x: float(x.split()[col]))))

    ysi = []
    for k in range(0, len(sigma_obj.all_data)):
        ysi.append(np.array(sigma_obj.all_data[k].apply(
            lambda x: float(x.split()[cols]))))

    pf_meta = []
    for i in range(0, len(yse)):
        pf_meta.append(yse[i] * yse[i])

    pf = []
    for i in range(0, len(pf_meta)):
        pf.append(pf_meta[i] * ysi[i])

    ysineg = []
    ysipos = []
    xsipos = []
    xsineg = []
    ysiposfin = []
    xsiposfin = []
    ysinegfin = []
    xsinegfin = []

    yseneg = []
    ysepos = []
    xsepos = []
    xseneg = []
    yseposfin = []
    xseposfin = []
    ysenegfin = []
    xsenegfin = []

    for k in range(0, len(seebeck_obj.all_data)):
        for j in range(0, len(x[k])):
            if x[k][j] >= 0:
                xsipos.append(x[k][j])
                ysipos.append(ysi[k][j])
            else:
                xsineg.append(x[k][j])
                ysineg.append(ysi[k][j])
        ysiposfin.append(np.array(ysipos))
        ysinegfin.append(np.array(ysineg))
        xsiposfin.append(np.array(xsipos))
        xsinegfin.append(np.array(xsineg))
        xsipos = []
        ysipos = []
        xsineg = []
        ysineg = []

    for k in range(0, len(seebeck_obj.all_data)):
        for j in range(0, len(x[k])):
            if x[k][j] >= 0:
                xsepos.append(x[k][j])
                ysepos.append(yse[k][j])
            else:
                xseneg.append(x[k][j])
                yseneg.append(yse[k][j])
        yseposfin.append(np.array(ysepos))
        ysenegfin.append(np.array(yseneg))
        xseposfin.append(np.array(xsepos))
        xsenegfin.append(np.array(xseneg))
        xsepos = []
        ysepos = []
        xseneg = []
        yseneg = []

    pf_meta_pos = []
    for i in range(0, len(yseposfin)):
        pf_meta_pos.append(yseposfin[i]*yseposfin[i])

    pf_pos = []
    for i in range(0, len(pf_meta_pos)):
        pf_pos.append(pf_meta_pos[i] * ysiposfin[i])

    pf_meta_neg = []
    for i in range(0, len(ysenegfin)):
        pf_meta_neg.append(ysenegfin[i] * ysenegfin[i])

    pf_neg = []
    for i in range(0, len(pf_meta_neg)):
        pf_neg.append(pf_meta_neg[i] * ysinegfin[i])

    print('To differentiate transport coefficients due to n-type or p-type conduction (electrons or holes as majority carriers) dashed and solid lines are used, respectively.')

    colours = []
    colours = ['royalblue', 'orange', 'green', 'red',
               'purple', 'brown', 'pink', 'grey', 'olive', 'cyan']

    from matplotlib.pyplot import figure

    for k in range(0, len(seebeck_obj.all_data)):
        endx = [xsiposfin[k][-1], xsinegfin[k][0]]
        endy = [pf_pos[k][-1], pf_neg[k][0]]
        plt.figure()
        plt.plot(endx, endy, color=colours[k])
        plt.plot(xsiposfin[k], pf_pos[k], color=colours[k],
                 label=str(seebeck_obj.temp[k])+' K')
        plt.plot(abs(xsinegfin[k]), pf_neg[k], '--', color=colours[k])
        plt.xlabel('Charge Carrier Concentration (cm$^{-3}$)', fontsize=12)
        plt.ylabel('Power Factor (10$^{-12}$WK$^{-2}$m$^{-1}$)', fontsize=12)
        plt.axhline(0, color='k')
        plt.title('Power Factor at ' + str(seebeck_obj.temp[k]) + ' K')
        plt.legend(loc='upper left', fontsize=12)
        plt.xscale('log')
        plt.savefig('powerfactor_carrier_at_' + str(seebeck_obj.temp[k]) + 'K___' + time.strftime(
            "%Y-%m-%d_%H%M%S") + '.jpg', format='jpg', dpi=600, bbox_inches='tight')
        plt.show()

    from matplotlib.pyplot import figure
    figure(figsize=(7, 7))
    for k in range(0, len(seebeck_obj.all_data)):
        endx = [xsiposfin[k][-1], xsinegfin[k][0]]
        endy = [pf_pos[k][-1], pf_neg[k][0]]
        plt.plot(endx, endy, color=colours[k])
        plt.plot(xsiposfin[k], pf_pos[k], color=colours[k],
                 label=str(seebeck_obj.temp[k])+' K')
        plt.plot(abs(xsinegfin[k]), pf_neg[k], '--', color=colours[k])
        plt.xlabel('Charge Carrier Concentration (cm$^{-3}$)', fontsize=12)
        plt.ylabel('Power Factor (10$^{-12}$WK$^{-2}$m$^{-1}$)', fontsize=12)
        plt.title('Power Factor at different T')
        plt.axhline(0, color='k')
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
        plt.xscale('log')
    plt.savefig('powerfactor_carrier_different_T_' + time.strftime("%Y-%m-%d_%H%M%S") +
                '.jpg', format='jpg', dpi=100, bbox_inches='tight')
    # plt.show()

    if save_to_file != False:
        save_plot(save_to_file)


def plot_cry_zt(seebeck_obj, sigma_obj, save_to_file=False):
    """
    Plot the ZT value for different temperatures.

    Args:
        seebeck_obj: Seebeck object containing the data for the Seebeck coefficient.
        sigma_obj: Sigma object containing the data for the electrical conductivity.
        save_to_file (optional): If True, saves the plot to a file. Default is False.

    Returns:
        None

    Notes:
        - Prompts the user to input the value of ktot in W-1K-1m-1.
        - Prompts the user to choose the direction to plot among ZT_xx, ZT_xy, ZT_xz, ZT_yx, ZT_yy, ZT_yz, ZT_yz, ZT_zx, ZT_zy, ZT_zz.
        - Calculates the ZT value using the Seebeck coefficient and electrical conductivity data.
        - Plots the ZT value for each temperature as a function of the chemical potential.
        - If save_to_file is True, saves the plot to a file named 'zt_at_T_K___YYYY-MM-DD_HHMMSS.jpg' for each temperature, and 'zt_different_T_YYYY-MM-DD_HHMMSS.jpg' for all temperatures combined.
    """
    import sys
    import matplotlib.pyplot as plt
    import numpy as np
    import time

    ktot = float(input(
        'Please insert the value of ktot in W-1K-1m-1'))
    case = input(
        'Please, choose the direction you want to plot. \nYou can choose among ZT_xx, ZT_xy, ZT_xz, ZT_yx, ZT_yy, ZT_yz, ZT_yz, ZT_zx, ZT_zy, ZT_zz\n')

    case = case.lower().replace('_', '')

    if case.isalpha() == True:
        pass
    else:
        sys.exit('Please, select a valid chioce')

    if case == 'ztxx':
        col = 3
    elif case == 'ztxy':
        col = 4
    elif case == 'ztxz':
        col = 5
    elif case == 'ztyx':
        col = 6
    elif case == 'ztyy':
        col = 7
    elif case == 'ztyz':
        col = 8
    elif case == 'ztzx':
        col = 9
    elif case == 'ztzy':
        col = 10
    elif case == 'ztzz':
        col = 11
    else:
        sys.exit('please, choose a valid chioce')

    if case == 'ztxx':
        cols = 3
    elif case == 'ztxy':
        cols = 4
    elif case == 'ztxz':
        cols = 5
    elif case == 'ztyx':
        cols = 4
    elif case == 'ztyy':
        cols = 6
    elif case == 'ztyz':
        cols = 7
    elif case == 'ztzx':
        cols = 5
    elif case == 'ztzy':
        cols = 7
    elif case == 'ztzz':
        cols = 8
    else:
        sys.exit('please, choose a valid chioce')

    x = []
    for k in range(0, len(seebeck_obj.all_data)):
        x.append(np.array(seebeck_obj.all_data[k].apply(
            lambda x: float(x.split()[0]))))

    yse = []
    for k in range(0, len(seebeck_obj.all_data)):
        yse.append(np.array(seebeck_obj.all_data[k].apply(
            lambda x: float(x.split()[col]))))

    ysi = []
    for k in range(0, len(sigma_obj.all_data)):
        ysi.append(np.array(sigma_obj.all_data[k].apply(
            lambda x: float(x.split()[cols]))))

    pf_meta = []
    for i in range(0, len(yse)):
        pf_meta.append(yse[i] * yse[i])

    pf = []
    for i in range(0, len(pf_meta)):
        pf.append(pf_meta[i] * ysi[i])

    zt = []
    for i in range(0, len(pf_meta)):
        zt.append((pf[i] * seebeck_obj.temp[i])/ktot)

    for k in range(0, len(seebeck_obj.all_data)):
        plt.figure()
        plt.plot(x[k], pf[k], label=str(seebeck_obj.temp[k])+' K')
        plt.xlabel('Chemical Potential (eV)', fontsize=12)
        plt.ylabel('ZT', fontsize=12)
        plt.axhline(0, color='k')
        plt.title('ZT at ' + str(seebeck_obj.temp[k]) + ' K')
        plt.legend(loc='upper left', fontsize=12)
        plt.savefig('zt_at_' + str(seebeck_obj.temp[k]) + 'K___' + time.strftime(
            "%Y-%m-%d_%H%M%S") + '.jpg', format='jpg', dpi=600, bbox_inches='tight')
        plt.show()

    for k in range(0, len(seebeck_obj.all_data)):
        plt.plot(x[k], pf[k], label=str(seebeck_obj.temp[k])+' K')
        plt.xlabel('Chemical Potential (eV)', fontsize=12)
        plt.ylabel('ZT', fontsize=12)
        plt.title('ZT at different T')
        plt.axhline(0, color='k')
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
    plt.savefig('zt_different_T_' + time.strftime("%Y-%m-%d_%H%M%S") +
                '.jpg', format='jpg', dpi=100, bbox_inches='tight')
    if save_to_file != False:
        save_plot(save_to_file)


def plot_cry_multiseebeck(*seebeck):
    """
    Plot the seebeck coefficients from different files as a function of chemical potential.

    Args:
        *seebeck: Variable number of seebeck objects containing the data for the Seebeck coefficient.

    Returns:
        None

    Notes:
        - Prompts the user to input the index of the temperature to plot.
        - Prompts the user to input the lower and higher values of chemical potential to plot in eV.
        - Prompts the user to choose the direction to plot among S_xx, S_xy, S_xz, S_yx, S_yy, S_yz, S_yz, S_zx, S_zy, S_zz.
        - Plots the seebeck coefficient for each seebeck object.
        - Differentiates transport coefficients due to n-type or p-type conduction using dashed and solid lines.
        - Saves the plot to a file named 'multiseebeckYYYY-MM-DD_HHMMSS.jpg', where YYYY-MM-DD_HHMMSS represents the current date and time.
    """
    import sys
    import matplotlib.pyplot as plt
    import numpy as np
    import time

    k = int(input(
        'Insert the index of temperature you want to plot \n(i.e. if your temperature are [T1, T2, T3] indexes are [0, 1, 2])'))
    minpot = float(
        input('Insert the lower value of chemical potential you want to plot in eV'))
    maxpot = float(
        input('Inser the higher value of chemical potential you want to plot in eV'))

    case = input(
        'Please, choose the direction you want to plot. \nYou can choose among S_xx, S_xy, S_xz, S_yx, S_yy, S_yz, S_yz, S_zx, S_zy, S_zz\n')

    case = case.lower().replace('_', '')

    if case.isalpha() == True:
        pass
    else:
        sys.exit('Please, select a valid chioce')

    if case == 'sxx':
        col = 3
    elif case == 'sxy':
        col = 4
    elif case == 'sxz':
        col = 5
    elif case == 'syx':
        col = 6
    elif case == 'syy':
        col = 7
    elif case == 'syz':
        col = 8
    elif case == 'szx':
        col = 9
    elif case == 'szy':
        col = 10
    elif case == 'szz':
        col = 11

    else:
        sys.exit('please, choose a valid chioce')

    print('To differentiate transport coefficients due to n-type or p-type conduction (electrons or holes as majority carriers) dashed and solid lines are used, respectively.')

    i = 0
    for n in seebeck:
        vol = n.volume

        x = []
        for kq in range(0, len(n.all_data)):
            x.append(np.array(n.all_data[kq].apply(
                lambda x: float(x.split()[0]))))

        carrier = []
        for kq in range(0, len(n.all_data)):
            carrier.append(np.array(n.all_data[kq].apply(
                lambda x: (float(x.split()[2])/vol))))

        y = []
        for kq in range(0, len(n.all_data)):
            y.append(np.array(n.all_data[kq].apply(
                lambda x: float(x.split()[col])*1000000)))

        yneg = []
        ypos = []
        xpos = []
        xneg = []
        yposfin = []
        xposfin = []
        ynegfin = []
        xnegfin = []

        for kq in range(0, len(n.all_data)):
            for j in range(0, len(carrier[kq])):
                if carrier[kq][j] >= 0:
                    xpos.append(x[kq][j])
                    ypos.append(y[kq][j])
                else:
                    xneg.append(x[kq][j])
                    yneg.append(y[kq][j])
            yposfin.append(ypos)
            ynegfin.append(yneg)
            xposfin.append(xpos)
            xnegfin.append(xneg)
            xpos = []
            ypos = []
            xneg = []
            yneg = []

        colours = ['royalblue', 'orange', 'green', 'red',
                   'purple', 'brown', 'pink', 'grey', 'olive', 'cyan']

        endx = []
        endy = []

        endx = [xposfin[k][-1], xnegfin[k][0]]
        endy = [yposfin[k][-1], ynegfin[k][0]]
        plt.plot(endx, endy, color=colours[i])
        plt.plot(xposfin[k], yposfin[k], color=colours[i], label=str(n.title))
        plt.plot(xnegfin[k], ynegfin[k], '--', color=colours[i])
        plt.xlabel('Chemical Potential (eV)', fontsize=12)
        plt.ylabel('Seebeck Coefficient ($\mu$V/K)', fontsize=12)
        plt.xlim(minpot, maxpot)
        plt.axhline(0, color='k')
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
        i = 1+i
    plt.title('MultiSeebeck ' + str(n.temp[k]) + ' K')
    plt.savefig('multiseebeck' + time.strftime("%Y-%m-%d_%H%M%S") +
                '.jpg', format='jpg', dpi=100, bbox_inches='tight')


def plot_cry_multisigma(*sigma):
    """
    Plot the electrical conductivities from different files as a function of the chemical potential.

    Args:
        *sigma: Variable number of sigma objects containing the data for the conductivity.

    Returns:
        None

    Notes:
        - Prompts the user to input the index of the temperature to plot.
        - Prompts the user to input the lower and higher values of chemical potential to plot in eV.
        - Prompts the user to choose the direction to plot among S_xx, S_xy, S_xz, S_yy, S_yz, S_zz.
        - Plots the electrical conductivity for each sigma object.
        - Differentiates transport coefficients due to n-type or p-type conduction using dashed and solid lines.
        - Saves the plot to a file named 'multisigmaYYYY-MM-DD_HHMMSS.jpg', where YYYY-MM-DD_HHMMSS represents the current date and time.
    """
    import sys
    import matplotlib.pyplot as plt
    import numpy as np
    import time

    k = int(input(
        'Insert the index of temperature you want to plot \n(i.e. if your temperature are [T1, T2, T3] indexes are [0, 1, 2])'))
    minpot = float(
        input('Insert the lower value of chemical potential you want to plot in eV'))
    maxpot = float(
        input('Inser the higher value of chemical potential you want to plot in eV'))

    case = input(
        'Please, choose the direction you want to plot. \nYou can choose among S_xx, S_xy, S_xz, S_yy, S_yz, S_zz\n')

    case = case.lower().replace('_', '')

    if case.isalpha() == True:
        pass
    else:
        sys.exit('Please, select a valid chioce')

    if case == 'sxx':
        col = 3
    elif case == 'sxy':
        col = 4
    elif case == 'sxz':
        col = 5
    elif case == 'syy':
        col = 6
    elif case == 'syz':
        col = 7
    elif case == 'szz':
        col = 8

    else:
        sys.exit('please, choose a valid chioce')

    i = 0
    print('To differentiate transport coefficients due to n-type or p-type conduction (electrons or holes as majority carriers) dashed and solid lines are used, respectively.')
    for n in sigma:
        vol = n.volume

        x = []
        for kq in range(0, len(n.all_data)):
            x.append(np.array(n.all_data[kq].apply(
                lambda x: float(x.split()[0]))))

        carrier = []
        for kq in range(0, len(n.all_data)):
            carrier.append(np.array(n.all_data[kq].apply(
                lambda x: (float(x.split()[2])/vol))))

        y = []
        for kq in range(0, len(n.all_data)):
            y.append(np.array(n.all_data[kq].apply(
                lambda x: float(x.split()[col]))))

        yneg = []
        ypos = []
        xpos = []
        xneg = []
        yposfin = []
        xposfin = []
        ynegfin = []
        xnegfin = []

        for kq in range(0, len(n.all_data)):
            for j in range(0, len(x[kq])):
                if carrier[kq][j] >= 0:
                    xpos.append(x[kq][j])
                    ypos.append(y[kq][j])
                else:
                    xneg.append(x[kq][j])
                    yneg.append(y[kq][j])
            yposfin.append(ypos)
            ynegfin.append(yneg)
            xposfin.append(xpos)
            xnegfin.append(xneg)
            xpos = []
            ypos = []
            xneg = []
            yneg = []

        colours = []
        colours = ['royalblue', 'orange', 'green', 'red',
                   'purple', 'brown', 'pink', 'grey', 'olive', 'cyan']
        endx = []
        endy = []

        endx = [xposfin[k][-1], xnegfin[k][0]]
        endy = [yposfin[k][-1], ynegfin[k][0]]
        plt.plot(endx, endy, color=colours[i])
        plt.plot(xposfin[k], yposfin[k], color=colours[i], label=str(n.title))
        plt.plot(xnegfin[k], ynegfin[k], '--', color=colours[i])
        plt.xlabel('Chemical Potential (eV)', fontsize=12)
        plt.ylabel('Electrical Conductivity (S/m)', fontsize=12)
        plt.axhline(0, color='k')
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
        plt.xlim(minpot, maxpot)
        i = 1+i
    plt.title('MultiSigma ' + str(sigma[0].temp[k]) + ' K')
    plt.savefig('multisigma' + time.strftime("%Y-%m-%d_%H%M%S") +
                '.jpg', format='jpg', dpi=100, bbox_inches='tight')


def plot_cry_lapl_profile(lapl_obj, save_to_file=False):
    """
    Plot the Laplacian profile of a crystal.

    Args:
        lapl_obj (object): Laplacian object containing the data for the Laplacian profile.
        save_to_file (bool, optional): Indicates whether to save the plot to a file. Defaults to False.

    Returns:
        None

    Notes:
        - Plots the Laplacian profile using the data from the Laplacian object.
        - The x-axis represents the distance in angstroms.
        - The y-axis represents the Laplacian in electrons per cubic angstrom to the fifth power (e/A^5).
        - The area under the curve where the Laplacian is negative is filled with a light blue color.
        - The area under the curve where the Laplacian is positive is filled with a light coral color.
        - If save_to_file is set to a file path, the plot is saved to that file.
    """
    import matplotlib.pyplot as plt
    import time

    plt.plot(lapl_obj.datax, lapl_obj.datay)

    plt.fill_between(lapl_obj.datax, lapl_obj.datay, where=(
        lapl_obj.datay < 0), color='lightblue', interpolate=True)
    plt.fill_between(lapl_obj.datax, lapl_obj.datay, where=(
        lapl_obj.datay > 0), color='lightcoral', interpolate=True)

    # plt.xlim(-0.5,0.5)
    # plt.ylim(-200,200)

    plt.xlabel('Distance [A]')
    plt.ylabel('Laplacian [e/A^5]')

    if save_to_file != False:
        save_plot(save_to_file)

    plt.show()


def plot_cry_density_profile(lapl_obj, save_to_file=False):
    """
    Plot the density profile of a crystal.

    Args:
        lapl_obj (object): Laplacian object containing the data for the density profile.
        save_to_file (bool, optional): Indicates whether to save the plot to a file. Defaults to False.

    Returns:
        None

    Notes:
        - Plots the density profile using the data from the Laplacian object.
        - The x-axis represents the distance in angstroms.
        - The y-axis represents the density in electrons per cubic angstrom (e/A^3).
        - If save_to_file is set to a file path, the plot is saved to that file.
    """
    import matplotlib.pyplot as plt
    import time

    plt.plot(lapl_obj.datax, lapl_obj.datay)

    plt.xlabel('Distance [A]')
    plt.ylabel('Density [e/A^3]')

    if save_to_file != False:
        save_plot(save_to_file)

    plt.show()


def plot_cry_young(theta, phi, S):
    """
    Compute Young's modulus for each direction of the space (i.e., each pair
    of theta and phi angles).

    Args:
        theta (float): Theta value.
        phi (float): Phi value.
        S (numpy.ndarray): Compliance matrix.

    Returns:
        float: Young's modulus values.

    Notes:
        - This function is intended to be called by cry_ela_plot
    """
    import numpy as np

    # C2V = Matrix to refer the Cartesian into Voigt's notation
    # Observe that the matrix should be written as is shown below
    # C2V = np.array([[1,6,5],[6,2,4],[5,4,3]])
    # Since python start counting from zero all numbers must be subtracted by 1
    C2V = np.array(
        [
            [0, 5, 4],
            [5, 1, 3],
            [4, 3, 2]
        ]
    )
    # print("The Matrix to convert Cartesian into Voigs Notation: \n", C2V)
    # creating the 1x3 vector "a"
    a = np.array(
        [
            np.sin(theta) * np.cos(phi),
            np.sin(theta) * np.sin(phi),
            np.cos(theta),
        ]
    )
    # e is a pseudo Young modulus value folowing the relation 1/e
    e = 0.0
    # i,j,k,l are updatable indices refering to cartesian notation that
    # will be converted by C2V into Voigt's
    for i in range(3):
        for j in range(3):
            v = C2V[i, j]
            for k in range(3):
                for l in range(3):
                    u = C2V[k, l]
                    # rf is a factor that must be multipled by the compliance element if
                    # certain conditions are satisfied
                    rf = 1
                    if v >= 3 and u >= 3:
                        rf = 4
                    if v >= 3 and u < 3:
                        rf = 2
                    if u >= 3 and v < 3:
                        rf = 2

                    rtmp = a[i] * a[j] * a[k] * a[l] * (S[v, u] / rf)
                    e = e + rtmp
    E_tmp = 1 / e  # is the Young Modulus of each cycle
    return E_tmp


def plot_cry_comp(theta, phi, S):
    """
    Compute linear compressibility for each direction of the space (i.e., each
    pair of theta and phi angles).

    Args:
        theta (float): Theta value.
        phi (float): Phi value.
        S (numpy.ndarray): Compliance matrix.

    Returns:
        float: Linear compressibility values.

    Notes:
        - This function is intended to be called by cry_ela_plot
    """
    import numpy as np

    C2V = np.array(
        [
            [0, 5, 4],
            [5, 1, 3],
            [4, 3, 2]
        ]
    )

    a = np.array(
        [
            np.sin(theta) * np.cos(phi),
            np.sin(theta) * np.sin(phi),
            np.cos(theta),
        ]
    )
    B = 0.0

    for i in range(3):
        for j in range(3):
            v = C2V[i, j]
            for k in range(3):
                u = C2V[k, k]
                rf = 1
                if v >= 3 and u >= 3:
                    rf = 4
                if v >= 3 and u < 3:
                    rf = 2
                if u >= 3 and v < 3:
                    rf = 2

                rtmp = a[i] * a[j] * (S[v, u] / rf)
                B = B + rtmp
    return B


def plot_cry_shear(theta_1D, phi_1D, S, ndeg, shear_choice):
    """
    For each direction of the space (i.e., for each pair
    of theta and phi angles) the shear modulus is computed for the third angle
    chi and the average, maximum and minimum values are stored.

    Args:
        theta_1D (numpy.ndarray): One-dimensional array of theta values.
        phi_1D (numpy.ndarray): One-dimensional array of phi values.
        S (numpy.ndarray): Compliance matrix.
        ndeg (int): Number of degrees for discretization.
        shear_choice (str): Type of shear property to plot. Options: "avg", "min", "max".

    Returns:
        numpy.ndarray: Shear property array.

    Notes:
        - This function is intended to be called by cry_ela_plot
    """
    import numpy as np

    C2V = np.array(
        [
            [0, 5, 4],
            [5, 1, 3],
            [4, 3, 2],
        ]
    )
    shear_chi = np.zeros(ndeg)
    shear_min = np.zeros((ndeg, ndeg))
    shear_max = np.zeros((ndeg, ndeg))
    shear_avg = np.zeros((ndeg, ndeg))
    chi_1D = np.linspace(0, 2 * np.pi, ndeg)

    for phi_idx in range(ndeg):
        phi = phi_1D[phi_idx]
        for theta_idx in range(ndeg):
            theta = theta_1D[theta_idx]
            for chi_idx in range(ndeg):
                chi = chi_1D[chi_idx]
                a = np.array(
                    [
                        np.sin(theta) * np.cos(phi),
                        np.sin(theta) * np.sin(phi),
                        np.cos(theta),
                    ]
                )
                b = np.array(
                    [
                        np.cos(theta) * np.cos(phi) * np.cos(chi)
                        - np.sin(phi) * np.sin(chi),
                        np.cos(theta) * np.sin(phi) * np.cos(chi)
                        + np.cos(phi) * np.sin(chi),
                        -np.sin(theta) * np.cos(chi),
                    ]
                )
                shear_tmp = 0
                for i in range(3):
                    for j in range(3):
                        v = C2V[i, j]
                        for k in range(3):
                            for l in range(3):
                                u = C2V[k, l]
                                rf = 1
                                if v >= 3 and u >= 3:
                                    rf = 4
                                if v >= 3 and u < 3:
                                    rf = 2
                                if u >= 3 and v < 3:
                                    rf = 2
                                rtmp = a[i] * b[j] * a[k] * \
                                    b[l] * (S[v, u] / rf)
                                shear_tmp = shear_tmp + rtmp
                shear_chi[chi_idx] = 1 / (4 * shear_tmp)
            shear_min[phi_idx, theta_idx] = np.amin(shear_chi)
            shear_max[phi_idx, theta_idx] = np.amax(shear_chi)
            shear_avg[phi_idx, theta_idx] = np.mean(shear_chi)

    if shear_choice == "avg":
        return shear_avg
    if shear_choice == "min":
        return shear_min
    if shear_choice == "max":
        return shear_max


def plot_cry_poisson(theta_1D, phi_1D, S, ndeg, poisson_choice):
    """
    For each direction of the space (i.e., for each pair
    of theta and phi angles) the Poisson ratio is computed for the third angle
    chi and the average, maximum and minimum values are stored.

    Args:
        theta_1D (numpy.ndarray): One-dimensional array of theta values.
        phi_1D (numpy.ndarray): One-dimensional array of phi values.
        S (numpy.ndarray): Compliance matrix.
        ndeg (int): Number of degrees for discretization.
        poisson_choice (str): Type of Poisson's ratio to plot. Options: "avg", "min", "max".

    Returns:
        numpy.ndarray: Poisson's ratio array.

    Notes:
        - This function is intended to be called by cry_ela_plot
    """
    import numpy as np

    C2V = np.array(
        [
            [0, 5, 4],
            [5, 1, 3],
            [4, 3, 2],
        ]
    )
    poisson_chi = np.zeros(ndeg)
    poisson_min = np.zeros((ndeg, ndeg))
    poisson_max = np.zeros((ndeg, ndeg))
    poisson_avg = np.zeros((ndeg, ndeg))
    chi_1D = np.linspace(0, 2 * np.pi, ndeg)

    for phi_idx in range(ndeg):
        phi = phi_1D[phi_idx]
        for theta_idx in range(ndeg):
            theta = theta_1D[theta_idx]
            for chi_idx in range(ndeg):
                chi = chi_1D[chi_idx]
                a = np.array(
                    [
                        np.sin(theta) * np.cos(phi),
                        np.sin(theta) * np.sin(phi),
                        np.cos(theta),
                    ]
                )
                b = np.array(
                    [
                        np.cos(theta) * np.cos(phi) * np.cos(chi)
                        - np.sin(phi) * np.sin(chi),
                        np.cos(theta) * np.sin(phi) * np.cos(chi)
                        + np.cos(phi) * np.sin(chi),
                        -np.sin(theta) * np.cos(chi),
                    ]
                )
                poisson_num = 0
                poisson_den = 0
                for i in range(3):
                    for j in range(3):
                        v = C2V[i, j]
                        for k in range(3):
                            for l in range(3):
                                u = C2V[k, l]
                                rf = 1
                                if v >= 3 and u >= 3:
                                    rf = 4
                                if v >= 3 and u < 3:
                                    rf = 2
                                if u >= 3 and v < 3:
                                    rf = 2
                                num = (a[i] * a[j] * b[k] * b[l] * S[v, u])/rf
                                den = (a[i] * a[j] * a[k] * a[l] * S[v, u])/rf
                                poisson_num = poisson_num + num
                                poisson_den = poisson_den + den
                poisson_chi[chi_idx] = - poisson_num / poisson_den
            poisson_min[phi_idx, theta_idx] = np.amin(poisson_chi)
            poisson_max[phi_idx, theta_idx] = np.amax(poisson_chi)
            poisson_avg[phi_idx, theta_idx] = np.mean(poisson_chi)

    if poisson_choice == "avg":
        return poisson_avg
    if poisson_choice == "min":
        return poisson_min
    if poisson_choice == "max":
        return poisson_max


def plot_cry_ela(choose, ndeg, *args, dpi=200, filetype=".png",
                 transparency=False):
    """
    Plot crystal elastic properties on the basis of the elastic tensor. A
    variable number of elastic tensors can be provided in order to get
    multiple plots in one shot, establishing a fixed color scale among them.

    Args:
        choose (str): Property to plot. Options: "young", "comp", "shear avg",
            "shear min", "shear max", "poisson avg", "poisson min", "poisson max".
        ndeg (int): Number of degrees for discretization.
        *args: Variable number of elastic tensors.
        dpi (int, optional): Dots per inch for saving the plot. Default is 200.
        filetype (str, optional): File format of the output plot. Default is ".png".
        transparency (bool, optional): Flag indicating whether to make the plot
            background transparent. Default is False.

    Returns:
        None
    """
    import numpy as np
    import matplotlib.pyplot as plt
    import math
    import time
    import sys
    from mpl_toolkits.mplot3d import axes3d, Axes3D
    from matplotlib import cm, colors, animation

    i = 0
    R = [None] * len(args)
    tmin = []
    tmax = []

    # Compute elastic properties for each tensor -->
    for C in args:

        # Inverse of the matrix C in GPa (Compliance)
        S = np.linalg.inv(C)

        # One dimentional array of theta from 0 to pi
        theta_1D = np.linspace(0, np.pi, ndeg)
        # One dimentional array of phi from 0 to 2pi
        phi_1D = np.linspace(0, 2 * np.pi, ndeg)
        # Make a 2D array for theta and phi
        theta_2D, phi_2D = np.meshgrid(theta_1D, phi_1D)

        # Call to function
        if choose == "young":
            R[i] = plot_cry_young(theta_2D, phi_2D, S)
        elif choose == "comp":
            R[i] = plot_cry_comp(theta_2D, phi_2D, S)
        elif choose == "shear avg":
            R[i] = plot_cry_shear(theta_1D, phi_1D, S, ndeg, "avg")
        elif choose == "shear min":
            R[i] = plot_cry_shear(theta_1D, phi_1D, S, ndeg, "min")
        elif choose == "shear max":
            R[i] = plot_cry_shear(theta_1D, phi_1D, S, ndeg, "max")
        elif choose == "poisson avg":
            R[i] = plot_cry_poisson(theta_1D, phi_1D, S, ndeg, "avg")
        elif choose == "poisson min":
            R[i] = plot_cry_poisson(theta_1D, phi_1D, S, ndeg, "min")
        elif choose == "poisson max":
            R[i] = plot_cry_poisson(theta_1D, phi_1D, S, ndeg, "max")

        i += 1
    # <--

    # Find highest and lowest values -->
    for k in range(i):
        tmin.append(np.min(R[k]))
        tmax.append(np.max(R[k]))
    vmin = min(tmin)
    vmax = max(tmax)
    # <--

    # Create plot for each tensor -->
    for k in range(i):
        X = R[k] * np.sin(theta_2D) * np.cos(phi_2D)
        Y = R[k] * np.sin(theta_2D) * np.sin(phi_2D)
        Z = R[k] * np.cos(theta_2D)

        norm = colors.Normalize(vmin=vmin, vmax=vmax, clip=False)
        fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))

        ax.plot_surface(
            X,
            Y,
            Z,
            rstride=1,
            cstride=1,
            facecolors=cm.jet(norm(R[k])),
            antialiased=True,
            alpha=0.75,
        )

        m = cm.ScalarMappable(cmap=cm.jet, norm=norm)
        m.set_array(R[k])
        fig.colorbar(m, shrink=0.7, location="left")

        # Make the planes transparent
        ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        # Make the grid lines transparent
        #  ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
        #  ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
        #  ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)
        # Fixing limits
        ax.set_xlim(-1 * np.max(R), np.max(R))
        ax.set_ylim(-1 * np.max(R), np.max(R))
        ax.set_zlim3d(-1 * np.max(R), np.max(R))
        ax.locator_params(nbins=5)  # tight=True,
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        ax.set_box_aspect(aspect=(1, 1, 1))  # Fix aspect ratio

        plt.show()
        fig.savefig(choose + time.strftime("%Y-%m-%d_%H%M%S") +
                    filetype, dpi=dpi, transparent=transparency)

        # <--


def save_plot(path_to_file, format='png'):
    """
    Save the plot as a file.

    Args:
        path_to_file (str): Path to the output file.
        format (str, optional): File format of the output plot. Default is 'png'.

    Raises:
        FileNotFoundError: If the specified folder does not exist.

    Returns:
        None
    """
    from os import path
    import warnings
    import matplotlib.pyplot as plt

    folder = path.split(path_to_file)[0]
    file = path.split(path_to_file)[1]
    extension = path.splitext(file)[-1]
    extension_list = ['.png', '.jpg', '.jpeg', '.tif','.pdf', '.svg', '.eps']

    if folder == '':
        folder = '.'
    if extension != '':
        if extension in extension_list:
            format = extension[1:]
        else:
            warnings.warn('Unrecognized file format. PNG format is used.',
                          stacklevel=2)

    if path.exists(folder) == True:
        plt.savefig('%s/%s.%s' % (folder, file, format))
    else:
        raise FileNotFoundError('Folder %s does not exist' % path_to_file)
