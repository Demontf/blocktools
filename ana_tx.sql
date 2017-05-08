/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50624
 Source Host           : localhost
 Source Database       : ana_tx

 Target Server Type    : MySQL
 Target Server Version : 50624
 File Encoding         : utf-8

 Date: 05/08/2017 21:46:43 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `edges`
-- ----------------------------
DROP TABLE IF EXISTS `edges`;
CREATE TABLE `edges` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tx_id` int(11) DEFAULT NULL,
  `pk_id` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL COMMENT '1 in 2 out',
  `value` double DEFAULT NULL,
  `idx` int(11) DEFAULT NULL COMMENT 'only for type = 2',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `pk`
-- ----------------------------
DROP TABLE IF EXISTS `pk`;
CREATE TABLE `pk` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pk` varchar(1000) DEFAULT NULL,
  `pk_hash_160` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `tx`
-- ----------------------------
DROP TABLE IF EXISTS `tx`;
CREATE TABLE `tx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tx_hash` varchar(255) DEFAULT NULL,
  `vin` int(11) DEFAULT NULL,
  `vout` varchar(255) DEFAULT NULL,
  `times` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=686 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
