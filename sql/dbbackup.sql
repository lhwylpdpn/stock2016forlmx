/*
SQLyog Ultimate v11.24 (32 bit)
MySQL - 5.6.21-log : Database - stock_foreign
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`stock_foreign` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `stock_foreign`;

/*Table structure for table `model_config` */

DROP TABLE IF EXISTS `model_config`;

CREATE TABLE `model_config` (
  `stockid` varchar(45) DEFAULT NULL,
  `flag` int(100) DEFAULT NULL,
  `open_status` int(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `order` */

DROP TABLE IF EXISTS `order`;

CREATE TABLE `order` (
  `orderid` varchar(45) DEFAULT NULL,
  `stockid` varchar(45) DEFAULT NULL,
  `order_time_send` datetime DEFAULT NULL,
  `price_open` float DEFAULT NULL,
  `price_close_except` float DEFAULT NULL,
  `norm_open` float DEFAULT NULL,
  `norm_cha_open` float DEFAULT NULL,
  `bucang` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `order_back` */

DROP TABLE IF EXISTS `order_back`;

CREATE TABLE `order_back` (
  `orderid` varchar(45) DEFAULT NULL,
  `order_stockA` varchar(45) DEFAULT NULL,
  `order_stockB` varchar(45) DEFAULT NULL,
  `order_time_send` datetime DEFAULT NULL,
  `ln_open` float DEFAULT NULL,
  `ln_close` float DEFAULT NULL,
  `norm_open` float DEFAULT NULL,
  `releation` float DEFAULT NULL,
  `avgA_B` float DEFAULT NULL,
  `stdA_B` float DEFAULT NULL,
  KEY `orderid` (`orderid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `order_result` */

DROP TABLE IF EXISTS `order_result`;

CREATE TABLE `order_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nameA` varchar(50) DEFAULT NULL,
  `openA` varchar(50) DEFAULT NULL,
  `openA_time` varchar(50) DEFAULT NULL,
  `closeA` varchar(50) DEFAULT NULL,
  `closeA_time` varchar(50) DEFAULT NULL,
  `lots_A` varchar(50) DEFAULT NULL,
  `nameB` varchar(50) DEFAULT NULL,
  `openB` varchar(50) DEFAULT NULL,
  `openB_time` varchar(50) DEFAULT NULL,
  `closeB` varchar(50) DEFAULT NULL,
  `closeB_time` varchar(50) DEFAULT NULL,
  `lots_B` varchar(50) DEFAULT NULL,
  `order_type` varchar(50) DEFAULT NULL,
  `orderid` varchar(50) DEFAULT NULL,
  `ln_e_open` varchar(50) DEFAULT NULL,
  `ln_e_close` varchar(50) DEFAULT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1167 DEFAULT CHARSET=utf8;

/*Table structure for table `releation_mid` */

DROP TABLE IF EXISTS `releation_mid`;

CREATE TABLE `releation_mid` (
  `stockid` varchar(45) DEFAULT NULL,
  `sample` varchar(45) DEFAULT NULL,
  `close_now` float DEFAULT NULL,
  `avgA_B` float DEFAULT NULL,
  `stdA_B` float DEFAULT NULL,
  `norm_ln_prev` varchar(45) DEFAULT NULL,
  `norm_ln_prev2` varchar(45) DEFAULT NULL,
  `avg_cha` float DEFAULT NULL,
  `std_cha` float DEFAULT NULL,
  `norm_cha_prev` varchar(45) DEFAULT NULL,
  `norm_cha_prev2` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `releation_mid_prev` */

DROP TABLE IF EXISTS `releation_mid_prev`;

CREATE TABLE `releation_mid_prev` (
  `stockidA` varchar(45) DEFAULT NULL,
  `stockidB` varchar(45) DEFAULT NULL,
  `sample` varchar(45) DEFAULT NULL,
  `releation` varchar(45) DEFAULT NULL,
  `lnA_B` float DEFAULT NULL,
  `avgA_B` float DEFAULT NULL,
  `stdA_B` float DEFAULT NULL,
  `norm_ln_prev` varchar(45) DEFAULT NULL,
  `norm_ln_prev2` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `releation_mid_record` */

DROP TABLE IF EXISTS `releation_mid_record`;

CREATE TABLE `releation_mid_record` (
  `time_` varchar(34) DEFAULT NULL,
  `stockid` varchar(45) DEFAULT NULL,
  `sample` varchar(45) DEFAULT NULL,
  `close_now` float DEFAULT NULL,
  `avgA_B` float DEFAULT NULL,
  `stdA_B` float DEFAULT NULL,
  `norm_ln_prev` varchar(45) DEFAULT NULL,
  `norm_ln_prev2` varchar(45) DEFAULT NULL,
  `avg_cha` float DEFAULT NULL,
  `std_cha` float DEFAULT NULL,
  `norm_cha_prev` varchar(45) DEFAULT NULL,
  `norm_cha_prev2` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `releation_mid_test` */

DROP TABLE IF EXISTS `releation_mid_test`;

CREATE TABLE `releation_mid_test` (
  `stockidA` varchar(45) DEFAULT NULL,
  `stockidB` varchar(45) DEFAULT NULL,
  `sample` varchar(45) DEFAULT NULL,
  `releation` varchar(45) DEFAULT NULL,
  `lnA_B` float DEFAULT NULL,
  `avgA_B` float DEFAULT NULL,
  `stdA_B` float DEFAULT NULL,
  `norm_ln_prev` varchar(45) DEFAULT NULL,
  `norm_ln_prev2` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `stock` */

DROP TABLE IF EXISTS `stock`;

CREATE TABLE `stock` (
  `stockid` varchar(100) DEFAULT NULL,
  `date` varchar(45) DEFAULT NULL,
  `time` varchar(45) DEFAULT NULL,
  `open_` float DEFAULT NULL,
  `high` float DEFAULT NULL,
  `low` float DEFAULT NULL,
  `close` float DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `per` varchar(50) DEFAULT NULL,
  `tag` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `stock_back` */

DROP TABLE IF EXISTS `stock_back`;

CREATE TABLE `stock_back` (
  `stockid` varchar(100) DEFAULT NULL,
  `date` varchar(45) DEFAULT NULL,
  `time` varchar(45) DEFAULT NULL,
  `open_` float DEFAULT NULL,
  `high` float DEFAULT NULL,
  `low` float DEFAULT NULL,
  `close` float DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `per` varchar(50) DEFAULT NULL,
  `tag` int(11) DEFAULT NULL,
  KEY `stockid` (`stockid`,`date`,`time`),
  KEY `stockid_2` (`stockid`),
  KEY `date` (`date`,`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
