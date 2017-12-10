# coding=utf8

import re
import json
from glob import glob

types = ('*.md', '*.markdown')
patterns = ['{}'.format(each) for each in types]

class Post:
    def __init__(self, id, raw_data):
        self.raw_data = raw_data
        self.metadata = {
            'id': id,
            'title': None,
            'slug': None,
            'date': None,
            'categories': None,
            'tags': None
        }
        self.markdown = None
        self.transform(raw_data)
    
    def get(self, key):
        return self.metadata[key]

    def parse_metadata(raw_data):
        metadata_pattern = r'^(\w*)\: (.+)$'
        parser = re.compile(metadata_pattern)
        for line in raw_data.split('\n'):
            m = parser.search(line)
            if m is not None:
                self.metadata[m.group(1).lower()] = m.group(2)
                last_metadata = m.group(0)
        return last_metadata


    def transform(self, raw_data):
        last_metadata = parse_metadata(raw_data)
        self.markdown = raw_data.split(last_metadata)[-1]

    def json(self):
        return {
            'id': self.metadata['id'],
            'title': self.metadata['title'],
            'slug': self.metadata['slug'],
            'markdown': self.markdown,
            'image': None,
            'featured': 0,
            'page': 0,
            'status': 'published',
            'language': 'en_US',
            'author_id': 1,
            'created_at': self.metadata['date'],
            'updated_at': self.metadata['date'],
            'published_at': self.metadata['date'],
            'created_by': 1,
            'updated_by': 1,
            'published_by': 1
        }

class Pghost:
    def __init__(self):
        self.data_block = {
            'meta': {
                'version': '000'
            }, 
            'data': {
                'posts': [],
                'tags':[], 
                'posts_tags': []
            },
            'users': [{
                
            }]
        }
    
    def parse(self):
        posts = []
        paths = [path for pattern in patterns for path in glob(pattern)]
        for index, path in enumerate(paths):
            with open(path) as fin:
                posts.append(Post(index, fin.read()))

        tags = {}
        posts_tags = {}
        for post in posts:
            _tags = post.get('tags').split(',')
            for tag in _tags:
                if tag not in tags.keys():
                    tags[tag] = {
                        'id': len(tags.keys()) + 1,
                        'name': tag,
                        'slug': tag,
                        'description': None,
                    }
                self.data_block['data']['posts_tags'].append({'tag_id':
                    tags[tag]['id'], 'post_id':
                    post.get('id')})
            self.data_block['data']['posts'].append(post.json())
        self.data_block['data']['tags'] = [value for key, value in tags.items()]
    
    def export(self):
        with open('blog.json', 'w') as fout:
            json.dump(self.data_block, fout, sort_keys=True, indent=4, ensure_ascii=False)
    
