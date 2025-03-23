# 必要なモジュールをインポート
from django.shortcuts import render
from django.http import HttpResponseRedirect
# 新しいモデルをここにインポート
from .models import Course, Enrollment, Question, Choice, Submission
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
import logging

# ロガーのインスタンスを取得
logger = logging.getLogger(__name__)

# ビューを定義する場所
# submit関数の定義
def submit(request, course_id):
    # 受け取ったcourse_idを基に、該当するCourseオブジェクトを取得
    course = get_object_or_404(Course, pk=course_id)
    
    # 現在ログイン中のユーザーを取得
    user = request.user
    
    # ユーザーがこのコースに登録しているEnrollmentオブジェクトを取得
    enrollment = Enrollment.objects.get(user=user, course=course)
    
    # 新しいSubmissionオブジェクトを作成し、登録情報を関連付け
    submission = Submission.objects.create(enrollment=enrollment)
    
    # ユーザーの解答（選択肢）を抽出
    choices = extract_answers(request)
    
    # 抽出した選択肢をSubmissionオブジェクトにセット
    submission.choices.set(choices)
    
    # 作成したSubmissionオブジェクトのIDを取得
    submission_id = submission.id
    
    # 試験結果ページにリダイレクトする
    # course_idとsubmission_idをURLのパラメータとして渡す
    return HttpResponseRedirect(reverse(viewname='onlinecourse:exam_result', args=(course_id, submission_id,)))


# ユーザー登録のリクエストを処理するビュー
def registration_request(request):
    context = {}
    if request.method == 'GET':
        # GETリクエストの場合、登録フォームを表示
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # POSTリクエストの場合、フォームデータを処理
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # 既存のユーザーを確認
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            # 新しいユーザーを作成
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            # 登録後、トップページにリダイレクト
            return redirect("onlinecourse:index")
        else:
            # ユーザーが既に存在する場合、エラーメッセージを表示
            context['message'] = "User already exists."
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)


# ログインリクエストを処理するビュー
def login_request(request):
    context = {}
    if request.method == "POST":
        # POSTリクエストの場合、ユーザー名とパスワードを取得し認証
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            # ユーザーが認証されればログイン
            login(request, user)
            # ログイン後、トップページにリダイレクト
            return redirect('onlinecourse:index')
        else:
            # 認証失敗の場合、エラーメッセージを表示
            context['message'] = "Invalid username or password."
            return render(request, 'onlinecourse/user_login_bootstrap.html', context)
    else:
        # GETリクエストの場合、ログインフォームを表示
        return render(request, 'onlinecourse/user_login_bootstrap.html', context)


# ログアウトリクエストを処理するビュー
def logout_request(request):
    # ログアウト処理
    logout(request)
    # ログアウト後、トップページにリダイレクト
    return redirect('onlinecourse:index')


# ユーザーが指定したコースに登録しているかを確認する関数
def check_if_enrolled(user, course):
    is_enrolled = False
    if user.id is not None:
        # ユーザーがこのコースに登録しているか確認
        num_results = Enrollment.objects.filter(user=user, course=course).count()
        if num_results > 0:
            is_enrolled = True
    return is_enrolled


# コースの一覧を表示するビュー
class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        user = self.request.user
        # 登録者数でコースをソートして上位10件を表示
        courses = Course.objects.order_by('-total_enrollment')[:10]
        for course in courses:
            if user.is_authenticated:
                # ユーザーが認証されていれば、コースへの登録状態を確認
                course.is_enrolled = check_if_enrolled(user, course)
        return courses


# コースの詳細を表示するビュー
class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail_bootstrap.html'


# ユーザーがコースに登録するビュー
def enroll(request, course_id):
    # コースIDからコースオブジェクトを取得
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    # ユーザーが既に登録しているか確認
    is_enrolled = check_if_enrolled(user, course)
    if not is_enrolled and user.is_authenticated:
        # ユーザーが未登録ならば、登録処理を実行
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()

    # 登録後、コース詳細ページにリダイレクト
    return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))

# 試験結果を表示する関数
def show_exam_result(request, course_id, submission_id):
    context = {}  # テンプレートに渡すコンテキスト用の辞書を作成

    # 指定されたコースID（course_id）に該当するコースを取得（存在しない場合は404エラーを返す）
    course = get_object_or_404(Course, pk=course_id)

    # 指定された提出ID（submission_id）に該当する提出データを取得
    submission = Submission.objects.get(id=submission_id)

    # 提出された解答（選択肢）を取得（多対多の関係）
    choices = submission.choices.all()

    total_score = 0  # 合計スコアを初期化

    # コースに関連する全ての問題を取得
    questions = course.question_set.all()

    # 各問題に対して採点処理を行う
    for question in questions:
        # 正解の選択肢（is_correct=True）を取得
        correct_choices = question.choice_set.filter(is_correct=True)

        # ユーザーが選択した選択肢を取得
        selected_choices = choices.filter(question=question)

        # ユーザーの選択が正解の選択肢と完全一致する場合、スコアを加算
        if set(correct_choices) == set(selected_choices):
            total_score += question.grade  # 問題ごとの得点を加算

    # コンテキストに情報を格納
    context['course'] = course  # コース情報
    context['grade'] = total_score  # ユーザーの得点
    context['choices'] = choices  # ユーザーが選択した選択肢

    # 試験結果のページをレンダリングし、コンテキストを渡す
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)

# submit関数の定義
def submit(request, course_id):
    # 受け取ったcourse_idを基に、該当するCourseオブジェクトを取得
    course = get_object_or_404(Course, pk=course_id)
    
    # 現在ログイン中のユーザーを取得
    user = request.user
    
    # ユーザーがこのコースに登録しているEnrollmentオブジェクトを取得
    enrollment = Enrollment.objects.get(user=user, course=course)
    
    # 新しいSubmissionオブジェクトを作成し、登録情報を関連付け
    submission = Submission.objects.create(enrollment=enrollment)
    
    # ユーザーの解答（選択肢）を抽出
    choices = extract_answers(request)
    
    # 抽出した選択肢をSubmissionオブジェクトにセット
    submission.choices.set(choices)
    
    # 作成したSubmissionオブジェクトのIDを取得
    submission_id = submission.id
    
    # 試験結果ページにリダイレクトする
    # course_idとsubmission_idをURLのパラメータとして渡す
    return HttpResponseRedirect(reverse(viewname='onlinecourse:exam_result', args=(course_id, submission_id,)))


# 選択された解答を抽出するためのヘルパー関数
def extract_answers(request):
   submitted_anwsers = []
   # POSTリクエスト内の選択肢の値を全て取得
   for key in request.POST:
       if key.startswith('choice'):
           value = request.POST[key]
           # 取得した値を選択肢IDに変換してリストに追加
           choice_id = int(value)
           submitted_anwsers.append(choice_id)
   return submitted_anwsers
