DEBUG = False

import os
import sys
from pathlib import Path
import json
from enum import Enum
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, \
                                QLineEdit, QFileDialog, QLabel, QWidget, \
                                QHBoxLayout, QVBoxLayout, QCheckBox, \
                                QMessageBox
from PySide2.QtCore import QSize, Qt, QThread, Signal, QObject
if DEBUG:
    import debugpy

class OPENDIALOGMODE(Enum):
    FILEOPENDIALOG = 1
    DIRECTORYOPENDIALOG = 2
    SAVEOPENDIALOG = 3

class _Worker(QObject):
    finished = Signal() # this signal is emitted when the task is finished

    def __init__(self, target, *args, **kwargs):
        super().__init__()

        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._result = None

        self._thread = QThread()
        self.moveToThread(self._thread)
        # connect thread's "started" signal to worker's "do_work" method
        self._thread.started.connect(self._do_work)

    def _do_work(self):
        if DEBUG:
            debugpy.debug_this_thread()
        self._result = self._target(*self._args, **self._kwargs)

        # Emit the "finished" signal when the task is completed
        self.finished.emit()

    def cleanup_thread(self):
        self._thread.quit()
        self._thread.wait()
    
    def run(self):
        self._thread.start()

    @property
    def result(self):
        return self._result


class _CheckboxWidget(QCheckBox):
    def __init__(self, label, initial_state, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.setText(label)
        self.setChecked(initial_state)
        # self.stateChanged.connect(self.checkbox_state_changed)

    @property
    def state(self):
        if self.checkState() == Qt.CheckState.Checked:
            return True
        elif self.checkState() == Qt.CheckState.Unchecked:
            return False
    
class _SelectionWidget(QWidget):
    def __init__(self, label_text, mode, prev_path=None, filter_text=None, filter_extension=None):
        super().__init__()

        # add inputs to object
        self._mode = mode
        self._filter_text = filter_text
        self._filter_extension = filter_extension
        self._prev_path = prev_path if prev_path is not None else ""
    
        # initialize variables
        self._path = None

        # set widgets and layout
        self._label = QLabel(label_text)
        self._label.setFixedWidth(90)

        self._line_edit = QLineEdit()
        self._line_edit.setFixedWidth(700)
        self._line_edit.textChanged.connect(self.set_path)
        
        self._button = QPushButton("Open")
        self._button.clicked.connect(self._open_dialog)

        layout = QHBoxLayout()
        layout.addWidget(self._label)
        layout.addWidget(self._line_edit)
        layout.addWidget(self._button)
        self.setLayout(layout)
    
    @property
    def filter_str(self):
        if self._filter_text==None or self._filter_extension==None:
            retval = "All Files (*.*)"
        else:
            ext = " ".join(["*" + x if x[0]=="." else "." + x for x in self._filter_extension.split(" ")])
            retval = f"{self._filter_text} ({ext});; All Files (*.*)"
    
        return retval

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, val):
        if isinstance(val, str):
            self._path = Path(val)
        elif isinstance(val, Path):
            self._path = val
        
        self._line_edit.setText(str(self._path))
    
    # connect this to the selection widget's line edit's changed signal
    def set_path(self, val):
        # print(f"Setting path to {val}")
        self._path = Path(val)
    
    @property
    def folder(self):
        if self.path.is_file():
            return self.path.parent()
        elif self.path.is_dir():
            return self.path

    def _open_dialog(self):
        if self._mode == OPENDIALOGMODE.FILEOPENDIALOG:
            dir_ = str(self.path.parent) if self.path != None else ""
            sel, _ = QFileDialog.getOpenFileName(self, "Open File", dir_, self.filter_str)
            test = 1
        elif self._mode == OPENDIALOGMODE.DIRECTORYOPENDIALOG:
            dir_ = str(self.path) if self.path != None else ""
            sel = QFileDialog.getExistingDirectory(dir=dir_)
        elif self._mode == OPENDIALOGMODE.SAVEOPENDIALOG:
            dir_ = str(self.path.parent) if self.path != None else ""
            sel, _ = QFileDialog.getSaveFileName(self, "Save As", dir_, self.filter_str)

        if sel != "":
            self.path = Path(sel)
            self._line_edit.setText(str(self.path))
    
    def __str__(self):
        return str(self.path)

    def setEnabled(self, arg__1: bool) -> None:
        self._line_edit.setEnabled(arg__1)
        self._button.setEnabled(arg__1)
        return super().setEnabled(arg__1)

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NEX5 Conversion Tool")

        # set up widgets for specifying paths
        self._ks3_folder_path = _SelectionWidget("KS3 Data Folder:", mode=OPENDIALOGMODE.DIRECTORYOPENDIALOG)
        self._pl2_file_path = _SelectionWidget("PL2 File:", mode=OPENDIALOGMODE.FILEOPENDIALOG, filter_text="PL2 Files", filter_extension=".pl2")
        self._probe_map_file_path = _SelectionWidget("Probe Map:", mode=OPENDIALOGMODE.FILEOPENDIALOG, filter_text="Probe Maps", filter_extension=".mat .prb")
        self._output_file_path = _SelectionWidget("Output File:", mode=OPENDIALOGMODE.SAVEOPENDIALOG, filter_text="NEX5 Files", filter_extension=".nex5")
        self._read_json_paths()
        vlayout = QVBoxLayout()
        vlayout.addWidget(self._ks3_folder_path)
        vlayout.addWidget(self._pl2_file_path)
        vlayout.addWidget(self._probe_map_file_path)
        vlayout.addWidget(self._output_file_path)        

        # set up checkboxes
        hlayout = QHBoxLayout()
        self._ai_checkbox = _CheckboxWidget("Include AI", True)
        self._fp_checkbox = _CheckboxWidget("Include FP", True)
        self._event_checkbox = _CheckboxWidget("Include Digital Events", True)
        self._waveform_checkbox = _CheckboxWidget("Include KS3 Waveforms", False)
        self._good_clusters_checkbox = _CheckboxWidget("Include Good Clusters", True)
        self._mua_clusters_checkbox = _CheckboxWidget("Include MUA Clusters", False)
        self._noise_clusters_checkbox = _CheckboxWidget("Include Noise Clusters", False)
        hlayout.addWidget(self._ai_checkbox)
        hlayout.addWidget(self._fp_checkbox)
        hlayout.addWidget(self._event_checkbox)
        hlayout.addWidget(self._waveform_checkbox)
        hlayout.addWidget(self._good_clusters_checkbox)
        hlayout.addWidget(self._mua_clusters_checkbox)
        # hlayout.addWidget(self._noise_clusters_checkbox)  # excluding from GUI without removing, in case we need to re-add this functionality later
        vlayout.addLayout(hlayout)

        # set up main processing button
        self._process_button = QPushButton("Process Data")  # this button gets connected to a function in the controller -- see 
        self._process_button.clicked.connect(self.process_data)
        vlayout.addWidget(self._process_button)
        
        widget = QWidget()
        widget.setLayout(vlayout)

        self.setCentralWidget(widget)

        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")

    def closeEvent(self, event):
        if hasattr(self, "_worker"):
            self._worker.cleanup_thread()
            self._worker.deleteLater()
        # self._controller.cleanup_model()
        super().closeEvent(event)

    def update_status_bar(self, message):
        self.status_bar.showMessage(message)
    
    def _read_json_paths(self):
        json_path = "data.json"
        if os.path.exists(json_path):
            with open(json_path, "r") as file:
                paths = json.load(file)
                ks3 = paths["ks3_folder_path"]
                pl2 = paths["pl2_file_path"]
                map_ = paths["probe_map_file_path"]
                out = paths["output_file_path"]

                if os.path.exists(ks3):
                    self._ks3_folder_path.path = ks3
                
                if os.path.exists(pl2):
                    self._pl2_file_path.path = pl2
                
                if os.path.exists(map_):
                    self._probe_map_file_path.path = map_

                if os.path.exists(out):
                    self._output_file_path.path = out

    def _write_json_paths(self):
        json_path = "data.json"
        with open(json_path, "w") as file:
            paths = {}
            paths["ks3_folder_path"] = str(self._ks3_folder_path)
            paths["pl2_file_path"] = str(self._pl2_file_path)
            paths["probe_map_file_path"] = str(self._probe_map_file_path)
            paths["output_file_path"] = str(self._output_file_path)

            json.dump(paths, file)
    
    # define functions/properties to be used by controller
    @property
    def ks3_folder_path(self):
        return self._ks3_folder_path.path

    @property
    def pl2_file_path(self):
        return self._pl2_file_path.path

    @property
    def probe_map_file_path(self):
        return self._probe_map_file_path.path

    @property
    def output_file_path(self):
        out = self._output_file_path.path
        if out.parent == Path("."):
            ks3 = self.ks3_folder_path
            out = ks3 / out
        if out.suffix != ".nex5":
            out = out.with_suffix(".nex5")
        
        return out

    @property
    def include_AI_data(self):
        return self._ai_checkbox.state
    
    @property
    def include_FP_data(self):
        return self._fp_checkbox.state

    @property
    def include_event_data(self):
        return self._event_checkbox.state
    
    @property
    def include_KS3_waveform_data(self):
        return self._waveform_checkbox.state

    @property
    def include_good_clusters(self):
        return self._good_clusters_checkbox.state
    
    @property
    def include_mua_clusters(self):
        return self._mua_clusters_checkbox.state
    
    @property
    def include_noise_clusters(self):
        return self._noise_clusters_checkbox.state
    
    def add_controller(self, controller):
        self._controller = controller
        self._controller.gui_error_signal.connect(self.raise_GUI_error)

    def _setAllWidgetsEnableState(self, state:bool) -> None:
        self._process_button.setEnabled(state)
        self._ks3_folder_path.setEnabled(state)
        self._pl2_file_path.setEnabled(state)
        self._probe_map_file_path.setEnabled(state)
        self._output_file_path.setEnabled(state)

        self._ai_checkbox.setEnabled(state)
        self._fp_checkbox.setEnabled(state)
        self._event_checkbox.setEnabled(state)
        self._waveform_checkbox.setEnabled(state)

        self._good_clusters_checkbox.setEnabled(state)
        self._mua_clusters_checkbox.setEnabled(state)
        self._noise_clusters_checkbox.setEnabled(state)

    def process_data(self):
        ks3_invalid = not self.ks3_folder_path.exists()
        pl2_invalid = not self.pl2_file_path.exists()
        prb_invalid = not self.probe_map_file_path.exists()
        if ks3_invalid or pl2_invalid or prb_invalid:
            S = []
            if ks3_invalid:
                S.append("Invalid Kilosort folder path.")
            if pl2_invalid:
                S.append("Invalid PL2 file path.")
            if prb_invalid:
                S.append("Invalid probe map path.")
            message = " ".join(S)
            title = "Invalid Path" + "s" if len(S) > 1 else ""
            self.raise_GUI_error(title, message)
            
            return
    
        output_exists = self.output_file_path.exists()
        if output_exists:
            self.raise_GUI_error(title="Invalid Output", message=f"The specified output path already exists. Choose another.")
            return

        if hasattr(self, "_controller"):
            # disable ui elements
            self._setAllWidgetsEnableState(False)

            # create Worker object and feed it _controller.process_data() as target function
            self._worker = _Worker(self._controller.process_data)
            
            # connect worker's finished signal to slot for triggering self.on_data_processing_completion
            self._worker.finished.connect(self.on_data_processing_completion)

            # start the thread
            self._worker.run()

    
    def on_data_processing_completion(self):
        # Re-enable the button
        self._setAllWidgetsEnableState(True)

        # Clean up the thread and worker objects
        if hasattr(self, "_worker"):
            self._worker.cleanup_thread()
            self._worker.deleteLater()

    def cleanup(self):
        self._write_json_paths()
    
    def raise_GUI_error(self, title, message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setText(message)
        dlg.exec_()
        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GUI()
    window.show()

    app.exec_()

    window.cleanup()