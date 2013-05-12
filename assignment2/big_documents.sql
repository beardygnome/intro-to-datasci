SELECT  COUNT(*)
FROM    (
        SELECT  docid
        FROM    Frequency
        GROUP BY
                docid
        HAVING  SUM(count) > 300
        ) AS x;
