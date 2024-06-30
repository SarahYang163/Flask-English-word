mysql_setting = {
    'host': '43.138.75.243',
    'port': 3306,
    'user': 'root',
    'passwd': "@2|d5^ZKstp6~BJS",
    # 数据库名称
    'db': 'web_online_words',
    'charset': 'utf8'
}

sql_need_display_word = """
    select English as word
    from AllEnglishKnowledge
    where table_name ='ItProfessionWords'
    and score <=100
    limit %s
    offset %s
    """
sql_get_ENG = """
    select English as word
    from AllEnglishKnowledge
    where Chinese=%s
"""
sql_word = """
    select id,frequency,score
    from AllEnglishKnowledge
    where  English="{}"
    """
