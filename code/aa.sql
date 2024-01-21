
-- UPDATE imagetbl SET Work_User = NULL WHERE Work_User = 'humanf59' AND Work_Yn ='N';

-- UPDATE imagetbl SET Work_User = 'humanf49' WHERE (Img_Path = '20201109') AND (Work_User IS NULL) LIMIT 5000;
SELECT Work_User, COUNT(*) FROM imagetbl WHERE Work_User IS NOT NULL AND Work_Yn = 'N' GROUP BY Work_User;
-- SELECT Img_Path, COUNT(*) FROM imagetbl GROUP BY Img_Path; 
 
-- SELECT Work_User, Date_Format(Work_Date, '%Y-%m-%d'), count(*) FROM workhistory group by Date_Format(Work_Date, '%Y-%m-%d'), Work_User;
-- SELECT Work_User, Date_Format(Work_Date, '%Y-%m-%d'), count(*) FROM imagetbl group by Date_Format(Work_Date, '%Y-%m-%d'), Work_User, Work_Yn HAVING Work_Yn = 'Y';
COMMIT;