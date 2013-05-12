SELECT  COUNT(*)
FROM    (
        SELECT  term
        FROM    Frequency
        WHERE   docid = '10398_txt_earn'
        AND     count = 1

        UNION

        SELECT  term
        FROM    Frequency
        WHERE   docid = '925_txt_trade'
        AND     count = 1
        ) AS x;
