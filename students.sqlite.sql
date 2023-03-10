BEGIN TRANSACTION;
CREATE TABLE "student" (
	`id`	TEXT,
	`name`	TEXT,
	`surname`	TEXT,
	PRIMARY KEY(`id`)
);
CREATE TABLE "exam_score" (
	`student_id`	TEXT,
	`exam_id`	TEXT,
	`score`	REAL,
	PRIMARY KEY(`student_id`,`exam_id`)
);
CREATE TABLE "exam" (
	`exam_id`	TEXT,
	`exam_name`	TEXT,
	PRIMARY KEY(`exam_id`)
);
CREATE INDEX `student_index` ON `student` (`id` )




;
COMMIT;