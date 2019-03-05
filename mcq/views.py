# Create your views here.
from django.core.context_processors import csrf
from django.db.models import Sum
from django.shortcuts import render_to_response
from django.template import RequestContext

from book.models import *
from box.models import *
from mcq.models import *


def subtopic_mcq(request, course_id, topic_id, subtopic_id):
    try:
        subtopic = Subtopic.objects.get(pk=subtopic_id)
        cq_list = Question.objects.filter(subtopic=subtopic)
        answer_list = Answer.objects.filter(question__in=cq_list)
        # guess_list = MCQGuess.objects.filter(submitted_by=request.user)
        guess_list = MCQGuess.objects.filter(question__in=cq_list, submitted_by=request.user)
        sum_correct = MCQGuess.objects.filter(question__in=cq_list, submitted_by=request.user).aggregate(
            score1=Sum('score'))
        marks_available = guess_list.count()
        print sum_correct['score1']
        print guess_list.count()
        print cq_list
        print answer_list
        final_score = 0
        if sum_correct['score1']:
            final_score = str("%.2f" % ((int(sum_correct['score1']) / float(marks_available)) * 100))
        return render_to_response("mcq/quiz.html",
                                  add_csrf(request, guess_list=guess_list, subtopic=subtopic, cq_list=cq_list,
                                           answer_list=answer_list, final_score=final_score))
    except MCQGuess.DoesNotExist:
        return render_to_response("mcq/quiz.html",
                                  add_csrf(request, subtopic=subtopic, cq_list=cq_list, answer_list=answer_list))


def process_mcq(request, course_id, topic_id, subtopic_id):
    subtopic = Subtopic.objects.get(pk=subtopic_id)
    cq_list = Question.objects.filter(subtopic=subtopic)
    answer_list = Answer.objects.all()
    if request.method == "POST":
        score = 0
        marks_available = 0
        p = request.POST
        for question in cq_list:
            marks_available += 1
            choice = p.get(str(question.id) + "_choice", '')
            print "choice" + choice
            if choice == '':
                print "Please enter a choice"
                error_msg = "Attempt all questions!"
                return render_to_response("mcq/quiz.html",
                                          add_csrf(request, subtopic=subtopic, cq_list=cq_list, answer_list=answer_list,
                                                   error_msg=error_msg))
            correct_answer = Answer.objects.get(question=question, correct=True)
            print correct_answer.answer
            user_answer = Answer.objects.get(pk=choice)

            print choice
            print user_answer
            if user_answer == correct_answer:
                print "Correct answer!!!"
                question_score = 1
            else:
                question_score = 0
            guess_obj = MCQGuess(question=question, submitted_by=request.user, answer_given=user_answer,
                                 score=question_score)
            guess_obj.save()
        # final_score = str("%.2f" % ((score/ float(marks_available))*100))
        guess_list = MCQGuess.objects.filter(question__in=cq_list, submitted_by=request.user)
        sum_correct = MCQGuess.objects.filter(question__in=cq_list, submitted_by=request.user).aggregate(
            score1=Sum('score'))
        marks_available = guess_list.count()
        final_score = 0
        final_score = str("%.2f" % ((int(sum_correct['score1']) / float(marks_available)) * 100))
        print final_score
        # guess_list = MCQGuess.objects.filter(question__in=cq_list, submitted_by=request.user)
        return render_to_response("mcq/quiz.html",
                                  add_csrf(request, guess_list=guess_list, subtopic=subtopic, cq_list=cq_list,
                                           answer_list=answer_list, final_score=final_score))
    else:
        return render_to_response("mcq/quiz.html",
                                  add_csrf(request, subtopic=subtopic, cq_list=cq_list, answer_list=answer_list,
                                           final_score=final_score))


def add_csrf(request, **kwargs):
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    csrfContext = RequestContext(request, d)
    return csrfContext


def create_mcq(request, course_id, topic_id, subtopic_id):
    subtopic = Subtopic.objects.get(pk=subtopic_id)
    course = Course.objects.get(pk=course_id)
    message = " Add MCQ"
    data_dict = {'subtopic': subtopic_id}
    print "in create mcq"
    question_form = QuestionForm(initial=data_dict)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST or None)
        print request.POST
    # if question_form.is_valid() and answer_form.is_valid():
    if question_form.is_valid():

        p = request.POST
        answer_choice1 = ""
        answer_choice2 = ""
        answer_choice3 = ""
        for i in range(1, 4):
            if i == 1:
                answer_choice1 = p.get("Answer" + str(i), "")
            if i == 2:
                answer_choice2 = p.get("Answer" + str(i), "")
            if i == 3:
                answer_choice3 = p.get("Answer" + str(i), "")
            if p.get("Answer" + str(i), "") == "":
                message = "Please add 3 mcq choices!"
                # question_form = QuestionForm(initial=data_dict)
                question_form = question_form
                # print answer_choice1, answer_choice2, answer_choice3
                context = dict(user=request.user, create_mcquestion_form=question_form, subtopic=subtopic,
                               message=message, answer_choice1=answer_choice1, answer_choice2=answer_choice2,
                               answer_choice3=answer_choice3)
                return render_to_response("book/admin_question.html", context_instance=RequestContext(request, context))

        counter = 0
        for i in range(1, 4):

            if p.get("answer_choice", "") == "answer_choice" + str(i):
                correct = True
            else:
                correct = False
                counter += 1
                if counter == 3:
                    message = "Please choose 1 correct answer!"
                    # question_form = QuestionForm(initial=data_dict)
                    context = dict(user=request.user, create_mcquestion_form=question_form, subtopic=subtopic,
                                   message=message, answer_choice1=answer_choice1, answer_choice2=answer_choice2,
                                   answer_choice3=answer_choice3)
                    return render_to_response("book/admin_question.html",
                                              context_instance=RequestContext(request, context))

            question = question_form.save()
            answer = Answer(question=question, answer=p.get("Answer" + str(i), ""), correct=correct)
            answer.save()
        message = subtopic.topic.name + "/" + subtopic.name + "/" + " Multiple Choice Question Added"
        cq_list = Question.objects.filter(subtopic=subtopic)
        answer_list = Answer.objects.all()
        # return render_to_response("book/admin_question.html", add_csrf(request, message =message, subtopic=subtopic, cq_list=cq_list, answer_list=answer_list))

        topic_list = Topic.objects.filter(course=course)
        subtopic_list = Subtopic.objects.all()[:]
        context = dict(message=message, topic_list=topic_list, subtopic_list=subtopic_list, user=request.user,
                       course=course)
        return render_to_response("book/all_topics.html", context_instance=RequestContext(request, context))

    else:
        question_form = QuestionForm(initial=data_dict)
        context = dict(user=request.user, create_mcquestion_form=question_form, subtopic=subtopic)
    return render_to_response("book/admin_question.html", context_instance=RequestContext(request, context))


def edit_mcq(request, course_id, topic_id, subtopic_id, question_id):
    question = Question.objects.get(pk=question_id)
    subtopic = Subtopic.objects.get(pk=subtopic_id)
    question_form = Question.objects.get(pk=question_id)
    message = subtopic.name + "/" + " Edit MCQ"
    answer_list = Answer.objects.filter(question=question_id)
    print answer_list
    form = QuestionForm()
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES, instance=question)
        if question_form.is_valid():
            p = request.POST
            # for i in range(1,4):
            i = 0
            for answer in answer_list:
                i += 1
                if p.get("answer_choice", "") == "answer_choice" + str(i):
                    correct = True
                else:
                    correct = False

                question = question_form.save()
                answer.question = question
                answer.answer = p.get("Answer" + str(i), "")
                answer.correct = correct
                answer.save()
            message = subtopic.name + "/" + " MCQ Edited"
            cq_list = Question.objects.filter(subtopic=subtopic)
            answer_list = Answer.objects.filter(question__in=cq_list)
            return render_to_response("mcq/quiz.html",
                                      add_csrf(request, message=message, subtopic=subtopic, cq_list=cq_list,
                                               answer_list=answer_list))
    else:
        form = QuestionForm(instance=question)
    context = dict(user=request.user, edit_mcq_form=form, subtopic=subtopic, question=question, message=message,
                   answer_list=answer_list)
    return render_to_response("mcq/admin_question_answer.html", context_instance=RequestContext(request, context))


def delete_mcq(request, course_id, topic_id, subtopic_id, question_id):
    question = Question.objects.get(pk=question_id)
    subtopic = Subtopic.objects.get(pk=subtopic_id)
    name = subtopic.name + "/" + question.question
    message = name + " deleted"
    question.delete()
    cq_list = Question.objects.filter(subtopic=subtopic)
    answer_list = Answer.objects.filter(question__in=cq_list)
    return render_to_response("mcq/quiz.html", add_csrf(request, message=message, subtopic=subtopic, cq_list=cq_list,
                                                        answer_list=answer_list))
