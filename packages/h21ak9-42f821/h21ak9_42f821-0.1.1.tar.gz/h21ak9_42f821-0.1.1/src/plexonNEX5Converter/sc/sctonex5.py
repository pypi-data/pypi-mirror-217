import numpy as np
from phylib.io.model import load_model
from ..pypl2 import pl2_ad, pl2_events
from ..nex.NexFileData import *
from ..nex.NexFileWriters import Nex5FileWriter
import csv

def is_valid_file(file_path: str) -> bool:
    import os.path
    return os.path.isfile(file_path)

def get_probe_info(probe_file: str) -> tuple:
    """
    Gets values from a .prb file.
    https://spyking-circus.readthedocs.io/en/latest/code/probe.html

    Args:
        probe_file - probe (.prb) file
    Returns:
        See link above for information on the three variables returned.
        Returns (0,0,{}) if the .prb file doesn't exist or can't be parsed.
    """
    if not is_valid_file(probe_file):
        return 0,0,{}

    try:
        from importlib.util import spec_from_loader, module_from_spec
        from importlib.machinery import SourceFileLoader
        spec = spec_from_loader("probe_module", SourceFileLoader("probe_module", probe_file))
        probe_module = module_from_spec(spec)
        spec.loader.exec_module(probe_module)
    except:
        return 0,0,{}

    return probe_module.total_nb_channels, probe_module.radius, probe_module.channel_groups

def get_probe_channel_location_map(probe_file: str, reverse_flag:bool=False) -> dict:
    """
    Gets dict where the key is the x,y coordinate and the value is the channel number.

    Args:
        probe_file - probe (.prb) file
        reverse_flag - expresses whether channel map should be keyed on coordinates (False) or channel numbers (True)
    Returns:
        Dict that should appear as:
            {(x1,y1):channel1, (x2,y2:channel2) ...} --> reverse_flag = False
            {channel1:(x1,y1), channel2:(x2,y2) ...} --> reverse_flag = True
        Returns empty dict on failure.
    """
    if not is_valid_file(probe_file):
        return {}

    _ ,_ , channel_groups = get_probe_info(probe_file)

    if channel_groups == {}:
        return {}
    
    channel_location_map = {}
    for group in channel_groups.keys():
        channel_location_map = channel_location_map | {tuple(v): k for k, v in channel_groups[group]['geometry'].items()}
    
    if not reverse_flag:
        return channel_location_map
    else:
        return {value: key for key, value in channel_location_map.items()}

def debug_print_probe_channel_groups(probe_file: str) -> str:
    if not is_valid_file(probe_file):
        return ''

    _ ,_ , channel_groups = get_probe_info(probe_file)

    if channel_groups == {}:
        return ''
    print("DEBUG_PRINT_PROBE_CHANNEL_GROUPS")
    for s in channel_groups[1]["geometry"].items():
        print('Ch: {} Coords: {}'.format(s[0], s[1]))

def debug_print_model_channel_positions(params_file: str) -> str:
    if not is_valid_file(params_file):
        return ''
    
    model = load_model(params_file)
    print("DEBUG_PRINT_MODEL_CHANNEL_POSITIONS")
    for s in range(len(model.channel_positions) - 1):
        print('Ch: {} Coords: {}'.format(s, model.channel_positions[s]))

def get_probe_valid_channels(probe_file: str) -> list:
    """
    Args:
        probe_file - probe (.prb) file
    Returns:
        List of valid channel numbers on the probe. Assume unlisted channels were disabled or noisy.
        Returns empty list on failure.
    """
    if not is_valid_file(probe_file):
        return []
    
    _, _ , channel_groups = get_probe_info(probe_file)

    if channel_groups == {}:
        return []

    return channel_groups[1]["channels"]

def get_cluster_best_channel(cluster_info_file: str, cluster_id: int) -> int:
    """
    Parse cluster_info.tsv to get the best channel for a cluster ID.

    REMEMBER THAT THIS IS THE CHANNEL IN THE SORTING AND DOES NOT NECESSARILY
    EQUAL THE CHANNEL NUMBER IN THE PL2 FILE IT CAME FROM!
    """
    if not is_valid_file(cluster_info_file):
        return -1
    
    lines = []
    with open(cluster_info_file) as f:
        read = csv.reader(f, delimiter="\t", quotechar='"')
        for row in read:
            if row[0] == str(cluster_id):
                return int(row[2])
    
    return -1
    
def spyking_circus_channel_to_pl2_channel(params_file: str, probe_file: str, spyking_circus_channel: int) -> int:
    if not is_valid_file(params_file):
        return -1
    
    if not is_valid_file(probe_file):
        return -1
    
    model = load_model(params_file)
    sc_xpos, sc_ypos = model.channel_positions[spyking_circus_channel]
    probe_channel_location_map = get_probe_channel_location_map(probe_file)
    pl2_channel = probe_channel_location_map[(int(sc_xpos), (int(sc_ypos)))]
    return pl2_channel
    



def get_params_info(params_file: str) -> tuple:
    pass
def spykingcircus_to_nex5(prb_file, npy_folder, pl2_file, nex5_file, include_waveforms = False):
    pass


if __name__ == '__main__':
    #debug
    debug_print_probe_channel_groups(r"C:\Users\chris\Spikes\sc_file5\SiNAPS_256_file5.prb")
    debug_print_model_channel_positions(r"C:\Users\chris\Spikes\sc_file5\file5\file5\file5.GUI\params.py")