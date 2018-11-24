DESIGN		= valurap

PINS		= cfg/mojo.ucf
DEVICE		= xc6slx9-2-tqg144
IMPACT		= cfg/impact.run

TOP		= mojo_top

BGFLAGS		= -g StartUpClk:CCLK -g DonePipe:Yes -g Compress -g DriveDone:Yes

# standard opts
#MAPFLAGS	= -ol std
# with optimizations
MAPFLAGS	= -bp -ol high -timing -xe n -logic_opt on -convert_bram8

# standard opts
#PARFLAGS	= -ol std
# with optimizations
PARFLAGS	= -ol high

# Top 

SRC = \
	src/cclk_detector.v \
	src/dds_uart_clock.v \
	src/uart_transceiver.v \
	src/$(TOP).v

all:		bits

remake:		clean-build all

clean:
		rm -f *~ */*~ a.out *.log *.key *.edf *.ps trace.dat

clean-build:
		rm -rf build

cleanall:	clean
		rm -rf build $(DESIGN).bit

bits:		$(DESIGN).bit

download: bits
		cd build && impact -batch ../${IMPACT}

#
# Simulation
#

TB?= s3g_rx_tb

build/top_exe: $(SRC) tb/$(TB).v
	@[ -d build ] || mkdir build
	echo verilog work ../tb/$(TB).v > build/fuse.src
	cd build && fuse -prj fuse.src -o top_exe work.$(TB)

sim:    build/top_exe

sim-run: build/top_exe
	cd build && ./top_exe -gui -view ../tb/$(TB).wcfg &


build/top.out: $(SRC) tb/$(TB).v
	@[ -d build ] || mkdir build
	echo ../tb/$(TB).v > build/iverilog.src
	cd build && iverilog -I ../src -c iverilog.src -o top.out

isim:    build/top.out
	cd build && ./top.out

isim-run: build/top.out
	cd build && gtkwave -a ../tb/$(TB).sav &

#
# Synthesis
#
build/project.src:
		@[ -d build ] || mkdir build
		@rm -f $@
		for i in $(SRC); do echo verilog work ../$$i >> $@; done

build/project.xst: build/project.src
		echo "run" > $@
		echo "-top $(TOP)" >> $@
		echo "-p $(DEVICE)" >> $@
		echo "-opt_mode Speed" >> $@
		echo "-opt_level 1" >> $@
		echo "-ifn project.src" >> $@
		echo "-ifmt mixed" >> $@
		echo "-ofn project.ngc" >> $@
		echo "-ofmt NGC" >> $@
		echo "-infer_ramb8 No" >> $@

build/project.ngc: build/project.xst $(SRC)
		cd build && xst -ifn project.xst -ofn project.log

build/project.ngd: build/project.ngc $(PINS)
		cd build && ngdbuild -p $(DEVICE) project.ngc -uc ../$(PINS)

build/project.ncd: build/project.ngd
		cd build && map -pr b -p $(DEVICE) -w project $(MAPFLAGS)

build/project_r.ncd: build/project.ncd
		cd build && par -w project project_r.ncd $(PARFLAGS)

build/project_r.twr: build/project_r.ncd
		cd build && trce -v 25 project_r.ncd project.pcf

$(DESIGN).bit:	build/project_r.ncd build/project_r.twr
		cd build && bitgen project_r.ncd -l -w $(BGFLAGS)
		@cp -f build/project_r.bit $@

