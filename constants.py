sql_need_display_word = """
    select English as word
    from AllEnglishKnowledge
    where table_name ='ItProfessionWords'
    and score <=100
    limit {}
    offset {}
    """
sql_get_ENG = """
    select English as word
    from AllEnglishKnowledge
    where Chinese='{}'
"""
sql_word = """
    select id,frequency,score
    from AllEnglishKnowledge
    where  English='{}'
    """
