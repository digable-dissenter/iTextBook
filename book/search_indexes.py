from haystack.indexes import *
from book.models import Course
from book.models import Subtopic
from book.models import Topic


class CourseIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
        
site.register(Course, CourseIndex)

class TopicIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

        
site.register(Topic, TopicIndex)

class SubtopicIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

        
site.register(Subtopic, SubtopicIndex)
