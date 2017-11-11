import os, re
import json
import pdb
import collections
from django.utils.text import slugify
from bs4 import BeautifulSoup

omitted_dirs = []
sourceLink = 'http://tanzil.info'
source = 'Tanzil Quran Text'
works = []

def jaggedListToDict(text):
	node = { str(i): t for i, t in enumerate(text) }
	node = collections.OrderedDict(sorted(node.items(), key=lambda k: int(k[0])))
	for child in node:
		if isinstance(node[child], list):
			if len(node[child]) == 1:
				node[child] = node[child][0]
			else:
				node[child] = jaggedListToDict(node[child])
	return node


def main():
	if not os.path.exists('cltk_json'):
		os.makedirs('cltk_json')

	for root, dirs, files in os.walk("."):
		path = root.split('/')
		print((len(path) - 1) * '---', os.path.basename(root))
		for fname in files:
			if fname.endswith('xml'):
				with open(os.path.join(root, fname)) as f:
					soup = BeautifulSoup(f.read(), 'html.parser')

				work = {
					'originalTitle': 'القرآن‎‎',
					'englishTitle': 'The Holy Quran',
					'author': '(Original Book)',
					'source': source,
					'sourceLink': sourceLink,
					'language': 'arabic',
					'text': {},
				}

				text = []
				chapters = soup.findAll('chapter')
				for i, chapter in enumerate(chapters):
					text.append([])
					verses = chapter.findAll('verse')
					for verse in verses:
						text[i].append(verse.text)


				work['text'] = jaggedListToDict(text)
				fname = slugify(work['source']) + '__' + slugify(work['englishTitle'][0:140]) + '__' + slugify(work['language']) + '.json'
				fname = fname.replace(" ", "")

				with open('cltk_json/' + fname, 'w') as f:
					json.dump(work, f)

if __name__ == '__main__':
	main()
