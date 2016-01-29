/*
--------------------------------------------------------
--  MemberShip Stored Procedure for MySQL
--------------------------------------------------------
*/

CREATE DATABASE IF NOT EXISTS ms;

USE ms;


DELIMITER ;;

/*
--------------------------------------------------------
-- create_app
--------------------------------------------------------
*/

DROP PROCEDURE IF EXISTS create_app;;

CREATE PROCEDURE create_app (
   IN p_app_key VARCHAR(64)
 , IN p_app_secret VARCHAR(256)
 , IN p_app_name VARCHAR(256)
 , IN p_support_android TINYINT UNSIGNED
 , IN p_support_ios TINYINT UNSIGNED
 , IN p_support_playstore TINYINT UNSIGNED
 , IN p_support_appstore TINYINT UNSIGNED
 , IN p_support_gameflier TINYINT UNSIGNED
 , IN p_playstore_url VARCHAR(128)
 , IN p_appstore_url VARCHAR(128)
 , IN p_gameflier_url VARCHAR(128)
 , IN p_gcm_sender_id VARCHAR(128)
 , IN p_gcm_server_api_key VARCHAR(256)
 , IN p_gcm_config_path VARCHAR(128)
 , IN p_facebook_app_id VARCHAR(128)
 , IN p_facebook_app_name VARCHAR(128)
 , IN p_facebook_app_secret VARCHAR(128)
 , IN p_facebook_api_version VARCHAR(16)
 , IN p_status TINYINT UNSIGNED
)
BEGIN

	-- OUTPUT
	DECLARE o_app_id BIGINT UNSIGNED;

	INSERT INTO ms_app (
			app_key
		, app_secret
		, app_name
		, support_android
		, support_ios
		, support_playstore
		, support_appstore
		, support_gameflier
		, playstore_url
		, appstore_url
		, gameflier_url
		, gcm_sender_id
		, gcm_server_api_key
		, gcm_config_path
		, facebook_app_id
		, facebook_app_name
		, facebook_app_secret
		, facebook_api_version
		, status
	) VALUES (
			p_app_key
		, p_app_secret
		, p_app_name
		, p_support_android
		, p_support_ios
		, p_support_playstore
		, p_support_appstore
		, p_support_gameflier
		, p_playstore_url
		, p_appstore_url
		, p_gameflier_url
		, p_gcm_sender_id
		, p_gcm_server_api_key
		, p_gcm_config_path
		, p_facebook_app_id
		, p_facebook_app_name
		, p_facebook_app_secret
		, p_facebook_api_version
		, p_status
	);

	SELECT LAST_INSERT_ID();

END ;;


/*
--------------------------------------------------------
-- update_app
--------------------------------------------------------
*/

DROP PROCEDURE IF EXISTS update_app ;;

CREATE PROCEDURE update_app (
	 IN p_app_id BIGINT UNSIGNED
 , IN p_app_name VARCHAR(256)
 , IN p_support_android TINYINT UNSIGNED
 , IN p_support_ios TINYINT UNSIGNED
 , IN p_support_playstore TINYINT UNSIGNED
 , IN p_support_appstore TINYINT UNSIGNED
 , IN p_support_gameflier TINYINT UNSIGNED
 , IN p_playstore_url VARCHAR(128)
 , IN p_appstore_url VARCHAR(128)
 , IN p_gameflier_url VARCHAR(128)
 , IN p_gcm_sender_id VARCHAR(128)
 , IN p_gcm_server_api_key VARCHAR(256)
 , IN p_gcm_config_path VARCHAR(128)
 , IN p_facebook_app_id VARCHAR(128)
 , IN p_facebook_app_name VARCHAR(128)
 , IN p_facebook_app_secret VARCHAR(128)
 , IN p_facebook_api_version VARCHAR(16)
 , IN p_status TINYINT UNSIGNED
)
BEGIN

	UPDATE ms_app SET
			app_name = p_app_name
		, support_android = p_support_android
		, support_ios = p_support_ios
		, support_playstore = p_support_playstore
		, support_appstore = p_support_appstore
		, support_gameflier = p_support_gameflier
		, playstore_url = p_playstore_url
		, appstore_url = p_appstore_url
		, gameflier_url = p_gameflier_url
		, gcm_sender_id = p_gcm_sender_id
		, gcm_server_api_key = p_gcm_server_api_key
		, gcm_config_path = p_gcm_config_path
		, facebook_app_id = p_facebook_app_id
		, facebook_app_name = p_facebook_app_name
		, facebook_app_secret = p_facebook_app_secret
		, facebook_api_version = p_facebook_api_version
		, status = p_status
	WHERE app_id = p_app_id;

END ;;


/*
--------------------------------------------------------
--  member_info
--------------------------------------------------------
*/

DROP PROCEDURE IF EXISTS member_info;;

CREATE PROCEDURE member_info (
   IN p_app_id BIGINT UNSIGNED
 , IN p_udid VARCHAR(128)
 , IN p_device_platform TINYINT UNSIGNED
 , IN p_service_platform TINYINT UNSIGNED
 , IN p_gcm_token VARCHAR(512)
 , IN p_facebook_id BIGINT UNSIGNED
 , IN p_facebook_email VARCHAR(128)
 , IN p_status TINYINT UNSIGNED
)
BEGIN

	-- OUTPUT
	DECLARE o_member_id BIGINT UNSIGNED;

	-- UDID에 해당하는 사용자가 존재하는지 확인
	SELECT member_id INTO o_member_id
		FROM ms_member
			WHERE app_id = p_app_id AND udid = p_udid AND status = p_status;

	IF o_member_id > 0 THEN

		-- 페이스북 계정이 다시 생겨서 들어오는 경우는 facebook_id로 매칭되어 있던 계정정보를 사용불가로 변경하거나 조치를 취해야 함
		IF p_facebook_id > 0 THEN

			UPDATE ms_member SET
				status = p_status + 1	-- 사용제한
			WHERE 
				app_id = p_app_id AND 
				member_id != o_member_id AND facebook_id = p_facebook_id;

		END IF;

		-- 기존 UDID정보가 남아있는 사용자
		UPDATE ms_member SET
        gcm_token = p_gcm_token
			, facebook_id = p_facebook_id
			, facebook_email = p_facebook_email
			, last_device_platform = p_device_platform
			, last_service_platform = p_service_platform
			, last_login_date = CURRENT_TIMESTAMP
		WHERE
			app_id = p_app_id AND member_id = o_member_id;

		SELECT o_member_id;

	ELSE

		-- 페이스북 계정이 이미 존재하면?
		IF p_facebook_id > 0 THEN

			SELECT member_id INTO o_member_id
			FROM ms_member
			WHERE 
				app_id = p_app_id AND 
				facebook_id = p_facebook_id AND status = p_status;

		END IF;

		IF o_member_id > 0 THEN

			-- 기존 페이스북 계정 사용자의 UDID를 업데이트
			UPDATE ms_member SET
					udid = p_udid
				, gcm_token = p_gcm_token
				, facebook_email = p_facebook_email
				, last_device_platform = p_device_platform
				, last_service_platform = p_service_platform
				, last_login_date = CURRENT_TIMESTAMP
			WHERE
				app_id = p_app_id AND member_id = o_member_id;

			SELECT o_member_id;

		ELSE

			-- 신규 사용자 생성
			INSERT INTO ms_member (
					app_id
				, udid
				, device_platform
				, service_platform
        , gcm_token
				, facebook_id
				, facebook_email
				, status
				, last_device_platform
				, last_service_platform
				, last_login_date
			) VALUES (
					p_app_id
				, p_udid
				, p_device_platform
				, p_service_platform
        , p_gcm_token
				, p_facebook_id
				, p_facebook_email
				, p_status
				, p_device_platform
				, p_service_platform
				, CURRENT_TIMESTAMP
			);

			SELECT LAST_INSERT_ID();

		END IF;

	END IF;

END ;;


/*
--------------------------------------------------------
-- member_push_notification
--------------------------------------------------------
*/

DROP PROCEDURE IF EXISTS member_push_notification ;;

CREATE PROCEDURE member_push_notification (
   IN p_app_id BIGINT UNSIGNED
 , IN p_member_id BIGINT UNSIGNED
)
BEGIN

	-- OUTPUT
	DECLARE o_push_notification TINYINT UNSIGNED;

	-- 토글된 푸시알림 정보를 얻어옴
	SELECT IF (push_notification=1,0,1) INTO o_push_notification
		FROM ms_member 
	WHERE member_id = p_member_id AND app_id = p_app_id;

	-- 푸시알림을 토글시킴
	UPDATE ms_member SET
		push_notification = o_push_notification
	WHERE
		member_id = p_member_id AND app_id = p_app_id;

	SELECT o_push_notification;

END ;;


/*
--------------------------------------------------------
--  purchase
--------------------------------------------------------
*/

DROP PROCEDURE IF EXISTS purchase ;;

CREATE PROCEDURE purchase (
   IN p_app_id BIGINT UNSIGNED
 , IN p_member_id BIGINT UNSIGNED
 , IN p_product_id BIGINT UNSIGNED
 , IN p_service_platform TINYINT UNSIGNED
 , IN p_product_price VARCHAR(64)
 , IN p_inapp_order_id VARCHAR(128)
 , IN p_inapp_package_name VARCHAR(64)
 , IN p_inapp_product_sku VARCHAR(64)
 , IN p_inapp_purchase_time INT UNSIGNED
 , IN p_inapp_purchase_state TINYINT UNSIGNED
 , IN p_inapp_purchase_token VARCHAR(512)
 , IN p_inapp_developer_payload VARCHAR(256)
 , IN p_inapp_signature VARCHAR(512)
 , IN p_inapp_appstore_name VARCHAR(64)
 , IN p_inapp_receipt VARCHAR(512)
 , IN p_status TINYINT UNSIGNED
)
BEGIN

	INSERT INTO ms_app_payment (
			app_id
		, member_id
		, product_id
		, service_platform
		, product_price
		, inapp_order_id
		, inapp_package_name
		, inapp_product_sku
		, inapp_purchase_time
		, inapp_purchase_state
		, inapp_purchase_token
		, inapp_developer_payload
		, inapp_signature
		, inapp_appstore_name
		, inapp_receipt
		, status
	) VALUES (
			p_app_id
		, p_member_id
		, p_product_id
		, p_service_platform
		, p_product_price
		, p_inapp_order_id
		, p_inapp_package_name
		, p_inapp_product_sku
		, p_inapp_purchase_time
		, p_inapp_purchase_state
		, p_inapp_purchase_token
		, p_inapp_developer_payload
		, p_inapp_signature
		, p_inapp_appstore_name
		, p_inapp_receipt
		, p_status
	);

	SELECT LAST_INSERT_ID();

END ;;


/*
--------------------------------------------------------
--  purchase_effectuate
--------------------------------------------------------
*/

DROP PROCEDURE IF EXISTS purchase_effectuate ;;

CREATE PROCEDURE purchase_effectuate (
   IN p_app_id BIGINT UNSIGNED
 , IN p_member_id BIGINT UNSIGNED
 , IN p_payment_id BIGINT UNSIGNED
 , IN p_order_id VARCHAR(128)
 , IN p_purchase_status TINYINT UNSIGNED
 , IN p_effectuate_status TINYINT UNSIGNED
)
BEGIN

	-- OUTPUT
	DECLARE o_payment_id BIGINT UNSIGNED;

	-- 구매상태인 결제정보가 있는지 확인
	SELECT payment_id INTO o_payment_id
		FROM ms_app_payment
	WHERE
		payment_id = p_payment_id AND 
		app_id = p_app_id AND
		member_id = p_member_id AND 
		status = p_purchase_status AND
		inapp_order_id = p_order_id;

	IF o_payment_id > 0 THEN

		UPDATE ms_app_payment SET
			status = p_effectuate_status
		WHERE
			payment_id = p_payment_id AND 
			app_id = p_app_id AND
			member_id = p_member_id AND
			inapp_order_id = p_order_id;

	END IF;

	SELECT o_payment_id;

END ;;


DELIMITER ;


