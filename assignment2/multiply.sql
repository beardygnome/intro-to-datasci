SELECT  value
FROM    (
        SELECT  A.row_num
                ,B.col_num
                ,SUM(A.value * B.value) AS value
        FROM    A
        INNER JOIN
                B
        ON      A.col_num = B.row_num
        GROUP BY
                A.row_num
                ,B.col_num
        ) AS x
WHERE   row_num = 2
AND     col_num = 3;
