-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 03, 2026 at 01:36 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sarisari_erp`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add audit log', 7, 'add_auditlog'),
(26, 'Can change audit log', 7, 'change_auditlog'),
(27, 'Can delete audit log', 7, 'delete_auditlog'),
(28, 'Can view audit log', 7, 'view_auditlog'),
(29, 'Can add brand', 8, 'add_brand'),
(30, 'Can change brand', 8, 'change_brand'),
(31, 'Can delete brand', 8, 'delete_brand'),
(32, 'Can view brand', 8, 'view_brand'),
(33, 'Can add category', 9, 'add_category'),
(34, 'Can change category', 9, 'change_category'),
(35, 'Can delete category', 9, 'delete_category'),
(36, 'Can view category', 9, 'view_category'),
(37, 'Can add customer', 10, 'add_customer'),
(38, 'Can change customer', 10, 'change_customer'),
(39, 'Can delete customer', 10, 'delete_customer'),
(40, 'Can view customer', 10, 'view_customer'),
(41, 'Can add employee', 11, 'add_employee'),
(42, 'Can change employee', 11, 'change_employee'),
(43, 'Can delete employee', 11, 'delete_employee'),
(44, 'Can view employee', 11, 'view_employee'),
(45, 'Can add expense', 12, 'add_expense'),
(46, 'Can change expense', 12, 'change_expense'),
(47, 'Can delete expense', 12, 'delete_expense'),
(48, 'Can view expense', 12, 'view_expense'),
(49, 'Can add purchase order', 13, 'add_purchaseorder'),
(50, 'Can change purchase order', 13, 'change_purchaseorder'),
(51, 'Can delete purchase order', 13, 'delete_purchaseorder'),
(52, 'Can view purchase order', 13, 'view_purchaseorder'),
(53, 'Can add supplier', 14, 'add_supplier'),
(54, 'Can change supplier', 14, 'change_supplier'),
(55, 'Can delete supplier', 14, 'delete_supplier'),
(56, 'Can view supplier', 14, 'view_supplier'),
(57, 'Can add product', 15, 'add_product'),
(58, 'Can change product', 15, 'change_product'),
(59, 'Can delete product', 15, 'delete_product'),
(60, 'Can view product', 15, 'view_product'),
(61, 'Can add purchase item', 16, 'add_purchaseitem'),
(62, 'Can change purchase item', 16, 'change_purchaseitem'),
(63, 'Can delete purchase item', 16, 'delete_purchaseitem'),
(64, 'Can view purchase item', 16, 'view_purchaseitem'),
(65, 'Can add sale', 17, 'add_sale'),
(66, 'Can change sale', 17, 'change_sale'),
(67, 'Can delete sale', 17, 'delete_sale'),
(68, 'Can view sale', 17, 'view_sale'),
(69, 'Can add sale item', 18, 'add_saleitem'),
(70, 'Can change sale item', 18, 'change_saleitem'),
(71, 'Can delete sale item', 18, 'delete_saleitem'),
(72, 'Can view sale item', 18, 'view_saleitem'),
(73, 'Can add trip', 19, 'add_trip'),
(74, 'Can change trip', 19, 'change_trip'),
(75, 'Can delete trip', 19, 'delete_trip'),
(76, 'Can view trip', 19, 'view_trip'),
(77, 'Can add trip item', 20, 'add_tripitem'),
(78, 'Can change trip item', 20, 'change_tripitem'),
(79, 'Can delete trip item', 20, 'delete_tripitem'),
(80, 'Can view trip item', 20, 'view_tripitem');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$720000$qRUkHwzKu8l8fDsTQINLnz$z7I9eS0U9d2ePCc2euDagJmK3EIZMN+OiVT3rpG3QEs=', '2026-07-03 10:23:45.055723', 1, 'admin', '', '', 'admin@example.com', 1, 1, '2026-06-27 09:35:35.270450'),
(2, 'pbkdf2_sha256$720000$JfZP9bqS9S6enQiCyb6vBF$IiIxlb/DRNKt9jP+nNpfchgTh/h/MpLSjoMupafJR2g=', '2026-07-02 11:33:57.966871', 0, 'maria', '', '', 'maria@clara.com', 0, 1, '2026-07-02 11:21:07.457825'),
(3, 'pbkdf2_sha256$720000$1YpV2pO8V7FJ0PiuIDeCZB$1WVPzJkTwVKKcWqMGQFh7hTZ4FkLMRVJjhL9lJBrcDk=', NULL, 0, 'juan', '', '', 'juan@delacruz.com', 0, 1, '2026-07-02 11:21:08.412966'),
(4, 'pbkdf2_sha256$720000$TsoQsu12l7J4AmAuLfkPDt$CgVWPgBwpdtwjMPGXe0XrY3uPif4wMEpsCVQUlhxvos=', NULL, 0, 'pedro', '', '', 'pedro@penduko.com', 0, 1, '2026-07-02 11:21:09.402602'),
(5, 'pbkdf2_sha256$720000$fLKHkvs9dHo94RDHPAWzLT$+pU5crDYFm0ybQ8SKkhaYofBUzfCEVHi/mJyGm5p1aw=', '2026-07-02 11:40:56.999640', 0, 'nena', '', '', 'nena@sarisari.com', 0, 1, '2026-07-02 11:23:57.258557'),
(6, 'pbkdf2_sha256$720000$YiJLHXEppjst1GUkt6o1CO$XLAWXu+Pn0BfiKbEkTc7y5AUuUxLO1SiLtJ7XmB3F0c=', '2026-07-02 11:24:51.517344', 0, 'tomas', '', '', 'tomas@minimart.com', 0, 1, '2026-07-02 11:23:58.221122');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_auditlog`
--

CREATE TABLE `core_auditlog` (
  `id` bigint(20) NOT NULL,
  `user` varchar(150) NOT NULL,
  `action` varchar(100) NOT NULL,
  `module` varchar(100) NOT NULL,
  `details` longtext DEFAULT NULL,
  `timestamp` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `core_auditlog`
--

INSERT INTO `core_auditlog` (`id`, `user`, `action`, `module`, `details`, `timestamp`) VALUES
(13, 'system', 'Database Seeding', 'System Setup', 'Successfully populated system tables with initial demonstration records.', '2026-06-28 09:59:01.109717'),
(14, 'admin', 'Create Sale', 'Sales', 'Created Invoice DFT-20260628-7573 worth PHP 1280.00. Method: Cash. Status: Draft.', '2026-06-28 15:56:29.297167'),
(15, 'admin', 'Create Sale', 'Sales', 'Created Invoice DFT-20260702-5335 worth PHP 660.00. Method: GCash. Status: Draft.', '2026-07-02 11:09:18.123207'),
(16, 'admin', 'Create Sale', 'Sales', 'Created Invoice DFT-20260702-9711 worth PHP 660.00. Method: Cash. Status: Draft.', '2026-07-02 11:12:12.596376'),
(17, 'admin', 'Create Sale', 'Sales', 'Created Invoice DFT-20260702-4361 worth PHP 1310.00. Method: Cash. Status: Draft.', '2026-07-02 11:12:46.027679'),
(18, 'admin', 'Create Sale', 'Sales', 'Created Invoice DFT-20260702-3849 worth PHP 1150.00. Method: Cash. Status: Draft.', '2026-07-02 11:13:39.708643'),
(19, 'nena', 'Create Sale', 'Sales', 'Created Invoice DFT-20260702-2403 worth PHP 1280.00. Method: Cash. Status: Draft.', '2026-07-02 11:32:47.549220'),
(20, 'nena', 'Create Sale', 'Sales', 'Created Invoice DFT-20260702-3545 worth PHP 680.00. Method: Cash. Status: Draft.', '2026-07-02 11:33:05.453738'),
(21, 'nena', 'Create Sale', 'Sales', 'Created Invoice DFT-20260702-5635 worth PHP 610.00. Method: Cash. Status: Draft.', '2026-07-02 11:41:08.372453'),
(22, 'nena', 'Create Sale', 'Sales', 'Created Invoice DFT-20260702-2856 worth PHP 610.00. Method: Cash. Status: Draft.', '2026-07-02 11:41:13.997816'),
(23, 'nena', 'Create Sale', 'Sales', 'Created Invoice DFT-20260702-9661 worth PHP 660.00. Method: Cash. Status: Draft.', '2026-07-02 11:46:16.926316'),
(24, 'admin', 'Create Sale', 'Sales', 'Created Invoice DFT-20260703-4495 worth PHP 650.00. Method: Cash. Status: Draft.', '2026-07-03 10:03:30.566795'),
(25, 'admin', 'Create Sale', 'Sales', 'Created Invoice DFT-20260703-2808 worth PHP 1350.00. Method: Cash. Status: Draft.', '2026-07-03 10:17:54.914092'),
(26, 'system', 'Create Sale', 'Sales', 'Created Invoice DFT-20260703-6978 worth PHP 720.00. Method: Cash. Status: Draft.', '2026-07-03 10:23:12.347088'),
(27, 'admin', 'Create Sale', 'Sales', 'Created Invoice DFT-20260703-4805 worth PHP 720.00. Method: Cash. Status: Draft.', '2026-07-03 10:24:11.082055'),
(28, 'admin', 'Create Sale', 'Sales', 'Created Invoice DFT-20260703-8949 worth PHP 3490.00. Method: Cash. Status: Draft.', '2026-07-03 10:24:50.806280'),
(29, 'admin', 'Create Sale', 'Sales', 'Created Invoice DFT-20260703-9590 worth PHP 720.00. Method: Cash. Status: Draft.', '2026-07-03 10:28:23.126320'),
(30, 'admin', 'Create Sale', 'Sales', 'Created Invoice DFT-20260703-4573 worth PHP 1980.00. Method: Cash. Status: Draft.', '2026-07-03 10:29:41.960014'),
(31, 'admin', 'Create Sale', 'Sales', 'Created Invoice DFT-20260703-7051 worth PHP 2530.00. Method: Cash. Status: Draft.', '2026-07-03 10:32:48.248232'),
(32, 'admin', 'Create Sale', 'Sales', 'Created Invoice DFT-20260703-4958 worth PHP 1350.00. Method: Cash. Status: Draft.', '2026-07-03 10:33:39.484182'),
(33, 'admin', 'Create Sale', 'Sales', 'Created Invoice DFT-20260703-8321 worth PHP 1350.00. Method: Cash. Status: Draft.', '2026-07-03 10:35:02.251872'),
(34, 'admin', 'Create Sale', 'Sales', 'Created Invoice DFT-20260703-3203 worth PHP 1380.00. Method: Cash. Status: Draft.', '2026-07-03 10:36:58.715764'),
(35, 'admin', 'Create Sale', 'Sales', 'Created Invoice DFT-20260703-9687 worth PHP 1380.00. Method: Cash. Status: Draft.', '2026-07-03 10:39:08.254258'),
(36, 'admin', 'Create Sale', 'Sales', 'Created Invoice DFT-20260703-1702 worth PHP 660.00. Method: Cash. Status: Draft.', '2026-07-03 10:44:11.661774');

-- --------------------------------------------------------

--
-- Table structure for table `core_brand`
--

CREATE TABLE `core_brand` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `core_brand`
--

INSERT INTO `core_brand` (`id`, `name`, `description`) VALUES
(25, 'Coca-Cola Company', NULL),
(26, 'San Miguel Brewery', NULL),
(27, 'PepsiCo', NULL),
(28, 'Monde Nissin', NULL),
(29, 'Unilever', NULL),
(30, 'PMFTC Inc.', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `core_category`
--

CREATE TABLE `core_category` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `core_category`
--

INSERT INTO `core_category` (`id`, `name`, `description`) VALUES
(21, 'Beverages', 'Soft drinks, beers, energy drinks, and water'),
(22, 'Snacks', 'Chips, biscuits, candies, and crackers'),
(23, 'Groceries', 'Canned goods, noodles, sauces, condiments'),
(24, 'Household', 'Soaps, detergents, toiletries, and cleaners'),
(25, 'Tobacco & Liquor', 'Cigarettes, hard liquor, and spirits');

-- --------------------------------------------------------

--
-- Table structure for table `core_customer`
--

CREATE TABLE `core_customer` (
  `id` bigint(20) NOT NULL,
  `name` varchar(150) NOT NULL,
  `contact` varchar(50) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `address` longtext DEFAULT NULL,
  `credit_limit` decimal(12,2) NOT NULL,
  `credit_balance` decimal(12,2) NOT NULL,
  `reward_points` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `core_customer`
--

INSERT INTO `core_customer` (`id`, `name`, `contact`, `email`, `address`, `credit_limit`, `credit_balance`, `reward_points`, `user_id`) VALUES
(13, 'Aling Nena\'s Sari-Sari Store', '09123456789', 'nena@gmail.com', 'Cagsalaosao, Calbayog City', 15000.00, 3400.00, 162, 5),
(14, 'Mang Tomas Minimart', '09876543210', 'tomas@minimart.ph', 'Rawis, Calbayog City', 30000.00, 0.00, 450, 6),
(15, 'Tita Baby\'s Wholesale Outlet', '09223334444', 'baby@outlook.com', 'Oquendo, Calbayog City', 10000.00, 850.00, 75, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `core_employee`
--

CREATE TABLE `core_employee` (
  `id` bigint(20) NOT NULL,
  `name` varchar(150) NOT NULL,
  `role` varchar(50) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `base_salary` decimal(10,2) NOT NULL,
  `overtime` decimal(10,2) NOT NULL,
  `deductions` decimal(10,2) NOT NULL,
  `incentives` decimal(10,2) NOT NULL,
  `status` varchar(20) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `core_employee`
--

INSERT INTO `core_employee` (`id`, `name`, `role`, `phone`, `base_salary`, `overtime`, `deductions`, `incentives`, `status`, `user_id`) VALUES
(17, 'Juan Dela Cruz', 'Salesman', '09331112222', 15000.00, 0.00, 0.00, 0.00, 'Active', 3),
(18, 'Pedro Penduko', 'Driver', '09332223333', 12000.00, 0.00, 0.00, 0.00, 'Active', 4),
(19, 'Cardo Dalisay', 'Helper', '09333334444', 10000.00, 0.00, 0.00, 0.00, 'Active', NULL),
(20, 'Sheyde Vasquez', 'Admin', '09175558888', 30000.00, 0.00, 0.00, 0.00, 'Active', 1),
(21, 'Maria Clara', 'Cashier', NULL, 15000.00, 0.00, 0.00, 0.00, 'Active', 2);

-- --------------------------------------------------------

--
-- Table structure for table `core_expense`
--

CREATE TABLE `core_expense` (
  `id` bigint(20) NOT NULL,
  `category` varchar(100) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `description` longtext DEFAULT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_product`
--

CREATE TABLE `core_product` (
  `sku` varchar(50) NOT NULL,
  `name` varchar(200) NOT NULL,
  `cost_price` decimal(10,2) NOT NULL,
  `wholesale_price` decimal(10,2) NOT NULL,
  `retail_price` decimal(10,2) NOT NULL,
  `stock_quantity` int(11) NOT NULL,
  `min_stock` int(11) NOT NULL,
  `max_stock` int(11) NOT NULL,
  `barcode` varchar(100) DEFAULT NULL,
  `qr_code` longtext DEFAULT NULL,
  `expiration_date` date DEFAULT NULL,
  `brand_id` bigint(20) DEFAULT NULL,
  `category_id` bigint(20) DEFAULT NULL,
  `supplier_id` bigint(20) DEFAULT NULL,
  `image_url` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `core_product`
--

INSERT INTO `core_product` (`sku`, `name`, `cost_price`, `wholesale_price`, `retail_price`, `stock_quantity`, `min_stock`, `max_stock`, `barcode`, `qr_code`, `expiration_date`, `brand_id`, `category_id`, `supplier_id`, `image_url`) VALUES
('COKE-1.5L', 'Coca-Cola Original 1.5L (Case of 12)', 550.00, 620.00, 660.00, 45, 10, 150, '4800001001502', NULL, '2026-12-25', 25, 21, 13, 'https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=600&q=80'),
('LUCKYME-PC', 'Lucky Me Pancit Canton Original 80g (Box of 72)', 620.00, 680.00, 720.00, 35, 8, 80, '4800022334401', NULL, '2026-10-26', 28, 23, 15, 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=600&q=80'),
('PILSER-320', 'San Miguel Pale Pilsen 320ml (Case of 24)', 980.00, 1080.00, 1150.00, 8, 15, 150, '4800011223302', NULL, '2027-06-28', 26, 21, 14, 'https://images.unsplash.com/photo-1600788886242-5c96aabe3757?auto=format&fit=crop&w=600&q=80'),
('REDHORSE-1L', 'Red Horse Beer Extra Strong 1L (Case of 12)', 1150.00, 1280.00, 1350.00, 60, 15, 200, '4800011223301', NULL, '2027-06-28', 26, 21, 14, 'https://images.unsplash.com/photo-1566633806327-68e152aaf26d?auto=format&fit=crop&w=600&q=80'),
('SAFEGUARD-W', 'Safeguard White Soap 130g (Pack of 36)', 1350.00, 1450.00, 1520.00, 18, 5, 50, '4800033445501', NULL, '2028-06-27', 29, 24, 15, 'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=600&q=80'),
('SPRITE-1.5L', 'Sprite Lemon-Lime 1.5L (Case of 12)', 540.00, 610.00, 650.00, 25, 10, 100, '4800001001503', NULL, '2026-12-25', 25, 21, 13, 'https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?auto=format&fit=crop&w=600&q=80');

-- --------------------------------------------------------

--
-- Table structure for table `core_purchaseitem`
--

CREATE TABLE `core_purchaseitem` (
  `id` bigint(20) NOT NULL,
  `qty` int(11) NOT NULL,
  `cost` decimal(10,2) NOT NULL,
  `total` decimal(12,2) NOT NULL,
  `product_id` varchar(50) NOT NULL,
  `purchase_order_id` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_purchaseorder`
--

CREATE TABLE `core_purchaseorder` (
  `po_no` varchar(50) NOT NULL,
  `date` datetime(6) NOT NULL,
  `total` decimal(12,2) NOT NULL,
  `status` varchar(50) NOT NULL,
  `supplier_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_sale`
--

CREATE TABLE `core_sale` (
  `invoice_no` varchar(50) NOT NULL,
  `date` datetime(6) NOT NULL,
  `route` varchar(100) DEFAULT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  `tax` decimal(12,2) NOT NULL,
  `total` decimal(12,2) NOT NULL,
  `method` varchar(50) NOT NULL,
  `status` varchar(20) NOT NULL,
  `customer_id` bigint(20) DEFAULT NULL,
  `salesman_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `core_sale`
--

INSERT INTO `core_sale` (`invoice_no`, `date`, `route`, `subtotal`, `tax`, `total`, `method`, `status`, `customer_id`, `salesman_id`) VALUES
('DFT-20260628-7573', '2026-06-28 15:56:29.039184', NULL, 1280.00, 153.60, 1280.00, 'Cash', 'Draft', NULL, NULL),
('DFT-20260702-2403', '2026-07-02 11:32:47.510082', NULL, 1280.00, 153.60, 1280.00, 'Cash', 'Draft', 13, NULL),
('DFT-20260702-2856', '2026-07-02 11:41:13.976922', NULL, 610.00, 73.20, 610.00, 'Cash', 'Draft', 13, NULL),
('DFT-20260702-3545', '2026-07-02 11:33:05.436238', NULL, 680.00, 81.60, 680.00, 'Cash', 'Draft', 13, NULL),
('DFT-20260702-3849', '2026-07-02 11:13:39.697470', NULL, 1150.00, 138.00, 1150.00, 'Cash', 'Draft', NULL, NULL),
('DFT-20260702-4361', '2026-07-02 11:12:45.999290', NULL, 1310.00, 157.20, 1310.00, 'Cash', 'Draft', NULL, NULL),
('DFT-20260702-5335', '2026-07-02 11:09:18.071234', 'Route 1 - Cagsalaosao City Center', 660.00, 79.20, 660.00, 'GCash', 'Draft', 13, NULL),
('DFT-20260702-5635', '2026-07-02 11:41:08.348885', NULL, 610.00, 73.20, 610.00, 'Cash', 'Draft', 13, NULL),
('DFT-20260702-9661', '2026-07-02 11:46:16.894406', NULL, 660.00, 79.20, 660.00, 'Cash', 'Draft', 13, NULL),
('DFT-20260702-9711', '2026-07-02 11:12:12.568960', NULL, 660.00, 79.20, 660.00, 'Cash', 'Draft', NULL, NULL),
('DFT-20260703-1702', '2026-07-03 10:44:11.637986', NULL, 660.00, 79.20, 660.00, 'Cash', 'Draft', NULL, NULL),
('DFT-20260703-2808', '2026-07-03 10:17:54.886548', NULL, 1350.00, 162.00, 1350.00, 'Cash', 'Draft', NULL, NULL),
('DFT-20260703-3203', '2026-07-03 10:36:58.695662', NULL, 1380.00, 165.60, 1380.00, 'Cash', 'Draft', NULL, NULL),
('DFT-20260703-4495', '2026-07-03 10:03:30.272832', NULL, 650.00, 78.00, 650.00, 'Cash', 'Draft', NULL, NULL),
('DFT-20260703-4573', '2026-07-03 10:29:41.948326', NULL, 1980.00, 237.60, 1980.00, 'Cash', 'Draft', NULL, NULL),
('DFT-20260703-4805', '2026-07-03 10:24:11.068420', NULL, 720.00, 86.40, 720.00, 'Cash', 'Draft', NULL, NULL),
('DFT-20260703-4958', '2026-07-03 10:33:38.402381', NULL, 1350.00, 162.00, 1350.00, 'Cash', 'Draft', NULL, NULL),
('DFT-20260703-6978', '2026-07-03 10:23:10.783015', NULL, 720.00, 86.40, 720.00, 'Cash', 'Draft', NULL, NULL),
('DFT-20260703-7051', '2026-07-03 10:32:47.207848', NULL, 2530.00, 303.60, 2530.00, 'Cash', 'Draft', NULL, NULL),
('DFT-20260703-8321', '2026-07-03 10:35:01.858451', NULL, 1350.00, 162.00, 1350.00, 'Cash', 'Draft', NULL, NULL),
('DFT-20260703-8949', '2026-07-03 10:24:50.782284', NULL, 3490.00, 418.80, 3490.00, 'Cash', 'Draft', NULL, NULL),
('DFT-20260703-9590', '2026-07-03 10:28:23.109475', NULL, 720.00, 86.40, 720.00, 'Cash', 'Draft', NULL, NULL),
('DFT-20260703-9687', '2026-07-03 10:39:08.210218', NULL, 1380.00, 165.60, 1380.00, 'Cash', 'Draft', NULL, NULL),
('INV-2026-0001', '2026-06-28 09:59:01.124759', 'Route 1 - Cagsalaosao City Center', 4960.00, 595.20, 5555.20, 'Credit', 'Posted', 13, 17);

-- --------------------------------------------------------

--
-- Table structure for table `core_saleitem`
--

CREATE TABLE `core_saleitem` (
  `id` bigint(20) NOT NULL,
  `qty` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `total` decimal(12,2) NOT NULL,
  `product_id` varchar(50) NOT NULL,
  `sale_id` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `core_saleitem`
--

INSERT INTO `core_saleitem` (`id`, `qty`, `price`, `total`, `product_id`, `sale_id`) VALUES
(16, 8, 620.00, 4960.00, 'COKE-1.5L', 'INV-2026-0001'),
(17, 1, 1280.00, 1280.00, 'REDHORSE-1L', 'DFT-20260628-7573'),
(18, 1, 660.00, 660.00, 'COKE-1.5L', 'DFT-20260702-5335'),
(19, 1, 660.00, 660.00, 'COKE-1.5L', 'DFT-20260702-9711'),
(20, 1, 660.00, 660.00, 'COKE-1.5L', 'DFT-20260702-4361'),
(21, 1, 650.00, 650.00, 'SPRITE-1.5L', 'DFT-20260702-4361'),
(22, 1, 1150.00, 1150.00, 'PILSER-320', 'DFT-20260702-3849'),
(23, 1, 1280.00, 1280.00, 'REDHORSE-1L', 'DFT-20260702-2403'),
(24, 1, 680.00, 680.00, 'LUCKYME-PC', 'DFT-20260702-3545'),
(25, 1, 610.00, 610.00, 'SPRITE-1.5L', 'DFT-20260702-5635'),
(26, 1, 610.00, 610.00, 'SPRITE-1.5L', 'DFT-20260702-2856'),
(27, 1, 660.00, 660.00, 'COKE-1.5L', 'DFT-20260702-9661'),
(28, 1, 650.00, 650.00, 'SPRITE-1.5L', 'DFT-20260703-4495'),
(29, 1, 1350.00, 1350.00, 'REDHORSE-1L', 'DFT-20260703-2808'),
(30, 1, 720.00, 720.00, 'LUCKYME-PC', 'DFT-20260703-6978'),
(31, 1, 720.00, 720.00, 'LUCKYME-PC', 'DFT-20260703-4805'),
(32, 2, 660.00, 1320.00, 'COKE-1.5L', 'DFT-20260703-8949'),
(33, 1, 650.00, 650.00, 'SPRITE-1.5L', 'DFT-20260703-8949'),
(34, 1, 1520.00, 1520.00, 'SAFEGUARD-W', 'DFT-20260703-8949'),
(35, 1, 720.00, 720.00, 'LUCKYME-PC', 'DFT-20260703-9590'),
(36, 3, 660.00, 1980.00, 'COKE-1.5L', 'DFT-20260703-4573'),
(37, 1, 720.00, 720.00, 'LUCKYME-PC', 'DFT-20260703-7051'),
(38, 1, 660.00, 660.00, 'COKE-1.5L', 'DFT-20260703-7051'),
(39, 1, 1150.00, 1150.00, 'PILSER-320', 'DFT-20260703-7051'),
(40, 1, 1350.00, 1350.00, 'REDHORSE-1L', 'DFT-20260703-4958'),
(41, 1, 1350.00, 1350.00, 'REDHORSE-1L', 'DFT-20260703-8321'),
(42, 1, 720.00, 720.00, 'LUCKYME-PC', 'DFT-20260703-3203'),
(43, 1, 660.00, 660.00, 'COKE-1.5L', 'DFT-20260703-3203'),
(44, 1, 660.00, 660.00, 'COKE-1.5L', 'DFT-20260703-9687'),
(45, 1, 720.00, 720.00, 'LUCKYME-PC', 'DFT-20260703-9687'),
(46, 1, 660.00, 660.00, 'COKE-1.5L', 'DFT-20260703-1702');

-- --------------------------------------------------------

--
-- Table structure for table `core_supplier`
--

CREATE TABLE `core_supplier` (
  `id` bigint(20) NOT NULL,
  `name` varchar(150) NOT NULL,
  `company_name` varchar(150) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `address` longtext DEFAULT NULL,
  `tin` varchar(20) DEFAULT NULL,
  `outstanding_balance` decimal(12,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `core_supplier`
--

INSERT INTO `core_supplier` (`id`, `name`, `company_name`, `phone`, `email`, `address`, `tin`, `outstanding_balance`) VALUES
(13, 'Coca-Cola Beverages PH', 'Coca-Cola Bottlers Philippines Inc.', '02-8866-2653', 'orders@coca-cola.com.ph', 'Manila Gateway, Taguig, Metro Manila', '000-111-222-000', 45000.00),
(14, 'San Miguel Brewery Inc.', 'San Miguel Corporation', '02-8632-3000', 'sales@smb.sanmiguel.com.ph', 'Ortigas Center, Pasig City', '111-222-333-000', 125000.00),
(15, 'Monde Nissin Corp', 'Monde Nissin Corporation', '02-8588-9100', 'sales@mondenissin.com', 'Sta. Rosa, Laguna', '222-333-444-000', 0.00);

-- --------------------------------------------------------

--
-- Table structure for table `core_trip`
--

CREATE TABLE `core_trip` (
  `id` bigint(20) NOT NULL,
  `date` date NOT NULL,
  `truck_id` varchar(50) NOT NULL,
  `route` varchar(100) NOT NULL,
  `status` varchar(50) NOT NULL,
  `cash_collected` decimal(12,2) NOT NULL,
  `cash_predicted` decimal(12,2) NOT NULL,
  `shortage` decimal(12,2) NOT NULL,
  `logs` longtext DEFAULT NULL,
  `driver_id` bigint(20) DEFAULT NULL,
  `helper_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `core_trip`
--

INSERT INTO `core_trip` (`id`, `date`, `truck_id`, `route`, `status`, `cash_collected`, `cash_predicted`, `shortage`, `logs`, `driver_id`, `helper_id`) VALUES
(5, '2026-06-27', 'TRUCK-A (ELF-4W)', 'Route 1 - Cagsalaosao City Center', 'Completed', 2800.00, 2800.00, 0.00, 'Trip reconciled automatically. Helper bonus (50) and Driver bonus (100) added.', 18, 19);

-- --------------------------------------------------------

--
-- Table structure for table `core_tripitem`
--

CREATE TABLE `core_tripitem` (
  `id` bigint(20) NOT NULL,
  `qty_loaded` int(11) NOT NULL,
  `qty_sold` int(11) NOT NULL,
  `qty_returned` int(11) NOT NULL,
  `product_id` varchar(50) NOT NULL,
  `trip_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `core_tripitem`
--

INSERT INTO `core_tripitem` (`id`, `qty_loaded`, `qty_sold`, `qty_returned`, `product_id`, `trip_id`) VALUES
(5, 10, 8, 2, 'COKE-1.5L', 5);

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(7, 'core', 'auditlog'),
(8, 'core', 'brand'),
(9, 'core', 'category'),
(10, 'core', 'customer'),
(11, 'core', 'employee'),
(12, 'core', 'expense'),
(15, 'core', 'product'),
(16, 'core', 'purchaseitem'),
(13, 'core', 'purchaseorder'),
(17, 'core', 'sale'),
(18, 'core', 'saleitem'),
(14, 'core', 'supplier'),
(19, 'core', 'trip'),
(20, 'core', 'tripitem'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-06-27 04:17:40.707356'),
(2, 'auth', '0001_initial', '2026-06-27 04:17:41.344276'),
(3, 'admin', '0001_initial', '2026-06-27 04:17:41.495882'),
(4, 'admin', '0002_logentry_remove_auto_add', '2026-06-27 04:17:41.509650'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-06-27 04:17:41.520164'),
(6, 'contenttypes', '0002_remove_content_type_name', '2026-06-27 04:17:41.619228'),
(7, 'auth', '0002_alter_permission_name_max_length', '2026-06-27 04:17:41.683934'),
(8, 'auth', '0003_alter_user_email_max_length', '2026-06-27 04:17:41.706406'),
(9, 'auth', '0004_alter_user_username_opts', '2026-06-27 04:17:41.716008'),
(10, 'auth', '0005_alter_user_last_login_null', '2026-06-27 04:17:41.794489'),
(11, 'auth', '0006_require_contenttypes_0002', '2026-06-27 04:17:41.796531'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2026-06-27 04:17:41.807466'),
(13, 'auth', '0008_alter_user_username_max_length', '2026-06-27 04:17:41.826744'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2026-06-27 04:17:41.843363'),
(15, 'auth', '0010_alter_group_name_max_length', '2026-06-27 04:17:41.861280'),
(16, 'auth', '0011_update_proxy_permissions', '2026-06-27 04:17:41.871529'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2026-06-27 04:17:41.889593'),
(18, 'core', '0001_initial', '2026-06-27 04:17:42.925267'),
(19, 'sessions', '0001_initial', '2026-06-27 04:17:42.964943'),
(20, 'core', '0002_product_image_url', '2026-06-28 07:20:44.564296'),
(21, 'core', '0003_employee_user', '2026-07-02 11:20:08.930119'),
(22, 'core', '0004_customer_user', '2026-07-02 11:22:12.983869');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('5unc6ars945giq9cu9cqs8e2sjwysq96', '.eJxVjEEOwiAQRe_C2hChUjou3fcMZIYZpGogKe3KeHfbpAvdvvf-f6uA65LD2mQOE6urMur0ywjjU8ou-IHlXnWsZZkn0nuiD9v0WFlet6P9O8jY8rYmh8DWAhkWjIkTe7ADC1AajPHUs7EoEMlfuoQubRgc0bl3AIltpz5fICE5OQ:1wfFsj:ECT8od58YA7rUhnRGQ0x0PW7UhBFqwSteo8zAWl0j5I', '2026-07-16 11:47:01.119155'),
('dvbvbgupo4pwr12nuvwnli5ldq6es9qs', '.eJxVjEEOwiAQRe_C2hChUjou3fcMZIYZpGogKe3KeHfbpAvdvvf-f6uA65LD2mQOE6urMur0ywjjU8ou-IHlXnWsZZkn0nuiD9v0WFlet6P9O8jY8rYmh8DWAhkWjIkTe7ADC1AajPHUs7EoEMlfuoQubRgc0bl3AIltpz5fICE5OQ:1wfb3h:oVp_UjTRGe4YIAOoYKyKnJauMY2uAPfhH1NWl5xj_4E', '2026-07-17 10:23:45.081479'),
('mvbbbhephlbbv4tdvrbn7tbq44rh0hl6', '.eJxVjEEOwiAQRe_C2hChUjou3fcMZIYZpGogKe3KeHfbpAvdvvf-f6uA65LD2mQOE6urMur0ywjjU8ou-IHlXnWsZZkn0nuiD9v0WFlet6P9O8jY8rYmh8DWAhkWjIkTe7ADC1AajPHUs7EoEMlfuoQubRgc0bl3AIltpz5fICE5OQ:1wdPXG:8R61iBFePmfC2jM4fCX9UtUJKJ_i-We7-GHa6ZEzXEM', '2026-07-11 09:41:14.947556'),
('t7kehvaoi6yjfy8j1ptq9j1xek3kyh7k', '.eJxVjEEOwiAQRe_C2hChUjou3fcMZIYZpGogKe3KeHfbpAvdvvf-f6uA65LD2mQOE6urMur0ywjjU8ou-IHlXnWsZZkn0nuiD9v0WFlet6P9O8jY8rYmh8DWAhkWjIkTe7ADC1AajPHUs7EoEMlfuoQubRgc0bl3AIltpz5fICE5OQ:1wfaf1:h2slzqJthPkIW-agM-Eyhbk5j9HiQrRRtjXBMSzvc5I', '2026-07-17 09:58:15.628288');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `core_auditlog`
--
ALTER TABLE `core_auditlog`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `core_brand`
--
ALTER TABLE `core_brand`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `core_category`
--
ALTER TABLE `core_category`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `core_customer`
--
ALTER TABLE `core_customer`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `core_employee`
--
ALTER TABLE `core_employee`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `core_expense`
--
ALTER TABLE `core_expense`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `core_product`
--
ALTER TABLE `core_product`
  ADD PRIMARY KEY (`sku`),
  ADD KEY `core_product_brand_id_a97b95f2_fk_core_brand_id` (`brand_id`),
  ADD KEY `core_product_category_id_b9d8ff9f_fk_core_category_id` (`category_id`),
  ADD KEY `core_product_supplier_id_493af3ba_fk_core_supplier_id` (`supplier_id`);

--
-- Indexes for table `core_purchaseitem`
--
ALTER TABLE `core_purchaseitem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_purchaseitem_product_id_29f76f93_fk_core_product_sku` (`product_id`),
  ADD KEY `core_purchaseitem_purchase_order_id_5c4e8596_fk_core_purc` (`purchase_order_id`);

--
-- Indexes for table `core_purchaseorder`
--
ALTER TABLE `core_purchaseorder`
  ADD PRIMARY KEY (`po_no`),
  ADD KEY `core_purchaseorder_supplier_id_0242d2c5_fk_core_supplier_id` (`supplier_id`);

--
-- Indexes for table `core_sale`
--
ALTER TABLE `core_sale`
  ADD PRIMARY KEY (`invoice_no`),
  ADD KEY `core_sale_customer_id_2acb5b23_fk_core_customer_id` (`customer_id`),
  ADD KEY `core_sale_salesman_id_3ce2c67b_fk_core_employee_id` (`salesman_id`);

--
-- Indexes for table `core_saleitem`
--
ALTER TABLE `core_saleitem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_saleitem_product_id_2972cee0_fk_core_product_sku` (`product_id`),
  ADD KEY `core_saleitem_sale_id_ac8b60ae_fk_core_sale_invoice_no` (`sale_id`);

--
-- Indexes for table `core_supplier`
--
ALTER TABLE `core_supplier`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `core_trip`
--
ALTER TABLE `core_trip`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_trip_driver_id_ecc55dbe_fk_core_employee_id` (`driver_id`),
  ADD KEY `core_trip_helper_id_2db0913f_fk_core_employee_id` (`helper_id`);

--
-- Indexes for table `core_tripitem`
--
ALTER TABLE `core_tripitem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_tripitem_product_id_a308957a_fk_core_product_sku` (`product_id`),
  ADD KEY `core_tripitem_trip_id_8016407d_fk_core_trip_id` (`trip_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=81;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `core_auditlog`
--
ALTER TABLE `core_auditlog`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `core_brand`
--
ALTER TABLE `core_brand`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `core_category`
--
ALTER TABLE `core_category`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `core_customer`
--
ALTER TABLE `core_customer`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `core_employee`
--
ALTER TABLE `core_employee`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `core_expense`
--
ALTER TABLE `core_expense`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `core_purchaseitem`
--
ALTER TABLE `core_purchaseitem`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `core_saleitem`
--
ALTER TABLE `core_saleitem`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- AUTO_INCREMENT for table `core_supplier`
--
ALTER TABLE `core_supplier`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `core_trip`
--
ALTER TABLE `core_trip`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `core_tripitem`
--
ALTER TABLE `core_tripitem`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `core_customer`
--
ALTER TABLE `core_customer`
  ADD CONSTRAINT `core_customer_user_id_76763a70_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `core_employee`
--
ALTER TABLE `core_employee`
  ADD CONSTRAINT `core_employee_user_id_938b4b84_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `core_product`
--
ALTER TABLE `core_product`
  ADD CONSTRAINT `core_product_brand_id_a97b95f2_fk_core_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `core_brand` (`id`),
  ADD CONSTRAINT `core_product_category_id_b9d8ff9f_fk_core_category_id` FOREIGN KEY (`category_id`) REFERENCES `core_category` (`id`),
  ADD CONSTRAINT `core_product_supplier_id_493af3ba_fk_core_supplier_id` FOREIGN KEY (`supplier_id`) REFERENCES `core_supplier` (`id`);

--
-- Constraints for table `core_purchaseitem`
--
ALTER TABLE `core_purchaseitem`
  ADD CONSTRAINT `core_purchaseitem_product_id_29f76f93_fk_core_product_sku` FOREIGN KEY (`product_id`) REFERENCES `core_product` (`sku`),
  ADD CONSTRAINT `core_purchaseitem_purchase_order_id_5c4e8596_fk_core_purc` FOREIGN KEY (`purchase_order_id`) REFERENCES `core_purchaseorder` (`po_no`);

--
-- Constraints for table `core_purchaseorder`
--
ALTER TABLE `core_purchaseorder`
  ADD CONSTRAINT `core_purchaseorder_supplier_id_0242d2c5_fk_core_supplier_id` FOREIGN KEY (`supplier_id`) REFERENCES `core_supplier` (`id`);

--
-- Constraints for table `core_sale`
--
ALTER TABLE `core_sale`
  ADD CONSTRAINT `core_sale_customer_id_2acb5b23_fk_core_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `core_customer` (`id`),
  ADD CONSTRAINT `core_sale_salesman_id_3ce2c67b_fk_core_employee_id` FOREIGN KEY (`salesman_id`) REFERENCES `core_employee` (`id`);

--
-- Constraints for table `core_saleitem`
--
ALTER TABLE `core_saleitem`
  ADD CONSTRAINT `core_saleitem_product_id_2972cee0_fk_core_product_sku` FOREIGN KEY (`product_id`) REFERENCES `core_product` (`sku`),
  ADD CONSTRAINT `core_saleitem_sale_id_ac8b60ae_fk_core_sale_invoice_no` FOREIGN KEY (`sale_id`) REFERENCES `core_sale` (`invoice_no`);

--
-- Constraints for table `core_trip`
--
ALTER TABLE `core_trip`
  ADD CONSTRAINT `core_trip_driver_id_ecc55dbe_fk_core_employee_id` FOREIGN KEY (`driver_id`) REFERENCES `core_employee` (`id`),
  ADD CONSTRAINT `core_trip_helper_id_2db0913f_fk_core_employee_id` FOREIGN KEY (`helper_id`) REFERENCES `core_employee` (`id`);

--
-- Constraints for table `core_tripitem`
--
ALTER TABLE `core_tripitem`
  ADD CONSTRAINT `core_tripitem_product_id_a308957a_fk_core_product_sku` FOREIGN KEY (`product_id`) REFERENCES `core_product` (`sku`),
  ADD CONSTRAINT `core_tripitem_trip_id_8016407d_fk_core_trip_id` FOREIGN KEY (`trip_id`) REFERENCES `core_trip` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
