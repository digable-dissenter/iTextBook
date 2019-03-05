from time import gmtime, strftime
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from box.models import *
from box.models import Question as Q1
from mcq.models import *


def main(request):
    try:
        course_list = Course.objects.all()
        context = dict(course_list=course_list, user=request.user)
    except Course.DoesNotExist:
        context = dict(user=request.user)
    return render_to_response("book/index.html", context_instance=RequestContext(request, context))


def create_course(request):
    form = CourseForm()
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES or None)
        print request.POST
        print request.FILES
        if form.is_valid():
            course = form.save(commit=False)
            course.language = request.POST["language"]
            course.save()
            course_list = Course.objects.all()
            message = course.name + " Successfully Added!"
            context = dict(course_list=course_list, user=request.user, message=message)
            return render_to_response("book/index.html", context_instance=RequestContext(request, context))

    else:
        form = CourseForm()
    variables = RequestContext(request, {'create_course_form': form})
    return render_to_response("book/admin_course.html", variables)


def edit_course(request, course_id):
    course = Course.objects.get(pk=int(course_id))
    form = CourseForm()
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            course = form.save(commit=False)
            course.language = request.POST["language"]
            course.save()
            course.save()
            course_list = Course.objects.all()
            message = course.name + " Successfully Edited!"
            context = dict(course_list=course_list, user=request.user, message=message)
            return render_to_response("book/index.html", context_instance=RequestContext(request, context))

    else:
        form = CourseForm(instance=course)
    context = dict(user=request.user, edit_course_form=form, course=course)
    return render_to_response("book/admin_course.html", context_instance=RequestContext(request, context))


def delete_course(request, course_id):
    course = Course.objects.get(pk=int(course_id))
    message = course.name + " Successfully Deleted!"
    course.delete()
    course_list = Course.objects.all()
    context = dict(course_list=course_list, user=request.user, message=message)
    return render_to_response("book/index.html", context_instance=RequestContext(request, context))


def all_topics(request, course_id):
    try:
        course = Course.objects.get(pk=int(course_id))
        topic_list = Topic.objects.filter(course=course)
        subtopic_list = Subtopic.objects.all()[:]
        context = dict(topic_list=topic_list, subtopic_list=subtopic_list, user=request.user, course=course)
    except Topic.DoesNotExist:
        context = dict(user=request.user)
        return render_to_response("book/index.html", context_instance=RequestContext(request, context))
    return render_to_response("book/all_topics.html", context_instance=RequestContext(request, context))


def topic(request, course_id, topic_id):
    try:
        topic = Topic.objects.get(pk=topic_id)
        subtopic_list = Subtopic.objects.filter(topic=topic_id)
        context = dict(topic=topic, subtopic_list=subtopic_list, user=request.user)
    except Topic.DoesNotExist:
        context = dict(user=request.user)
        return render_to_response("book/index.html", context_instance=RequestContext(request, context))
    return render_to_response("book/topic.html", context_instance=RequestContext(request, context))


def create_topic1(request, course_id):
    course = Course.objects.get(pk=course_id)
    message = course.name + "/" + " Add Topic"
    data_dict = {'course': course_id}
    print "in create topic 1"
    form = TopicForm(initial=data_dict)
    if request.method == 'POST':
        form = TopicForm(request.POST or None)
        print request.POST
    if form.is_valid():
        # topic=form.save()
        topic = form.save(commit=False)
        topic.number = 0
        topic.save()
        course = Course.objects.get(pk=int(course_id))
        message = topic.course.name + "/" + topic.name + "/" + " Successfully Added!"
        topic_list = Topic.objects.filter(course=course)
        subtopic_list = Subtopic.objects.all()[:]
        context = dict(message=message, topic_list=topic_list, subtopic_list=subtopic_list, user=request.user,
                       course=course)
        return render_to_response("book/all_topics.html", context_instance=RequestContext(request, context))

    else:
        form = TopicForm(initial=data_dict)
    context = dict(user=request.user, create_topic_form=form, course=course, message=message)
    # variables = RequestContext(request, {'create_topic_form': form })
    return render_to_response("book/admin_topic.html", context_instance=RequestContext(request, context))


def edit_topic(request, course_id, topic_id):
    topic = Topic.objects.get(pk=topic_id)
    form = TopicForm()
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES, instance=topic)
        # print request.POST
        # print request.FILES
        if form.is_valid():
            print topic.pk
            print "in after from valid edit topic"
            topic = form.save(commit=False)
            topic.number = 0
            topic.save()
            course = Course.objects.get(pk=int(course_id))
            message = topic.course.name + "/" + topic.name + "/" + " Successfully Edited!"
            topic_list = Topic.objects.filter(course=course)
            subtopic_list = Subtopic.objects.all()[:]
            context = dict(message=message, topic_list=topic_list, subtopic_list=subtopic_list, user=request.user,
                           course=course)
            return render_to_response("book/all_topics.html", context_instance=RequestContext(request, context))

    else:
        form = TopicForm(instance=topic)
    context = dict(user=request.user, edit_topic_form=form, topic=topic)
    return render_to_response("book/admin_topic.html", context_instance=RequestContext(request, context))


def delete_topic(request, course_id, topic_id):
    topic = Topic.objects.get(pk=topic_id)
    name = topic.course.name + "/" + topic.name
    topic.delete()
    message = name + " deleted"
    course = Course.objects.get(pk=int(course_id))
    topic_list = Topic.objects.filter(course=course)
    subtopic_list = Subtopic.objects.all()[:]
    context = dict(topic_list=topic_list, subtopic_list=subtopic_list, user=request.user, message=message,
                   course=course)
    return render_to_response("book/all_topics.html", context_instance=RequestContext(request, context))


def subtopics(request, course_id, topic_id, subtopic_id):
    try:
        subtopic = Subtopic.objects.get(pk=subtopic_id)
        context = dict(subtopic=subtopic, user=request.user)
    except Topic.DoesNotExist:
        context = dict(user=request.user)
        return render_to_response("book/index.html", context_instance=RequestContext(request, context))
    return render_to_response("book/subtopic.html", context_instance=RequestContext(request, context))


def create_subtopic1(request, course_id, topic_id):
    topic = Topic.objects.get(pk=topic_id)
    message = topic.course.name + "/" + topic.name + "/" + " Add Subtopic"
    data_dict = {'topic': topic_id}
    form = SubtopicForm(initial=data_dict)
    if request.method == 'POST':
        form = SubtopicForm(request.POST, request.FILES)
        print request.POST
        print request.FILES
        if form.is_valid():
            subtopic = form.save(commit=False)
            subtopic.number = 0
            subtopic.save()
            # subtopic=form.save()
            course = Course.objects.get(pk=int(course_id))
            message = subtopic.topic.course.name + "/" + subtopic.topic.name + "/" + subtopic.name + " Successfully Added!"
            topic_list = Topic.objects.filter(course=course)
            subtopic_list = Subtopic.objects.all()[:]
            context = dict(message=message, topic_list=topic_list, subtopic_list=subtopic_list, user=request.user,
                           course=course)
            return render_to_response("book/all_topics.html", context_instance=RequestContext(request, context))
    else:
        form = SubtopicForm(initial=data_dict)
    context = dict(user=request.user, create_subtopic_form=form, topic=topic, message=message)
    # variables = RequestContext(request, {'create_subtopic_form': form })
    return render_to_response("book/admin_subtopic.html", context_instance=RequestContext(request, context))


def edit_subtopics(request, course_id, topic_id, subtopic_id):
    subtopic = Subtopic.objects.get(pk=subtopic_id)
    form = SubtopicForm()
    if request.method == 'POST':
        form = SubtopicForm(request.POST, request.FILES, instance=subtopic)
        if form.is_valid():
            print subtopic.pk
            print "in after from valid edit subtopic"
            subtopic = form.save(commit=False)
            subtopic.number = 0
            subtopic.save()
            course = Course.objects.get(pk=int(course_id))
            message = subtopic.topic.course.name + "/" + subtopic.topic.name + "/" + subtopic.name + " Successfully Edited!"
            topic_list = Topic.objects.filter(course=course)
            subtopic_list = Subtopic.objects.all()[:]
            context = dict(message=message, topic_list=topic_list, subtopic_list=subtopic_list, user=request.user,
                           course=course)
            return render_to_response("book/all_topics.html", context_instance=RequestContext(request, context))
    else:
        form = SubtopicForm(instance=subtopic)
    context = dict(user=request.user, edit_subtopic_form=form, subtopic=subtopic, topic=subtopic.topic)
    return render_to_response("book/admin_subtopic.html", context_instance=RequestContext(request, context))


def delete_subtopic(request, course_id, topic_id, subtopic_id):
    subtopic = Subtopic.objects.get(pk=subtopic_id)
    name = subtopic.topic.course.name + "/" + subtopic.topic.name + "/" + subtopic.name
    subtopic.delete()
    message = name + " deleted"
    course = Course.objects.get(pk=int(course_id))
    topic_list = Topic.objects.filter(course=course)
    subtopic_list = Subtopic.objects.all()[:]
    context = dict(topic_list=topic_list, subtopic_list=subtopic_list, user=request.user, message=message,
                   course=course)
    return render_to_response("book/all_topics.html", context_instance=RequestContext(request, context))


def video_view(request, course_id, topic_id, subtopic_id):
    try:
        subtopic = Subtopic.objects.get(pk=subtopic_id)
        context = dict(subtopic=subtopic, user=request.user)
    except Topic.DoesNotExist:
        context = dict(user=request.user)
        return render_to_response("book/index.html", context_instance=RequestContext(request, context))
    return render_to_response("book/subtopic_video.html", context_instance=RequestContext(request, context))


def pdf_view(request):
    with open(MEDIA_ROOT + 'textbook/byteofpython_120.pdf', 'r') as pdf:
        response = HttpResponse(pdf.read(), mimetype='application/pdf')
        response['Content-Disposition'] = 'inline;filename=byteofpython_120.pdf'
        return response
    pdf.closed


def textbook_view(request, course_id, topic_id, subtopic_id):
    subtopic = Subtopic.objects.get(pk=subtopic_id)
    print subtopic.pdfbook
    with open(MEDIA_ROOT + str(subtopic.pdfbook), 'r') as pdf:
        response = HttpResponse(pdf.read(), mimetype='application/pdf')
        response['Content-Disposition'] = 'inline;filename=subtopic.pdfbook'
        return response
    pdf.closed


def slides_view(request, course_id, topic_id, subtopic_id):
    subtopic = Subtopic.objects.get(pk=subtopic_id)
    print subtopic.pdfslides
    with open(MEDIA_ROOT + str(subtopic.pdfslides), 'r') as pdf:
        response = HttpResponse(pdf.read(), mimetype='application/pdf')
        response['Content-Disposition'] = 'inline;filename=subtopic.pdfslides'
        return response
    pdf.closed


def annotations(request, subtopic_id):
    if request.method == 'POST':
        subtopic = Subtopic.objects.get(pk=subtopic_id)
        p = request.POST
        subtopic_id = subtopic_id
        user = request.user
        annotation_old = Annotation.objects.filter(subtopic=subtopic, created_by=request.user)
        annotation_old.delete()
        annotation = p["annotation"]
        annotation_obj = Annotation(subtopic=subtopic, created_by=user, annotation_text=annotation)
        annotation_obj.save()
        message = "Last Saved " + strftime("%Y-%m-%d %H:%M:%S", gmtime())
    else:
        subtopic = Subtopic.objects.get(pk=subtopic_id)
        annotation = Annotation.objects.filter(subtopic=subtopic, created_by=request.user)
        return render_to_response('book/subtopic_annotation.html',
                                  add_csrf(request, annotation=annotation, subtopic=subtopic))
    annotation = Annotation.objects.filter(subtopic=subtopic, created_by=request.user)
    return render_to_response("book/subtopic_annotation.html",
                              add_csrf(request, annotation=annotation, subtopic=subtopic, message=message))


def comments(request, subtopic_id):
    if request.method == 'POST':
        subtopic = Subtopic.objects.get(pk=subtopic_id)
        print subtopic.name
        p = request.POST
        subtopic_id = subtopic_id
        user = request.user
        comments = p["comments"]
        comment_obj = Comments(subtopic=subtopic, created_by=user, comment_text=comments)
        comment_obj.save()
    else:
        subtopic = Subtopic.objects.get(pk=subtopic_id)
        print subtopic.name
        print subtopic.id
        print "im in else"
        comments = Comments.objects.filter(subtopic=subtopic)
        return render_to_response('book/subtopic_comments.html',
                                  add_csrf(request, comments=comments, subtopic=subtopic))
    comments = Comments.objects.filter(subtopic=subtopic)
    return render_to_response("book/subtopic_comments.html", add_csrf(request, comments=comments, subtopic=subtopic))


def add_csrf(request, **kwargs):
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    csrfContext = RequestContext(request, d)
    return csrfContext


def pdf_view1(request):
    context = dict(filename=MEDIA_URL + 'textbook/byteofpython_120.pdf', user=request.user)
    return render_to_response("book/pdf_iframe.html", context_instance=RequestContext(request, context))


def lecturer_help(request):
    context = dict(filename=MEDIA_URL + 'help/lecturer_overview.pdf', user=request.user)
    return render_to_response("book/pdf_iframe.html", context_instance=RequestContext(request, context))


def student_help(request):
    context = dict(filename=MEDIA_URL + 'help/student_overview.pdf', user=request.user)
    return render_to_response("book/pdf_iframe.html", context_instance=RequestContext(request, context))


def pdf_view_google(request):
    context = dict(filename='www.iasted.org/conferences/formatting/presentations-tips.ppt', user=request.user)
    return render_to_response("book/pdf_iframegoogle.html", context_instance=RequestContext(request, context))


def all_topics(request, course_id):
    try:
        course = Course.objects.get(pk=int(course_id))
        topic_list = Topic.objects.filter(course=course)
        subtopic_list = Subtopic.objects.all()[:]
        context = dict(topic_list=topic_list, subtopic_list=subtopic_list, user=request.user, course=course)
    except Topic.DoesNotExist:
        context = dict(user=request.user)
        return render_to_response("book/index.html", context_instance=RequestContext(request, context))
    return render_to_response("book/all_topics.html", context_instance=RequestContext(request, context))


def analytics(request):
    try:
        course_list = Course.objects.all()
        topic_list = Topic.objects.all()
        subtopic_list = Subtopic.objects.all()[:]
        context = dict(topic_list=topic_list, subtopic_list=subtopic_list, user=request.user, course_list=course_list)
    except Topic.DoesNotExist:
        context = dict(user=request.user)
        return render_to_response("book/analytics.html", context_instance=RequestContext(request, context))
    return render_to_response("book/analytics.html", context_instance=RequestContext(request, context))


def general_analytics(request, course_id):
    course = Course.objects.get(pk=course_id)
    topic_list = Topic.objects.filter(course=course)
    subtopic_list = Subtopic.objects.filter(topic__in=topic_list)
    question_list = Question.objects.filter(subtopic__in=subtopic_list)
    user_list = User.objects.all()
    mcq_attempts = MCQGuess.objects.none()
    mcq_dict = {}
    cq_dict = {}
    comment_dict = {}
    for user in user_list:
        # create a query set with user and count
        mcq_count = MCQGuess.objects.filter(submitted_by=user, question=question_list).count()
        # mcq_dict.setdefault(user.username, []).append(mcq_count)
        mcq_dict.setdefault(user.username, mcq_count)

        cq_count = Attempt.objects.filter(user=user).count()
        cq_dict.setdefault(user.username, cq_count)

        comment_count = Comments.objects.filter(created_by=user, subtopic__in=subtopic_list).count()
        comment_dict.setdefault(user.username, comment_count)

    print mcq_dict
    context = dict(user=request.user, course=course, mcq_dict=mcq_dict, cq_dict=cq_dict, comment_dict=comment_dict)
    return render_to_response("book/general_analytics.html", context_instance=RequestContext(request, context))


def cq_analytics(request, course_id, user_username):
    course = Course.objects.get(pk=course_id)
    topic_list = Topic.objects.filter(course=course)
    subtopic_list = Subtopic.objects.filter(topic__in=topic_list)
    question_list = Question.objects.filter(subtopic__in=subtopic_list)
    user_analytics = User.objects.get(username=user_username)
    cq_attmpt_list = Attempt.objects.filter(user=user_analytics, question__in=question_list)
    context = dict(user=request.user, course=course, cq_attmpt_list=cq_attmpt_list, user_analytics=user_analytics)
    return render_to_response("book/cq_analytics.html", context_instance=RequestContext(request, context))


def mcq_analytics(request, course_id, user_username):
    course = Course.objects.get(pk=course_id)
    topic_list = Topic.objects.filter(course=course)
    subtopic_list = Subtopic.objects.filter(topic__in=topic_list)
    question_list = Question.objects.filter(subtopic__in=subtopic_list)
    user_analytics = User.objects.get(username=user_username)
    comment_list = Comments.objects.filter(created_by=user_analytics, subtopic__in=subtopic_list)
    answer_list = Answer.objects.filter(question__in=question_list)
    mcq_attmpt_list = MCQGuess.objects.filter(submitted_by=user_analytics, question__in=question_list)
    context = dict(user=request.user, course=course, answer_list=answer_list, mcq_attmpt_list=mcq_attmpt_list,
                   user_analytics=user_analytics)
    return render_to_response("book/mcq_analytics.html", context_instance=RequestContext(request, context))


def subtopic_mcq_analytics(request, subtopic_id):
    subtopic = Subtopic.objects.get(pk=subtopic_id)
    question_list = Question.objects.filter(subtopic=subtopic)
    user_list = User.objects.all()
    # mcq_list=Question
    answer_list = Answer.objects.all()
    mcq_attmpt_list = MCQGuess.objects.filter(question__in=question_list)
    print mcq_attmpt_list
    context = dict(user=request.user, answer_list=answer_list, subtopic=subtopic, question_list=question_list,
                   mcq_attmpt_list=mcq_attmpt_list)
    return render_to_response("book/subtopic_analytics.html", context_instance=RequestContext(request, context))


def subtopic_cq_analytics(request, subtopic_id):
    subtopic = Subtopic.objects.get(pk=subtopic_id)
    cq_list = Q1.objects.filter(subtopic=subtopic)
    print cq_list
    test_case_list = TestCase.objects.filter(question__in=cq_list)
    user_list = User.objects.all()
    attempt_list = Attempt.objects.filter(question__in=cq_list)
    keyword_list = Keyword.objects.filter(question__in=cq_list)
    context = dict(user=request.user, attempt_list=attempt_list, subtopic=subtopic, test_case_list=test_case_list,
                   keyword_list=keyword_list, cq_list=cq_list, user_list=user_list)
    return render_to_response("book/subtopic_analytics.html", context_instance=RequestContext(request, context))


def subtopic_comments_analytics(request, subtopic_id):
    subtopic = Subtopic.objects.get(pk=subtopic_id)
    comment_list = Comments.objects.filter(subtopic=subtopic)
    user_list = User.objects.all()
    context = dict(user=request.user, comment_list=comment_list, subtopic=subtopic, user_list=user_list)
    return render_to_response("book/subtopic_analytics.html", context_instance=RequestContext(request, context))


def comment_analytics(request, course_id, user_username):
    course = Course.objects.get(pk=course_id)
    topic_list = Topic.objects.filter(course=course)
    subtopic_list = Subtopic.objects.filter(topic__in=topic_list)
    user_analytics = User.objects.get(username=user_username)
    comment_list = Comments.objects.filter(created_by=user_analytics, subtopic__in=subtopic_list)
    context = dict(user=request.user, course=course, comment_list=comment_list, user_analytics=user_analytics)
    return render_to_response("book/comments_analytics.html", context_instance=RequestContext(request, context))


def all_users(request):
    try:
        user_list = User.objects.all()
        context = dict(user=request.user, user_list=user_list)
    except User.DoesNotExist:
        context = dict(user=request.user)
        return render_to_response("book/index.html", context_instance=RequestContext(request, context))
    return render_to_response("registration/all_users.html", context_instance=RequestContext(request, context))


def delete_user(request, user_username):
    try:
        user1 = User.objects.get(username=user_username)
        user1.delete()
        user_list = User.objects.all()
        message = user_username + " deleted"
        context = dict(user=request.user, user_list=user_list, message=message)
    except User.DoesNotExist:
        context = dict(user=request.user)
        return render_to_response("book/index.html", context_instance=RequestContext(request, context))
    return render_to_response("registration/all_users.html", context_instance=RequestContext(request, context))


def admin_user(request, user_username):
    try:
        user1 = User.objects.get(username=user_username)
        user1.is_staff = True
        user1.is_superuser = True
        user1.save()
        user_list = User.objects.all()
        message = user_username + " upgraded to Admin"
        context = dict(user=request.user, user_list=user_list, message=message)
    except User.DoesNotExist:
        context = dict(user=request.user)
        return render_to_response("book/index.html", context_instance=RequestContext(request, context))
    return render_to_response("registration/all_users.html", context_instance=RequestContext(request, context))


def unadmin_user(request, user_username):
    try:
        user1 = User.objects.get(username=user_username)
        user1.is_superuser = False
        user1.is_staff = False
        user1.save()
        user_list = User.objects.all()
        message = user_username + " downgraded from Admin"
        context = dict(user=request.user, user_list=user_list, message=message)
    except User.DoesNotExist:
        context = dict(user=request.user)
        return render_to_response("book/index.html", context_instance=RequestContext(request, context))
    return render_to_response("registration/all_users.html", context_instance=RequestContext(request, context))
