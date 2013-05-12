SELECT  COUNT(*)
FROM    (
        SELECT  *
        FROM    Frequency
        WHERE   docid = '10398_txt_earn'
        ) AS x;
