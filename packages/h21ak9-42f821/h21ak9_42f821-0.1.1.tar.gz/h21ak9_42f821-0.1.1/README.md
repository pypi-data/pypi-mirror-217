# plexonNEX5converter: tool for integrating Kilosort into OmniPlex/SiNAPS workflow

Users of Plexon's OmniPlex platform with high-density SiNAPS probes may opt to use Kilosort to sort spikes based on templates spread across multiple pixels, an exceedingly difficult task to perform manually. After running the data through Kilosort, they may further wish to open the data in NeuroExplorer, a de-facto standard for neurodata analysis in use across hundreds of laboratories around the world.

**plexonNEX5converter** is a simple GUI-based application that integrates the output of Kilosort with field potential (FP), analog (AI), and digital event (EVT) data from the associated PL2 file, into a single .nex5 file compatible with NeuroExplorer. It requires four inputs:

 1. KS3 Data Folder - this is the path to the folder containing the Kilosort data, i.e., the folder in which params.py may be found.
 2. PL2 File - this is the path to the PL2 file upon whose data Kilosort was run (after conversion to RIL-format).
 3. Probe Map - this is the path to the channel map .mat file for the SiNAPS probe that was provided to Kilosort.
 4. Output File - this is the path of the output file. Note that if only the filename is specified (i.e., no parent path is provided), the output file will appear in the KS3 Data Folder.

Also included are six checkboxes:

 1. Include AI -- whether analog data from the PL2 file should be included
 2. Include FP -- whether field potential data from the PL2 file should be included
 3. Include Digital Events -- whether digital event data from the PL2 file should be included
 4. Include KS3 Waveforms -- whether whitened spike waveforms from Kilosort should be included alongside spike timestamps
 5. Include Good Clusters -- whether clusters labeled "good" during curation by Phy should be included
 6. Include MUA Clusters -- whether clusters labeled "MUA" (multi-unit activity) during curation by Phy should be included


