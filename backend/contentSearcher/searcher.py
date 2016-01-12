import lucene
from webIndex import WebIndexer
from org.apache.lucene.analysis.core import SimpleAnalyzer,WhitespaceAnalyzer
from org.apache.lucene.search.highlight import Highlighter,QueryScorer, SimpleHTMLFormatter
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.util import Version
from org.apache.lucene.analysis.standard import StandardAnalyzer
import jieba
import re
import json
import web.net


def getSite(s):
    res = re.search(r'site:\s*(\S+)', s)
    if not res:
        return u''
    else:
        return u' AND url:http*\:\/\/*'+ res.group(1) +'\/*'

def mainPart(s):
    return re.sub(r'site:\s*(\S+)', '', s)

def query(s):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    print (s)
    a = WebIndexer()
    result = []
    try:
        res = a.query(u'name:"'+' '.join(jieba.cut(s, cut_all=False))+'" ', 'name')
    except Exception, e:
        print (e)
        print unicode(e.getJavaException())
    for doc in res:
        c = a.searcher.doc(doc.doc)
        print (unicode(c))
        result.append({'id': c.get('id_'), 'name': c.get('rawname'), 'price': c.get('price'), 'author': c.get('author'), 'category': c.get('category'), 'url': c.get('url'), 'imgurl': c.get('imgurl'), 'detail': c.get('detail')})
    return json.dumps(result)

