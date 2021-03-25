-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- 主機： localhost:3306
-- 產生時間： 2021 年 03 月 25 日 10:02
-- 伺服器版本： 8.0.23-0ubuntu0.20.04.1
-- PHP 版本： 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `IIT`
--

-- --------------------------------------------------------

--
-- 資料表結構 `Photos`
--

CREATE TABLE `Photos` (
  `ID` int NOT NULL,
  `PIC_1` text NOT NULL,
  `PIC_2` text NOT NULL,
  `Email` text NOT NULL,
  `UUID` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- 傾印資料表的資料 `Photos`
--

INSERT INTO `Photos` (`ID`, `PIC_1`, `PIC_2`, `Email`, `UUID`) VALUES
(8, '37cd592c-952f-47a1-8ab9-32bb5a3959b8.jpg', '276fe69d-4595-4fe9-ad01-f5fbc4d18b04.jpg', 'jefflin.je598@gmail.com', 'ffc99e23-dcea-447c-89ab-7277a196ef6b');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `Photos`
--
ALTER TABLE `Photos`
  ADD PRIMARY KEY (`ID`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `Photos`
--
ALTER TABLE `Photos`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
