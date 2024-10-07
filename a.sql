BEGIN;
--
-- Create model Risk
--
CREATE TABLE "risk_manager_risk" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "risk_description" varchar(500) NULL, "risk_type" varchar(50) NULL, "responsibility" varchar(50) NULL, "recommendation" varchar(1000) NULL, "impact" varchar(50) NULL, "impact_description" varchar(500) NULL, "probability" varchar(50) NULL, "timeline" varchar(50) NULL, "response_status" varchar(50) NULL, "risk_status" varchar(50) NULL, "completed_actions" varchar(500) NULL, "future_actions" varchar(500) NULL, "date_reported" varchar(50) NULL, "last_update" datetime NULL, "created_by" varchar(50) NULL, "date_created" datetime NULL, "updated_by" varchar(50) NULL);
--
-- Create model RiskCategory
--
CREATE TABLE "risk_manager_riskcategory" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL, "created_by" varchar(50) NOT NULL, "date_created" datetime NOT NULL);
--
-- Create model RiskStatus
--
CREATE TABLE "risk_manager_riskstatus" ("status_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "status" varchar(50) NULL, "created_by" varchar(50) NULL, "date_created" datetime NULL);
--
-- Create model RiskAssessment
--
CREATE TABLE "risk_manager_riskassessment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "risk_type" varchar(50) NOT NULL, "impact" varchar(50) NOT NULL, "impact_description" varchar(50) NOT NULL, "probability" varchar(50) NOT NULL, "timeline" varchar(50) NOT NULL, "response_status" varchar(50) NOT NULL, "risk_status" varchar(50) NOT NULL, "completed_actions" varchar(50) NOT NULL, "future_actions" varchar(50) NOT NULL, "created_by" varchar(50) NOT NULL, "date_created" datetime NOT NULL, "risk_id" bigint NOT NULL REFERENCES "risk_manager_risk" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model RiskAction
--
CREATE TABLE "risk_manager_riskaction" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "action_type" varchar(255) NOT NULL, "risk_status" varchar(255) NOT NULL, "completed_actions" varchar(500) NOT NULL, "future_actions" varchar(500) NOT NULL, "created_by" varchar(50) NOT NULL, "date_created" date NOT NULL, "risk_id" bigint NOT NULL REFERENCES "risk_manager_risk" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "risk_manager_riskassessment_risk_id_a308713c" ON "risk_manager_riskassessment" ("risk_id");
CREATE INDEX "risk_manager_riskaction_risk_id_1ba12249" ON "risk_manager_riskaction" ("risk_id");
COMMIT;
