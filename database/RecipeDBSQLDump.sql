-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema recipe
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema recipe
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `recipe` DEFAULT CHARACTER SET utf8 ;
USE `recipe` ;

-- -----------------------------------------------------
-- Table `recipe`.`recipe`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `recipe`.`recipe` ;

CREATE TABLE IF NOT EXISTS `recipe`.`recipe` (
  `name` VARCHAR(45) NULL,
  `prep` INT NULL,
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(500) NULL,
  `instruction` VARCHAR(2000) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `recipe`.`ingredient`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `recipe`.`ingredient` ;

CREATE TABLE IF NOT EXISTS `recipe`.`ingredient` (
  `iname` VARCHAR(45) NULL,
  `amount` INT NULL,
  `units` VARCHAR(45) NULL,
  `id` INT NOT NULL AUTO_INCREMENT,
  `recipe_id` INT NOT NULL,
  PRIMARY KEY (`id`, `recipe_id`),
  INDEX `fk_ingredient_recipe_idx` (`recipe_id` ASC),
  CONSTRAINT `fk_ingredient_recipe`
    FOREIGN KEY (`recipe_id`)
    REFERENCES `recipe`.`recipe` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
