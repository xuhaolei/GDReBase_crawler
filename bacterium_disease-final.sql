/*
Navicat MySQL Data Transfer

Source Server         : 本机服务器
Source Server Version : 80017
Source Host           : localhost:3306
Source Database       : bacterium_disease

Target Server Type    : MYSQL
Target Server Version : 80017
File Encoding         : 65001

Date: 2021-01-27 23:46:08
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `tb_bacterium`
-- ----------------------------
DROP TABLE IF EXISTS `tb_bacterium`;
CREATE TABLE `tb_bacterium` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `nickname` varchar(255) DEFAULT NULL,
  `kingdom` int(11) DEFAULT NULL,
  `phylum` int(11) DEFAULT NULL,
  `class_` int(11) DEFAULT NULL,
  `order` int(11) DEFAULT NULL,
  `family` int(11) DEFAULT NULL,
  `genus` int(11) DEFAULT NULL,
  `species` int(11) DEFAULT NULL,
  `remark` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='这个表是菌表，表示界门纲目科属种，这个界门纲目科属种的数据交给我吧\r\n另外，群落结构 ph值也可以看做是一个菌，因为某一个疾病的发生可能不是和某几种菌相联系而是和比如，ph值，比如群落结构多样性有关。\r\n（上次和老师讨论的时候老师讲的）';

-- ----------------------------
-- Records of tb_bacterium
-- ----------------------------

-- ----------------------------
-- Table structure for `tb_bacteriums`
-- ----------------------------
DROP TABLE IF EXISTS `tb_bacteriums`;
CREATE TABLE `tb_bacteriums` (
  `bacteriums_id` int(11) NOT NULL,
  `bacterium_id` int(11) NOT NULL,
  `remark` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`bacteriums_id`,`bacterium_id`),
  KEY `id3` (`bacterium_id`),
  KEY `bacteriums_id` (`bacteriums_id`),
  CONSTRAINT `id3` FOREIGN KEY (`bacterium_id`) REFERENCES `tb_bacterium` (`id`),
  CONSTRAINT `id4` FOREIGN KEY (`bacteriums_id`) REFERENCES `tb_entity` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='这个表示菌群表\r\nbacteriums_id为菌群id\r\nbacterium_id是外键（引用了db_bacterium表中的id)\r\nremark为备注信息（可以为空）';

-- ----------------------------
-- Records of tb_bacteriums
-- ----------------------------

-- ----------------------------
-- Table structure for `tb_disease`
-- ----------------------------
DROP TABLE IF EXISTS `tb_disease`;
CREATE TABLE `tb_disease` (
  `id` int(11) NOT NULL,
  `type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='疾病表\r\nid为疾病id唯一标识';

-- ----------------------------
-- Records of tb_disease
-- ----------------------------

-- ----------------------------
-- Table structure for `tb_entity`
-- ----------------------------
DROP TABLE IF EXISTS `tb_entity`;
CREATE TABLE `tb_entity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `id_inner` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='实体表\r\nid为唯一标识的id\r\nname:名字\r\ngroup:哪个类别：疾病、表型等\r\nid_inner:内部id，就比如group为疾病，该字段对应疾病表内部id';

-- ----------------------------
-- Records of tb_entity
-- ----------------------------

-- ----------------------------
-- Table structure for `tb_paper`
-- ----------------------------
DROP TABLE IF EXISTS `tb_paper`;
CREATE TABLE `tb_paper` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` text,
  `authors` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `date` date DEFAULT NULL,
  `institution` varchar(255) DEFAULT NULL,
  `keywords` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `abstract` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `url` varchar(255) DEFAULT NULL,
  `filename` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `valid` tinyint(2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='这个表示论文表，有论文id（作为relation表的外键）\r\n除了论文名和论文id其他的都可以设置为空（NULL）\r\nname:论文名\r\nauthot:论文作者\r\ninstitution:发表机构（哪个期刊）\r\ntime:发表时间，精确到某一年吧\r\n例：该字段写 2018\r\n';

-- ----------------------------
-- Records of tb_paper
-- ----------------------------

-- ----------------------------
-- Table structure for `tb_relation`
-- ----------------------------
DROP TABLE IF EXISTS `tb_relation`;
CREATE TABLE `tb_relation` (
  `relation_id` int(11) NOT NULL AUTO_INCREMENT,
  `entity1_id` int(11) NOT NULL,
  `entity2_id` int(11) NOT NULL,
  `direction` varchar(255) DEFAULT NULL,
  `more_or_less1` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `more_or_less2` varchar(255) DEFAULT NULL,
  `source` int(11) DEFAULT NULL,
  `sample` int(11) DEFAULT NULL,
  `remark` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`relation_id`),
  KEY `bacterium_id0` (`entity1_id`),
  KEY `disease_id0` (`entity2_id`),
  KEY `source_id0` (`source`),
  KEY `sample_id0` (`sample`),
  CONSTRAINT `bacterium_id0` FOREIGN KEY (`entity1_id`) REFERENCES `tb_entity` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `disease_id0` FOREIGN KEY (`entity2_id`) REFERENCES `tb_entity` (`id`),
  CONSTRAINT `sample_id0` FOREIGN KEY (`sample`) REFERENCES `tb_sample` (`id`),
  CONSTRAINT `source_id0` FOREIGN KEY (`source`) REFERENCES `tb_paper` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='疾病-细菌 关系表\r\nrelation_id为唯一标识的，是int数字类型\r\nentity1_id为实体1id 外键 对应entity表\r\nentity2_id为实体2id 外键 对应entity表\r\ndirection为方向(word表里面 关联-方向)\r\n若为 不详:这个字段写0\r\n       1->2:这个字段写1\r\n       2->1:这个字段写2\r\n       1<->2:这个字段写3\r\nmore_or_less1为实体1增减性\r\nmore_or_less2为实体2增减性\r\nsource为来源（word表里面来源）\r\n论文id 外键\r\nsample为外键\r\n对应sample表中sample_id\r\nremark不是对应word表里的备注，可以不写保留空值';

-- ----------------------------
-- Records of tb_relation
-- ----------------------------

-- ----------------------------
-- Table structure for `tb_sample`
-- ----------------------------
DROP TABLE IF EXISTS `tb_sample`;
CREATE TABLE `tb_sample` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sample` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  `remark` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='数据样本表，我看一种疾病可能含有多个样本建立这样一个表。\r\nsample_id为主键 为唯一标识的\r\ndisease_id为疾病id是外键\r\nsample为样本对应word表里面的 样本\r\nremark对应word表的备注';

-- ----------------------------
-- Records of tb_sample
-- ----------------------------
