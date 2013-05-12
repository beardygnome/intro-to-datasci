SELECT  COUNT(*)
FROM    (
        SELECT  one.docid
        FROM
                (
                SELECT  docid
                FROM    Frequency
                WHERE   term = 'transactions'
                ) AS one
        INNER JOIN
                (
                SELECT  docid
                FROM    Frequency
                WHERE   term = 'world'
                ) as two
        ON      one.docid = two.docid
        ) AS x;
