-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: job_tracker
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `job_tracker`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `job_tracker` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `job_tracker`;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('e5aa7f64380b');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `applications`
--

DROP TABLE IF EXISTS `applications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `applications` (
  `application_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `comapany_id` int DEFAULT NULL,
  `role_title` varchar(30) DEFAULT NULL,
  `status` enum('applied','screening','interviewing','offer','rejected','withdrawn') NOT NULL,
  `applied_date` date DEFAULT NULL,
  `job_url` varchar(250) DEFAULT NULL,
  `notes` text,
  PRIMARY KEY (`application_id`),
  KEY `user_id` (`user_id`),
  KEY `comapany_id` (`comapany_id`),
  KEY `ix_applications_application_id` (`application_id`),
  CONSTRAINT `applications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `applications_ibfk_2` FOREIGN KEY (`comapany_id`) REFERENCES `companies` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `applications`
--

LOCK TABLES `applications` WRITE;
/*!40000 ALTER TABLE `applications` DISABLE KEYS */;
INSERT INTO `applications` VALUES (1,9,14,'SDE','rejected','2026-07-30','https://careers.cred.club/openings',NULL),(2,9,8,'Python Backend Engineer','rejected','2026-08-01',NULL,NULL),(3,9,18,'AI Engineer','offer','2026-08-01',NULL,NULL),(4,10,19,'AI developer','offer','2026-08-01',NULL,NULL),(5,10,20,'backend engineer','interviewing','2026-08-01',NULL,NULL),(6,12,24,'BT service engineer','interviewing','2026-08-02',NULL,NULL),(7,9,2,'AI reaearch and applied AI','rejected','2026-08-02',NULL,NULL),(8,9,26,'fastapi engineer','rejected','2026-08-03',NULL,'4-6lpa'),(9,9,27,'Gen AI engineer','applied','2026-08-08',NULL,NULL),(10,9,28,'ml engineer','screening','2026-08-09',NULL,'one test done'),(11,9,28,'data analyst','applied','2026-08-09',NULL,'test link yet to arrive');
/*!40000 ALTER TABLE `applications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `companies`
--

DROP TABLE IF EXISTS `companies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `companies` (
  `company_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `company_name` varchar(30) DEFAULT NULL,
  `NOTE` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`company_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_companies_company_id` (`company_id`),
  CONSTRAINT `companies_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `companies`
--

LOCK TABLES `companies` WRITE;
/*!40000 ALTER TABLE `companies` DISABLE KEYS */;
INSERT INTO `companies` VALUES (1,9,'Rubrik','Pays well. Salary for me : 15 LPA + HRA.'),(2,9,'Google Deepmind','prepare for Graphs/Trees'),(3,9,'Microsoft','Practice SQL joins'),(4,9,'Postman','Explain REST principles'),(5,9,'Icertis','Revise FastAPI DI'),(6,9,'Haptik','Learn Redis caching'),(7,9,'Thoughtworks','Focus on clean code'),(8,9,'PhonePe','Optimize SQL queries'),(9,9,'Razorpay','System design basics'),(10,9,'Flipkart','Binary tree problems'),(11,9,'BrowserStack','Docker networking'),(12,9,'Zoho','OOP interview ques'),(13,9,'Nagarro','JWT authentication'),(14,9,'CRED','Design URL shortener'),(15,6,'Falana','dhimkana'),(17,9,'ZS','Prepare for SQL and query optimization'),(18,9,'Visteon','current company but different role of AI'),(19,10,'ANPA','Ai developer'),(20,10,'google',''),(21,11,'mod 1',''),(22,11,'mod 2',''),(23,11,'mod 3',''),(24,12,'Noise','BT services company'),(25,9,'Google Deepmind','for AI research role'),(26,9,'Novago','asked for referral from linkedin'),(27,9,'cube','linkedin applied'),(28,9,'IBM','ml engineer');
/*!40000 ALTER TABLE `companies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interviews`
--

DROP TABLE IF EXISTS `interviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interviews` (
  `interview_id` int NOT NULL AUTO_INCREMENT,
  `application_id` int DEFAULT NULL,
  `round_name` varchar(20) DEFAULT NULL,
  `scheduled_at` datetime DEFAULT NULL,
  PRIMARY KEY (`interview_id`),
  KEY `application_id` (`application_id`),
  KEY `ix_interviews_interview_id` (`interview_id`),
  CONSTRAINT `interviews_ibfk_1` FOREIGN KEY (`application_id`) REFERENCES `applications` (`application_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interviews`
--

LOCK TABLES `interviews` WRITE;
/*!40000 ALTER TABLE `interviews` DISABLE KEYS */;
INSERT INTO `interviews` VALUES (1,2,'HR','2026-08-07 10:00:00');
/*!40000 ALTER TABLE `interviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(30) NOT NULL,
  `hashed_password` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `ix_users_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (6,'admin@gmail.com','$2b$12$EgBptxQ6dEFLMhINt7Jyruv/g8ohJ4SFHbAdtkKqXfPuQkA25rOby','2026-07-28 14:37:58'),(7,'company@gmail.com','$2b$12$N2Su.Z8Sq5veCRDX6XIWt.BckIiP0D3FPxaA5IXSQlz7bxSTnJmLq','2026-07-28 15:49:03'),(9,'anmol1@gmail.com','$2b$12$7/45gwIQk23N1CN.GVqDh.i8negogfpaW.hpqJtyR9i7P6BA2b8O6','2026-07-29 13:07:55'),(10,'trial@gmail.com','$2b$12$EdSLy/9x6CtQu2af.31dYu2Bs6JDEL6fTDEwDVepol64L1irnDghi','2026-08-01 13:29:12'),(11,'mod@gmail.com','$2b$12$YV6TdubEns32m.obhLHFvuY6VolR.9RQsJY0To3AHIdXPY9s4bwcm','2026-08-01 13:43:18'),(12,'reyansh@gmail.com','$2b$12$xkCKkGsjCwfzkSlImwYG3OZqhubykB8IfDQ1F9khfQFwDYfren.zy','2026-08-02 09:41:40'),(13,'anmolpatalay@gmail.com','$2b$12$xh8vhXIALiGG/P2vAOXDdumxbN5fikhy4Sram/gt8DLTKLXptWGSe','2026-08-02 09:47:23');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-15  0:46:37
