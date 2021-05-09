"""
This module is an example of a barebones QWidget plugin for napari

It implements the ``napari_experimental_provide_dock_widget`` hook specification.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below according to your needs.
"""
from napari_plugin_engine import napari_hook_implementation
from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from ._function import determine_quality
from napari import Viewer


def thread_worker(args):
    pass


class ImageQualityPanel(QWidget):
    """
    The image quality panel is a Widget in the user interface that
    shows visually how high the image quality is at the moment.
    """
    def __init__(self, napari_viewer: Viewer):

        super().__init__(napari_viewer.window.qt_viewer)
        self._viewer = napari_viewer

        self.setObjectName("Image quality")

        # setup user interface
        self.label = QLabel("0")
        font = self.label.font()
        font.setPointSize(30)
        self.label.setFont(font)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self._reset)

        self.setLayout(QHBoxLayout(self))
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.reset_button)
        self.layout().addStretch()

        # initial state
        self._reset()

        # threading
        # https://napari.org/guides/stable/threading.html
        @thread_worker
        def loop_run():
            while self._viewer.window.qt_viewer:  # loop until napari closes
                # get currently active layer
                selected_layers = self._viewer.layers.selection
                if len(selected_layers) > 0:
                    # measure quality and update GUI
                    quality = determine_quality(selected_layers.active.data)
                    self._update_quality(quality)

                time.sleep(0.1)

        # Start the loop
        worker = loop_run()
        worker.start()

    def _reset(self):
        self.best_quality = 0

    def _update_quality(self, quality):
        """
        Updates the image quality display
        """
        if self.best_quality < quality:
            self.best_quality = quality

        # put current quality in label
        self.label.setText(str(quality)[0:5])

        # color label according to quality
        ratio_to_best = quality / self.best_quality
        if ratio_to_best > 0.9:
            self.label.setStyleSheet("QLabel { color : green }")
        elif ratio_to_best > 0.5:
            self.label.setStyleSheet("QLabel { color : yellow }")
        else:
            self.label.setStyleSheet("QLabel { color : red }")

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    # you can return either a single widget, or a sequence of widgets
    return [ImageQualityPanel]
