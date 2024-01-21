-- UPDATE imagetbl SET Work_User = 'test' WHERE (Img_Path = '20201105') AND (Work_User IS NULL) LIMIT 5;
-- SELECT Work_User, COUNT(*) FROM imagetbl WHERE Work_User IS NOT NULL AND Work_Yn = 'N' GROUP BY Work_User;
-- UPDATE imagetbl SET Work_User = NULL WHERE Work_User = 'test' AND Work_Yn ='N'; 
SELECT Img_Path, count(*) FROM imagetbl
GROUP BY Img_Path;
-- DELETE FROM imagetbl WHERE Img_Path = 'N';
COMMIT;