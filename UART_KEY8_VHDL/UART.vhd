-- UART that transmits binary encoded in SW[7:0] when KEY0 is pressed
-- baudrate: 9600
--
-- Based on the youtube video https://www.youtube.com/watch?v=fMmcSpgOtJ4
-- 
-- Author: Qianshu Lu
-- Date: Oct. 12, 2016


library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

ENTITY UART IS
PORT(
	CLOCK_50: 		IN STD_LOGIC;
	SW: 				IN STD_LOGIC_VECTOR(17 downto 0);
	KEY: 				IN STD_LOGIC_VECTOR(3 downto 0);
	LEDR: 			OUT STD_LOGIC_VECTOR(17 downto 0);
	LEDG:				OUT STD_LOGIC_VECTOR(7 downto 0);
	UART_TXD:		OUT STD_LOGIC;
	UART_RXD:		IN STD_LOGIC
);
END UART;

ARCHITECTURE MAIN OF UART IS
SIGNAL TX_DATA: STD_LOGIC_VECTOR(7 downto 0);
SIGNAL TX_START: STD_LOGIC:='0';
SIGNAL TX_BUSY: STD_LOGIC;

COMPONENT TX
PORT(
	CLK: 	IN STD_LOGIC;
	START:		IN STD_LOGIC;
	BUSY:			OUT STD_LOGIC;
	DATA:			IN STD_LOGIC_VECTOR(7 downto 0);
	TX_LINE:		OUT STD_LOGIC
);
END COMPONENT TX;

BEGIN
C1: TX PORT MAP(CLOCK_50, TX_START, TX_BUSY, TX_DATA, UART_TXD);

PROCESS(CLOCK_50)
BEGIN
IF(CLOCK_50'EVENT AND CLOCK_50='1')THEN
	IF(KEY(0)='0' AND TX_BUSY='0')THEN
		TX_DATA<=SW(7 downto 0);
		TX_START<='1';
		LEDG<=TX_DATA;
	ELSE
		TX_START<='0';
	END IF;
END IF;

END PROCESS;
END MAIN;

