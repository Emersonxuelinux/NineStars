/*
Navicat MySQL Data Transfer

Source Server         : NineStars
Source Server Version : 50527
Source Host           : localhost:3306
Source Database       : NineStars

Target Server Type    : MYSQL
Target Server Version : 50527
File Encoding         : 65001

Date: 2014-06-26 11:55:07
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for Project_List
-- ----------------------------
DROP TABLE IF EXISTS `Project_List`;
CREATE TABLE `Project_List` (
  `projectTag` varchar(255) NOT NULL,
  `sn` int(3) NOT NULL,
  `workDir` varchar(255) NOT NULL,
  `saltId` varchar(255) NOT NULL,
  `ip` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of Project_List
-- ----------------------------
INSERT INTO `Project_List` VALUES ('android', '1', '/data/makepack', 'dban-1', '192.168.1.x.x');
