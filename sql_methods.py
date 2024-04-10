"""Defines the methods (which query the database) used within the API 
that do not relate to the endpoints."""
# pylint: disable=bare-except, unused-variable, unsupported-binary-operation

from psycopg2 import sql
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor, RealDictRow

QUERY_DIRECTORY = "./queries/"


def read_in_query(file):
    """Reads a query file into memory to be stored in a variable."""
    with open(f"{QUERY_DIRECTORY}{file}", "r", encoding="utf-8") as f:
        return f.read()


GET_STORIES_QUERY = read_in_query("get_stories.sql")
INSERT_STORY_QUERY = read_in_query("insert_story.sql")
UPDATE_SCORE_QUERY = read_in_query("update_score.sql")
PATCH_STORY_QUERY = read_in_query("patch_story.sql")
BASIC_SELECT_QUERY = "SELECT id FROM stories WHERE id = {}"
DELETE_VOTES_QUERY = "DELETE FROM votes WHERE story_id = {}"
DELETE_STORY_QUERY = "DELETE FROM stories WHERE id = {} RETURNING *"


def get_stories_data(conn: connection,
                     search: str, sort: str, order: bool) -> list[RealDictRow] | dict[bool, str]:
    """Gets all stories from DB."""
    if not isinstance(search, str) or not isinstance(sort, str) or not isinstance(order, bool):
        return {"error": True, "message": "Invalid argument type(s)"}
    cur = conn.cursor(cursor_factory=RealDictCursor)

    search = sql.Literal(
        f"%%{search}%%") if search else sql.Identifier("title")
    sort = sql.SQL(sort) if sort else sql.SQL("created_at")
    order = sql.SQL("DESC") if order else sql.SQL("ASC")
    cur.execute(sql.SQL(GET_STORIES_QUERY).format(search, sort, order))

    rows = cur.fetchall()
    conn.commit()
    cur.close()

    if not rows:
        return {"error": True, "message": "No stories were found"}

    return rows


def insert_story(conn: connection, url: str, title: str) -> dict[bool, str]:
    """Inserts a story into the story table."""
    if not isinstance(url, str) or not isinstance(title, str):
        return {"error": True, "message": "Invalid argument type(s)"}

    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql.SQL(INSERT_STORY_QUERY).format(
        sql.Literal(title), sql.Literal(url)))

    rows = cur.fetchall()
    conn.commit()
    cur.close()

    if rows:
        return {"success": True, "message": "Insert story successful."}
    return {"error": True, "message": "Update score failed."}


def update_score(conn: connection, id_num: int, to_add: int) -> dict[bool, str]:
    """Updates the a stories id by inserting a new vote record into the votes table."""
    if not isinstance(id_num, int) or not isinstance(to_add, str):
        return {"error": True, "message": "Invalid argument type(s)"}

    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql.SQL(BASIC_SELECT_QUERY).format(sql.Literal(id_num)))

    rows = cur.fetchall()
    conn.commit()

    if not rows:
        return {"error": True, "message": "Incorrect ID."}

    cur.execute(sql.SQL(UPDATE_SCORE_QUERY).format(
        sql.Literal(id_num), sql.Literal(to_add)))

    rows = cur.fetchall()
    conn.commit()
    cur.close()

    if rows:
        return {"success": True, "message": "Update score successful."}
    return {"error": True, "message": "Update score failed."}


def patch_story(conn: connection, id_num: int, url: str, title: str) -> dict[bool, str]:
    """Updates a stories url and/or title with values passed as argument."""
    if not isinstance(id_num, int) or not isinstance(url, str) or not isinstance(title, str):
        return {"error": True, "message": "Invalid argument type(s)"}

    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(sql.SQL(PATCH_STORY_QUERY).format(
        sql.Literal(url), sql.Literal(title), sql.Literal(id_num)))
    rows = cur.fetchall()
    conn.commit()
    cur.close()

    if rows:
        return {"success": True, "message": "Update story successful."}
    return {"error": True, "message": "Update story failed."}


def delete_story(conn: connection, id_num: int) -> dict[bool, str]:
    """Deletes the story with the id passed in as argument."""
    if not isinstance(id_num, int):
        return {"error": True, "message": "Invalid argument type(s)"}

    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(sql.SQL(DELETE_VOTES_QUERY).format(sql.Literal(id_num)))
    cur.execute(sql.SQL(DELETE_STORY_QUERY).format(sql.Literal(id_num)))
    rows = cur.fetchall()
    conn.commit()
    cur.close()

    if rows:
        return {"success": True, "message": "Delete story successful."}
    return {"error": True, "message": "Update story failed."}
