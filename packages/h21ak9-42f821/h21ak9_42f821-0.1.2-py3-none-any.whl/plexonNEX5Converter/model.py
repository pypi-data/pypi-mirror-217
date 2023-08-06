import os
import re
import numpy as np
from pathlib import Path
from phylib.io.model import load_model
from phylib.io.traces import extract_waveforms
from scipy.io import loadmat
from collections import namedtuple
from string import ascii_lowercase
from .nex.NexFileData import *
from .nex.NexFileWriters import Nex5FileWriter
from .sc import sctonex5 as sc
from .pypl2 import pypl2api as pl2
from .pypl2 import pypl2lib as pl2lib
import traceback    # for formatting error traceback

class KS3ToNEX5Converter(object):
    """This class contains the fields and functions
       necessary to convert KS3 output to NEX5 format,
       integrating information from an associated PL2 
       file."""
    
    def __init__(self):
        self._ks3_folder_path = None
        self._pl2_file_path = None
        self._probe_map_file_path = None    # this will point to the .mat file fed into Kilosort
        self._output_file_path = None

        # flags for kilosort data to include
        self.include_KS3_spike_waveforms = None      # this is the waveform data

        # flags for pl2 data to include
        self.include_FP_data = None
        self.include_AI_data = None
        self.include_event_data = None

        self.include_good_clusters = None
        self.include_mua_clusters = None
        self.include_noise_clusters = None
        
        # including these flags but not implementing for now
        self.__include_WB_data = None
        self.__include_SPKC_data = None

        self._filedata = FileData()

        self._terminate_flag = False # this flag terminates the model's ongoing run when there is a problem

    def add_controller(self, controller):
        self._controller = controller

    def print_message(self, message:str) -> None:
        print(message)

        if hasattr(self, "_controller"):
            self._controller.relay_message_to_GUI(message)
        
    #### properties
    @property
    def ks3_folder_path(self):
        return self._ks3_folder_path
    
    @ks3_folder_path.setter
    def ks3_folder_path(self, val):
        self._ks3_folder_path = val
        params_path = os.path.join(self._ks3_folder_path, 'params.py')
        self._params = self._parse_params_file(params_path)

        if not self._terminate_flag:
            self._filedata.TimestampFrequency = self._params.sample_rate
            self._model = load_model(params_path)
    
    @property
    def pl2_file_path(self):
        return self._pl2_file_path
    
    @pl2_file_path.setter
    def pl2_file_path(self, val):
        self._pl2_file_path = val
        self._pl2_info = pl2.pl2_info(val)
    
    @property
    def probe_map_file_path(self):
        return self._probe_map_file_path

    @probe_map_file_path.setter
    def probe_map_file_path(self, val):
        self._probe_map_file_path = val

        # probe map comes from kilosort
        if val[-4:] == ".mat":
            self._probe_coordinates_to_channel_number_mapping = self._generate_kilosort_electrode_coordinate_to_probe_channel_mapping(val, reverse_flag=False)
            self._channel_number_to_probe_coordinates_mapping = self._generate_kilosort_electrode_coordinate_to_probe_channel_mapping(val, reverse_flag=True)
        
        # probe mamp comes from spyking circus
        elif val[-4:] == ".prb":
            self._probe_coordinates_to_channel_number_mapping = self._generate_spyking_circus_electrode_coordinate_to_probe_channel_mapping(val, reverse_flag=False)
            self._channel_number_to_probe_coordinates_mapping = self._generate_spyking_circus_electrode_coordinate_to_probe_channel_mapping(val, reverse_flag=True)


    
    @property
    def output_file_path(self):
        return self._output_file_path

    @output_file_path.setter
    def output_file_path(self, val):
        self._output_file_path = val


    #### functions
    def _parse_params_file(self, params_path:str):
        """Returns data contained in Kilosort3 output
           file 'params.py' as a NamedTuple with the
           following fields: dat_path, n_channels_dat,
           dtype, offset, sample_rate, hp_filtered."""
        
        def generate_pattern(field_name):
            return f"(?<={field_name} =).+"
    
        if not Path(params_path).exists():
            self._raise_error_in_gui(title="Invalid params.py path", message=f"params.py not found in {str(self.ks3_folder_path)}")
            self._terminate_flag = True
            return

        with open(params_path, 'rt') as file:
            txt = file.read()
            dat_path = re.findall(generate_pattern("dat_path"), txt)[0].replace("'","").strip()
            n_channels_dat = re.findall(generate_pattern("n_channels_dat"), txt)[0].strip()
            dtype = re.findall(generate_pattern("dtype"), txt)[0].replace("'","").strip()
            offset = re.findall(generate_pattern("offset"), txt)[0].strip()
            sample_rate = re.findall(generate_pattern("sample_rate"), txt)[0].strip()
            hp_filtered = re.findall(generate_pattern("hp_filtered"), txt)[0].strip()
        
        if not Path(dat_path).exists():
            self._raise_error_in_gui(title="Invalid dat_path", message="params.py contains a non-existent dat_path.")
            self._terminate_flag = True
        
        Params = namedtuple("Params", "dat_path n_channels_dat dtype offset sample_rate hp_filtered")
        return Params(dat_path, int(n_channels_dat), dtype, int(offset), float(sample_rate), True if hp_filtered=="True" else False)        
    
    def _generate_kilosort_electrode_coordinate_to_probe_channel_mapping(self, probe_map_path, reverse_flag=False):
        """Generates dictionary keyed on probe's electrode coordinates
           with probe's channel numbers as values"""
        
        probe_map = loadmat(probe_map_path)
        xcoords = list(probe_map["xcoords"][0].astype(np.float64))
        ycoords = list(probe_map["ycoords"][0].astype(np.float64))
        chanMap = list(probe_map["chanMap"][0].astype(np.int16))

        if not reverse_flag:
            return {(x, y): ch for x, y, ch in zip(xcoords, ycoords, chanMap)}
        else:
            return {ch:(x, y) for x, y, ch in zip(xcoords, ycoords, chanMap)}
    
    def _generate_spyking_circus_electrode_coordinate_to_probe_channel_mapping(self, probe_map_path, reverse_flag=False):
        """Generates dictionary keyed on probe's electrode coordinates
        with probe's channel numbers as values, for spyking circus prb
        map file"""

        mapping = sc.get_probe_channel_location_map(probe_map_path, reverse_flag)

        # channel numbers in spyking circus are 0-index but we want 1-index

        if not reverse_flag:
            return {key: value+1 for key, value in mapping.items()}
        else:
            return {key+1: value for key, value in mapping.items()}
    
    def _get_nearest_probe_channel_number(self, model, cluster_id, mapping):
        """Returns the probe number for the nearest channel
           to the specified cluster_id."""
        
        cluster_assoc_channels = model.get_cluster_channels(cluster_id)
        kilosort_channel_number = int(cluster_assoc_channels[0])
        XPos, YPos = model.channel_positions[kilosort_channel_number]
        probe_channel_number = int(mapping[(XPos, YPos)])

        return probe_channel_number

    def _get_unit_label(counts:dict, group:str):
        """Returns unit label for specified count of neurons
           to a probe electrode."""
        
        count = counts[group]
        if group == "mua":
            return f"m{count}"
        else:
            n_repeats = count // 26 + 1
            letter_index = (count - 1) % 26
            return ascii_lowercase[letter_index] * n_repeats

    def _get_cluster_timestamps(self, model, cluster_id):
        """Returns timestamps (in seconds) for the specified
           cluster_id"""
        
        spike_ids = model.get_cluster_spikes(cluster_id)
        timestamps = list(model.spike_times[spike_ids])

        return timestamps

    def _get_cluster_group(self, model, cluster_id):
        """Returns classification of the specified
           cluster_id -- 'good', 'mua', or 'noise'."""
        
        if "group" in model.metadata.keys() and cluster_id in model.metadata["group"]:
            return model.metadata["group"][cluster_id]
        elif "KSLabel" in model.metadata.keys() and cluster_id in model.metadata["KSLabel"]:
            return model.metadata["KSLabel"][cluster_id]
        else:
            return "unclassified"

    def _get_waveforms(self, model, cluster_id):
        """Returns waveforms for the specified cluster_id."""
        self.print_message(f"Extracting waveform data for cluster {cluster_id}.")
        
        # # Since model.get_cluster_spike_waveforms(cluster_id) breaks in the presence
        # # of _phy_spikes_subset.channels.npy, _phy_spikes_subset.spikes.npy, and 
        # # _phy_spikes_subset.waveforms.npy, rather than moving these files to a diff-
        # # erent location, explicitly write out the desired operations instead.
        # waveforms = model.get_cluster_spike_waveforms(cluster_id)
        # return waveforms

        # explicitly write out desired operations
        spike_ids = self._model.get_cluster_spikes(cluster_id)
        channel_ids = self._model.get_cluster_channels(cluster_id)
        nsw = self._model.n_samples_waveforms
        spike_samples = self._model.spike_samples[spike_ids]
        return extract_waveforms(self._model.traces, spike_samples, channel_ids, n_samples_waveforms=nsw)
    
    def _neuron_should_be_added(self, cluster_id):
        group = self._get_cluster_group(self._model, cluster_id)
        if group == "unclassified":
            self.print_message(f"Cluster {cluster_id} is unclassified. Skipping.")
            return False
        elif (group=="good" and self.include_good_clusters) or (group=="mua" and self.include_mua_clusters) or (group=="noise" and self.include_noise_clusters) or (group=="unclassified" and all([self.include_good_clusters, self.include_mua_clusters, self.include_noise_clusters])):
            return True
        else:
            return False

    def _ingest_ks3_data_into_nex5(self):
        if not self._terminate_flag:
            assert self.ks3_folder_path != None
            assert self.probe_map_file_path != None
            assert self._filedata != None

            self.print_message("Ingesting Kilosort3 data into NEX5 filedata object.")

            # declare dictionary that tracks how many neurons (i.e., clusters) have been assigned to each probe electrode
            neuron_counts = {ch: {"good":0, "mua":0, "noise":0} for ch in self._probe_coordinates_to_channel_number_mapping.values()}

            # count how many digits are needed to ensure that all neuron names are of the same length (zero-padding)
            n_digits_needed = len(str(max(self._probe_coordinates_to_channel_number_mapping.values())))

            # create list of cluster_ids ordered by
            # probe channel number, then MUAs
            # and then finally by Kilosort's cluster_id
            cluster_ids = [
                (
                    cluster_id,
                    self._get_nearest_probe_channel_number(self._model, cluster_id, self._probe_coordinates_to_channel_number_mapping),     # find the channel nearest to this cluster_id
                    self._get_cluster_group(self._model, cluster_id)    # get cluster's group
                )
                for cluster_id in self._model.cluster_ids
            ]
            cluster_ids.sort(key=lambda x: (x[1], x[2], x[0]))    # sort first by probe channel number, then by cluster group (good/mua/noise), then by kilosort cluster_id

            # loop through each cluster_id and gather all data needed to declare a Neuron object
            for cluster_id, probe_channel_number, group in cluster_ids:
                # check whether the neuron should be added based on good, mua, noise flags
                if self._neuron_should_be_added(cluster_id):
                    # assign unit label to cluster_id
                    neuron_counts[probe_channel_number][group] += 1
                    unit_label = KS3ToNEX5Converter._get_unit_label(neuron_counts[probe_channel_number], group)

                    # get cluster_id's timestamps
                    timestamps = self._get_cluster_timestamps(self._model, cluster_id)

                    # initialize Neuron object
                    neuron_name = f"SPK{str(probe_channel_number).zfill(n_digits_needed)}{unit_label}"
                    neuron = Neuron(name=neuron_name, timestamps=timestamps)

                    # populate fields of Neuron object
                    # neuron.WireNumber = probe_channel_number
                    neuron.WireNumber = int(cluster_id)
                    neuron.UnitNumber = neuron_counts[probe_channel_number]
                    neuron.XPos, neuron.YPos = self._channel_number_to_probe_coordinates_mapping[probe_channel_number]

                    # append the Neuron object to filedata
                    self._filedata.Neurons.append(neuron)

                    # get cluster_id's waveforms if needed
                    if self.include_KS3_spike_waveforms:
                        waveforms = self._get_waveforms(self._model, cluster_id)
                        waveforms = np.squeeze(waveforms[:,:,0])    # index 0 corresponds to the channel for which the cluster has the greatest amplitude

                        name = neuron_name + "_wf"
                        samplingRate = self._params.sample_rate
                        numPointsWave = waveforms.shape[1]
                        timestamps_wav = list(np.array(timestamps) - numPointsWave / self._params.sample_rate / 2)    # this accounts for the fact that for KS3 data, timepoints correspond to waveforms' center-point, whereas in NeuroExplorer, timepoints correspond to waveforms' beginning
                        values = waveforms

                        wf = Waveform(name, samplingRate, timestamps_wav, numPointsWave, values)
                        wf.UnitNumber = neuron_counts[probe_channel_number]
                        wf.WireNumber = int(cluster_id)

                        self._filedata.Waveforms.append(wf)
   
    def _ingest_pl2_data_into_nex5(self):
        if not self._terminate_flag:
            assert self.pl2_file_path != None
            assert self._filedata != None
            assert self._pl2_info != None

            def pull_ad_data(channel_prefix):
                # for use with FP, AI channels
                if channel_prefix not in ("AI","FP"):
                    raise ValueError("Invalid channel_prefix.")
                for ad_channel in self._pl2_info.ad:
                    if ad_channel.name[0:2] == channel_prefix:
                        ad = pl2.pl2_ad(filename=self.pl2_file_path, channel=ad_channel.name)
                        name = ad_channel.name
                        samplingRate = ad.adfrequency
                        fragmentStarts = ad.timestamps
                        fragmentStartIndexes = [sum(ad.fragmentcounts[0:i]) for i in range(len(ad.fragmentcounts))]
                        values = ad.ad
                        if len(values) > 0:
                            self._filedata.Continuous.append(Continuous(name, samplingRate, fragmentStarts, fragmentStartIndexes, values))

            if self.include_FP_data:
                self.print_message("Ingesting FP data from PL2 file.")
                pull_ad_data("FP")

            if self.include_AI_data:
                self.print_message("Ingesting AI data from PL2 file.")
                pull_ad_data("AI")

            if self.include_event_data:
                self.print_message("Ingesting Event data from PL2 file.")

                # create local file reader to extract frequency from file_info header using pypl2lib functions
                p = pl2lib.PyPL2FileReader()
                handle = p.pl2_open_file(self.pl2_file_path)
                pl2_file_info = pl2lib.PL2FileInfo()
                res = p.pl2_get_file_info(handle, pl2_file_info)
                frequency = pl2_file_info.m_TimestampFrequency
                p.pl2_close_file(handle)
                
                for event_channel in self._pl2_info.events:
                    e = pl2.pl2_events(filename=self.pl2_file_path, channel=event_channel.channel_name)
                    name = event_channel.name
                    timestamps = e.timestamps

                    if len(timestamps) > 0:
                        self._filedata.Events.append(Event(name=name, timestamps=timestamps))
    
    def _write_NEX5(self):
        if not self._terminate_flag:
            self.print_message("Writing NEX5 file.")
            w = Nex5FileWriter()
            w.WriteDataToNex5File(self._filedata, self._output_file_path)
    
    def cleanup(self):
        """Run this after run completes or terminates."""
        # self._return_phy_files_to_orig_folder()

        pass
    
    def run(self):
        try:
            self._ingest_ks3_data_into_nex5()
            self._ingest_pl2_data_into_nex5()
            self._write_NEX5()
            self.print_message(f"Completed writing to {self._output_file_path}.")
        except Exception as err:
            stack_trace = traceback.format_exc()
            print(stack_trace)
            self._raise_error_in_gui(title="Error", message=stack_trace)
        finally:
            self.cleanup()
        
        self.print_message("Ready.")
    
    #self._raise_error_in_gui(msg="params.py contains a non-existent dat_path.")
    def _raise_error_in_gui(self, title:str, message:str):
        self._controller.relay_error_to_GUI(title, message)

if __name__ == "__main__":
    C = KS3ToNEX5Converter()
    C.ks3_folder_path = r'C:\Users\nikhil\Documents\Projects\SiNAPS\kilosort\nex5\data\ks3_results_File5_curated'
    C.pl2_file_path = r'C:\Users\nikhil\Documents\Sample-Data\Corticale Real Data\File5.pl2'
    C.probe_map_file_path = r'C:\Users\nikhil\Documents\Projects\SiNAPS\electrode maps\sinaps-map-generator\maps\SiNAPS_1s_256ch_ChanMap.mat'
    C.output_file_path = os.path.join(C.ks3_folder_path, "output.nex5")

    C.include_AI_data = True
    C.include_event_data = True
    C.include_FP_data = True
    C.include_KS3_spike_waveforms = True

    C._filedata.Comment = "data ingested from Kilosort3 output, pl2 file"   # just to make file identical to the one generated by old script

    C.run()



