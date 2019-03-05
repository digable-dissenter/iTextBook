from django.conf.urls import patterns

urlpatterns = patterns('mcq.views',
                       (r'^course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/mcq/$',
                        "subtopic_mcq"),
                       (r'^course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/process_mcq/$',
                        "process_mcq"),
                       (
                       r'^admin/add/course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/addmcq/$',
                       "create_mcq"),
                       (
                       r'^admin/edit/course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/question(?P<question_id>\d+)/$',
                       "edit_mcq"),
                       (
                       r'^admin/delete/course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/question(?P<question_id>\d+)/$',
                       "delete_mcq"),
                       )
