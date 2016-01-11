# from lucene import \
    # QueryParser, IndexSearcher, StandardAnalyzer, SimpleFSDirectory, File, \
    # VERSION, initVM, Version, WhitespaceAnalyzer, getVMEnv, BooleanQuery, BooleanClause,\
    # WildcardQuery, Term, SimpleHTMLFormatter, SimpleFragmenter, Highlighter, StringReader,\
    # TokenStream, QueryScorer
import web
from web import form
import urllib2
import os
import random
import string
import backend.contentSearcher.searcher as searcher
##http://www.sucaijiayuan.com/api/demo.php?url=/demo/20130401-1
urls = (
    '/', 'index',
    '/im', 'index_img',
    '/s', 'text',
    '/i', 'image',
    '/api/search/text', 'apitext'
)

render = web.template.render('templates/', cache = False) # your templates

# def search_text(command):
    # Docs = []
    # vm_env = getVMEnv()
    # vm_env.attachCurrentThread()
    # STORE_DIR = "index"
    
    # directory = SimpleFSDirectory(File(STORE_DIR))
    # searcher = IndexSearcher(directory, True)
    # analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    
    # command_dict = {}
    # allowed_opt = ['site']
    # opt = 'contents'
    # for i in command.split(' '):
        # if ':' in i:
            # opt, value = i.split(':')[:2]
            # opt = opt.lower()
            # if opt in allowed_opt and value != '':
                # command_dict[opt] = command_dict.get(opt, '') + ' ' + value
        # else:
            # seg_list = jieba.cut(i)
            # command_dict[opt] = command_dict.get(opt, '') + ' ' + " ".join(seg_list)

    # querys = BooleanQuery()
    # for k,v in command_dict.iteritems():
        # if k=='site' :
            # t = Term(k, '*' + v)
            # query = WildcardQuery(t)
        # else:
            # query = QueryParser(Version.LUCENE_CURRENT, k, analyzer).parse(v)
        # querys.add(query, BooleanClause.Occur.MUST)
        
    # scoreDocs = searcher.search(querys, 10000).scoreDocs
    # formatter = SimpleHTMLFormatter("<font color=#FF0000>","</font>")
    # highlighter = Highlighter(formatter, QueryScorer(querys))
    
    # for scoreDoc in scoreDocs:
        # doc = searcher.doc(scoreDoc.doc)
        # doc_dic = {}
        # doc_dic["title"] = doc.get("title")
        # doc_dic["url"] = doc.get("url")
        # text = doc.get("contents")
        # ts = analyzer.tokenStream(doc.get("contents"), StringReader(text))
        # doc_dic["contents"] = highlighter.getBestFragments(ts, text, 2, "...")
        # tx_list = highlighter.getBestFragments(ts, text, 2, "...").split()
        # tx = ''.join(tx_list)
        # doc_dic["contents"] = tx
        # Docs.append(doc_dic)
    # searcher.close()
    # return Docs

# def search_image(command):
    # if command == ' ':
        # return []
    # Docs = []
    # vm_env = getVMEnv()
    # vm_env.attachCurrentThread()
    # STORE_DIR = "index_img"
    
    # directory = SimpleFSDirectory(File(STORE_DIR))
    # searcher = IndexSearcher(directory, True)
    # analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    
    # command_dict = {}
    # allowed_opt = ['site']
    # opt = 'contents'
    # for i in command.split(' '):
        # if ':' in i:
            # opt, value = i.split(':')[:2]
            # opt = opt.lower()
            # if opt in allowed_opt and value != '':
                # command_dict[opt] = command_dict.get(opt, '') + ' ' + value
        # else:
            # seg_list = jieba.cut(i)
            # command_dict[opt] = command_dict.get(opt, '') + ' ' + " ".join(seg_list)

    # querys = BooleanQuery()
    # for k,v in command_dict.iteritems():
        # if k=='site' :
            # t = Term(k, '*' + v)
            # query = WildcardQuery(t)
        # else:
            # query = QueryParser(Version.LUCENE_CURRENT, k, analyzer).parse(v)
        # querys.add(query, BooleanClause.Occur.MUST)
        
    # scoreDocs = searcher.search(querys, 10000).scoreDocs
    # formatter = SimpleHTMLFormatter("<font color=#FF0000>","</font>")
    # highlighter = Highlighter(formatter, QueryScorer(querys))
    
    # for scoreDoc in scoreDocs:
        # doc = searcher.doc(scoreDoc.doc)
        # doc_dic = {}
        # doc_dic["url"] = doc.get("url")
        # doc_dic["imgurl"] = doc.get("imgurl")
        # doc_dic["urltitle"] = doc.get("urltitle")
        # text = doc.get("contents")
        # ts = analyzer.tokenStream(doc.get("contents"), StringReader(text))
        # doc_dic["contents"] = highlighter.getBestFragments(ts, text, 2, "...")
        # Docs.append(doc_dic)
    # searcher.close()
    # return Docs

class index:
    def GET(self):
        return render.index()

class index_img:
    def GET(self):
        return render.index_img()

class text:
    def GET(self):
        user_data = web.input()
        t = user_data.keyword
        if t.split()==[]:
            return render.text([],[])
        a = search_text(t)
        key = t.split()
        return render.text(a,key)

class image:
    def GET(self):
        user_data = web.input()
        query = user_data.keyword
        print(query)
        if query==[]:
            return render.image('')
        else:
            return render.image(query)
    def POST(self):
        x=web.input(query={})
        if 'query' in x:
            fout=open('backend/'+string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 5)).replace(' ','')+'.jpg','wb')
            fout.write(x.query.file.read())
            fout.close()
        f=open("static/test.json","r")
        text=f.read()
        f.close()
        return render.image_upload(text)

class apitext:
    def GET(self):
        user_data = web.input()
        query = user_data.query
        print (query)
        return searcher.query(query)

if __name__ == "__main__":
    # initVM()
    app = web.application(urls, globals())
    app.run()
