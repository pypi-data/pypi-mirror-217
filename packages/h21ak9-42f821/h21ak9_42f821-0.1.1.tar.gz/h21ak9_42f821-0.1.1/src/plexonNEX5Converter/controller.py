import sys
from pathlib import Path
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QObject
from PySide2.QtCore import Signal
from .gui import GUI
from .model import KS3ToNEX5Converter
import traceback   # for formatting error traceback

class Controller(QObject):
    gui_error_signal = Signal((str, str))

    def __init__(self):
        super().__init__()

        # initialize GUI
        self.app = QApplication(sys.argv)
        self.GUI = GUI()
        self.GUI.add_controller(self)

        # initialize model
        self._initialize_model()
        
    def _initialize_model(self):
        self.model = KS3ToNEX5Converter()
        self.model.add_controller(self)

    def run(self):
        self.GUI.show()
        self.app.exec_()
        self.GUI.cleanup()

    def relay_message_to_GUI(self, message):
        self.GUI.update_status_bar(message)
    
    def relay_error_to_GUI(self, title, message):
        self.gui_error_signal.emit(title, message)

    
    def process_data(self):
        try:
            ks3 = self.GUI.ks3_folder_path
            pl2 = self.GUI.pl2_file_path
            prb = self.GUI.probe_map_file_path
            out = self.GUI.output_file_path

            self.model.ks3_folder_path = str(ks3)
            self.model.pl2_file_path = str(pl2)
            self.model.probe_map_file_path = str(prb)
            self.model.output_file_path = str(out)

            self.model.include_AI_data = self.GUI.include_AI_data
            self.model.include_FP_data = self.GUI.include_FP_data
            self.model.include_event_data = self.GUI.include_event_data
            self.model.include_KS3_spike_waveforms = self.GUI.include_KS3_waveform_data

            self.model.include_good_clusters = self.GUI.include_good_clusters
            self.model.include_mua_clusters = self.GUI.include_mua_clusters
            self.model.include_noise_clusters = self.GUI.include_noise_clusters

            self.model.run()
        except Exception as err:
            stack_trace = traceback.format_exc()
            print(stack_trace)
            self.relay_error_to_GUI(title="Error", message=stack_trace)
        

        # refresh model upon completion
        self._initialize_model()
    
    def cleanup_model(self):
        self.model.cleanup()

def run():
    c = Controller()
    c.run()
    
if __name__ == "__main__":
    run()