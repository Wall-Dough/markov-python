import sqlite3, os, sys, random, string

global first_words, words_table, max_length

def open_db(name):
	fn = name + ".db"
	if (os.path.isfile(fn)):
		conn = sqlite3.connect(fn)
		return conn
	else:
		print "No data available for this name"
		sys.exit(0)

def get_nice_text(text):
        text = text.lower().translate(string.maketrans("",""), string.punctuation)
        return text

def strify(text):
	printable = set(string.printable)
	return str(filter(lambda x: x in printable, text))

def get_first_words(conn):
	global first_words
	first_words = []
	cursor = conn.execute("SELECT WORD FROM firstwords");
	for row in cursor:
		word = strify(row[0])
		first_words.append(word)

def get_next_words(conn):
	global words_table
	words_table = {}
	cursor = conn.execute("SELECT WORD, NEXTS FROM nextwords");
	for row in cursor:
		word = strify(row[0])
		nexts = strify(row[1])
		if (len(nexts) == 0):
			words_table[word] = []
		else:
			words_table[word] = nexts.split("|")

def print_sentence():
        global words_table, first_words
        num_words = 0
        cur = random.choice(first_words)
        sentence = ""
        while True:
                sentence += cur + " "
                num_words += 1
                nice_cur = get_nice_text(cur)
                if (num_words >= max_length):
                        break
                if (len(words_table[nice_cur]) > 0):
                        cur = random.choice(words_table[nice_cur])
                else:
                        break
        print sentence.rstrip()

def get_data_from_db(name):
	conn = open_db(name)
	get_first_words(conn)
	get_next_words(conn)
	conn.close()

def main():
	global max_length
	if (len(sys.argv) != 4):
		print "Usage:"
		print "    python markov.py [output name] [max length] [num sentences]"
		print "        (output name is the name used for parse.py)"
		sys.exit(0)
	name = sys.argv[1]
	max_length = eval(sys.argv[2])
	num_sentences = eval(sys.argv[3])	
	get_data_from_db(name)
	for i in range(num_sentences):
		print_sentence()

if __name__ == "__main__":
	main()
