from quest.models  import Question  
from haystack import indexes 
class QuestionIndex(indexes.SearchIndex, indexes.Indexable):  
    text = indexes.CharField(document=True, use_template=True)      
    title= indexes.CharField(model_attr='title')
    adddtime=indexes.DateTimeField(model_attr='addtime')
    #questionid=
    def get_model(self):  
        return Question  
    def index_queryset(self):  
        """Used when the entire index for model is updated."""    
        return self.get_model().objects.all() 
     
