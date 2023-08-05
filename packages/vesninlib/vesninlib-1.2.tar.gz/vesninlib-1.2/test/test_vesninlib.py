import os
import shutil
from datetime import datetime
from pathlib import Path

from vesninlib.vesninlib import retrieve_data, plot_map, _UTC


class TestVesninLib:
    _filename = './test/roti_01_17.h5'
    _times = [t.replace(tzinfo=t.tzinfo or _UTC) for t in [datetime(2023, 2, 6, 1, 17)]]
    _description = 'ROTI'

    def test_retrieve_data(self):
        data = retrieve_data(self._filename, self._description, self._times)
        assert len(data[self._times[0]]) > 100

    def test_plot_map(self):
        path = os.getcwd() / Path('result')
        os.makedirs(path)
        savefig = path / Path('result.png')
        plot_map(self._times, {self._description:
                                  retrieve_data(self._filename, self._description, self._times)},
                self._description, savefig=savefig, ncols=1)
        assert 'result.png' in os.listdir(path)
        shutil.rmtree(path)
