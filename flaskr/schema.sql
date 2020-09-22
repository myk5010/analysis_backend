DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS materiel;
DROP TABLE IF EXISTS stock;
DROP TABLE IF EXISTS batch_in;
DROP TABLE IF EXISTS batch_out;

CREATE TABLE user 
-- 用户表
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE materiel 
-- 物料种类表
(
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `materiel_name` VARCHAR(30) UNIQUE NOT NULL, -- 物料名称
  `standard` VARCHAR(30), -- 规格
  `unit` VARCHAR(10) NOT NULL -- 单位
);

CREATE TABLE stock 
-- 库存表
(
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `materiel_id` INTEGER NOT NULL, -- 关联物料ID
  `amount` DECIMAL(6,1) NOT NULL, -- 总价
  `gross` DECIMAL(6,1) NOT NULL, -- 总量
  `comment` TEXT -- 备注
);

CREATE TABLE batch_in 
--  入库批次表
(
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `stock_id` INTEGER NOT NULL, -- 关联库存ID
  `serial` INTEGER NOT NULL, -- 批次序列号
  `in_number` DECIMAL(6,1) NOT NULL, -- 入库数量
  `in_time` DECIMAL(6,1) NOT NULL, -- 入库时间
  `price` DECIMAL(6,1) NOT NULL, -- 进货单价
  `comment` TEXT -- 备注
);

CREATE TABLE batch_out 
-- 出库批次表
(
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `batch_in_id` INTEGER NOT NULL, -- 关联入库批次ID
  `out_number` DECIMAL(6,1) NOT NULL, -- 出库数量
  `out_time` DECIMAL(6,1) NOT NULL, -- 出库时间
  `price` DECIMAL(6,1) NOT NULL, -- 出售单价
  `loss` DECIMAL(6,1) DEFAULT 0, -- 损耗
  `document` VARCHAR(20), -- 单据编号
  `code` VARCHAR(20), -- 物料长代码
  `comment` TEXT -- 备注
);