/*
--------------------------------------------------------
-- MemberShip Table Schema 2015-03-09
--------------------------------------------------------
*/

CREATE DATABASE IF NOT EXISTS ms;

USE ms;

/*
--------------------------------------------------------
--  DDL for Table ms_app
--------------------------------------------------------
*/

	DROP TABLE IF EXISTS `ms_app`;

	CREATE TABLE `ms_app`
	(
		`app_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		`app_key` VARCHAR(64) NOT NULL,
		`app_secret` VARCHAR(256) NOT NULL,
		`app_name` VARCHAR(256) NOT NULL,
		`support_android` TINYINT UNSIGNED DEFAULT 0,
		`support_ios` TINYINT UNSIGNED DEFAULT 0,
		`support_playstore` TINYINT UNSIGNED DEFAULT 0,
		`support_appstore` TINYINT UNSIGNED DEFAULT 0,
		`support_gameflier` TINYINT UNSIGNED DEFAULT 0,
		`playstore_url` VARCHAR(128),
		`appstore_url` VARCHAR(128),
		`gameflier_url` VARCHAR(128),
		`gcm_sender_id` VARCHAR(128),
		`gcm_server_api_key` VARCHAR(256),
		`gcm_config_path` VARCHAR(128),
		`facebook_app_id` VARCHAR(128),
		`facebook_app_name` VARCHAR(128),
		`facebook_app_secret` VARCHAR(128),
		`facebook_api_version` VARCHAR(16),
		`status` TINYINT UNSIGNED DEFAULT 0,
		`reg_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY(`app_id`),
		INDEX (`status`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*
--------------------------------------------------------
--  DDL for Table ms_app_product
--------------------------------------------------------
*/

	DROP TABLE IF EXISTS `ms_app_product`;

	CREATE TABLE `ms_app_product`
	(
		`app_id` BIGINT UNSIGNED NOT NULL,
		`product_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		`product_name` VARCHAR(128) NOT NULL,
		`product_detail` VARCHAR(256),
		`product_price` VARCHAR(64) NOT NULL,
		`inapp_id` VARCHAR(128) NOT NULL,
		`service_platform` TINYINT UNSIGNED DEFAULT 0,
		`currency` TINYINT UNSIGNED NOT NULL,
		`status` TINYINT UNSIGNED DEFAULT 0,
		`reg_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY(`product_id`),
		INDEX (`app_id`, `inapp_id`, `status`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8;

	
/*
--------------------------------------------------------
--  DDL for Table ms_app_payment
--------------------------------------------------------
*/

	DROP TABLE IF EXISTS `ms_app_payment`;

	CREATE TABLE `ms_app_payment`
	(
		`app_id` BIGINT UNSIGNED NOT NULL,
		`member_id` BIGINT UNSIGNED NOT NULL,
		`product_id` BIGINT UNSIGNED NOT NULL,
		`payment_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		`service_platform` TINYINT UNSIGNED DEFAULT 0,
		`product_price` VARCHAR(64) NOT NULL,
		`inapp_order_id` VARCHAR(128) NOT NULL,
		`inapp_package_name` VARCHAR(64) NOT NULL,
		`inapp_product_sku` VARCHAR(64)	NOT NULL,
		`inapp_purchase_time` INT UNSIGNED NOT NULL,
		`inapp_purchase_state` TINYINT UNSIGNED NOT NULL,
		`inapp_purchase_token` VARCHAR(512) NOT NULL,
		`inapp_developer_payload` VARCHAR(256) NOT NULL,
		`inapp_signature` VARCHAR(512) NOT NULL,
		`inapp_appstore_name` VARCHAR(64) NOT NULL,
		`inapp_receipt` VARCHAR(512) NOT NULL,
		`status` TINYINT UNSIGNED DEFAULT 0,
		`reg_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY(`payment_id`),
		INDEX (`app_id`, `member_id`, `product_id`, `service_platform`, `inapp_order_id`, `status`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*
--------------------------------------------------------
--  DDL for Table ms_member
--------------------------------------------------------
*/

	DROP TABLE IF EXISTS `ms_member`;

	CREATE TABLE `ms_member`
	(
		`app_id` BIGINT UNSIGNED NOT NULL,
		`member_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		`udid` VARCHAR(128) NOT NULL,
		`device_platform` TINYINT UNSIGNED DEFAULT 0,
		`service_platform` TINYINT UNSIGNED DEFAULT 0,
		`push_notification` TINYINT UNSIGNED DEFAULT 0,
		`gcm_token` VARCHAR(512),
		`facebook_id` BIGINT UNSIGNED,
		`facebook_email` VARCHAR(128),
		`status` TINYINT UNSIGNED DEFAULT 0,
		`reg_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		`last_device_platform` TINYINT UNSIGNED DEFAULT 0,
		`last_service_platform` TINYINT UNSIGNED DEFAULT 0,
		`last_login_date` TIMESTAMP,
		PRIMARY KEY(`member_id`, `udid`),
		INDEX (`app_id`, `facebook_id`, `udid`, `device_platform`, `service_platform`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*
--------------------------------------------------------
--  DDL for Table ms_member_history
--------------------------------------------------------
*/

	DROP TABLE IF EXISTS `ms_member_history`;

	CREATE TABLE `ms_member_history`
	(
		`app_id` BIGINT UNSIGNED NOT NULL,
		`member_id` BIGINT UNSIGNED NOT NULL,
		`category` TINYINT UNSIGNED,
		`int0` BIGINT UNSIGNED,
		`int1` BIGINT UNSIGNED,
		`int2` BIGINT UNSIGNED,
		`int3` BIGINT UNSIGNED,
		`int4` BIGINT UNSIGNED,
		`str0` VARCHAR(128),
		`reg_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		INDEX (`app_id`, `member_id`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*
--------------------------------------------------------
--  DDL for Table ms_admin
--------------------------------------------------------
*/

	DROP TABLE IF EXISTS `ms_admin`;

	CREATE TABLE `ms_admin`
	(
		`admin_id` VARCHAR(64) NOT NULL,
		`password` VARCHAR(128) NOT NULL,
		`access_apps` VARCHAR(128) DEFAULT '',
		`reg_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY(`admin_id`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8;

  -- Admin password
	INSERT INTO ms_admin (admin_id, password) VALUES ('admin', PASSWORD('xlam3red!'));
	INSERT INTO ms_admin (admin_id, password) VALUES ('operator', PASSWORD('1234'));
