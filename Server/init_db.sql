-- ==========================================
-- Database Initialization Script
-- Generated at: 2025-12-22 17:54:23.463367
-- ==========================================

-- 1. Select Database and Cleanup Tables
USE designer_db;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS check_in_config;
DROP TABLE IF EXISTS check_in_records;
DROP TABLE IF EXISTS features_config;
DROP TABLE IF EXISTS plugin_groups;
DROP TABLE IF EXISTS points_history;
DROP TABLE IF EXISTS vip_config;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS user_sessions;
SET FOREIGN_KEY_CHECKS = 1;

-- 2. Create Tables
CREATE TABLE check_in_config (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	consecutive_days INTEGER NOT NULL, 
	base_points INTEGER NOT NULL, 
	bonus_points INTEGER NOT NULL, 
	total_points INTEGER NOT NULL, 
	enabled BOOL, 
	created_at DATETIME DEFAULT now(), 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (consecutive_days)
);

CREATE TABLE check_in_records (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id INTEGER NOT NULL, 
	username VARCHAR(50) NOT NULL, 
	check_in_date DATE NOT NULL, 
	points_earned INTEGER NOT NULL, 
	consecutive_days INTEGER NOT NULL, 
	vip_multiplier FLOAT, 
	created_at DATETIME DEFAULT now(), 
	PRIMARY KEY (id)
);

CREATE TABLE features_config (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	feature_key VARCHAR(50) NOT NULL, 
	feature_name VARCHAR(100) NOT NULL, 
	category VARCHAR(50), 
	points_cost INTEGER, 
	vip_points_cost INTEGER, 
	svip_points_cost INTEGER, 
	enabled BOOL, 
	description TEXT, 
	created_at DATETIME DEFAULT now(), 
	updated_at DATETIME, 
	PRIMARY KEY (id)
);

CREATE TABLE plugin_groups (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	name VARCHAR(64) NOT NULL, 
	current_version_file VARCHAR(255), 
	comment TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE points_history (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id INTEGER NOT NULL, 
	username VARCHAR(50) NOT NULL, 
	type VARCHAR(20) NOT NULL, 
	amount INTEGER NOT NULL, 
	balance INTEGER NOT NULL, 
	description VARCHAR(255), 
	created_at DATETIME DEFAULT now(), 
	PRIMARY KEY (id)
);

CREATE TABLE vip_config (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	vip_type VARCHAR(20) NOT NULL, 
	name VARCHAR(50) NOT NULL, 
	price FLOAT NOT NULL, 
	daily_quota INTEGER NOT NULL, 
	points_multiplier FLOAT, 
	enabled BOOL, 
	description TEXT, 
	created_at DATETIME DEFAULT now(), 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (vip_type)
);

CREATE TABLE users (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	username VARCHAR(64) NOT NULL, 
	hashed_password VARCHAR(128) NOT NULL, 
	created_at DATETIME NOT NULL DEFAULT now(), 
	group_id INTEGER, 
	permissions TEXT, 
	expire_date DATETIME, 
	email VARCHAR(255), 
	is_verified BOOL, 
	verification_code VARCHAR(6), 
	reset_token VARCHAR(128), 
	reset_token_expire DATETIME, 
	nickname VARCHAR(50), 
	avatar VARCHAR(500), 
	points INTEGER, 
	level INTEGER, 
	vip_type VARCHAR(20), 
	vip_expire DATETIME, 
	vip_daily_quota INTEGER, 
	vip_quota_reset_date DATE, 
	total_check_in_days INTEGER, 
	consecutive_check_in INTEGER, 
	last_check_in_date DATE, 
	PRIMARY KEY (id), 
	FOREIGN KEY(group_id) REFERENCES plugin_groups (id)
);

CREATE TABLE user_sessions (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id INTEGER NOT NULL, 
	device_id VARCHAR(128) NOT NULL, 
	active BOOL NOT NULL, 
	expires_at DATETIME, 
	created_at DATETIME NOT NULL DEFAULT now(), 
	login_at DATETIME, 
	logout_at DATETIME, 
	duration_seconds INTEGER, 
	last_seen_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

-- 3. Insert Initial Data
-- Default User Group
INSERT INTO plugin_groups (name, comment) VALUES ('default', 'Default User Group');
-- VIP Config
INSERT INTO vip_config (vip_type, name, price, daily_quota, points_multiplier) VALUES ('vip', 'VIP会员', 30.0, 20, 1.5);
INSERT INTO vip_config (vip_type, name, price, daily_quota, points_multiplier) VALUES ('svip', 'SVIP会员', 88.0, -1, 2.0);
-- Check-in Config
INSERT INTO checkin_config (consecutive_days, base_points, bonus_points, total_points) VALUES (1, 10, 0, 10);
INSERT INTO checkin_config (consecutive_days, base_points, bonus_points, total_points) VALUES (3, 10, 5, 15);
INSERT INTO checkin_config (consecutive_days, base_points, bonus_points, total_points) VALUES (7, 10, 20, 30);
-- Feature Config
INSERT INTO feature_configs (feature_key, feature_name, points_cost, category) VALUES ('ai_remove_bg', '智能抠图', 10, 'ai');
-- 4. Create Admin User (admin / password123)

INSERT INTO users (
    username, hashed_password, email, is_verified, permissions, 
    group_id, nickname, level, vip_type, vip_expire, 
    created_at, points, total_check_in_days, consecutive_check_in, vip_daily_quota
) VALUES (
    'admin', 
    '$2b$12$UsFjs3Jwn5BG7u/RJ1efNuTF4zIsjT.pSm1mQEBXGWKR.3Kakhpmq', 
    'admin@example.com', 
    1, 
    'admin,vip,svip', 
    (SELECT id FROM plugin_groups WHERE name = 'default' LIMIT 1), 
    'Administrator', 
    999, 
    'svip', 
    '2099-12-31 23:59:59', 
    NOW(), 
    0, 0, 0, 0
);
