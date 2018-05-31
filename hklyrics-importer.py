import io
import json
import sqlite3


connection = sqlite3.connect('hklyrics.db')
cursor = connection.cursor()


def close_connection():
    connection.close()


def setup_tables():
    # Create singers table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS singers (
		          singer_name    TEXT    PRIMARY KEY
    		      )''')
    connection.commit()

    # Create songs table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS songs (
			  song_name      TEXT, 
			  singer_name    TEXT,
                          composer_name  TEXT,
                          lyricist_name  TEXT,
                          arranger_name  TEXT,
                          producer_name  TEXT,
                          lyrics         TEXT, 
			  FOREIGN KEY(singer_name) REFERENCES singers(singer_name)					
		      )''')
    connection.commit()


def insert_singer(singer_name):
    cursor.execute("INSERT INTO singers VALUES ('%s')" % singer_name)
    connection.commit()


def insert_song(singer_name, song_name, song): 
    cursor.execute("INSERT INTO songs VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (song_name, singer_name, song.composer, song.lyricist, song.arranger, song.producer, lyrics))
    connection.commit()


def read_data_from_file(filename):
    with io.open(filename, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data


def import_singer(singer_name):
    setup_tables()

    insert_singer(singer_name)

    data = read_data_from_file('data/%s.json' % singer_name)
    for song_name, song in data.iteritems():
        insert_song(singer_name, song_name, song)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Importing Hong Kong lyrics to sqlite database.')
    parser.add_argument('--singer', nargs='?', help='To input singer name')

    args = parser.parse_args() 
    if args.singer is not None:
        singer_name = unicode(args.singer, 'utf-8')
        print 'Importing singer %s' % singer_name
        import_singer(singer_name)

    close_connection()

