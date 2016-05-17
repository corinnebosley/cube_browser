import matplotlib.pyplot as plt


class Contourf(object):
    """
    Constructs a filled contour plot instance of a cube, using coordinates
    specified in the input arguments as axes coordinates and turning the
    remaining dimension coordinates into interactive sliders.

    """
    def __init__(self, cube, coords, **kwargs):
        """
        :param cube: the iris.cube.Cube instance to plot
        :param coords: the cube coordinate names or dimension indices to plot
                       in the order (x-axis, y-axis)
        :param kwargs: kwargs for plot customization,
            see :func:`matplotlib.pyplot.contourf`
            and :func:`iris.plot.contourf` for details of other
            valid keyword arguments.
        :return: iris.plot.contourf instance
        """

        self.cube = cube
        self.coords = coords  # coords to plot as x, y
        self.kwargs = kwargs
        self.axes = self.new_axes()
        self.qcs = None  # QuadContourSet
        # A mapping of 1d-coord name to dimension
        self.coord_dim = self.coord_dims()

    def __call__(self, **coord_values):
        """
        Constructs a static plot of the cube sliced at the coordinates
        specified in coord_values.  This is called once each time a slider
        position is moved, at which point the new coordinate values are plotted.

        :param coord_values: mapping dictionary of coordinate name or dimension
        index with value index at which to be sliced
        :return: matplotlib.pyplot axes instance
        """
        index = [slice(None)] * self.cube.ndim
        for name, value in kwargs.items():
            if name in self.coord_dim:
                index[self.coord_dim[name]] = value
        cube = self.cube[tuple(index)]
        plt.sca(self.axes)
        self.qcs = iplt.contourf(cube, coords=self.coords,
                                 axes=self.axes, **self.kwargs)
        return plt.gca()

    # This function is a temporary measure for the one-axis, one-plot scenario.
    def new_axes(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection=cube.coord_system().
                             as_cartopy_projection())
        return ax

    def coord_dims(self):
        """
        :return: a mapping dictionary of dimension coordinates
        """
        mapping = {}
        for dim in range(self.cube.ndim):
            coords = self.cube.coords(dimensions=(dim,))
            mapping.update([(c.name(), dim) for c in coords])
        return mapping

    def slider_coords(self):
        """
        :return: a list of the dim coords not used on the plot axes, to be
        used as slider coordinates
        """
        available = []
        for dim in range(len(self.cube.dim_coords)):
            if self.cube.dim_coords[dim].name() not in self.coords:
                available.append(self.cube.dim_coords[dim])
        return available

