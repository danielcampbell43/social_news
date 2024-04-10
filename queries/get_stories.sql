   SELECT s.id
        , s.title
        , s.url
        , s.created_at
        , s.updated_at
        , SUM(CASE
              WHEN vote = 'u' THEN 1
              WHEN vote = 'd' THEN -1
              ELSE 0
              END) AS "score"

     FROM stories AS s

          LEFT OUTER JOIN votes AS v
          ON s.id = v.story_id

    WHERE title ILIKE {}

 GROUP BY s.id
        , s.title
        , s.url
        , s.created_at
        , s.updated_at

 ORDER BY {} {}