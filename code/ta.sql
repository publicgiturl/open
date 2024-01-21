# 삭제 쿼리
-- TRUNCATE TABLE s1;
-- TRUNCATE TABLE s2_bb;
-- TRUNCATE TABLE s2_po;
-- TRUNCATE TABLE s3_po;
-- TRUNCATE TABLE s3_bb;
-- TRUNCATE TABLE imagetbl;

# 항공
-- SELECT SUM(BB), COUNT(BB) FROM s1;
-- SELECT SUM(class01), SUM(class02),SUM(class03),SUM(class04),SUM(class05),SUM(class06),SUM(class07),SUM(class08),SUM(class09),SUM(class10),SUM(class11),SUM(class12),SUM(class13),SUM(class14),SUM(class15),SUM(class16),SUM(class17),SUM(class18),SUM(class19),SUM(class20),SUM(class21),SUM(class22) FROM s1;

# 공사
#SELECT SUM(class30),SUM(class31),SUM(class32),SUM(class33),SUM(class34),SUM(class35),SUM(class36),SUM(class37),SUM(class37),SUM(class38),SUM(class39),SUM(class40),SUM(class41),SUM(class42),SUM(class43),SUM(class44),SUM(class45) FROM s2_bb;
#SELECT SUM(class29),SUM(class28),SUM(class27),SUM(class26),SUM(class25),SUM(class24),SUM(class23),SUM(class22),SUM(class21),SUM(class20),SUM(class19),SUM(class18),SUM(class17),SUM(class16),SUM(class15),SUM(class14),SUM(class13) FROM s2_bb;
#SELECT SUM(class12),SUM(class11),SUM(class10),SUM(class09),SUM(class08),SUM(class07),SUM(class06),SUM(class05),SUM(class04),SUM(class03),SUM(class02),SUM(class01) FROM s2_bb; 
#SELECT SUM(class01+class02+class03+class04+class05+class06+class07+class08) AS '안전보호구' FROM s2_bb;
#SELECT SUM(class01+class02+class03+class04+class05+class06+class07+class08) AS '안전보호구' FROM s2_po;
#SELECT SUM(class09+class10+class11+class12+class13+class14+class15+class16+class17+class18+class19) AS '중장비' FROM s2_bb;
#SELECT SUM(class20+ class21) AS '구조물' FROM s2_bb;
#SELECT SUM(class22+class23+class24+class25+class26+class27+class28+class29) AS '설치물' FROM s2_bb;
#SELECT SUM(class30+ class31) AS '비계' FROM s2_bb;
#SELECT SUM(class32+class33+class34+class35+class36+class37+class38+class39+class40+class41+class42+class43+class44+class45) AS '자재및공구' FROM s2_bb;
-- SELECT SUM(PO), COUNT(PO) FROM s2_po;
-- SELECT SUM(BB), COUNT(BB) FROM s2_bb;
-- COMMIT;
# 화재
-- SELECT count(BB), SUM(BB) FROM s3_bb; 
-- SELECT count(PO), SUM(PO) FROM s3_po;
-- SELECT SUM(class01), SUM(class02),SUM(class03),SUM(class04),SUM(class05),SUM(class06),SUM(class07),SUM(class08),SUM(class09),SUM(class10) FROM s3_bb;
-- SELECT SUM(class01), SUM(class02),SUM(class03),SUM(class04),SUM(class05),SUM(class06),SUM(class07),SUM(class08),SUM(class09),SUM(class10) FROM s3_po;

# 기타
-- SELECT SUM(class04) FROM s2_bb WHERE class04 != 0;
-- SELECT * FROM s2_bb WHERE class04 != 1 AND class04 != 0;
-- SELECT * FROM s3_po WHERE class07 != 0 ;


-- SELECT * FROM imagetbl WHERE Img_Name = 'S2-N1105M07655.jpg';
-- SELECT * FROM INNODB_LOCKS;
-- select Work_User, Work_Yn, date_format(Work_Date, '%Y-%m-%d'), count(*) from workhistory group by Date_Format(Work_Date, '%Y-%m-%d'), Work_User HAVING Work_Yn = 'Y';

-- SELECT Date_Format(Work_Date, '%Y-%m-%d'), Work_User, count(*) FROM imagetbl group by Date_Format(Work_Date, '%Y-%m-%d'), Work_User, Work_Yn HAVING Work_Yn = 'Y';

-- SELECT * FROM imagetbl WHERE Img_Name = 'S2-N0508M25013.jpg'

UPDATE imagetbl SET Work_Yn = 'E' WHERE Work_User = 'humanf1' AND Work_date ='2021-02-03'; 
-- SELECT * FROM imagetbl WHERE Work_User = 'humanf19' AND Work_Yn='N';mysqlinformation_schema
-- SELECT * FROM imagetbl WHERE Img_Name = 'S2-N0307M00009.jpg';
-- UPDATE imagetbl SET Work_User = 'humanf1' WHERE (Img_Path = '20210122') AND (Work_User IS NULL) LIMIT 5000;
-- DELETE FROM imagetbl where Img_Path = '20210114';
-- UPDATE imagetbl SET Img_Path = '20201120' WHERE Img_Path = 'D:/origin_image/20201120';
-- UPDATE imagetbl SET Work_Yn = 'N', Coordinates = NULL WHERE Img_Name= 'S2-N5001M00538.jpg';
SELECT Work_User, COUNT(*) FROM imagetbl WHERE Work_User IS NOT NULL AND Work_Yn = 'N' GROUP BY Work_User;
SELECT Img_Path, COUNT(*) FROM imagetbl WHERE Work_Yn = 'N' AND  Work_User IS NULL GROUP BY Img_Path; 
-- SELECT * FROM imagetbl WHERE Work_Yn = 'N' AND Img_Path = '20201029';
COMMIT;