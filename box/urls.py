from django.conf.urls import patterns

urlpatterns = patterns('box.views',
                       (r'^course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/cq/$',
                        "subtopic_quiz"),
                       (
                       r'^course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/cq(?P<cq_id>\d+)/attempt(?P<attempt_id>\d+)/$',
                       "subtopic_quiz_attempt"),
                       (r"^codepad/$", "codepad"),
                       (
                       r'^course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/cq(?P<cq_id>\d+)/$',
                       "codeform"),
                       (
                       r'^admin/add/course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/addcq/$',
                       "create_cq"),
                       (
                       r'^admin/edit/course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/question(?P<question_id>\d+)/$',
                       "edit_cq"),
                       (
                       r'^admin/add/course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/question(?P<question_id>\d+)/addkeyword/$',
                       "add_keyword"),
                       (
                       r'^admin/add/course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/question(?P<question_id>\d+)/addtestcase/$',
                       "add_testcase"),
                       (
                       r'^admin/delete/course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/question(?P<question_id>\d+)/keyword(?P<keyword_id>\d+)/$',
                       "delete_keyword"),
                       (
                       r'^admin/delete/course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/question(?P<question_id>\d+)/testcase(?P<testcase_id>\d+)/$',
                       "delete_testcase"),
                       (
                       r'^admin/delete/course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/question(?P<question_id>\d+)/$',
                       "delete_cq"),
                       )
