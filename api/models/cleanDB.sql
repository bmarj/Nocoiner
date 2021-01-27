
CREATE DATABASE [OrdersDB]
GO
USE [OrdersDB]
GO

CREATE TABLE [dbo].[sales_channel](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[description] [nvarchar](100) NOT NULL,
	code nvarchar(20) NOT NULL CONSTRAINT sales_channel_code UNIQUE,
	[service_id] [nvarchar](50) NULL CONSTRAINT [service_id] UNIQUE,
	[balanceable] [bit] NOT NULL  DEFAULT ((0)),
	[enabled] [bit] NOT NULL  DEFAULT ((1)),
	[product_alias_group] [int] NOT NULL  DEFAULT ((0)),
	[is_cross_insert] [bit] NOT NULL  DEFAULT ((0))
 CONSTRAINT [PK_sales_channel] PRIMARY KEY CLUSTERED (	[id] ASC)
)

GO
set identity_insert [sales_channel] ON
GO
INSERT [dbo].[sales_channel] (id, [description], code, [service_id], [balanceable], [enabled], [product_alias_group], [is_cross_insert]) VALUES (1, N'Amazon.com', N'CHAMAZON', N'amazon', 1, 1, 0, 0)
GO
INSERT [dbo].[sales_channel] (id, [description], code, [service_id], [balanceable], [enabled], [product_alias_group], [is_cross_insert]) VALUES (2, N'ShoppingBlitz.com', N'CHSBLITZ', N'shoppingblitz', 1, 1, 0, 0)
GO
INSERT [dbo].[sales_channel] (id, [description], code, [service_id], [balanceable], [enabled], [product_alias_group], [is_cross_insert]) VALUES (3, N'Return', N'CHRETURN', N'return', 0, 1, 0, 0)
GO
INSERT [dbo].[sales_channel] (id, [description], code, [service_id], [balanceable], [enabled], [product_alias_group], [is_cross_insert]) VALUES (4, N'Ebay.com', N'CHEBAY', N'ebay', 1, 1, 0, 0)
GO
INSERT [dbo].[sales_channel] (id, [description], code, [service_id], [balanceable], [enabled], [product_alias_group], [is_cross_insert]) VALUES (5, N'In Store', N'CHSTORE', N'Store', 0, 1, 0, 0)
GO
INSERT [dbo].[sales_channel] (id, [description], code, [service_id], [balanceable], [enabled], [product_alias_group], [is_cross_insert]) VALUES (6, N'reorder', N'CHREORDER', N'reorder', 0, 1, 0, 0)
GO
INSERT [dbo].[sales_channel] (id, [description], code, [service_id], [balanceable], [enabled], [product_alias_group], [is_cross_insert]) VALUES (7, N'Custom', N'CHCUSTOM', N'Custom', 0, 1, 0, 0)
GO
set identity_insert [sales_channel] OFF
GO

CREATE TABLE [dbo].[order_status](
	[id] [int] IDENTITY(1,1) NOT NULL,
	code nvarchar(20) NOT NULL CONSTRAINT order_status_code UNIQUE,
	[description] [nvarchar](500) NOT NULL,
	CONSTRAINT [PK_order_status] PRIMARY KEY CLUSTERED (id ASC),
)

GO
set identity_insert [order_status] ON
GO
INSERT [dbo].[order_status] (id, code, [description]) VALUES (1, 'PENDING', N'PENDING - Unpaid, payment not cleared yet, purchase was not confirmed etc.')
GO
INSERT [dbo].[order_status] (id, code, [description]) VALUES (2, 'UNSHIPPED', N'UNSHIPPED - Paid and confirmed, awaiting shipment')
GO
INSERT [dbo].[order_status] (id, code, [description]) VALUES (3, 'PARTIALLY', N'PARTIALLY SHIPPED - Some items in the order are shipped, some not.')
GO
INSERT [dbo].[order_status] (id, code, [description]) VALUES (4, 'SHIPPED', N'SHIPPED - All items in the order are shipped')
GO
INSERT [dbo].[order_status] (id, code, [description]) VALUES (5, 'CANCELLED', N'CANCELLED')
GO
set identity_insert [order_status] OFF

GO

CREATE TABLE [dbo].[ship_service_level](
	id [int] IDENTITY(1,1) NOT NULL,
	code nvarchar(20) NOT NULL CONSTRAINT ship_service_level_code UNIQUE, 
	[description] [nvarchar](500) NULL,
	CONSTRAINT [PK_ship_service_level] PRIMARY KEY CLUSTERED (id ASC),
)

GO

SET IDENTITY_INSERT [dbo].[ship_service_level] ON 
GO
INSERT [dbo].[ship_service_level] (id, code, [description]) VALUES (1, 'GROUND', N'Ground')
GO
INSERT [dbo].[ship_service_level] (id, code, [description]) VALUES (2, 'HOMEDELIVERY', N'Home Delivery')
GO
INSERT [dbo].[ship_service_level] (id, code, [description]) VALUES (3, 'PRIORITYMAIL', N'Priority Mail')
GO
INSERT [dbo].[ship_service_level] (id, code, [description]) VALUES (4, '2DAYAIR', N'2ND DAY AIR')
GO
INSERT [dbo].[ship_service_level] (id, code, [description]) VALUES (5, 'FIRSTCLASS', N'First Class')
GO
INSERT [dbo].[ship_service_level] (id, code, [description]) VALUES (6, 'UPSGROUND', N'UPS GROUND')
GO
SET IDENTITY_INSERT [dbo].[ship_service_level] OFF

GO

CREATE TABLE [dbo].[order](
	[id] int IDENTITY(1000000,1) NOT NULL, -- equal to [sales_order_number]	
	order_number nvarchar(50) NOT NULL,
	[purchase_date] [datetime] NOT NULL,
	[ship_name] [nvarchar](500) NOT NULL,
	[ship_phone] [nvarchar](100) NULL,
	[ship_email] [nvarchar](500) NULL,
	[ship_address] [nvarchar](500) NOT NULL,
	[ship_address_2] [nvarchar](500) NULL,
	[ship_city] [nvarchar](500) NULL,
	[ship_postal_code] [nvarchar](100) NULL,
	[ship_state] [nvarchar](500) NULL,	
	[ship_country] [nvarchar](500) NOT NULL,
	[buyer_name] [nvarchar](500) NULL,
	[buyer_phone] [nvarchar](100) NULL,
	[buyer_email] [nvarchar](500) NULL,
	[buyer_address] [nvarchar](500) NULL,
	[buyer_address_2] [nvarchar](500) NULL,
	[buyer_city] [nvarchar](500) NULL,
	[buyer_state] [nvarchar](500) NULL,
	[buyer_postal_code] [nvarchar](100) NULL,
	[buyer_country] [nvarchar](500) NULL,	
	--[sales_order_number] [int] IDENTITY(3090408,1) NOT NULL,
	[sales_channel_id] [int] NOT NULL
	CONSTRAINT [FK_order_sales_channel] FOREIGN KEY([sales_channel_id]) REFERENCES [dbo].[sales_channel] ([id]),
	[created_timestamp] [datetime] NOT NULL DEFAULT (getdate()),
	[total_qty] [int] NOT NULL DEFAULT(0),
	[order_status_id] [int] NOT NULL 
	CONSTRAINT [FK_order_order_status] FOREIGN KEY([order_status_id]) REFERENCES [dbo].[order_status] ([id]),
	[processing_status] nvarchar(20) NOT NULL DEFAULT('Pending'),
	[referring_order] [bigint] NULL,
	[is_prime] [bit] NOT NULL default(0),
	[is_premium] [bit] NOT NULL default(0),
	[shipping_priority] [nvarchar](128) NULL,
	CONSTRAINT [PK_order] PRIMARY KEY CLUSTERED ([id] ASC)
)
GO




GO
CREATE TABLE [dbo].[fulfillment_warehouse](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [varchar](64) NOT NULL,
	[code] [varchar](20) NOT NULL  CONSTRAINT fulfillment_warehouse_code UNIQUE,
	[enabled] [bit] NOT NULL DEFAULT(1),
    CONSTRAINT [PK_fulfillment_warehouse] PRIMARY KEY CLUSTERED (id ASC)
)
GO

SET IDENTITY_INSERT [dbo].[fulfillment_warehouse] ON 
GO
INSERT [dbo].[fulfillment_warehouse] (id, [name], [code], [enabled]) VALUES (3, N'California', N'CA', 1)
GO
INSERT [dbo].[fulfillment_warehouse] (id, [name], [code], [enabled]) VALUES (2, N'Nevada', N'NV', 0)
GO
INSERT [dbo].[fulfillment_warehouse] (id, [name], [code], [enabled]) VALUES (1, N'New Jersey', N'NJ', 1)
GO
SET IDENTITY_INSERT [dbo].[fulfillment_warehouse] OFF
GO


GO
CREATE TABLE [dbo].[order_line_status](
	id [int] IDENTITY(1,1) NOT NULL,
	[code] [varchar](20) NOT NULL  CONSTRAINT order_line_status_code UNIQUE,
	[description] [nvarchar](500) NOT NULL,
    CONSTRAINT [PK_order_line_status] PRIMARY KEY CLUSTERED (id ASC)
) 
GO

GO
SET IDENTITY_INSERT [dbo].[order_line_status] ON 
GO
INSERT [dbo].[order_line_status] (id, code, [description]) VALUES (1, 'PENDING', N'pending')
GO
INSERT [dbo].[order_line_status] (id, code, [description]) VALUES (2, 'EXPORTED', N'exported')
GO
INSERT [dbo].[order_line_status] (id, code, [description]) VALUES (3, 'CANCELLED', N'cancelled')
GO
INSERT [dbo].[order_line_status] (id, code, [description]) VALUES (4, 'IGNORED', N'ignored')
GO
INSERT [dbo].[order_line_status] (id, code, [description]) VALUES (5, 'COMPLETED', N'completed')
GO
SET IDENTITY_INSERT [dbo].[order_line_status] OFF
GO


CREATE TABLE [dbo].[order_line](
	id int IDENTITY(1,1) NOT NULL,
	[sku] [varchar](159) NULL,
	[order_id] int NOT NULL 
	CONSTRAINT FK_order_line_order FOREIGN KEY([order_id]) REFERENCES [dbo].[order] ([id]),
	[qty_ordered] [int] NOT NULL,
	[qty_shipped] [int] NOT NULL DEFAULT(0),
	[price] decimal(10,2) NOT NULL,
	[tax] decimal(10,2) NULL,
	currency_code nvarchar(3) NOT NULL, -- DEFAULT ('USD'), 
	[shipping_price] decimal(10,2) NULL,
	[shipping_tax] decimal(10,2) NULL,	
	[line_type] [nvarchar](10) NULL,	
	[purchase_order_number] [nvarchar](128) NULL,
	[order_line_status_id] int NULL 
	CONSTRAINT FK_order_line_order_line_status FOREIGN KEY([order_line_status_id]) REFERENCES [dbo].[order_line_status] ([id]),
	[exported] [bit] NOT NULL DEFAULT(0),
	[date_exported] [datetime] NULL,
	[username] [nvarchar](256) NULL,
	[notes] [nvarchar](max) NULL,
	--[linked_order_id] [nvarchar](128) NULL,
	[created_date] [datetime] NULL DEFAULT(getdate()),
	[processed_date] [datetime] NULL,
	[promise_date] [datetime] NULL,
	[fulfillment_warehouse_id] [int] NULL 
	CONSTRAINT FK_order_line_fulfillment_warehouse FOREIGN KEY([fulfillment_warehouse_id]) REFERENCES [dbo].[fulfillment_warehouse] ([id]),
	[is_premium] [bit] NOT NULL DEFAULT(0),
	[shipping_priority] [nvarchar](128) NULL,
 CONSTRAINT [PK_order_line] PRIMARY KEY CLUSTERED ( id ASC)
)

GO


CREATE NONCLUSTERED INDEX [ix_order_id] ON [dbo].[order_line]
(
	order_id ASC
)

GO


CREATE TABLE dbo.role(
	id int IDENTITY(1,1) NOT NULL CONSTRAINT [PK_role] PRIMARY KEY CLUSTERED (id ASC),
	name nvarchar(64) NOT NULL,
)
GO

CREATE TABLE dbo.permission(
	id int IDENTITY(1,1) NOT NULL CONSTRAINT [PK_permission] PRIMARY KEY CLUSTERED (id ASC),
	name nvarchar(64) NOT NULL,
)
GO


CREATE TABLE dbo.app_user(
	id int IDENTITY(1,1) NOT NULL CONSTRAINT [PK_app_user] PRIMARY KEY CLUSTERED (id ASC),
	first_name nvarchar(64) NOT NULL,
	last_name nvarchar(64) NOT NULL,
	username nvarchar(64) NOT NULL,
	password nvarchar(256) NOT NULL,
	active bit NOT NULL DEFAULT(1),
	email nvarchar(64) NOT NULL,
	last_login datetime,
	login_count int,
	fail_login_count int,
	created_on datetime NULL,
	changed_on datetime NULL,
	created_by_id int FOREIGN KEY(created_by_id) REFERENCES dbo.app_user (id),
	changed_by_id int FOREIGN KEY(changed_by_id) REFERENCES dbo.app_user (id)
)

GO


CREATE TABLE dbo.app_user_role(
	id int IDENTITY(1,1) NOT NULL CONSTRAINT [PK_app_user_role] PRIMARY KEY CLUSTERED (id ASC),
	app_user_id int NOT NULL,
	CONSTRAINT FK_app_user_role_app_user FOREIGN KEY(app_user_id) REFERENCES dbo.app_user (id),
	role_id int NOT NULL,
	CONSTRAINT FK_app_user_role_role FOREIGN KEY(role_id) REFERENCES dbo.role (id),
)
GO

CREATE UNIQUE INDEX user_role_index ON dbo.app_user_role (app_user_id, role_id)

GO

CREATE TABLE dbo.role_permission(
	id int IDENTITY(1,1) NOT NULL CONSTRAINT [PK_role_permission] PRIMARY KEY CLUSTERED (id ASC),
	role_id int NOT NULL,
	CONSTRAINT FK_role_permission_role FOREIGN KEY(role_id) REFERENCES dbo.role (id),
	permission_id int NOT NULL,
	CONSTRAINT FK_role_permission_permission FOREIGN KEY(permission_id) REFERENCES dbo.permission (id),
)
GO

CREATE UNIQUE INDEX role_permission_permission_index ON dbo.app_user_role (app_user_id, role_id)

GO


INSERT INTO role (name)
SELECT name FROM
(
	SELECT 'Admin' as name
	UNION
	SELECT 'Warehouse User'
) as names 
WHERE NOT EXISTS (select * from role where role.name=names.name)
GO

INSERT INTO permission (name)
SELECT name FROM
(
	SELECT 'orders' as name
	UNION
	SELECT 'order_lines'
	UNION
	SELECT 'users'
) as names 
WHERE NOT EXISTS (select * from permission where permission.name=names.name)
GO

INSERT INTO role_permission (role_id, permission_id)
SELECT role.id, permission.id
FROM role, permission
WHERE NOT EXISTS (select 9 from role_permission a where a.role_id=role.id and a.permission_id=permission.id)
GO

INSERT INTO app_user_role(app_user_id, role_id)
SELECT app_user.id, role.id
FROM app_user, role
WHERE NOT EXISTS (select 9 from app_user_role a where a.role_id=role.id and a.role_id=role.id)
and role.name='Admin'
GO



GO

insert into dbo.[order] (
	[purchase_date],
	order_number,
	[ship_name],
	[ship_phone],
	[ship_email],
	[ship_address],
	[ship_address_2],
	[ship_city],
	[ship_postal_code],
	[ship_state],
	[ship_country],
	[buyer_name],
	[buyer_phone],
	[buyer_email],
	[buyer_address],
	[buyer_address_2],
	[buyer_city],
	[buyer_state],
	[buyer_postal_code],
	[buyer_country],
	[sales_channel_id],
    [created_timestamp],
	[total_qty], 
	[order_status_id],
	[processing_status],
	[referring_order],
	[is_prime],
	[is_premium],
	[shipping_priority]
)
SELECT  
	[purchase_date],
	o.order_id,
	[ship_name],
	[ship_phone],
	[ship_email],
	[ship_address_1] as [ship_address],
	[ship_address_2],
	[ship_city],
	[ship_postal_code],
	[ship_state],
	[ship_country],
	[buyer_name],
	[buyer_phone],
	[buyer_email],
	[buyer_address_1] as [buyer_address],
	[buyer_address_2],
	[buyer_city],
	[buyer_state],
	[buyer_postal_code],
	[buyer_country],
	isnull((select id from sales_channel s where s.id=[sales_channel]), 1) as [sales_channel_id],
    [created] as 	[created_timestamp],
	isnull([total_qty], 0) as total_qty,
	(1) as [order_status_id],
	[processing_status],
	[referring_order],
	isnull([is_prime],0) as is_prime,
	isnull([is_premium],0) as [is_premium],
	[shipping_priority]
FROM 
[Test_Combined_Orders].[dbo].[orders] o join 
[Test_Combined_Orders].[dbo].order_flags orf 
ON orf.order_id=o.order_id

GO


INSERT INTO [OrdersDB].dbo.order_line
(
      [sku]
      ,[order_id]
      ,[qty_ordered]
      ,[qty_shipped]
      ,[price]
      ,[tax]
      ,[currency_code]
      ,[shipping_price]
      ,[shipping_tax]
      ,[line_type]
      ,[purchase_order_number]
      ,[order_line_status_id]
      ,[exported]
      ,[date_exported]
      ,[username]
      ,[notes]
      ,[created_date]
      ,[processed_date]
      ,[promise_date]
      ,[fulfillment_warehouse_id]
      ,[is_premium]
      ,[shipping_priority]
)
SELECT 
       [sku]
      ,(select id from dbo.[order] oo where oo.order_number=o.order_id) as [order_id]
      ,[qty_ordered]
      ,isnull(ol.[qty_shipped],0) as [qty_shipped]
      ,[price]
      ,[tax]
      ,'USD' as [currency_code]
      ,[shipping_price]
      ,[shipping_tax]
      ,[line_type]
      ,[purchase_order_number]
      ,(select oo.id from order_line_status oo join [Test_Combined_Orders].[dbo].[order_line_status] ols ON oo.description=ols.description where ols.status=olf.order_line_status) as [order_line_status_id]
      ,isnull([exported], 0) as [exported]
      ,[date_exported]
      ,[username]
      ,[notes]
      ,ol.created as [created_date]
      ,[processed_date]
      ,[promise_date]
      ,fulfillment_warehouse_id as [fulfillment_warehouse_id]
      ,[is_premium]
      ,[shipping_priority]
FROM
[Test_Combined_Orders].[dbo].[order_lines] ol 
JOIN [Test_Combined_Orders].[dbo].[order_line_flags] olf ON ol.guid_order_line=olf.guid_order_line
JOIN [Test_Combined_Orders].[dbo].orders o ON o.order_id=ol.order_id


GO












