-- 32 to 1 multiplexer; chooses one of 31 delayed and 1 original pulse to use for pulse shortening
-- Uses 5 switches to choose the delay corresponding to value of switches (converted from binary)
LIBRARY ieee;
USE ieee.std_logic_1164.all;
use IEEE.numeric_std.all;

ENTITY mux32to1 IS
	PORT
	(
-- Vector of delayed pulses(where 0 is the original pulse)
		delayedpulse	:IN		STD_LOGIC_VECTOR(31 DOWNTO 0);
-- These switches determine which pulse is output
		SW				:IN		STD_LOGIC_VECTOR(4 DOWNTO 0);
-- This is the output pulse
		pulseout		:OUT	STD_LOGIC
	);
END mux32to1;

ARCHITECTURE Behavior OF mux32to1 IS
BEGIN

	PROCESS(SW,delayedpulse)
	BEGIN
	
	IF to_integer(unsigned(SW)) = 0 THEN
		-- If switches are 0, select the non delayed pulse
		pulseout <= delayedpulse(0);
	ELSE
		-- Otherwise AND the inversion of the delayed pulse chosen by 32 - the switch value
		-- 32 - switch value is used simply for convenience, in order to select delays in 
		-- a decreasing order, if only switch value is used then lower switch values would
		-- select larger delays
		pulseout <= delayedpulse(0) AND NOT delayedpulse(32 - to_integer(unsigned(SW)));
	END IF;	
		
	END PROCESS;
END Behavior;
