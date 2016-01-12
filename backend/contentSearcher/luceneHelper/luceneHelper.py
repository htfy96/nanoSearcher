import sys, os, lucene, threading, time
from datetime import datetime

INDEX_DIR = "IndexFiles.index"

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import SimpleAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.search.spans import SpanTermQuery 
class LuceneHelper(object):
    def __init__(self, storeDir=os.path.join(os.path.curdir, INDEX_DIR), analyzer=StandardAnalyzer(Version.LUCENE_CURRENT), searchAnalyzer=StandardAnalyzer(Version.LUCENE_CURRENT)):
        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        self.store = SimpleFSDirectory(File(storeDir))
        self.analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE_OR_APPEND)
        try:
            self.writer=IndexWriter(self.store, config)
            base_dir = os.path.dirname(os.path.abspath(storeDir))
            directory = SimpleFSDirectory(File(os.path.join(base_dir, INDEX_DIR)))
            self.searcher = IndexSearcher(DirectoryReader.open(directory))
        except Exception,e:
            print unicode(e)
            print unicode(e.getJavaException())
        self.searchAnalyzer = searchAnalyzer
        self.count = 0


    def query(self,cmd, fieldName):
        query = QueryParser(Version.LUCENE_CURRENT, fieldName, self.searchAnalyzer).parse(cmd)
        res = self.searcher.search(query, 10000).scoreDocs
        return res
        

    def setFields(self,**kwargs):
        self.__fields__={}
        for key in kwargs:
            cfg=kwargs[key]
            self.__fields__[key]=FieldType()
            if cfg.get('index','') == True:
                self.__fields__[key].setIndexed(True)
            else:
                self.__fields__[key].setIndexed(False)
            if cfg.get('store','') == True:
                self.__fields__[key].setStored(True)
            else:
                self.__fields__[key].setStored(False)
            if cfg.get('tokenize','')==True:
                self.__fields__[key].setTokenized(True)
                self.__fields__[key].setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
            else:
                self.__fields__[key].setTokenized(False)

    def add(self,**kwargs):
        doc=Document()
        for key in kwargs:
            cont = kwargs[key]
            if key not in self.__fields__:
                print ('Invalid key:',key)
                return
            doc.add(Field(key, cont, self.__fields__[key]))
        self.writer.addDocument(doc)
        self.count += 1
        if self.count > 15:
            self.writer.commit()
            self.count = 0


    def __del__(self):
        self.writer.commit()
        self.writer.close()
        print ("closed")

if __name__ == '__main__':
    crawler = WebPageIndexer()
    storeAndIndex={'store':True, 'index':True}
    storeAndIndexAndTokenize={'store':True, 'index':True, 'tokenize':True}
    crawler.setFields(name=storeAndIndex, path=storeAndIndex,
            url=storeAndIndex, title=storeAndIndex, content=storeAndIndexAndTokenize)
    crawler.add(name='my webpage', path='/home/lz/.vim', url='http://www.mya.com', title='title heading', content=
            'blahblah blah blah one two three four five lipsum no ki')
    res = (crawler.query('blah', 'content'))
    print (crawler.__fields__)
    for doc in res:
        print (crawler.searcher.doc(doc.doc).get('name'))
