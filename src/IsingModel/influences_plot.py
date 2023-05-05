import simcx
from game_of_ice import GameOfIce


class InfluencesPlot(simcx.MplVisual):
    def __init__(self, sim: GameOfIce, **kwargs):
        super(InfluencesPlot, self).__init__(sim, **kwargs)
        self.sim = sim
        self.ax = self.figure.add_subplot(111)
        data = sim.sum_inf_neighbours
        self.im_data = self.ax.imshow(data)

    def draw(self):
        self.im_data.set_data(self.sim.sum_inf_neighbours)
        self.im_data.make_image(None)



