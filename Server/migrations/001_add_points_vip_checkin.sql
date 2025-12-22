-- ============================================================
-- DesignerCEP 数据库迁移脚本
-- 版本: 001
-- 功能: 添加积分、VIP、签到系统
-- ============================================================

-- ========== 1. 扩展 users 表 ==========
ALTER TABLE users 
ADD COLUMN nickname VARCHAR(50) DEFAULT NULL COMMENT '昵称',
ADD COLUMN avatar VARCHAR(500) DEFAULT NULL COMMENT '头像URL',
ADD COLUMN points INT DEFAULT 0 COMMENT '积分余额',
ADD COLUMN level INT DEFAULT 1 COMMENT '用户等级',
ADD COLUMN vip_type ENUM('none', 'vip', 'svip') DEFAULT 'none' COMMENT 'VIP类型',
ADD COLUMN vip_expire DATETIME DEFAULT NULL COMMENT 'VIP过期时间',
ADD COLUMN vip_daily_quota INT DEFAULT 0 COMMENT 'VIP每日剩余配额',
ADD COLUMN vip_quota_reset_date DATE DEFAULT NULL COMMENT 'VIP配额重置日期',
ADD COLUMN total_check_in_days INT DEFAULT 0 COMMENT '累计签到天数',
ADD COLUMN consecutive_check_in INT DEFAULT 0 COMMENT '连续签到天数',
ADD COLUMN last_check_in_date DATE DEFAULT NULL COMMENT '最后签到日期';

-- ========== 2. 功能配置表 ==========
CREATE TABLE IF NOT EXISTS features_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    feature_key VARCHAR(50) UNIQUE NOT NULL COMMENT '功能唯一标识',
    feature_name VARCHAR(100) NOT NULL COMMENT '功能显示名称',
    category VARCHAR(50) DEFAULT 'general' COMMENT '功能分类',
    points_cost INT NOT NULL DEFAULT 0 COMMENT '普通用户积分消耗',
    vip_points_cost INT DEFAULT 0 COMMENT 'VIP用户积分消耗',
    svip_points_cost INT DEFAULT 0 COMMENT 'SVIP用户积分消耗',
    enabled TINYINT(1) DEFAULT 1 COMMENT '是否启用',
    description TEXT COMMENT '功能描述',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_feature_key (feature_key),
    INDEX idx_enabled (enabled),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='功能配置表';

-- 初始数据
INSERT INTO features_config (feature_key, feature_name, category, points_cost, vip_points_cost, svip_points_cost, description) VALUES
('ai_color_match', 'AI智能配色', 'ai', 50, 0, 0, '使用AI生成智能配色方案'),
('smart_layer_naming', '智能图层命名', 'layer', 30, 0, 0, '自动为图层生成语义化命名'),
('batch_export', '批量导出图层', 'export', 100, 0, 0, '批量导出多个图层为文件'),
('remove_background', '智能抠图', 'ai', 80, 0, 0, '使用AI自动去除背景'),
('style_transfer', '风格迁移', 'ai', 120, 0, 0, 'AI艺术风格转换');

-- ========== 3. VIP配置表 ==========
CREATE TABLE IF NOT EXISTS vip_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    vip_type ENUM('vip', 'svip') NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL COMMENT '套餐名称',
    price DECIMAL(10,2) NOT NULL COMMENT '价格（元/月）',
    daily_quota INT NOT NULL COMMENT '每日免费配额（-1=无限）',
    points_multiplier DECIMAL(3,2) DEFAULT 1.00 COMMENT '签到积分倍数',
    enabled TINYINT(1) DEFAULT 1,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='VIP配置表';

INSERT INTO vip_config (vip_type, name, price, daily_quota, points_multiplier, description) VALUES
('vip', 'VIP会员', 30.00, 20, 1.50, '每日20次免费使用，签到积分x1.5'),
('svip', 'SVIP会员', 88.00, -1, 2.00, '无限次免费使用，签到积分x2');

-- ========== 4. 签到配置表 ==========
CREATE TABLE IF NOT EXISTS check_in_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    consecutive_days INT NOT NULL UNIQUE COMMENT '连续天数',
    base_points INT NOT NULL COMMENT '基础积分',
    bonus_points INT NOT NULL COMMENT '奖励积分',
    total_points INT NOT NULL COMMENT '总积分',
    enabled TINYINT(1) DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_consecutive_days (consecutive_days)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='签到奖励配置表';

INSERT INTO check_in_config (consecutive_days, base_points, bonus_points, total_points) VALUES
(1, 10, 0, 10),
(3, 10, 5, 15),
(7, 10, 20, 30),
(15, 10, 40, 50),
(30, 10, 90, 100);

-- ========== 5. 签到记录表 ==========
CREATE TABLE IF NOT EXISTS check_in_records (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    username VARCHAR(50) NOT NULL,
    check_in_date DATE NOT NULL,
    points_earned INT NOT NULL COMMENT '获得积分',
    consecutive_days INT NOT NULL COMMENT '连续天数',
    vip_multiplier DECIMAL(3,2) DEFAULT 1.00 COMMENT 'VIP倍数',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_date (username, check_in_date),
    INDEX idx_user_id (user_id),
    INDEX idx_date (check_in_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='签到记录表';

-- ========== 6. 积分历史表 ==========
CREATE TABLE IF NOT EXISTS points_history (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    username VARCHAR(50) NOT NULL,
    type ENUM('checkin', 'consume', 'reward', 'refund', 'admin') NOT NULL,
    amount INT NOT NULL COMMENT '积分变动（正数=获得，负数=消费）',
    balance INT NOT NULL COMMENT '变动后余额',
    feature_key VARCHAR(50) DEFAULT NULL COMMENT '关联功能key',
    description VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_type (type),
    INDEX idx_feature_key (feature_key),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='积分历史表';

-- ========== 7. 功能使用日志表 ==========
CREATE TABLE IF NOT EXISTS feature_usage_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    username VARCHAR(50) NOT NULL,
    feature_key VARCHAR(50) NOT NULL,
    cost_type ENUM('free', 'vip_quota', 'points') NOT NULL,
    points_cost INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_feature_key (feature_key),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='功能使用日志表';

-- ========== 8. 创建迁移记录表 ==========
CREATE TABLE IF NOT EXISTS migrations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    version VARCHAR(20) NOT NULL UNIQUE,
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO migrations (version) VALUES ('001_add_points_vip_checkin');

