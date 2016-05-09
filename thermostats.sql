-- phpMyAdmin SQL Dump
-- version 4.2.12deb2+deb8u1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 08, 2016 at 10:27 PM
-- Server version: 5.5.44-0+deb8u1
-- PHP Version: 5.6.20-0+deb8u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `thermostats`
--

-- --------------------------------------------------------

--
-- Table structure for table `Thermostats`
--

CREATE TABLE IF NOT EXISTS `Thermostats` (
  `Id` int(11) NOT NULL,
  `Location` text NOT NULL,
  `Fan_Pin` int(11) NOT NULL,
  `Compressor_Pin` int(11) NOT NULL,
  `Temp_Target` int(11) NOT NULL,
  `Temp_Actual` int(11) NOT NULL,
  `Fan_Status` tinyint(1) NOT NULL,
  `Compressor_Status` tinyint(1) NOT NULL,
  `Enabled` tinyint(1) NOT NULL,
  `Fan_Time` int(11) NOT NULL,
  `Compressor_Time` int(11) NOT NULL,
  `Fan_Change_Recent` int(11) NOT NULL,
  `Compressor_Change_Recent` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Thermostats`
--

INSERT INTO `Thermostats` (`Id`, `Location`, `Fan_Pin`, `Compressor_Pin`, `Temp_Target`, `Temp_Actual`, `Fan_Status`, `Compressor_Status`, `Enabled`, `Fan_Time`, `Compressor_Time`, `Fan_Change_Recent`, `Compressor_Change_Recent`) VALUES
(0, 'on building', 12, 16, 80, 76, 0, 0, 1, 0, 0, 0, 0),
(1, 'by panel', 20, 21, 85, 76, 0, 0, 1, 0, 0, 0, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Thermostats`
--
ALTER TABLE `Thermostats`
 ADD UNIQUE KEY `Id` (`Id`), ADD KEY `Unit` (`Id`,`Fan_Pin`,`Compressor_Pin`,`Temp_Target`,`Fan_Status`,`Compressor_Status`,`Enabled`,`Fan_Time`,`Compressor_Time`,`Fan_Change_Recent`,`Compressor_Change_Recent`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
