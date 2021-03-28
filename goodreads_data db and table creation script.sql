-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: localhost    Database: goodreads_data
-- ------------------------------------------------------
-- Server version	8.0.21

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
-- Database
--
DROP DATABASE IF EXISTS  goodreads_data;
CREATE DATABASE goodreads_data;
USE goodreads_data;

--
-- Table structure for table `authors`
--

DROP TABLE IF EXISTS `authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `book_updates`
--

DROP TABLE IF EXISTS `book_updates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_updates` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rating` decimal(3,2) DEFAULT NULL,
  `qty_ratings` int DEFAULT NULL,
  `qty_reviews` int DEFAULT NULL,
  `scrape_datetime` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `descriptions`
--

DROP TABLE IF EXISTS `descriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `descriptions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `description` varchar(10000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `edition_author_mapping`
--

DROP TABLE IF EXISTS `edition_author_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `edition_author_mapping` (
  `edition_id` int DEFAULT NULL,
  `author_id` int DEFAULT NULL,
  KEY `edition_id` (`edition_id`),
  KEY `author_id` (`author_id`),
  CONSTRAINT `edition_author_mapping_ibfk_1` FOREIGN KEY (`edition_id`) REFERENCES `editions` (`id`),
  CONSTRAINT `edition_author_mapping_ibfk_2` FOREIGN KEY (`author_id`) REFERENCES `authors` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `edition_genre_mapping`
--

DROP TABLE IF EXISTS `edition_genre_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `edition_genre_mapping` (
  `edition_id` int DEFAULT NULL,
  `genre_id` int DEFAULT NULL,
  KEY `edition_id` (`edition_id`),
  KEY `genre_id` (`genre_id`),
  CONSTRAINT `edition_genre_mapping_ibfk_1` FOREIGN KEY (`edition_id`) REFERENCES `editions` (`id`),
  CONSTRAINT `edition_genre_mapping_ibfk_2` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `edition_series_mapping`
--

DROP TABLE IF EXISTS `edition_series_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `edition_series_mapping` (
  `edition_id` int DEFAULT NULL,
  `series_id` int DEFAULT NULL,
  KEY `edition_id` (`edition_id`),
  KEY `series_id` (`series_id`),
  CONSTRAINT `edition_series_mapping_ibfk_1` FOREIGN KEY (`edition_id`) REFERENCES `editions` (`id`),
  CONSTRAINT `edition_series_mapping_ibfk_2` FOREIGN KEY (`series_id`) REFERENCES `series` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `editions`
--

DROP TABLE IF EXISTS `editions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `editions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `goodreads_id` varchar(250) DEFAULT NULL,
  `isbn` varchar(13) DEFAULT NULL,
  `title` varchar(250) DEFAULT NULL,
  `format` varchar(250) DEFAULT NULL,
  `number_in_series` varchar(250) DEFAULT NULL,
  `release_date` varchar(10) DEFAULT NULL,
  `first_published_date` varchar(10) DEFAULT NULL,
  `qty_rpages` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `goodreads_id` (`goodreads_id`),
  KEY `isbn` (`isbn`),
  CONSTRAINT `editions_ibfk_1` FOREIGN KEY (`goodreads_id`) REFERENCES `openlibrary_goodreads` (`goodreads_id`),
  CONSTRAINT `editions_ibfk_2` FOREIGN KEY (`isbn`) REFERENCES `nyt_bestseller_isbns` (`isbn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `genres`
--

DROP TABLE IF EXISTS `genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genres` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lists`
--

DROP TABLE IF EXISTS `lists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lists` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(250) DEFAULT NULL,
  `details` varchar(250) DEFAULT NULL,
  `url` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `url` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nyt_bestseller_isbn_list_mapping`
--

DROP TABLE IF EXISTS `nyt_bestseller_isbn_list_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nyt_bestseller_isbn_list_mapping` (
  `lists_id` int DEFAULT NULL,
  `isbn` varchar(13) DEFAULT NULL,
  KEY `lists_id` (`lists_id`),
  KEY `isbn` (`isbn`),
  CONSTRAINT `nyt_bestseller_isbn_list_mapping_ibfk_1` FOREIGN KEY (`lists_id`) REFERENCES `nyt_bestseller_lists` (`id`),
  CONSTRAINT `nyt_bestseller_isbn_list_mapping_ibfk_2` FOREIGN KEY (`isbn`) REFERENCES `nyt_bestseller_isbns` (`isbn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nyt_bestseller_isbns`
--

DROP TABLE IF EXISTS `nyt_bestseller_isbns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nyt_bestseller_isbns` (
  `isbn` varchar(13) NOT NULL,
  PRIMARY KEY (`isbn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nyt_bestseller_lists`
--

DROP TABLE IF EXISTS `nyt_bestseller_lists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nyt_bestseller_lists` (
  `id` int NOT NULL AUTO_INCREMENT,
  `list_name_encoded` varchar(250) DEFAULT NULL,
  `date` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `openlibrary_book`
--

DROP TABLE IF EXISTS `openlibrary_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `openlibrary_book` (
  `id` int NOT NULL AUTO_INCREMENT,
  `openlibrary_id` varchar(50) DEFAULT NULL,
  `title` varchar(250) DEFAULT NULL,
  `author` varchar(50) DEFAULT NULL,
  `edition_count` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `openlibrary_goodreads`
--

DROP TABLE IF EXISTS `openlibrary_goodreads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `openlibrary_goodreads` (
  `goodreads_id` varchar(250) NOT NULL,
  PRIMARY KEY (`goodreads_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `openlibrary_goodreads_mapping`
--

DROP TABLE IF EXISTS `openlibrary_goodreads_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `openlibrary_goodreads_mapping` (
  `open_library_book_id` int DEFAULT NULL,
  `goodreads_id` varchar(250) DEFAULT NULL,
  KEY `open_library_book_id` (`open_library_book_id`),
  KEY `goodreads_id` (`goodreads_id`),
  CONSTRAINT `openlibrary_goodreads_mapping_ibfk_1` FOREIGN KEY (`open_library_book_id`) REFERENCES `openlibrary_book` (`id`),
  CONSTRAINT `openlibrary_goodreads_mapping_ibfk_2` FOREIGN KEY (`goodreads_id`) REFERENCES `openlibrary_goodreads` (`goodreads_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `openlibrary_isbn`
--

DROP TABLE IF EXISTS `openlibrary_isbn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `openlibrary_isbn` (
  `isbn` varchar(13) NOT NULL,
  PRIMARY KEY (`isbn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `openlibrary_isbn_mapping`
--

DROP TABLE IF EXISTS `openlibrary_isbn_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `openlibrary_isbn_mapping` (
  `open_library_book_id` int DEFAULT NULL,
  `isbn` varchar(13) DEFAULT NULL,
  KEY `open_library_book_id` (`open_library_book_id`),
  KEY `isbn` (`isbn`),
  CONSTRAINT `openlibrary_isbn_mapping_ibfk_1` FOREIGN KEY (`open_library_book_id`) REFERENCES `openlibrary_book` (`id`),
  CONSTRAINT `openlibrary_isbn_mapping_ibfk_2` FOREIGN KEY (`isbn`) REFERENCES `openlibrary_isbn` (`isbn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `openlibrary_languages`
--

DROP TABLE IF EXISTS `openlibrary_languages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `openlibrary_languages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `language` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `openlibrary_languages_mapping`
--

DROP TABLE IF EXISTS `openlibrary_languages_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `openlibrary_languages_mapping` (
  `open_library_book_id` int DEFAULT NULL,
  `language_id` int DEFAULT NULL,
  KEY `open_library_book_id` (`open_library_book_id`),
  KEY `language_id` (`language_id`),
  CONSTRAINT `openlibrary_languages_mapping_ibfk_1` FOREIGN KEY (`open_library_book_id`) REFERENCES `openlibrary_book` (`id`),
  CONSTRAINT `openlibrary_languages_mapping_ibfk_2` FOREIGN KEY (`language_id`) REFERENCES `openlibrary_languages` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `openlibrary_publish_years`
--

DROP TABLE IF EXISTS `openlibrary_publish_years`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `openlibrary_publish_years` (
  `id` int NOT NULL AUTO_INCREMENT,
  `year` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `openlibrary_publish_years_mapping`
--

DROP TABLE IF EXISTS `openlibrary_publish_years_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `openlibrary_publish_years_mapping` (
  `open_library_book_id` int DEFAULT NULL,
  `publish_year_id` int DEFAULT NULL,
  KEY `open_library_book_id` (`open_library_book_id`),
  KEY `publish_year_id` (`publish_year_id`),
  CONSTRAINT `openlibrary_publish_years_mapping_ibfk_1` FOREIGN KEY (`open_library_book_id`) REFERENCES `openlibrary_book` (`id`),
  CONSTRAINT `openlibrary_publish_years_mapping_ibfk_2` FOREIGN KEY (`publish_year_id`) REFERENCES `openlibrary_publish_years` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `series`
--

DROP TABLE IF EXISTS `series`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `series` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `update_description_mapping`
--

DROP TABLE IF EXISTS `update_description_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `update_description_mapping` (
  `book_update_id` int DEFAULT NULL,
  `description_id` int DEFAULT NULL,
  KEY `book_update_id` (`book_update_id`),
  KEY `description_id` (`description_id`),
  CONSTRAINT `update_description_mapping_ibfk_1` FOREIGN KEY (`book_update_id`) REFERENCES `book_updates` (`id`),
  CONSTRAINT `update_description_mapping_ibfk_2` FOREIGN KEY (`description_id`) REFERENCES `descriptions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `update_edition_mapping`
--

DROP TABLE IF EXISTS `update_edition_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `update_edition_mapping` (
  `book_update_id` int DEFAULT NULL,
  `edition_id` int DEFAULT NULL,
  KEY `book_update_id` (`book_update_id`),
  KEY `edition_id` (`edition_id`),
  CONSTRAINT `update_edition_mapping_ibfk_1` FOREIGN KEY (`book_update_id`) REFERENCES `book_updates` (`id`),
  CONSTRAINT `update_edition_mapping_ibfk_2` FOREIGN KEY (`edition_id`) REFERENCES `editions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `update_list_mapping`
--

DROP TABLE IF EXISTS `update_list_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `update_list_mapping` (
  `book_update_id` int DEFAULT NULL,
  `list_id` int DEFAULT NULL,
  KEY `book_update_id` (`book_update_id`),
  KEY `list_id` (`list_id`),
  CONSTRAINT `update_list_mapping_ibfk_1` FOREIGN KEY (`book_update_id`) REFERENCES `book_updates` (`id`),
  CONSTRAINT `update_list_mapping_ibfk_2` FOREIGN KEY (`list_id`) REFERENCES `lists` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-28 17:50:30
