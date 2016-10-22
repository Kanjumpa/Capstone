-- The coincidence determinator
-- modified by Jeff Nicholls
LIBRARY ieee;
USE ieee.std_logic_1164.all;

ENTITY coincidence_pulse IS
	PORT
	(
		a, b, c, d	:IN 	STD_LOGIC;
		y			:OUT 	STD_LOGIC
	);
END coincidence_pulse;

ARCHITECTURE circuit OF coincidence_pulse IS
BEGIN
-- A coincidence is determined by ANDing together all of the relevant pulses.
-- If for example, you only want to find the coincidence between A and B
-- then supply a constant high signal to C and D, to mimick a definite coincidence
-- for C and D.  Then your coincidence is only dependent on the AND between A and B.
	y <= (a and c) and (b and d);
END circuit;