from django.urls import path  # DjangoのURLパターンを定義するためのモジュールをインポート
from django.conf import settings  # 設定ファイルを参照するためのモジュールをインポート
from django.conf.urls.static import static  # メディアファイルのURLを設定するための関数をインポート
from . import views  # 同じアプリ内のviewsモジュールをインポート

# アプリケーションの名前空間を設定（複数のアプリがある場合に識別しやすくするため）
app_name = 'onlinecourse'

# URLパターンのリストを定義
urlpatterns = [
    # トップページ（コース一覧）のルート
    # ユーザーがサイトのルート（'/'）にアクセスした際に、CourseListViewを表示
    path(route='', view=views.CourseListView.as_view(), name='index'),

    # ユーザー登録ページのルート
    # 'registration/' にアクセスすると、ユーザー登録処理（views.registration_request）が実行される
    path('registration/', views.registration_request, name='registration'),

    # ログインページのルート
    # 'login/' にアクセスすると、ログイン処理（views.login_request）が実行される
    path('login/', views.login_request, name='login'),

    # ログアウトページのルート
    # 'logout/' にアクセスすると、ログアウト処理（views.logout_request）が実行される
    path('logout/', views.logout_request, name='logout'),

    # コースの詳細ページのルート
    # '<int:pk>/' は、整数のコースID（pk）をURLから取得し、CourseDetailViewを表示
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),

    # コースへの登録ページのルート
    # '<int:course_id>/enroll/' にアクセスすると、指定したコースID（course_id）にユーザーが登録する処理（views.enroll）が実行される
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),

    # 試験の解答を送信するページのルート
    # '<int:course_id>/submit/' にアクセスすると、指定したコースID（course_id）の試験解答が送信される
    path('<int:course_id>/submit/', views.submit, name="submit"),

    # 試験結果を表示するページのルート
    # 'course/<int:course_id>/submission/<int:submission_id>/result/' にアクセスすると、
    # 指定したコースIDと提出ID（submission_id）の試験結果が表示される
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name="exam_result"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # メディアファイルのURL設定
