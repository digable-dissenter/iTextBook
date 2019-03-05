# Create your views here.
import mmap
import os
import subprocess
from datetime import datetime
from random import randint

from django import template
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template import RequestContext

from book.models import *
from box.models import *
from itextbook.settings import MEDIA_ROOT

register = template.Library()


def create_cq(request, course_id, topic_id, subtopic_id):
    subtopic = Subtopic.objects.get(pk=subtopic_id)
    course = Course.objects.get(pk=course_id)

    data_dict = {'subtopic': subtopic_id}
    print "in create cq"
    question_form = QuestionForm(initial=data_dict)
    cquestion_keyword_form = KeywordForm()
    cquestion_testcase_form = TestCaseForm()
    if request.method == 'POST':
        question_form = QuestionForm(request.POST or None)
        print request.POST
    if question_form.is_valid():
        p = request.POST

        cquestion_testcase_form = TestCaseForm(request.POST or None)
        message = "Please correct errors below!"
        if p.get("keyword", "") == "":
            keyword_error = " Please add a keyword and min use!"
            # add question and answers to context for error message on template and prefilled values
            context = dict(user=request.user, create_cquestion_form=question_form, subtopic=subtopic, message=message,
                           cquestion_keyword_form=cquestion_keyword_form,
                           cquestion_testcase_form=cquestion_testcase_form, keyword_error=keyword_error)
            return render_to_response("book/admin_question.html", context_instance=RequestContext(request, context))
        keyword_text = p.get("keyword", "")

        if p.get("min_use", "") == "":
            min_use_error = " Please add min use!"
            # add question and answers to context for error message on template and prefilled values
            context = dict(user=request.user, create_cquestion_form=question_form, subtopic=subtopic, message=message,
                           cquestion_keyword_form=cquestion_keyword_form,
                           cquestion_testcase_form=cquestion_testcase_form, keyword=keyword_text,
                           min_use_error=min_use_error)
            return render_to_response("book/admin_question.html", context_instance=RequestContext(request, context))
        min_use_text = p.get("min_use", "")

        testinput1 = p.get("testinput1", "")
        testinput2 = p.get("testinput2", "")
        testinput3 = p.get("testinput3", "")
        testoutput1 = p.get("testoutput1", "")
        testoutput2 = p.get("testoutput2", "")
        testoutput3 = p.get("testoutput3", "")

        test_cases_error = "Please add 3 Test Cases!"
        if p.get("testinput1", "") == "":
            testinput1_error = " Please add input!"
            # add question and answers to context for error message on template and prefilled values
            context = dict(user=request.user, testinput1_error=testinput1_error, create_cquestion_form=question_form,
                           test_cases_error=test_cases_error, subtopic=subtopic, message=message,
                           cquestion_keyword_form=cquestion_keyword_form,
                           cquestion_testcase_form=cquestion_testcase_form, keyword=keyword_text, min_use=min_use_text,
                           testoutput1=testoutput1, testoutput2=testoutput2, testoutput3=testoutput3,
                           testinput2=testinput2, testinput3=testinput3)
            return render_to_response("book/admin_question.html", context_instance=RequestContext(request, context))

        if p.get("testoutput1", "") == "":
            testoutput1_error = " Please add output!"
            # add question and answers to context for error message on template and prefilled values
            context = dict(user=request.user, testoutput1_error=testoutput1_error, create_cquestion_form=question_form,
                           subtopic=subtopic, test_cases_error=test_cases_error, message=message,
                           cquestion_keyword_form=cquestion_keyword_form,
                           cquestion_testcase_form=cquestion_testcase_form, keyword=keyword_text, min_use=min_use_text,
                           testinput1=testinput1, testoutput2=testoutput2, testoutput3=testoutput3,
                           testinput2=testinput2, testinput3=testinput3)
            return render_to_response("book/admin_question.html", context_instance=RequestContext(request, context))

        if p.get("testinput2", "") == "":
            testinput2_error = " Please add input!"
            # add question and answers to context for error message on template and prefilled values
            context = dict(user=request.user, testinput2_error=testinput2_error, create_cquestion_form=question_form,
                           test_cases_error=test_cases_error, subtopic=subtopic, message=message,
                           cquestion_keyword_form=cquestion_keyword_form,
                           cquestion_testcase_form=cquestion_testcase_form, keyword=keyword_text, min_use=min_use_text,
                           testoutput1=testoutput1, testoutput2=testoutput2, testoutput3=testoutput3,
                           testinput1=testinput1, testinput3=testinput3)
            return render_to_response("book/admin_question.html", context_instance=RequestContext(request, context))

        if p.get("testoutput2", "") == "":
            testoutput2_error = " Please add output!"
            # add question and answers to context for error message on template and prefilled values
            context = dict(user=request.user, testoutput2_error=testoutput2_error, create_cquestion_form=question_form,
                           subtopic=subtopic, test_cases_error=test_cases_error, message=message,
                           cquestion_keyword_form=cquestion_keyword_form,
                           cquestion_testcase_form=cquestion_testcase_form, keyword=keyword_text, min_use=min_use_text,
                           testinput1=testinput1, testoutput1=testoutput1, testoutput3=testoutput3,
                           testinput2=testinput2, testinput3=testinput3)
            return render_to_response("book/admin_question.html", context_instance=RequestContext(request, context))

        if p.get("testinput3", "") == "":
            testinput3_error = " Please add input!"
            # add question and answers to context for error message on template and prefilled values
            context = dict(user=request.user, testinput3_error=testinput3_error, create_cquestion_form=question_form,
                           test_cases_error=test_cases_error, subtopic=subtopic, message=message,
                           cquestion_keyword_form=cquestion_keyword_form,
                           cquestion_testcase_form=cquestion_testcase_form, keyword=keyword_text, min_use=min_use_text,
                           testoutput1=testoutput1, testoutput2=testoutput2, testoutput3=testoutput3,
                           testinput2=testinput2, testinput1=testinput1)
            return render_to_response("book/admin_question.html", context_instance=RequestContext(request, context))

        if p.get("testoutput3", "") == "":
            testoutput3_error = " Please add output!"
            # add question and answers to context for error message on template and prefilled values
            context = dict(user=request.user, testoutput3_error=testoutput3_error, create_cquestion_form=question_form,
                           subtopic=subtopic, test_cases_error=test_cases_error, message=message,
                           cquestion_keyword_form=cquestion_keyword_form,
                           cquestion_testcase_form=cquestion_testcase_form, keyword=keyword_text, min_use=min_use_text,
                           testinput1=testinput1, testoutput2=testoutput2, testoutput1=testoutput1,
                           testinput2=testinput2, testinput3=testinput3)
            return render_to_response("book/admin_question.html", context_instance=RequestContext(request, context))

        question = question_form.save()
        test_case1 = TestCase(question=question, test_input=p.get("testinput1", ""),
                              test_output=p.get("testoutput1", ""))
        test_case1.save()
        test_case2 = TestCase(question=question, test_input=p.get("testinput2", ""),
                              test_output=p.get("testoutput2", ""))
        test_case2.save()
        test_case3 = TestCase(question=question, test_input=p.get("testinput3", ""),
                              test_output=p.get("testoutput3", ""))
        test_case3.save()
        keyword = Keyword(question=question, text=keyword_text, min_use=p.get("min_use", ""))
        keyword.save()

        message = subtopic.topic.name + "/" + subtopic.name + "/" + " Coding Question Added"
        cq_list = Question.objects.filter(subtopic=subtopic)
        attempt_list = Attempt.objects.filter(question__in=cq_list)
        # return render_to_response("box/quiz.html", add_csrf(request, message =message, subtopic=subtopic, cq_list=cq_list, attempt_list=attempt_list))
        topic_list = Topic.objects.filter(course=course)
        subtopic_list = Subtopic.objects.all()[:]
        context = dict(message=message, topic_list=topic_list, subtopic_list=subtopic_list, user=request.user,
                       course=course)
        return render_to_response("book/all_topics.html", context_instance=RequestContext(request, context))

    else:
        context = dict(user=request.user, create_cquestion_form=question_form, subtopic=subtopic,
                       cquestion_keyword_form=cquestion_keyword_form, cquestion_testcase_form=cquestion_testcase_form)
    return render_to_response("book/admin_question.html", context_instance=RequestContext(request, context))


def edit_cq(request, course_id, topic_id, subtopic_id, question_id):
    question = Question.objects.get(pk=question_id)
    subtopic = Subtopic.objects.get(pk=subtopic_id)
    test_case_list = TestCase.objects.filter(question=question)
    form = QuestionForm(instance=question)
    message = subtopic.name + "/" + " Edit CQ"
    keyword_list = Keyword.objects.filter(question=question)
    # test_case_form=TestCaseForm(instance=test_case)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES, instance=question)
        if question_form.is_valid():
            p = request.POST
            # cquestion_testcase_form = TestCaseForm(request.POST,  instance=test_case)
            i = 0
            for keyword in keyword_list:
                i += 1
                if p.get("keyword" + str(i), "") == "":
                    keyword_error = " Please add a keyword and min use"
                    # add question and answers to context for error message on template and prefilled values
                    context = dict(user=request.user, edit_cq_form=question_form, question=question, subtopic=subtopic,
                                   message=message, keyword_error=keyword_error)
                    return render_to_response("box/admin_cq.html", context_instance=RequestContext(request, context))

                if p.get("min_use" + str(i), "") == "":
                    min_use_error = " Please add min use"
                    keyword = p.get("keyword" + str(i), "")
                    # add question and answers to context for error message on template and prefilled values
                    context = dict(user=request.user, edit_cq_form_form=question_form, question=question,
                                   subtopic=subtopic, message=message, keyword=keyword, keyword_list=keyword_list,
                                   min_use_error=min_use_error)
                    return render_to_response("box/admin_cq.html", context_instance=RequestContext(request, context))

                testinput1 = p.get("testinput1", "")
            testinput2 = p.get("testinput2", "")
            testinput3 = p.get("testinput3", "")
            testoutput1 = p.get("testoutput1", "")
            testoutput2 = p.get("testoutput2", "")
            testoutput3 = p.get("testoutput3", "")

            test_cases_error = "Please add 3 Test Cases!"
            if p.get("testinput1", "") == "":
                testinput1_error = " Please add input!"
                # add question and answers to context for error message on template and prefilled values
                context = dict(user=request.user, testinput1_error=testinput1_error, edit_cq_form=question_form,
                               test_cases_error=test_cases_error, question=question, subtopic=subtopic, message=message,
                               keyword_list=keyword_list, testoutput1=testoutput1, testoutput2=testoutput2,
                               testoutput3=testoutput3, testinput2=testinput2, testinput3=testinput3)
                return render_to_response("box/admin_cq.html", context_instance=RequestContext(request, context))

            if p.get("testoutput1", "") == "":
                testoutput1_error = " Please add output!"
                # add question and answers to context for error message on template and prefilled values
                context = dict(user=request.user, testoutput1_error=testoutput1_error, edit_cq_form=question_form,
                               question=question, subtopic=subtopic, test_cases_error=test_cases_error, message=message,
                               keyword_list=keyword_list, testinput1=testinput1, testoutput2=testoutput2,
                               testoutput3=testoutput3, testinput2=testinput2, testinput3=testinput3)
                return render_to_response("box/admin_cq.html", context_instance=RequestContext(request, context))

            if p.get("testinput2", "") == "":
                testinput2_error = " Please add input!"
                # add question and answers to context for error message on template and prefilled values
                context = dict(user=request.user, testinput2_error=testinput2_error, edit_cq_form=question_form,
                               test_cases_error=test_cases_error, subtopic=subtopic, message=message,
                               keyword_list=keyword_list, testoutput1=testoutput1, testoutput2=testoutput2,
                               testoutput3=testoutput3, testinput1=testinput1, testinput3=testinput3)
                return render_to_response("box/admin_cq.html", context_instance=RequestContext(request, context))

            if p.get("testoutput2", "") == "":
                testoutput2_error = " Please add output!"
                # add question and answers to context for error message on template and prefilled values
                context = dict(user=request.user, testoutput2_error=testoutput2_error, edit_cq_form=question_form,
                               question=question, subtopic=subtopic, test_cases_error=test_cases_error, message=message,
                               keyword_list=keyword_list, testinput1=testinput1, testoutput1=testoutput1,
                               testoutput3=testoutput3, testinput2=testinput2, testinput3=testinput3)
                return render_to_response("box/admin_cq.html", context_instance=RequestContext(request, context))

            if p.get("testinput3", "") == "":
                testinput3_error = " Please add input!"
                # add question and answers to context for error message on template and prefilled values
                context = dict(user=request.user, testinput3_error=testinput3_error, edit_cq_form=question_form,
                               test_cases_error=test_cases_error, question=question, subtopic=subtopic, message=message,
                               keyword_list=keyword_list, testoutput1=testoutput1, testoutput2=testoutput2,
                               testoutput3=testoutput3, testinput2=testinput2, testinput1=testinput1)
                return render_to_response("box/admin_cq.html", context_instance=RequestContext(request, context))

            if p.get("testoutput3", "") == "":
                testoutput3_error = " Please add output!"
                # add question and answers to context for error message on template and prefilled values
                context = dict(user=request.user, testoutput3_error=testoutput3_error, edit_cq_form=question_form,
                               question=question, subtopic=subtopic, test_cases_error=test_cases_error, message=message,
                               keyword_list=keyword_list, testinput1=testinput1, testoutput2=testoutput2,
                               testoutput1=testoutput1, testinput2=testinput2, testinput3=testinput3)
                return render_to_response("box/admin_cq.html", context_instance=RequestContext(request, context))

            question = question_form.save()
            j = 0
            for test_case in test_case_list:
                j += 1
                test_case.question = question
                test_case.test_input = p.get("testinput" + str(j), "")
                test_case.test_output = p.get("testoutput" + str(j), "")
                test_case.save()

            i = 0
            for keyword in keyword_list:
                i += 1
                keyword.question = question
                keyword.text = p.get("keyword" + str(i), "")
                keyword.min_use = p.get("min_use" + str(i), "")
                keyword.save()
                # keyword=Keyword(question = question, text = p.get("keyword", ""), min_use = p.get("min_use", ""))
                keyword.save()

            message = subtopic.name + "/" + " CQ Edited Successfully"
            cq_list = Question.objects.filter(subtopic=subtopic)
            attempt_list = Attempt.objects.filter(question__in=cq_list)
            return render_to_response("box/quiz.html",
                                      add_csrf(request, message=message, subtopic=subtopic, cq_list=cq_list,
                                               attempt_list=attempt_list))

    else:
        context = dict(user=request.user, edit_cq_form=form, test_case_list=test_case_list, subtopic=subtopic,
                       question=question, message=message, keyword_list=keyword_list)
        return render_to_response("box/admin_cq.html", context_instance=RequestContext(request, context))


def add_keyword(request, course_id, topic_id, subtopic_id, question_id):
    question = Question.objects.get(pk=question_id)
    # test_case= TestCase.objects.get(question=question)
    keyword_list = Keyword.objects.filter(question=question)
    test_case_list = TestCase.objects.filter(question=question)
    # test_case_form=TestCaseForm(instance=test_case)
    subtopic = Subtopic.objects.get(pk=subtopic_id)
    form = QuestionForm(instance=question)
    message = subtopic.name + "/" + " Edit MCQ"
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES, instance=question)
        if question_form.is_valid():
            p = request.POST
            if p.get("keyword", "") == "":
                keyword_error = " Please add a keyword and min use"
                # add question and answers to context for error message on template and prefilled values
                context = dict(user=request.user, add_keyword_form=form, subtopic=subtopic, question=question,
                               message=message, keyword_error=keyword_error)
                return render_to_response("box/admin_cq.html", context_instance=RequestContext(request, context))

            if p.get("min_use", "") == "":
                min_use_error = " Please add min use"
                keyword = p.get("keyword", "")
                # add question and answers to context for error message on template and prefilled values
                context = dict(user=request.user, add_keyword_form=form, subtopic=subtopic, question=question,
                               message=message, keyword=keyword, min_use_error=min_use_error)
                return render_to_response("box/admin_cq.html", context_instance=RequestContext(request, context))

            question = question_form.save()
            keyword = Keyword(question=question, text=p.get("keyword", ""), min_use=p.get("min_use", ""))
            keyword.save()

            message = subtopic.name + "/" + " Keyword Added - " + keyword.text
            cq_list = Question.objects.filter(subtopic=subtopic)

            return render_to_response("box/admin_cq.html",
                                      add_csrf(request, edit_cq_form=form, test_case_list=test_case_list,
                                               subtopic=subtopic, question=question, message=message,
                                               keyword_list=keyword_list))


    else:
        context = dict(user=request.user, add_keyword_form=form, subtopic=subtopic, question=question, message=message,
                       keyword_list=keyword_list, test_case_list=test_case_list)
        return render_to_response("box/admin_cq.html", context_instance=RequestContext(request, context))


def add_testcase(request, course_id, topic_id, subtopic_id, question_id):
    question = Question.objects.get(pk=question_id)
    keyword_list = Keyword.objects.filter(question=question)
    test_case_list = TestCase.objects.filter(question=question)
    subtopic = Subtopic.objects.get(pk=subtopic_id)
    form = QuestionForm(instance=question)
    message = subtopic.name + "/" + " Edit MCQ"
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES, instance=question)
        if question_form.is_valid():
            p = request.POST

            if p.get("testinput", "") == "":
                testinput_error = " Please add an input"
                # add question and answers to context for error message on template and prefilled values
                context = dict(user=request.user, add_testcase_form=form, subtopic=subtopic, question=question,
                               message=message, testinput_error=testinput_error)
                return render_to_response("box/admin_cq.html", context_instance=RequestContext(request, context))

            if p.get("testoutput", "") == "":
                testoutput_error = " Please add an output"
                testinput = p.get("testinput", "")
                # add question and answers to context for error message on template and prefilled values
                context = dict(user=request.user, add_testcase_form=form, subtopic=subtopic, question=question,
                               message=message, testinput=testinput, testoutput_error=testoutput_error)
                return render_to_response("box/admin_cq.html", context_instance=RequestContext(request, context))

            question = question_form.save()
            testcase = TestCase(question=question, test_input=p.get("testinput", ""),
                                test_output=p.get("testoutput", ""))
            testcase.save()

            message = subtopic.name + "/" + " TestCase Added - (" + testcase.test_input + "/" + testcase.test_output + ")"
            cq_list = Question.objects.filter(subtopic=subtopic)

            return render_to_response("box/admin_cq.html",
                                      add_csrf(request, edit_cq_form=form, test_case_list=test_case_list,
                                               subtopic=subtopic, question=question, message=message,
                                               keyword_list=keyword_list))
    else:
        context = dict(user=request.user, add_testcase_form=form, subtopic=subtopic, question=question, message=message,
                       keyword_list=keyword_list, test_case_list=test_case_list)
        return render_to_response("box/admin_cq.html", context_instance=RequestContext(request, context))


def delete_cq(request, course_id, topic_id, subtopic_id, question_id):
    question = Question.objects.get(pk=question_id)
    keywords_list = Keyword.objects.filter(question=question)
    for keyword in keywords_list:
        keyword.delete()
    test_case_list = TestCase.objects.filter(question=question)
    for test_case in test_case_list:
        test_case.delete()
    subtopic = Subtopic.objects.get(pk=subtopic_id)
    name = subtopic.name + "/" + question.text
    message = name + " and related keywords, test case deleted"
    question.delete()
    cq_list = Question.objects.filter(subtopic=subtopic)
    attempt_list = Attempt.objects.filter(question__in=cq_list)
    return render_to_response("box/quiz.html", add_csrf(request, message=message, subtopic=subtopic, cq_list=cq_list,
                                                        attempt_list=attempt_list))


def delete_keyword(request, course_id, topic_id, subtopic_id, question_id, keyword_id):
    question = Question.objects.get(pk=question_id)
    keyword = Keyword.objects.get(pk=keyword_id)
    subtopic = Subtopic.objects.get(pk=subtopic_id)
    name = subtopic.name + "/" + keyword.text
    message = name + " Keyword deleted"
    keyword.delete()
    test_case_list = TestCase.objects.filter(question=question)
    # test_case_form=TestCaseForm(instance=test_case)
    form = QuestionForm(instance=question)
    keyword_list = Keyword.objects.filter(question=question)
    context = dict(user=request.user, edit_cq_form=form, test_case_list=test_case_list, subtopic=subtopic,
                   question=question, message=message, keyword_list=keyword_list)
    return render_to_response("box/admin_cq.html", context_instance=RequestContext(request, context))


def delete_testcase(request, course_id, topic_id, subtopic_id, question_id, testcase_id):
    question = Question.objects.get(pk=question_id)
    testcase = TestCase.objects.get(pk=testcase_id)
    subtopic = Subtopic.objects.get(pk=subtopic_id)
    name = subtopic.name + "- (" + testcase.test_input + " / " + testcase.test_output
    message = name + ") TestCase successfully deleted!"
    testcase.delete()
    test_case_list = TestCase.objects.filter(question=question)
    # test_case_form=TestCaseForm(instance=test_case)
    form = QuestionForm(instance=question)
    keyword_list = Keyword.objects.filter(question=question)
    context = dict(user=request.user, edit_cq_form=form, test_case_list=test_case_list, subtopic=subtopic,
                   question=question, message=message, keyword_list=keyword_list)
    return render_to_response("box/admin_cq.html", context_instance=RequestContext(request, context))


def code_execution(stdout_result):
    if 'Error' in stdout_result:
        return 'Error: Your code failed to run, check your syntax and try again!'
    else:
        return stdout_result


def comments_check1(user_code):
    f = open(user_code)
    s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    comment = "#"
    comments_counter = 0
    if comment in s:
        for comment in s:
            comments_counter += 1
            break
    return comments_counter


def keywords_check1(keyword, min_num, user_code):
    keyword_counter = 0
    f = open((user_code), 'r')
    mystr = f.read()
    keyword_counter += mystr.count(keyword)
    f.close()
    return keyword_counter


def test_case(code, test_input, test_output, user):
    test_code = code.replace("var1", str(test_input))
    timestamp = str(datetime.now())[:-7]
    timestamp_string = ''.join(timestamp.split())
    file_n = "test_" + str(user) + "_" + timestamp_string
    file_name = file_n + ".py"
    dest_dir = os.path.join(MEDIA_ROOT, 'testcases')
    try:
        os.makedirs(dest_dir)
    except OSError:
        pass  # already exists
    path = os.path.join(dest_dir, file_name)
    FILE = open(path, "w")
    # Write all the lines at once:
    FILE.writelines(test_code)
    FILE.close()
    test_response = file_name + " created successfully with contents " + test_code
    return path


def subtopic_quiz_attempt(request, course_id, topic_id, subtopic_id, cq_id, attempt_id):
    try:
        subtopic = Subtopic.objects.get(pk=int(subtopic_id))
        question = Question.objects.get(pk=int(cq_id))
        attempt = Attempt.objects.get(pk=int(attempt_id))
        f = open(attempt.code).readlines()
    except attempt.DoesNotExist:
        context = dict(subtopic=subtopic, user=request.user, question=question)
        return render_to_response("box/quiz_attempt.html", context_instance=RequestContext(request, context))
    context = dict(subtopic=subtopic, user=request.user, question=question, attempt=attempt, f=f)
    return render_to_response("box/quiz_attempt.html", context_instance=RequestContext(request, context))


def subtopic_quiz(request, course_id, topic_id, subtopic_id):
    try:
        subtopic = Subtopic.objects.get(pk=subtopic_id)
        cq_list = Question.objects.filter(subtopic=subtopic)
        attempt_list = Attempt.objects.filter(question__in=cq_list, user=request.user)
        print cq_list
    except subtopic.DoesNotExist:
        context = dict(subtopic=subtopic, user=request.user)
        return render_to_response("box/quiz.html", context_instance=RequestContext(request, context))
    context = dict(subtopic=subtopic, user=request.user, cq_list=cq_list, attempt_list=attempt_list)
    return render_to_response("box/quiz.html", context_instance=RequestContext(request, context))


def codeform(request, course_id, topic_id, subtopic_id, cq_id):
    course = Course.objects.get(pk=course_id)
    if request.method == "POST":
        p = request.POST

        if p.get("code", "") == "":
            code_error = " Please enter some code!"
            subtopic = Subtopic.objects.get(pk=int(subtopic_id))
            question = Question.objects.get(pk=int(cq_id))
            return render_to_response("box/codeform.html",
                                      add_csrf(request, subtopic=subtopic, question=question, code_error=code_error))

        code = p["code"]
        language = str(course.language)
        user = request.user
        rand1 = randint(100, 99999999999)
        rand2 = randint(100, 99999999999)
        rand = rand1 + rand2
        file_n = str(user) + "_" + str(rand)
        # timestamp=str(datetime.now())[:-7]
        # timestamp_string = ''.join(timestamp.split())
        # file_n = str(user) + "_"+timestamp_string
        print language
        file_ext = ""
        if language == "python3.2":
            file_ext = ".py"
        if language == "java":
            file_ext = ".java"
        # rand= randint(100, 99999999999)
        # file_n = str(user) + "_"+str(rand)
        if language == "c":
            file_ext = ".c"
        # rand= randint(100, 99999999999)
        # file_n = str(user) + "_"+str(rand)
        if language == "perl":
            file_ext = ".pl"
        print file_ext
        # input = p["input"]

        file_name = file_n + file_ext
        print file_name
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # dest_dir = os.path.join(script_dir, 'submissions')
        dest_dir = os.path.join(MEDIA_ROOT, 'submissions')
        download_path = 'submissions/' + file_name
        try:
            os.makedirs(dest_dir)
        except OSError:
            pass  # already exists
        path = os.path.join(dest_dir, file_name)
        # Let's create some data:
        # Create a file object:
        # in "write" mode
        FILE = open(path, "w")
        # Write all the lines at once:
        if language == "java":
            class_name_added = "class " + file_n + " { " + code + " } "
            FILE.writelines(class_name_added)
        else:
            FILE.writelines(code)
        FILE.close()
    else:
        subtopic = Subtopic.objects.get(pk=int(subtopic_id))
        try:
            question = Question.objects.get(pk=int(cq_id))
            return render_to_response('box/codeform.html',
                                      dict(user=request.user, question=question, subtopic=subtopic),
                                      context_instance=RequestContext(request))
        except Question.DoesNotExist:
            return render_to_response('box/codeform.html', dict(user=request.user, subtopic=subtopic),
                                      context_instance=RequestContext(request))

    subtopic = Subtopic.objects.get(pk=int(subtopic_id))
    question = Question.objects.get(pk=int(cq_id))
    # Test case
    test_case_list = TestCase.objects.filter(question=question)
    score = 0
    marks_available = 0
    marks_lost = ""
    marks_gained = ""
    test_result = ""
    counter = 0
    for test_case_obj in test_case_list:
        counter += 1
        test_output = test_case_obj.test_output
        test_input = test_case_obj.test_input

        if language == "java":
            test_response = java(test_input, file_n, path, dest_dir)
            print counter
            print test_response
        if language == "c":
            test_response = c_code(test_input, file_n, path, dest_dir)
            print counter
        else:
            test_proc = subprocess.Popen(course.language + " " + path, shell=True, stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            test_response = test_proc.communicate(input=test_input)[0]

        if 'Error' in test_response:
            test_result = 'Your code failed to run, check your syntax and try again!'
            marks_lost = "Code did not execute, "
            marks_gained = "None"
            feedback = "Score: " + str(
                score) + " Remark: " + test_result + "Marks Gained: " + marks_gained + " Marks Lost: " + marks_lost
            attempt_obj = Attempt(user=user, question=question, score=score, code=path, feedback=feedback)
            attempt_obj.save()
            print "after attmpt obj save Error in test_response"
            return render_to_response("box/codeform.html",
                                      add_csrf(request, output=test_response, testcase=test_result, score=score,
                                               question=question, subtopic=subtopic, code=code, marks_lost=marks_lost,
                                               marks_gained=marks_gained, download_path=download_path))
        # else:
        #	score+=5
        #	marks_available += 5
        #	marks_gained += "Code Executed, ("+str(var1) +","+ str(test_output)+"),"
        if str(test_output) in str(test_response):
            test_result += "Test case " + "[" + str(counter) + "] " + "passed, "
            score += 5
            marks_gained += "Test case " + "[" + str(counter) + "] " + "passed, "
        if not str(test_output) in str(test_response):
            test_result += "Test case " + "[" + str(counter) + "] " + "failed, "
            marks_lost += "Test case " + "[" + str(counter) + "] " + "failed, "
        marks_available += 5

    # comments
    comments = str(comments_check1(path))
    if int(comments) > 0:
        score += 5
        marks_gained += "Use of comments, "
    else:
        marks_lost += "No comments, "
    marks_available += 5
    # keywords
    # for loop for each keyword returned to run keywrd fxn and concatenate output +=
    keywordlist = Keyword.objects.filter(question=question)
    keywords = ""
    for kw in keywordlist:
        min_keywords = kw.min_use
        keyword = kw.text
        keyword_counter = (keywords_check1(keyword, min_keywords, path))
        if keyword_counter >= (min_keywords):
            score += 5
            marks_gained += "Keyword " + keyword + " used sufficiently, "
        else:
            marks_lost += "Keyword " + keyword + "not used or used too few times, "
        marks_available += 5
        keywords += (keyword + "(" + str(keyword_counter) + "), ")
    final_score = str("%.2f" % ((score / float(marks_available)) * 100))
    feedback = "Score: " + final_score + " Required output: " + test_output + " Your output: " + test_response + " Remark: " + test_result + "Comments used: " + comments + " Keywords used: " + keywords + "Marks Gained: " + marks_gained + " Marks Lost: " + marks_lost
    attempt_obj = Attempt(user=user, question=question, score=final_score, code=path, feedback=feedback)
    attempt_obj.save()
    return render_to_response("box/codeform.html",
                              add_csrf(request, test_case_obj=test_case_obj, subtopic=subtopic, question=question,
                                       code=code, output=test_response, score=float(final_score), testcase=test_result,
                                       comments=comments, keywords=keywords, marks_gained=marks_gained,
                                       marks_lost=marks_lost, download_path=download_path))


def codepad(request):
    if request.method == "POST":
        p = request.POST
        if p.get("code", "") == "":
            code_error = " Please enter some code!"
            return render_to_response("box/codepad.html", add_csrf(request, code_error=code_error))

        code = p["code"]
        input = p["input"]
        user = request.user
        rand1 = randint(100, 99999999999)
        rand2 = randint(100, 99999999999)
        rand = rand1 + rand2
        file_n = str(user) + "_" + str(rand)
        file_name = file_n + ".py"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # dest_dir = os.path.join(script_dir, 'submissions')
        dest_dir = os.path.join(MEDIA_ROOT, 'codepad')
        download_path = 'codepad/' + file_name
        print download_path
        try:
            os.makedirs(dest_dir)
        except OSError:
            pass  # already exists
        path = os.path.join(dest_dir, file_name)
        # Let's create some data:
        # Create a file object:
        # in "write" mode
        FILE = open(path, "w")
        # Write all the lines at once:
        FILE.writelines(code)
        FILE.close()
        script_response = file_name + " created successfully with contents " + code

    else:
        return render_to_response('box/codepad.html', dict(user=request.user), context_instance=RequestContext(request))

    proc = subprocess.Popen("python3.2 " + path, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    script_response = proc.communicate(input=input)[0]
    return render_to_response("box/codepad.html",
                              add_csrf(request, script_response=script_response, code=code, input=input,
                                       download_path=download_path))


def java(test_input, file_n, path, dest_dir):
    cwd = dest_dir
    ccmd = ['javac', path]
    print path
    process = subprocess.Popen(ccmd, cwd=cwd)
    process.wait()
    rcmd = ['java', file_n]
    process = subprocess.Popen(rcmd, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    test_response = process.communicate(input=test_input)[0]
    # test_response = process.stdout.read()
    # print test_response
    return test_response


def c_code(test_input, file_n, path, dest_dir):
    cwd = dest_dir
    ccmd = ['gcc', '-o', file_n, path]
    process = subprocess.Popen(ccmd, cwd=cwd)
    process.wait()
    rcmd = ['./' + file_n]
    process = subprocess.Popen(rcmd, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    test_response = process.communicate(input=test_input)[0]
    print test_response
    return test_response


def add_csrf(request, **kwargs):
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    csrfContext = RequestContext(request, d)
    return csrfContext
