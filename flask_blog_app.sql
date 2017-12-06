CREATE DATABASE FlaskBlogApp;

CREATE TABLE `FlaskBlogApp`.`blog_user` (
  `user_id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(45) NULL,
  `user_username` VARCHAR(45) NULL,
  `user_password` VARCHAR(255) NULL,
  PRIMARY KEY (`user_id`));

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(45),
    IN p_username VARCHAR(45),
    IN p_password VARCHAR(255)
)
BEGIN
    IF ( select exists (select 1 from blog_user where user_username = p_username) ) THEN

        select 'Username Exists !!';

    ELSE

        insert into blog_user
        (
            user_name,
            user_username,
            user_password
        )
        values
        (
            p_name,
            p_username,
            p_password
        );

    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(
    -> IN p_username VARCHAR(20)
    -> )
    -> BEGIN
    ->     select * from blog_user where user_username = p_username;
    -> END$$
DELIMITER ;

CREATE TABLE `tbl_blog` (
  `blog_id` int(11) NOT NULL AUTO_INCREMENT,
  `blog_title` varchar(45) DEFAULT NULL,
  `blog_description` varchar(5000) DEFAULT NULL,
  `blog_user_id` int(11) DEFAULT NULL,
  `blog_date` datetime DEFAULT NULL,
  PRIMARY KEY (`blog_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;