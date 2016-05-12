import ipywidgets
import IPython
import matplotlib.pyplot as plt
import iris.plot as iplt


class Contourf(object):
    def __init__(self, cube, coords, axes, callback=None, **kwargs):
        self.cube = cube
        self.coords = coords # coords to plot
        self.axes = axes
        self.callback = callback
#        self.args = args
        self.kwargs = kwargs
        self.qcs = None  # QuadContourSet
        # A mapping of 1d-coord name to dimension
        self.coord_dim = self.coord_dims()

    # This constructs the original and updated plots
    def __call__(self, **kwargs):
        index = [slice(None)] * self.cube.ndim
        for name, value in kwargs.items():
            index[self.coord_dim[name]] = value
        cube = self.cube[tuple(index)]
        plt.sca(self.axes)
        self.qcs = iplt.contourf(cube, coords=self.coords, **self.kwargs)
        return plt.gca()

    # This makes a mapping dictionary of DIMENSION coordinates
    def coord_dims(self):
        mapping = {}
        for dim in range(self.cube.ndim):
            coords = self.cube.coords(dimensions=(dim,))
            mapping.update([(c.name(), dim) for c in coords])
        return mapping

    def slider_coords(self):
        available = []
        for dim in range(len(self.cube.dim_coords)):
            if self.cube.dim_coords[dim].name() not in self.coords:
                available.append(self.cube.dim_coords[dim])
        return available


class Viewer(object):
    def __init__(self, *plots):
        self.plots = plots
        self.nplots = []
        # This bit asks the plots what coordinates it needs to make into sliders
        # It compiles a list of actual coordinates (warts and all)
        self._sliders = {}
        self._slidermap = {}
        for plot in self.plots:
            for coord in plot.slider_coords():
                if coord not in self._slidermap:
                    self._slidermap[coord.name()] = coord.shape[0]
                    slider = ipywidgets.IntSlider(min=0, max=coord.shape[0],
                                                  description=coord.name())
                    slider.observe(self.on_change, names='value')
                    self._sliders[coord.name()] = slider
        self.form = ipywidgets.VBox()
        self.form.children = self._sliders.values()
        # This bit displays the slider and the plot.
        # I think I can do it without having to use IPython blah blah,
        # but not sure how yet.
        IPython.display.display(self.form)
        # Need to put an IPython image hook in here when I know how to use
        # them properly.

    # This tells the plot to respond to value changes in the sliders
    def on_change(self, change):
        for name, slider in self._sliders.items():
            self._slidermap[name] = slider.value
        for plot in self.plots:
            plot(**self._slidermap)