UPDATE stories 

   SET URL = {},
       title = {},
       updated_at = NOW()::timestamp

 WHERE id = {}

 RETURNING id