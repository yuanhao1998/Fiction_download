# 查询book表中是否包含该链接的书籍
book_query1 = 'SELECT 1 FROM tb_book WHERE href = %s'

# 查询书籍对应的链接
book_query2 = 'SELECT href FROM tb_book WHERE id = %s'

# 查询用户是否添加过该书籍
bookshelves_query1 = 'SELECT 1 FROM tb_bookshelves WHERE user_id = %s AND book_id = %s'

# 更新用户的阅读记录
bookshelves_query2 = 'UPDATE tb_bookshelves SET chapter_id = %s WHERE book_id = %s'

# 查询用户书架列表
bookshelves_query3 = 'SELECT bk.id book_id, book_name, author, chapter_id  ' \
                     'FROM tb_bookshelves bks ' \
                     'LEFT JOIN tb_book bk on bks.book_id = bk.id ' \
                     'WHERE bks.user_id = %s'

# 每本书都有专门的一张表存储
create_book_table = "CREATE TABLE IF NOT EXISTS %s (" \
                    "id INT auto_increment PRIMARY KEY ," \
                    "book_id INT NOT NULL," \
                    "chapter_name VARCHAR(100) NOT NULL," \
                    "content LONGTEXT NOT NULL," \
                    "is_delete TINYINT(1) DEFAULT 0 NOT NULL)"

select_book_table = 'SELECT id chapter_id, chapter_name FROM %s'
