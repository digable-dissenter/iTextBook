from django.conf.urls import patterns

urlpatterns = patterns('',
                       (r"^$", "book.views.main"),
                       (r"^users/$", "book.views.all_users"),
                       (r"^admin/analytics/course/(?P<course_id>\d+)/$", "book.views.general_analytics"),
                       (r"^admin/analytics/dashboard/$", "book.views.analytics"),
                       (r"^admin/analytics/course/(?P<course_id>\d+)/cq/user/(?P<user_username>\w+)/$",
                        "book.views.cq_analytics"),
                       (r"^admin/analytics/course/(?P<course_id>\d+)/mcq/user/(?P<user_username>\w+)/$",
                        "book.views.mcq_analytics"),
                       (r"^admin/analytics/mcq/subtopic/(?P<subtopic_id>\d+)/$", "book.views.subtopic_mcq_analytics"),
                       (r"^admin/analytics/cq/subtopic/(?P<subtopic_id>\d+)/$", "book.views.subtopic_cq_analytics"),
                       (r"^admin/analytics/comments/subtopic/(?P<subtopic_id>\d+)/$",
                        "book.views.subtopic_comments_analytics"),
                       (r"^admin/analytics/course/(?P<course_id>\d+)/comments/user/(?P<user_username>\w+)/$",
                        "book.views.comment_analytics"),
                       (r"^admin/users/delete/user/(?P<user_username>\w+)/$", "book.views.delete_user"),
                       (r"^admin/users/make_admin/user/(?P<user_username>\w+)/$", "book.views.admin_user"),
                       (r"^admin/users/remove_admin/user/(?P<user_username>\w+)/$", "book.views.unadmin_user"),
                       (r'^admin/edit/course/(?P<course_id>\d+)/$', "book.views.edit_course"),
                       (r'^admin/delete/course(?P<course_id>\d+)/$', "book.views.delete_course"),
                       (r'^course(?P<course_id>\d+)/$', "book.views.all_topics"),
                       (r'^course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/$', "book.views.topic"),
                       (r'^admin/edit/course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/$', "book.views.edit_topic"),
                       (r'^admin/delete/course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/$', "book.views.delete_topic"),
                       (r'^admin/add/course(?P<course_id>\d+)/addtopic/$', "book.views.create_topic1"),
                       (r'^course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/$',
                        "book.views.subtopics"),
                       (r'^admin/edit/course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/$',
                        "book.views.edit_subtopics"),
                       (
                       r'^admin/delete/course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/$',
                       "book.views.delete_subtopic"),
                       (r'^admin/add/course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/addsubtopic/$',
                        "book.views.create_subtopic1"),
                       (r'^course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/slides/$',
                        "book.views.slides_view"),
                       (r'^course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/textbook/$',
                        "book.views.textbook_view"),
                       (r'^course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/video/$',
                        "book.views.video_view"),
                       (r"^annotation/(?P<subtopic_id>\d+)/$", "book.views.annotations"),
                       (r"^comments/(?P<subtopic_id>\d+)/$", "book.views.comments"),
                       (r"^pdfview/$", "book.views.pdf_view"),
                       (r"^pdfviewgoogle/$", "book.views.pdf_view_google"),
                       (r"^pdfview1/$", "book.views.pdf_view1"),
                       (r"^admin/help/$", "book.views.lecturer_help"),
                       (r"^help/$", "book.views.student_help"),
                       (r"^codeform/$", "box.views.codeform"),
                       (r"^admin/add/addcourse/$", "book.views.create_course"),
                       )
