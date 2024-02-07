"""
GUI for a CountVsTime Application

Copyright (c) April 2023, Chris Egerstrom
All rights reserved.

This work is licensed under the terms of the 3-Clause BSD license.
For a copy, see <https://opensource.org/licenses/BSD-3-Clause>.
"""

#TO-DO, NEEDS SOME DEBUGGING
from functools import partial
from importlib import reload

from pyqtgraph.Qt import QtWidgets
from pyqtgraph import SpinBox
from nspyre import LinePlotWidget
from nspyre import ParamsWidget
from nspyre import ProcessRunner
from nspyre import DataSink

import experiments.AttenuatorTesting as AttenTest
from guis.guiElements_general import AutoSaveWidget
from guis.guiElements_general import flexSave


class CustomAttenTestingWidget(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle('AttenuatorTesting')

        self.params_widget = ParamsWidget({
            'atten_voltage': {
                'display_text': 'Attenuator voltage/laser power',
                'widget': SpinBox(
                    value=1.0,
                    bounds=(0, 5),
                    dec=True,
                ),
            },
        })

        #Setup run and stop buttons
        runButton = QtWidgets.QPushButton('Run')
        runButton.clicked.connect(self.runClicked)

        stopButton = QtWidgets.QPushButton('Stop')
        stopButton.clicked.connect(self.stop)

        # stop the process if the widget is closed
        self.destroyed.connect(partial(self.stop))

        # the process running the sweep function
        self.sweepProc = ProcessRunner()

        # Qt layout that arranges the params, checkboxes, and buttons vertically
        params_layout = QtWidgets.QVBoxLayout()
        params_layout.addWidget(self.params_widget)
        params_layout.addStretch()
        params_layout.addWidget(runButton)
        params_layout.addWidget(stopButton)

        self.setLayout(params_layout)


    def runClicked(self):
        """Runs when the 'run' button is pressed."""

        # reload the spin measurements module at runtime in case any changes were made to the code
        reload(AttenTest)

        # create an instance of the ODMR class that implements the experimental logic.
        LC = AttenTest.AttenTesting()

        # run the sweep function in a new thread
        self.sweepProc.run(
            LC.AttenTest,
            self.params_widget.atten_voltage,
        )


    def stop(self):
        """Stop the sweep process."""

        self.sweepProc.kill()




