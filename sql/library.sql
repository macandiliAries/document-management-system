SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `library`
--
CREATE DATABASE IF NOT EXISTS `library` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `library`;

-- --------------------------------------------------------

--
-- Table structure for table `docs`
--

DROP TABLE IF EXISTS `docs`;
CREATE TABLE IF NOT EXISTS `docs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `authorId` int(11) NOT NULL,
  `docTypeId` int(11) NOT NULL,
  `statusId` int(11) NOT NULL,
  `approverId` int(11) DEFAULT NULL,
  `effectiveDate` datetime NOT NULL,
  `contents` longtext NOT NULL,
  `lastEditedBy` int(11) DEFAULT NULL,
  `lastEditedOn` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_DocType` (`docTypeId`),
  KEY `FK_DocStatus` (`statusId`),
  KEY `FK_AuthorDoc` (`authorId`),
  KEY `FK_ApproverDoc` (`approverId`),
  KEY `FK_DocEditedBy` (`lastEditedBy`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;

--
-- RELATIONSHIPS FOR TABLE `docs`:
--   `approverId`
--       `users` -> `id`
--   `lastEditedBy`
--       `users` -> `id`
--   `statusId`
--       `doc_status_types` -> `id`
--   `docTypeId`
--       `doc_types` -> `id`
--   `authorId`
--       `users` -> `id`
--

--
-- Truncate table before insert `docs`
--

TRUNCATE TABLE `docs`;
--
-- Dumping data for table `docs`
--

INSERT INTO `docs` (`id`, `title`, `authorId`, `docTypeId`, `statusId`, `approverId`, `effectiveDate`, `contents`, `lastEditedBy`, `lastEditedOn`) VALUES
(1, 'Test Document 1', 1, 1, 3, 1, '2022-06-09 22:17:04', '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p><p>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>', 1, '2022-06-09 22:16:45'),
(2, 'Test Document 2', 1, 2, 2, NULL, '0000-00-00 00:00:00', '<p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.</p><p>Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>', NULL, '0000-00-00 00:00:00'),
(3, 'Test Document 3', 1, 3, 3, 1, '2022-06-09 22:13:06', '<p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.</p><p>Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.</p>', 1, '2022-06-09 22:11:56'),
(4, 'Test Document 4', 1, 4, 4, 1, '2022-06-09 22:13:30', '<pneque porro=\"\" quisquam=\"\" est,=\"\" qui=\"\" dolorem=\"\" ipsum=\"\" quia=\"\" dolor=\"\" sit=\"\" amet,=\"\" consectetur,=\"\" adipisci=\"\" velit,=\"\" sed=\"\" non=\"\" numquam=\"\" eius=\"\" modi=\"\" tempora=\"\" incidunt=\"\" ut=\"\" labore=\"\" et=\"\" dolore=\"\" magnam=\"\" aliquam=\"\" quaerat=\"\" voluptatem.<=\"\" p=\"\"></pneque>', 1, '2022-06-09 22:12:02'),
(5, 'Test Document 5', 1, 5, 6, 1, '2022-06-09 22:13:47', '<p>Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur?</p><p>Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?</p>', 1, '2022-06-09 22:13:56'),
(6, 'Test Document 6', 1, 3, 5, 1, '2022-06-09 22:14:32', '<p>At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga</p>', 1, '2022-06-09 22:14:50'),
(7, 'Test Document 7', 1, 2, 1, NULL, '0000-00-00 00:00:00', '<p>Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus.</p>', NULL, '0000-00-00 00:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `doc_revisions`
--

DROP TABLE IF EXISTS `doc_revisions`;
CREATE TABLE IF NOT EXISTS `doc_revisions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `docId` int(11) NOT NULL,
  `revisionNumber` varchar(255) NOT NULL,
  `dateRevised` datetime NOT NULL,
  `significantChanges` varchar(255) DEFAULT NULL,
  `reviserId` int(11) DEFAULT NULL,
  `isApproved` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `FK_RevisionDoc` (`docId`),
  KEY `FK_RevisionUser` (`reviserId`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4;

--
-- RELATIONSHIPS FOR TABLE `doc_revisions`:
--   `docId`
--       `docs` -> `id`
--   `reviserId`
--       `users` -> `id`
--

--
-- Truncate table before insert `doc_revisions`
--

TRUNCATE TABLE `doc_revisions`;
--
-- Dumping data for table `doc_revisions`
--

INSERT INTO `doc_revisions` (`id`, `docId`, `revisionNumber`, `dateRevised`, `significantChanges`, `reviserId`, `isApproved`) VALUES
(1, 1, 'v1.0', '2022-05-04 20:17:31', 'Initial creation of the document.', 1, 1),
(2, 2, 'v1.0', '2022-05-05 20:17:31', 'Initial creation of the document.', 1, 1),
(3, 3, 'v1.0', '2022-05-05 20:17:31', 'Initial creation of the document.', 1, 1),
(4, 4, 'v1.0', '2022-05-05 20:17:31', 'Initial creation of the document.', 1, 1),
(5, 5, 'v1.0', '2022-05-05 20:17:31', 'Initial creation of the document.', 1, 1),
(6, 6, 'v1.0', '2022-05-05 20:17:31', 'Initial creation of the document.', 1, 1),
(7, 7, 'v1.0', '2022-05-05 20:17:31', 'Initial creation of the document.', 1, 1),
(8, 6, 'v1.1', '2022-06-09 22:15:09', 'Revision for Test Document 6', 1, 0),
(9, 1, 'v1.1', '2022-06-09 22:17:00', 'Test revision for the first document.', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `doc_status_types`
--

DROP TABLE IF EXISTS `doc_status_types`;
CREATE TABLE IF NOT EXISTS `doc_status_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `statusType` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;

--
-- RELATIONSHIPS FOR TABLE `doc_status_types`:
--

--
-- Truncate table before insert `doc_status_types`
--

TRUNCATE TABLE `doc_status_types`;
--
-- Dumping data for table `doc_status_types`
--

INSERT INTO `doc_status_types` (`id`, `statusType`) VALUES
(1, 'Draft'),
(2, 'For Review'),
(3, 'Approved'),
(4, 'For Revision'),
(5, 'For Revision Review'),
(6, 'Draft Revision');

-- --------------------------------------------------------

--
-- Table structure for table `doc_types`
--

DROP TABLE IF EXISTS `doc_types`;
CREATE TABLE IF NOT EXISTS `doc_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `docType` varchar(50) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

--
-- RELATIONSHIPS FOR TABLE `doc_types`:
--

--
-- Truncate table before insert `doc_types`
--

TRUNCATE TABLE `doc_types`;
--
-- Dumping data for table `doc_types`
--

INSERT INTO `doc_types` (`id`, `docType`) VALUES
(1, 'Journal'),
(2, 'Report'),
(3, 'Instruction'),
(4, 'Article'),
(5, 'Others');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `user_type` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `address` varchar(255) NOT NULL,
  `contact_num` varchar(13) NOT NULL,
  `status` varchar(10) NOT NULL DEFAULT 'active',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;

--
-- RELATIONSHIPS FOR TABLE `users`:
--

--
-- Truncate table before insert `users`
--

TRUNCATE TABLE `users`;
--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `full_name`, `user_type`, `email`, `address`, `contact_num`, `status`) VALUES
(1, 'admin', 'gAAAAABiodjoKqJyHaC7tMe6r8XVN-1CFYFEarlH8L59XMDiOS7grovJtsS9-tMlwUbnZmbm5otnWAWfksI-2RvWCMbxpVXDNg==', 'John Doe', 'Super Admin', 'john.doe@test.com', 'Quezon City', '09123456789', 'active'),
(2, 'admin2', 'gAAAAABiodjoKqJyHaC7tMe6r8XVN-1CFYFEarlH8L59XMDiOS7grovJtsS9-tMlwUbnZmbm5otnWAWfksI-2RvWCMbxpVXDNg==', 'Jane Doe', 'Admin', 'jane.doe@test.com', 'Davao City', '09123456789', 'active'),
(3, 'admin3', 'gAAAAABiodjoKqJyHaC7tMe6r8XVN-1CFYFEarlH8L59XMDiOS7grovJtsS9-tMlwUbnZmbm5otnWAWfksI-2RvWCMbxpVXDNg==', 'Rosa Parks', 'Super Admin', 'rosa.parks@test.com', 'Pasig City', '09123456789', 'active'),
(4, 'admin4', 'gAAAAABiodjoKqJyHaC7tMe6r8XVN-1CFYFEarlH8L59XMDiOS7grovJtsS9-tMlwUbnZmbm5otnWAWfksI-2RvWCMbxpVXDNg==', 'Martin Luther Queen', 'Admin', 'mlqueen@test.com', 'Mandaluyong City', '09123456789', 'active'),
(5, 'admin5', 'gAAAAABiodjoKqJyHaC7tMe6r8XVN-1CFYFEarlH8L59XMDiOS7grovJtsS9-tMlwUbnZmbm5otnWAWfksI-2RvWCMbxpVXDNg==', 'Carl Marks', 'Admin', 'carl.marks@test.com', 'Makati City', '09123456789', 'active'),
(6, 'admin6', 'gAAAAABiodjoKqJyHaC7tMe6r8XVN-1CFYFEarlH8L59XMDiOS7grovJtsS9-tMlwUbnZmbm5otnWAWfksI-2RvWCMbxpVXDNg==', 'Marie Reute', 'Admin', 'marie.reute@test.com', 'Cavite City', '09123456789', 'active');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `docs`
--
ALTER TABLE `docs`
  ADD CONSTRAINT `FK_ApproverDoc` FOREIGN KEY (`approverId`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `FK_DocEditedBy` FOREIGN KEY (`lastEditedBy`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `FK_DocStatus` FOREIGN KEY (`statusId`) REFERENCES `doc_status_types` (`id`),
  ADD CONSTRAINT `FK_DocType` FOREIGN KEY (`docTypeId`) REFERENCES `doc_types` (`id`),
  ADD CONSTRAINT `FK_UserDoc` FOREIGN KEY (`authorId`) REFERENCES `users` (`id`);

--
-- Constraints for table `doc_revisions`
--
ALTER TABLE `doc_revisions`
  ADD CONSTRAINT `FK_RevisionDoc` FOREIGN KEY (`docId`) REFERENCES `docs` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `FK_RevisionUser` FOREIGN KEY (`reviserId`) REFERENCES `users` (`id`);
COMMIT;

--
-- Create the root user.
--
CREATE USER IF NOT EXISTS 'library_user_1'@'localhost' IDENTIFIED BY 'uj17JpqspOIPr_MAy8sFs2vIyPpPdMHsg_WrKNGx5f8=';
GRANT ALL PRIVILEGES ON library.* TO 'library_user_1'@'localhost';
FLUSH PRIVILEGES;