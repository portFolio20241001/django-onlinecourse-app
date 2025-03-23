from django.contrib import admin  # Djangoの管理サイト用モジュールをインポート

# <HINT> ここで新しいモデルをインポートする
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission  # モデルをインポート

#----------------------　インラインで管理するクラス　--------------------------------

# Choice（選択肢）をインラインで管理するクラス
class ChoiceInline(admin.StackedInline):  
    model = Choice  # 関連するモデルをChoiceに設定
    extra = 2  # 追加できる空の選択肢の数（デフォルト2）

# Question（質問）をインラインで管理するクラス
class QuestionInline(admin.StackedInline):  
    model = Question  # 関連するモデルをQuestionに設定
    extra = 2  # 追加できる空の質問の数（デフォルト2）

# Lesson（レッスン）をインラインで管理するクラス
class LessonInline(admin.StackedInline):  
    model = Lesson  # 関連するモデルをLessonに設定
    extra = 5  # 追加できる空のレッスンの数（デフォルト5）


#----------------------　モデル管理クラス　--------------------------------


# Course（コース）モデルの管理クラス
class CourseAdmin(admin.ModelAdmin):  
    inlines = [LessonInline]  # コースの管理画面でレッスンをインライン表示
    list_display = ('name', 'pub_date')  # 管理画面で表示するカラム（コース名と公開日）
    list_filter = ['pub_date']  # 公開日でフィルタリング可能にする
    search_fields = ['name', 'description']  # コース名と説明で検索可能にする

# Lesson（レッスン）モデルの管理クラス
class LessonAdmin(admin.ModelAdmin):  
    list_display = ['title']  # 管理画面でタイトルを表示

# <HINT> Question と Choice モデルを登録する

# Question（質問）モデルの管理クラス
class QuestionAdmin(admin.ModelAdmin):  
    inlines = [ChoiceInline]  # 質問の管理画面で選択肢をインライン表示
    list_display = ['content']  # 管理画面で質問の内容を表示


#----------------------　Django管理サイトにモデルを登録　--------------------------------

# モデルをDjango管理サイトに登録する
admin.site.register(Course, CourseAdmin)        # Courseモデルを登録（管理画面用）
admin.site.register(Lesson, LessonAdmin)        # Lessonモデルを登録（管理画面用）
admin.site.register(Instructor)                 # Instructor（講師）モデルを登録
admin.site.register(Learner)                    # Learner（学習者）モデルを登録
admin.site.register(Question, QuestionAdmin)    # Question（質問）モデルを登録（管理画面用）
admin.site.register(Choice)                     # Choice（選択肢）モデルを登録（管理画面用）
admin.site.register(Submission)                 # Submission（提出物）モデルを登録（管理画面用）
