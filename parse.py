import sqlite3, os, sys, random, string

global words_table, prev_word, max_length, first_words, num_sentences

def create_db(name):
	fn = name + ".db"
	
	try:
		os.remove(fn)
	except OSError:
		pass
	
	conn = sqlite3.connect(fn)
	print "Created file: " + fn
	return conn

def get_nice_text(text):
	text = text.lower().translate(string.maketrans("",""), string.punctuation)
	return text

def add_entry(text):
	global words_table, prev_word, first_words
	text = text.replace("|", "")
	nice_text = get_nice_text(text)

	# Add current word to previous words list of next words
	if (prev_word == ""):
		first_words.append(text)
	else:
		words_table[prev_word].append(text)
		
	if (nice_text not in words_table):
		words_table[nice_text] = []

	prev_word = nice_text
	
def save_entries(conn):
	global first_words, words_table
	conn.execute('''CREATE TABLE firstwords
		(WORD VARCHAR(255) NOT NULL);''')
	for word in first_words:
		word = word.replace("'", "''")
		instruction = "INSERT INTO firstwords VALUES ('" + word + "');"
		# print instruction
		conn.execute(instruction)

	conn.execute('''CREATE TABLE nextwords
		(WORD VARCHAR(255) NOT NULL,
		NEXTS VARCHAR(255));''')
	for k in words_table:
		nexts = "|".join(words_table[k])
		nexts = nexts.replace("'", "''")
		instruction = "INSERT INTO nextwords VALUES ('" + k + "', '" + nexts + "');"
		# print instruction
		conn.execute(instruction)


def parse_file(o_name, f_name):
	global words_table, prev_word, first_words, num_sentences
	words_table = {}
	first_words = []
	f = open(f_name)
	conn = create_db(o_name)
	for line in f:
		line = line.replace("\n", "")
		sentences = line.split(".")
		for s in sentences:
			words = s.split()
			prev_word = ""
			for w in words:
				if (len(w) > 0):
					add_entry(w)
	f.close()
	save_entries(conn)
	conn.commit()
	conn.close()
	f.close()

def main():
	global max_length, num_sentences
	if (len(sys.argv) != 5):
		print "Usage:"
		print "    python parse.py [output name] [input file]"
		sys.exit(0)
	# Gets name from second cmd-line argument
	name = sys.argv[1]
	f_in_name = sys.argv[2]

	parse_file(name, f_in_name)

if __name__ == "__main__":
	main()
