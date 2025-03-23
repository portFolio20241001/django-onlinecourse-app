import sys
from django.utils.timezone import now

# Djangoのデータベースモデルをインポートする
try:
    from django.db import models
except Exception:
    # Djangoがインストールされていない場合、エラーメッセージを表示して終了する
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
import uuid  # 一意の識別子を生成するためのUUIDモジュールをインポート

# Instructor（講師）モデルの定義
class Instructor(models.Model):
    # ユーザー情報（外部キーとしてDjangoの認証ユーザーモデルを参照）
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Djangoの認証ユーザーモデルと関連付ける
        on_delete=models.CASCADE,  # ユーザーが削除されたら、関連する講師データも削除する
    )
    full_time = models.BooleanField(default=True)  # フルタイム講師かどうか（デフォルトはTrue）
    total_learners = models.IntegerField()  # 担当する学習者の総数（整数）

    def __str__(self):
        # オブジェクトを文字列で表現する際にユーザー名を返す
        return self.user.username

# Learner（学習者）モデルの定義
class Learner(models.Model):
    # ユーザー情報（外部キーとしてDjangoの認証ユーザーモデルを参照）
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Djangoの認証ユーザーモデルと関連付ける
        on_delete=models.CASCADE,  # ユーザーが削除されたら、関連する学習者データも削除する
    )

    # 学習者の職業を定義（選択肢）
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'dba'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin')
    ]
    
    # 職業の選択フィールド（デフォルトは「Student」）
    occupation = models.CharField(
        null=False,  # 必須フィールド
        max_length=20,  # 最大20文字まで
        choices=OCCUPATION_CHOICES,  # 選択肢を指定
        default=STUDENT  # デフォルト値を設定
    )
    social_link = models.URLField(max_length=200)  # 学習者のSNSリンク（最大200文字）

    def __str__(self):
        # ユーザー名と職業を文字列として返す
        return self.user.username + "," + self.occupation

# Course（コース）モデルの定義
class Course(models.Model):
    name = models.CharField(null=False, max_length=30, default='online course')  # コース名（最大30文字）
    image = models.ImageField(upload_to='course_images/')  # コースの画像（アップロード先を指定）
    description = models.CharField(max_length=1000)  # コースの説明（最大1000文字）
    pub_date = models.DateField(null=True)  # コースの公開日
    instructors = models.ManyToManyField(Instructor)  # コースに関連する講師（多対多）
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')  # 受講者（Enrollmentを通じて管理）
    total_enrollment = models.IntegerField(default=0)  # 登録者数（デフォルトは0）
    is_enrolled = False  # 受講しているかどうかのフラグ（DBには保存されない）

    def __str__(self):
        # コース名と説明を文字列として返す
        return "Name: " + self.name + "," + "Description: " + self.description

# Lesson（レッスン）モデルの定義
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")  # レッスンのタイトル（最大200文字）
    order = models.IntegerField(default=0)  # レッスンの順番（整数値）
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # コースとの関連（外部キー）
    content = models.TextField()  # レッスンの内容

# Enrollment（受講登録）モデルの定義
class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    BETA = 'BETA'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
        (BETA, 'BETA')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 受講者
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # コース
    date_enrolled = models.DateField(default=now)  # 受講開始日
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)  # 受講モード
    rating = models.FloatField(default=5.0)  # コースの評価

# Question（質問）モデルの定義
class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # コース（外部キー）
    content = models.CharField(max_length=200)  # 質問の内容（最大200文字）
    grade = models.IntegerField(default=50)  # 質問の配点

    def __str__(self):
        return "Question: " + self.content  # 質問内容を返す

    def is_get_score(self, selected_ids):
        # 正解の選択肢の数を取得
        all_answers = self.choice_set.filter(is_correct=True).count()
        # ユーザーが選択した正解の数を取得
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        # すべての正解を選択していたらTrue、それ以外はFalse
        return all_answers == selected_correct

# 選択肢（Choice）モデルの定義
class Choice(models.Model):
    # 質問（Question）に対する選択肢（Choice）
    # 1つの質問（Question）は複数の選択肢（Choice）を持つ（1対多の関係）
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    # 選択肢の内容（テキスト）
    content = models.CharField(max_length=200)
    
    # この選択肢が正解かどうか（Trueなら正解、Falseなら不正解）
    is_correct = models.BooleanField(default=False)

# Submission（提出物）モデルの定義（多対多：1つの受講登録が複数の選択肢を持つ可能性あり）
class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)  # 1つの受講登録に対する外部キー
    choices = models.ManyToManyField(Choice)  # 多対多（複数の選択肢を選択可能）