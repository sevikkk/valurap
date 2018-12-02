Next iteration of 3d printer
============================

Hardware
--------

* 20x20 and 20x40 v-profile, linear rails based on PVC rollers
* E3D Titan Aero Extruder

Electronics
-----------

* Orange PI Zero as main brains and network
* Mojo v3 as FPGA
* TMC2130 Stepper drivers

Directories
-----------

* fpga/ - verilog sources for SLX9 on Mojo 
* mojo_soft/ - software for mega32u4 on Mojo
* host_soft/ - python sources running on Zero
* pcbs/ - KiCad files for PCBs 

