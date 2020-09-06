# ��ѯbook�����Ƿ���������ӵ��鼮
book_query1 = 'SELECT 1 FROM tb_book WHERE href = %s'

# ��ѯ�鼮��Ӧ������
book_query2 = 'SELECT href FROM tb_book WHERE id = %s'

# ��ѯ�û��Ƿ���ӹ����鼮
bookshelves_query1 = 'SELECT 1 FROM tb_bookshelves WHERE user_id = %s AND book_id = %s'

# �����û����Ķ���¼
bookshelves_query2 = 'UPDATE tb_bookshelves SET chapter_id = %s WHERE book_id = %s'

# ��ѯ�û�����б�
bookshelves_query3 = 'SELECT bk.id book_id, book_name, author, chapter_id  ' \
                     'FROM tb_bookshelves bks ' \
                     'LEFT JOIN tb_book bk on bks.book_id = bk.id ' \
                     'WHERE bks.user_id = %s'

# ÿ���鶼��ר�ŵ�һ�ű�洢
create_book_table = "CREATE TABLE IF NOT EXISTS %s (" \
                    "id INT auto_increment PRIMARY KEY ," \
                    "book_id INT NOT NULL," \
                    "chapter_name VARCHAR(100) NOT NULL," \
                    "content LONGTEXT NOT NULL," \
                    "is_delete TINYINT(1) DEFAULT 0 NOT NULL)"

select_book_table = 'SELECT id chapter_id, chapter_name FROM %s'
