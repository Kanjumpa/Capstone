-- Coincidence Counter Circuit Using Asynchronous Delay
-- Finished April 7th 2008, Whitman College
-- Designed by Mark Beck, beckmk@whitman.edu and Jesse Lord, lordjw@whitman.edu
-- With delay chain tweaks by William Morong, wmorong@berkeley.edu
-- Editions by Jeff Nicholls, jeff.nicholls@mail.utoronto.ca including
	-- Adaption to DE2-115 Cyclone IV FPGA (adjustments to GPIO pin assignments)
	-- Passive determination of all possible coincidences (2,3,4-fold)
	-- Implementation of up to 32 different delays (increased from 3)
	-- Small changes in documentation
-------------------------------------------------------------------------------
-- This circuit takes input signals from four photon detectors A,B,C,D
-- and shortens each pulse to decrease unintended overlap of signals;
-- thus decreasing the number of false coincidence detections.
-- In this design file, the input pulses are obtained using the GPIO.
-- The shortened single photon detection signal and coincidence photon
-- detections are output on the RS232 port using signal UART_TXD

-- top level entity
LIBRARY ieee;
USE ieee.std_logic_1164.all;
use IEEE.numeric_std.all;
LIBRARY altera_mf;
USE altera_mf.altera_mf_components.all;

ENTITY RS232coincidencecounter IS
	PORT
	(
-- The transmitter to the RS-232 port where the data is sent out to LabView
		UART_TXD	:OUT	STD_LOGIC;
-- The 50 MHz clock that is provided on the DE2-115 Board
		Clock_50	:IN		STD_LOGIC;
-- The switchs 0 through 17 on the DE2-115 Board	
		SW			:IN		STD_LOGIC_VECTOR(17 DOWNTO 0);
-- The 40 pin expansion header GPIO pins, which can be used as input or output signals
-- The 40 pins are labeled on the board as GPIO.  This program sets however many that 
-- are needed as input as GPIO_IN and the rest to GPIO_OUT.  See documentation for
-- a pinout description.
		GPIO_IN		:IN		STD_LOGIC_VECTOR(7 DOWNTO 0);
		GPIO_OUT	:OUT	STD_LOGIC_VECTOR(35 DOWNTO 8);
-- The red LED lights 0 through 17 on the DE2 Board
		LEDR		:OUT	STD_LOGIC_VECTOR(17 DOWNTO 0)
	);
END RS232coincidencecounter;

ARCHITECTURE Behavior OF RS232coincidencecounter IS

-- Constant parameter which is the width of the counters
	CONSTANT COUNTER_WIDTH : integer := 32;
-- Constant parameter which is the number of coincidences determined
	CONSTANT NUM_COINCIDENCES : integer := 11;
-- Constant parameter which is the number switches needed to choose delay
	CONSTANT NUM_SWITCHES : integer := 5;
-- Constant parameter which is the number of LCELL delays created
	CONSTANT DELAY_CHAIN_WIDTH : integer := 33;
-- Constant parameter which is the number of LCELL delays used
	CONSTANT DELAYS_USED : integer := 31;

-- This COMPONENT chooses one of the three delayed pulses, inverts the chosen pulse,
-- then ANDs the inverted, delayed pulse with the original (effectively shortening the original)
	COMPONENT mux32to1
		PORT
		(
			delayedpulse	:IN		STD_LOGIC_VECTOR(DELAYS_USED DOWNTO 0);
			SW				:IN		STD_LOGIC_VECTOR(NUM_SWITCHES-1 DOWNTO 0);
			pulseout		:OUT	STD_LOGIC
		);
	END COMPONENT;
-- This COMPONENT outputs one pulse for each coincidence by using a four input AND gate to combine the photon detector signals
-- For two and three fold coincidences, extra inputs are set high as dummy signals.
	COMPONENT coincidence_pulse
		PORT
		(
			a, b, c, d	:IN	 STD_LOGIC;
			y			:OUT STD_LOGIC
		);
	END COMPONENT;	
-- This COMPONENT is the Megafunction "lpm_counter" using a 14 bit output and an asynchronous clear
-- Used for implementing the data trigger
	COMPONENT data_trigger_counter
		PORT
		(
			aclr	: IN 	STD_LOGIC;
			clock	: IN 	STD_LOGIC;
			q		: OUT 	STD_LOGIC_VECTOR (14 DOWNTO 0)
		);
	END COMPONENT;	
-- This COMPONENT is the Megafunction "lpm_counter" using a 13 bit output and an asynchronous clear
-- Used for implementing the baud clock
	COMPONENT baud_counter
		PORT
		(
			aclr	: IN 	STD_LOGIC;
			clock	: IN 	STD_LOGIC;
			q		: OUT 	STD_LOGIC_VECTOR (12 DOWNTO 0)
		);
	END COMPONENT;	
-- This COMPONENT is the Megafunction "lpm_counter" using a 32 bit output and an asynchronous clear
-- Used for storing count and coincidence data
	COMPONENT counter
		PORT
		(
			aclr	: IN	STD_LOGIC;
			clock	: IN	STD_LOGIC;
			q		: OUT	STD_LOGIC_VECTOR (COUNTER_WIDTH-1 DOWNTO 0)
		);
	END COMPONENT;
-- This COMPONENT takes in the single photon and coincidence photon counts and sends it out
-- on the RS232 port, the data stream is started by data_trigger every 1/10th of a second
-- and the rate of the data_stream is controled by the 19200 bits/sec baud clock
	COMPONENT DataOut
		PORT
		(
			A				:IN		STD_LOGIC_VECTOR(COUNTER_WIDTH-1 DOWNTO 0);
			B				:IN		STD_LOGIC_VECTOR(COUNTER_WIDTH-1 DOWNTO 0);
			C				:IN		STD_LOGIC_VECTOR(COUNTER_WIDTH-1 DOWNTO 0);
			D				:IN		STD_LOGIC_VECTOR(COUNTER_WIDTH-1 DOWNTO 0);
			Coincidence		:IN		STD_LOGIC_VECTOR(NUM_COINCIDENCES*COUNTER_WIDTH-1 DOWNTO 0);
			clk				:IN		STD_LOGIC;
			data_trigger	:IN		STD_LOGIC;
			UART_TXD		:OUT	STD_LOGIC
		);
	END COMPONENT;

-- This SIGNAL counts the baud clock until it reaches 1920, which occurs every 1/10th of a second
	SIGNAL data_trigger_count: STD_LOGIC_VECTOR(14 DOWNTO 0);
-- This SIGNAL is turned on every 1/10th of a second for one 50 MHz clock pulse and resets
-- the photon detection counters
	SIGNAL data_trigger_reset: STD_LOGIC;
-- This SIGNAL is turned on every 1/10th of a second and begins the data stream out
	SIGNAL data_trigger: STD_LOGIC;
-- This SIGNAL acts as a clock to output data at the baud rate of 19200 bits/second
	SIGNAL baud_rate_clk: STD_LOGIC;
-- This SIGNAL counts the 50 MHz clock pulses until it reaches 2604 in order to time the baud clock
	SIGNAL baud_rate_count: STD_LOGIC_VECTOR(12 DOWNTO 0);
-- These SIGNALs represent the four input pulse from the photon detectors		
	SIGNAL A, B, C, D: STD_LOGIC;
-- These SIGNALs represent the delayed versions of each channel which are eventually fed into the mux
	SIGNAL A_internal, B_internal, C_internal, D_internal: STD_LOGIC_VECTOR(DELAY_CHAIN_WIDTH-1 DOWNTO 0);
-- These SIGNALS are the input to the 32to1 mux and are a concatenation of a selection of the 
-- internals and the original pulse
	SIGNAL A_Muxin, B_Muxin, C_Muxin, D_Muxin: STD_LOGIC_VECTOR(DELAYS_USED DOWNTO 0);
	
-- The SYN_KEEP attribute preserves a signal through the compiler, so redundant logic is not optimized away.
-- Required to keep LCELL delays.
	ATTRIBUTE syn_keep : boolean;
	ATTRIBUTE syn_keep of A_internal: signal is true;
	ATTRIBUTE syn_keep of B_internal: signal is true;
	ATTRIBUTE syn_keep of C_internal: signal is true;
	ATTRIBUTE syn_keep of D_internal: signal is true;

-- These SIGNALs represent the shortened pulses output by the mux32to1 COMPONENT		
	SIGNAL A_s, B_s, C_s, D_s: STD_LOGIC;
-- These SIGNALs represent the four output pulses	
	SIGNAL A_f, B_f, C_f, D_f: STD_LOGIC;
-- This SIGNAL represents the outputs of the four input AND gates that detect each coincidence
-- Coincidences are labeled in the following way:
-- 		AB = Coincidence(0)
-- 		AC = Coincidence(1)
-- 		AD = Coincidence(2)
-- 		BC = Coincidence(3)
-- 		BD = Coincidence(4)
-- 		CD = Coincidence(5)
-- 		ABC = Coincidence(6)
-- 		BCD = Coincidence(7)
-- 		ACD = Coincidence(8)
-- 		ABD = Coincidence(9)
-- 		ABCD = Coincidence(10)
	SIGNAL Coincidence: STD_LOGIC_VECTOR(NUM_COINCIDENCES-1 DOWNTO 0);
-- This SIGNAL represents the top level design entity instantiation of
-- the number of coincidences counted.  It is divided into 11 different groups of widths
-- equal to the width of each counter (32).  It is essentially the coincidence count bus.
-- Least significant sub-buses are associated with coincidence(0) and up.
	SIGNAL Count_top: STD_LOGIC_VECTOR(NUM_COINCIDENCES*COUNTER_WIDTH-1 DOWNTO 0);
-- This SIGNAL represents the the number of coincidences counted
	SIGNAL Count_out: STD_LOGIC_VECTOR(NUM_COINCIDENCES*COUNTER_WIDTH-1 DOWNTO 0);
-- This SIGNAL represents the top level design entity instantiation of the number of counts
-- in the detectors A, B, C, and D respectively
	SIGNAL A_top, B_top, C_top, D_top: STD_LOGIC_VECTOR(COUNTER_WIDTH-1 DOWNTO 0);
-- This SIGNAL represents the number of counts in the detectors A, B, C, and D respectively
	SIGNAL A_out, B_out, C_out, D_out: STD_LOGIC_VECTOR(COUNTER_WIDTH-1 DOWNTO 0);
-- This SIGNAL is the only variable that is sent to the computer from the program	
	SIGNAL Output: STD_LOGIC_VECTOR(COUNTER_WIDTH-1 DOWNTO 0);

BEGIN
-- This initializes the input APDs signals
-- These are the only inputs
	A <= GPIO_IN(0);
	B <= GPIO_IN(2);
	C <= GPIO_IN(4);
	D <= GPIO_IN(6);

-- This creates, using iteration, a chain of LCELL buffers for each A, B, C, D signal,
-- which act to delay the signals.
-- Number of cells is arbitrary, although determines the maximum possible delay which
-- can be used.
-- In this case 33 delays are created, of which only 31 are used in the end
	LCA_1: LCELL PORT MAP(a_in=> A, a_out=>A_internal(0));
	Gen_delay_A : FOR i in 0 to DELAY_CHAIN_WIDTH-2 GENERATE
		LC : LCELL PORT MAP(a_in => A_internal(i),a_out => A_internal(i+1));
	END GENERATE;

	LCB_1: LCELL PORT MAP(a_in=> B, a_out=>B_internal(0));
	Gen_delay_B : FOR i in 0 to DELAY_CHAIN_WIDTH-2 GENERATE
		LC : LCELL PORT MAP(a_in => B_internal(i),a_out => B_internal(i+1));
	END GENERATE;
	
	LCC_1: LCELL PORT MAP(a_in=> C, a_out => C_internal(0));
	Gen_delay_C : FOR i in 0 to DELAY_CHAIN_WIDTH-2 GENERATE
		LC : LCELL PORT MAP(a_in => C_internal(i),a_out => C_internal(i+1));
	END GENERATE;
	
	LCD_1: LCELL PORT MAP(a_in=> D, a_out => D_internal(0));
	Gen_delay_D : FOR i in 0 to DELAY_CHAIN_WIDTH-2 GENERATE
		LC : LCELL PORT MAP(a_in => D_internal(i),a_out => D_internal(i+1));
	END GENERATE;
	

-- Append the bus of delayed signals to the non-delayed signal for easier
-- input into the 32to1 mux
-- For this case the delays we use correspond to the most significant bits and we use
-- a number equivalent to constant DELAYS_USED which in this case is 31
	A_Muxin <= A_internal(DELAY_CHAIN_WIDTH-1 DOWNTO DELAY_CHAIN_WIDTH-DELAYS_USED) & A;
	B_Muxin <= B_internal(DELAY_CHAIN_WIDTH-1 DOWNTO DELAY_CHAIN_WIDTH-DELAYS_USED) & B;
	C_Muxin <= C_internal(DELAY_CHAIN_WIDTH-1 DOWNTO DELAY_CHAIN_WIDTH-DELAYS_USED) & C;
	D_Muxin <= D_internal(DELAY_CHAIN_WIDTH-1 DOWNTO DELAY_CHAIN_WIDTH-DELAYS_USED) & D;
	
-- These COMPONENTs shape the input pulses based on switches 17 through 13
-- Input is the bus of delayed pulses, output is the shortened pulse
-- chosen by the switches
	MA: mux32to1 PORT MAP( A_Muxin, SW(17 DOWNTO 13), A_s );
	MB: mux32to1 PORT MAP( B_Muxin, SW(17 DOWNTO 13), B_s );
	MC: mux32to1 PORT MAP( C_Muxin, SW(17 DOWNTO 13), C_s );
	MD: mux32to1 PORT MAP( D_Muxin, SW(17 DOWNTO 13), D_s );

-- Determination of all possible coincidences between shortened pulses
-- Constant highs are used as dummy signals to produce lower order coincidences
	CP0: coincidence_pulse PORT MAP( A_s, B_s, '1', '1', Coincidence(0)); -- AB
	CP1: coincidence_pulse PORT MAP( A_s, '1', C_s, '1', Coincidence(1)); -- AC
	CP2: coincidence_pulse PORT MAP( A_s, '1', '1', D_s, Coincidence(2)); -- AD
	CP3: coincidence_pulse PORT MAP( '1', B_s, C_s, '1', Coincidence(3)); -- BC
	CP4: coincidence_pulse PORT MAP( '1', B_s, '1', D_s, Coincidence(4)); -- BD
	CP5: coincidence_pulse PORT MAP( '1', '1', C_s, D_s, Coincidence(5)); -- CD
	CP6: coincidence_pulse PORT MAP( A_s, B_s, C_s, '1', Coincidence(6)); -- ABC
	CP7: coincidence_pulse PORT MAP( '1', B_s, C_s, D_s, Coincidence(7)); -- BCD
	CP8: coincidence_pulse PORT MAP( A_s, '1', C_s, D_s, Coincidence(8)); -- ACD
	CP9: coincidence_pulse PORT MAP( A_s, B_s, '1', D_s, Coincidence(9)); -- ABD
	CP10: coincidence_pulse PORT MAP( A_s, B_s, C_s, D_s, Coincidence(10)); -- ABCD

-- Once the output of the 14 bit counter reaches 1920, this process turns on the SIGNAL 'data_trigger'
-- The SIGNAL 'data_trigger' then acts as a clock pulse, reseting the counts
	PROCESS ( data_trigger_count )
		BEGIN
		IF data_trigger_count = "000011110000000" THEN
			data_trigger_reset <= '1';
			data_trigger <= '1';
		ELSIF data_trigger_count = "000000000000000" THEN
			data_trigger_reset <= '0';
			data_trigger <= '1';
		ELSIF data_trigger_count = "000000000000001" THEN
			data_trigger_reset <= '0';
			data_trigger <= '1';
		ELSE
			data_trigger_reset <= '0';
			data_trigger <= '0';
		END IF;
	END PROCESS;
	
-- Once the output of the 13 bit counter reaches 2,604, this process turns on the SIGNAL 'baud_rate_clk'
-- The SIGNAL 'baud_rate_clk' then acts as a clock pulse, send the data out at the specified baud rate
	PROCESS ( baud_rate_count )
		BEGIN
		IF baud_rate_count = "0101000101100" THEN
			baud_rate_clk <= '1';
		ELSE
			baud_rate_clk <= '0';
		END IF;
	END PROCESS;
	
-- Uses the 14 bit counter and ~9,600 baud rate clock to count to 1/10th of a second to trigger DataOut
	CX: data_trigger_counter PORT MAP ( data_trigger_reset, baud_rate_clk, data_trigger_count );

-- Uses the 13 bit counter and 50 MHz clock to count the baud rate
	CY: baud_counter PORT MAP ( baud_rate_clk, Clock_50, baud_rate_count );

-- Use the 32 bit counter to count the detection of single photons and coincidence photons
-- It outputs the data in 32-bit arrays and resets every 1/10th of a second
	C0: counter PORT MAP ( data_trigger_reset, Coincidence(0), Count_top(1*COUNTER_WIDTH-1 DOWNTO 0*COUNTER_WIDTH));
	C1: counter PORT MAP ( data_trigger_reset, Coincidence(1), Count_top(2*COUNTER_WIDTH-1 DOWNTO 1*COUNTER_WIDTH));
	C2: counter PORT MAP ( data_trigger_reset, Coincidence(2), Count_top(3*COUNTER_WIDTH-1 DOWNTO 2*COUNTER_WIDTH));
	C3: counter PORT MAP ( data_trigger_reset, Coincidence(3), Count_top(4*COUNTER_WIDTH-1 DOWNTO 3*COUNTER_WIDTH));
	C4: counter PORT MAP ( data_trigger_reset, Coincidence(4), Count_top(5*COUNTER_WIDTH-1 DOWNTO 4*COUNTER_WIDTH));
	C5: counter PORT MAP ( data_trigger_reset, Coincidence(5), Count_top(6*COUNTER_WIDTH-1 DOWNTO 5*COUNTER_WIDTH));
	C6: counter PORT MAP ( data_trigger_reset, Coincidence(6), Count_top(7*COUNTER_WIDTH-1 DOWNTO 6*COUNTER_WIDTH));
	C7: counter PORT MAP ( data_trigger_reset, Coincidence(7), Count_top(8*COUNTER_WIDTH-1 DOWNTO 7*COUNTER_WIDTH));
	C8: counter PORT MAP ( data_trigger_reset, Coincidence(8), Count_top(9*COUNTER_WIDTH-1 DOWNTO 8*COUNTER_WIDTH));
	C9: counter PORT MAP ( data_trigger_reset, Coincidence(9), Count_top(10*COUNTER_WIDTH-1 DOWNTO 9*COUNTER_WIDTH));
	C10: counter PORT MAP ( data_trigger_reset, Coincidence(10), Count_top(11*COUNTER_WIDTH-1 DOWNTO 10*COUNTER_WIDTH));
	CA: counter PORT MAP ( data_trigger_reset, A_s, A_top );
	CB: counter PORT MAP ( data_trigger_reset, B_s, B_top );
	CC: counter PORT MAP ( data_trigger_reset, C_s, C_top );
	CD: counter PORT MAP ( data_trigger_reset, D_s, D_top );
	
-- This process sets the single photon and coincidence photon count output arrays every 1/10th of a second
	PROCESS( data_trigger_reset )
	BEGIN
		IF data_trigger_reset'EVENT AND data_trigger_reset = '1' THEN
			A_out <= A_top;
			B_out <= B_top;
			C_out <= C_top;
			D_out <= D_top;
			Count_out <= Count_top;
		END IF;
	END PROCESS;
	
-- Sends the A, B, C, D and the Coincidence counts out on the RS-232 port
	D0: DataOut PORT MAP( A_out, B_out, C_out, D_out, Count_out, baud_rate_clk, data_trigger, UART_TXD);
	
-- Turns on the corresponding red LED whenever one of the DE2 board switches is turned on
	LEDR <= SW;
	
-- Grounding output pins to prevent noise
	GPIO_OUT(35) <= '0';
	GPIO_OUT(33) <= '0';
	GPIO_OUT(31) <= '0';
	GPIO_OUT(29) <= '0';
	GPIO_OUT(27) <= '0';
	GPIO_OUT(25) <= '0';
	GPIO_OUT(23) <= '0';
	GPIO_OUT(21) <= '0';
	GPIO_OUT(19) <= '0';
	GPIO_OUT(17) <= '0';
	GPIO_OUT(15) <= '0';
	GPIO_OUT(13) <= '0';
	GPIO_OUT(11) <= '0';
	GPIO_OUT(9) <= '0';
	
-- Sending the original signals, shortened signals, coincidence signals and the 10 Hz clock (data_trigger)
-- to debug circuit if necessary
-- Refer to documentation for pinout description
	GPIO_OUT(34) <= A;
	GPIO_OUT(32) <= A_s;
	GPIO_OUT(30) <= B;
	GPIO_OUT(28) <= B_s;
	GPIO_OUT(26) <= C;
	GPIO_OUT(24) <= C_s;
	GPIO_OUT(22) <= D;
	GPIO_OUT(20) <= D_s;
	GPIO_OUT(18) <= A_internal(10);
	GPIO_OUT(16) <= NOT A_internal(10);
	GPIO_OUT(14) <= A_internal(27);
	GPIO_OUT(12) <= NOT A_internal(27);
	GPIO_OUT(10) <= data_trigger;
	GPIO_OUT(8) <= coincidence(0);
	
END Behavior;
