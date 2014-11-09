CREATE TABLE `books` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `booknum` int(11) NOT NULL DEFAULT '0',
  `title` varchar(255) DEFAULT NULL,
  `author` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;