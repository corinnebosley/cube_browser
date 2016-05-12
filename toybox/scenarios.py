import ipywidgets
import IPython
import matplotlib.pyplot as plt
import iris.plot as iplt


#  This is the thing that you construct, but its first job is to enlist _Base
#  to drag all the information out of the cube.
class Contourf(object):
    def __init__(self, cube, coords, axes, *args, **kwargs):
        self.cube = cube
        self.coords = coords  # coords to plot
        self.axes = axes
        self.args = args
        self.kwargs = kwargs
        self.qcs = None  # QuadContourSet
        # A mapping of 1d-coord name to dimension
        self.coord_dim = self.coord_dims()

    def __call__(self, **kwargs):
        index = [slice(None)] * self.cube.ndim
        for name, value in kwargs.items():
            index[self.coord_dim[name]] = value
        cube = self.cube[tuple(index)]
#        plt.sca(self.axes)
        self.qcs = iplt.contourf(cube, *self.args, **self.kwargs)
        return plt.gca()

    def coord_dims(self):
        mapping = {}
        for dim in range(self.cube.ndim):
            coords = self.cube.coords(dimensions=(dim,))
            mapping.update([(c.name(), dim) for c in coords])
        return mapping

    def slide_extent(self, name):
        if name not in self.coord_dim:
            emsg = 'Cannot use {!r} to slide over cube {!r}.'
            raise ValueError(emsg.format(name, self.cube.name()))
        return self.cube.shape[self.coord_dim[name]]


#  Viewer is the thing which puts all the plots together and shows them to you.
class Viewer(object):
    def __init__(self, plot):
        self.cube = plot.cube
        self.coords = plot.coords
        self.axes = plot.axes
        self.args = plot.args
        self.kwargs = plot.kwargs
        self._sliders = {}
        self.coord_dim = plot.coord_dim
        # This bit turns all dim coords which aren't on the axes into sliders
        # and maps them for plotting
        for name in self.coord_dim:
            if name not in self.coords:
                depth = plot.slide_extent(name)
                slider = ipywidgets.IntSlider(min=0, max=depth,
                                              description=name)
                slider.observe(self.on_change, names='value')
                self._sliders[name] = slider
        self.plot = plot
        self.form = ipywidgets.HBox()
        self.form.children = self._sliders.values()
        IPython.display.display(self.form)
        plt.sca(self.axes)

# This tells the plot to respond to value changes in the sliders
    def on_change(self, change):
        s_coords = {}
        for name, slider in self._sliders.items():
            s_coords[name] = slider.value
        self.axes = self.plot(**s_coords)


