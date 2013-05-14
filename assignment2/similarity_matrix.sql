SELECT  count
FROM    (
        SELECT  A.docid
                ,B.docid
                ,SUM(A.count * B.count) AS count
        FROM    (
                SELECT  *
                FROM    Frequency
                WHERE   docid = '10080_txt_crude'
                ) AS A
        INNER JOIN
                (
                SELECT  *
                FROM    Frequency
                WHERE   docid = '17035_txt_earn'
                ) AS B
        ON      A.term = B.term
        GROUP BY
                A.docid
                ,B.docid
        ) AS x;
