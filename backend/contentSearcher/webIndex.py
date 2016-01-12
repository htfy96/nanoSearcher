from luceneHelper.luceneHelper import LuceneHelper
from org.apache.lucene.analysis.core import SimpleAnalyzer,WhitespaceAnalyzer
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.util import Version

class WebIndexer(LuceneHelper):
    def __init__(self, **kwargs):
        LuceneHelper.__init__(self,analyzer=WhitespaceAnalyzer(Version.LUCENE_CURRENT), searchAnalyzer=WhitespaceAnalyzer(Version.LUCENE_CURRENT),**kwargs)
        storeAndIndex={'store':True, 'index':True}
        storeAndIndexAndTokenize={'store':True, 'index':True, 'tokenize':True}
        self.setFields(id_=storeAndIndex, name=storeAndIndexAndTokenize, price=storeAndIndex,
        imgurl=storeAndIndex, author=storeAndIndex, category=storeAndIndex, detail=storeAndIndex, url=storeAndIndex, rawname=storeAndIndex)
        
    def __del__(self):
        LuceneHelper.__del__(self)

if __name__=='__main__':
    index = WebIndexer()
