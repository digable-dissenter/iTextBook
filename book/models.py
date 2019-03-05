from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm


class Course(models.Model):
    name = models.CharField(max_length=60, blank=False, null=True)
    description = models.TextField(max_length=500, blank=False, null=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    language = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

    # (r'^course(?P<course_id>\d+)/$', "book.views.all_topics"),
    @models.permalink
    def get_absolute_url(self):
        return ('book.views.all_topics', (), {
            'course_id': str(self.id)})


class CourseForm(ModelForm):
    """
    Auto generated form to create Course models.
    """

    class Meta:
        model = Course
        exclude = ('language')


# create a course with topic as inline
class Topic(models.Model):
    course = models.ForeignKey(Course)
    number = models.IntegerField(max_length=2, blank=False, null=False)  # this should auto increment
    name = models.CharField(max_length=60, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

# (r'^course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/$', "book.views.topic"),

# @models.permalink
# def get_absolute_url(self):
# return ('book.views.topics', (), {
# 'course_id': str(self.course.id),
# 'topic_id': str(self.id)})


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        exclude = ('number')


# Topic (eg Loops) -> Topics (eg For Loops, While Loops) -> Notes, Video, Assessments etc
class TopicAdmin(admin.ModelAdmin):
    list_display = ["course", "number", "name", "created"]

    list_filter = ["number", "created"]
    search_fields = ["name"]


admin.site.register(Topic, TopicAdmin)


class Subtopic(models.Model):
    topic = models.ForeignKey(Topic)
    number = models.IntegerField(max_length=2, blank=False, null=False)
    name = models.CharField(max_length=60, blank=True, null=True)
    pdfslides = models.FileField(upload_to="slides/", blank=False, null=True)
    video = models.FileField(upload_to="videos/", blank=False, null=True)
    pdfbook = models.FileField(upload_to="textbook/", blank=False, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    # (r'^course(?P<course_id>\d+)/$', "book.views.all_topics"),
    # (r'^course(?P<course_id>\d+)/topic(?P<topic_id>\d+)/subtopics(?P<subtopic_id>\d+)/$', "book.views.subtopics"),

    @models.permalink
    def get_absolute_url(self):
        return ('book.views.subtopics', (), {
            'course_id': str(self.topic.course.id),
            'topic_id': str(self.topic.id),
            'subtopic_id': str(self.id)})


class SubtopicForm(ModelForm):
    class Meta:
        model = Subtopic
        exclude = ('number')


class SubtopicAdmin(admin.ModelAdmin):
    list_display = ["topic", "number", "name", "pdfslides", "video", "pdfbook", "created"]

    list_filter = ["topic"]
    search_fields = ["topic"]


admin.site.register(Subtopic, SubtopicAdmin)


class Annotation(models.Model):
    subtopic = models.ForeignKey(Subtopic)
    created_by = models.ForeignKey(User)
    annotation_text = models.TextField(max_length=500)

    def __unicode__(self):
        return self.annotation_text


class AnnotationAdmin(admin.ModelAdmin):
    list_display = ["subtopic", "created_by", "annotation_text"]

    list_filter = ["subtopic"]


admin.site.register(Annotation, AnnotationAdmin)


class Comments(models.Model):
    subtopic = models.ForeignKey(Subtopic)
    created_by = models.ForeignKey(User)
    comment_text = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.comment_text


class CommentsAdmin(admin.ModelAdmin):
    list_display = ["subtopic", "created_by", "comment_text", "created"]

    list_filter = ["subtopic", "created"]


admin.site.register(Comments, CommentsAdmin)


class TopicInline(admin.TabularInline):
    model = Topic


class CourseAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    inlines = [TopicInline]


admin.site.register(Course, CourseAdmin)
