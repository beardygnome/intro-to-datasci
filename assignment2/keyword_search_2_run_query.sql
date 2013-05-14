SELECT  MAX(count)
FROM    (
        SELECT  A.docid
                ,SUM(A.count * B.count) AS count
        FROM    (
                SELECT  *
                FROM    keyword
                ) AS A
        INNER JOIN
                (
                SELECT  *
                FROM    keyword
                WHERE   docid = 'q'
                ) AS B
        ON      A.term = B.term
        GROUP BY
                A.docid
        ) AS x;
